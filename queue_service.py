import os
import json
import logging
from redis import Redis
from rq import Queue, Worker
from models import ModelService
from database import DatabaseService
from utils.socketio_utils import emit_network_data

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.environ.get('QUEUE_LOG_FILE', 'queue.log'))
    ]
)
logger = logging.getLogger(__name__)

# Initialize Redis connection
redis_url = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
# Get Redis password from environment variable if available
redis_password = os.environ.get('REDIS_PASSWORD', 'root123')
if redis_password and 'redis://:' not in redis_url:
    # Insert password into URL if not already present
    parts = redis_url.split('://')
    if len(parts) == 2:
        redis_url = f"{parts[0]}://:{redis_password}@{parts[1]}"

redis_conn = Redis.from_url(redis_url)

# Initialize RQ queue
queue = Queue('prediction_queue', connection=redis_conn)

def process_network_data(data, flow_features_dict):
    """
    Process network data from the queue

    Args:
        data (dict): The preprocessed data for the model
        flow_features_dict (dict): The original flow features dictionary

    Returns:
        dict: The processed network data
    """
    logger.info("Processing network data from queue")

    # Get model service instance
    model_service = ModelService()

    # Make prediction
    logger.debug("Making prediction with model")
    prediction_result = model_service.predict(data)

    # Check if prediction contains an error
    if "error" in prediction_result:
        logger.error(f"Error in prediction: {prediction_result['error']}")
        return None

    # Store data and prediction in database
    # Import app only when needed to avoid circular imports
    from app import app
    with app.app_context():
        network_data = DatabaseService.add_network_data(data, prediction_result)

        # Emit network data to connected clients
        try:
            # Import only when needed to avoid circular imports
            from app import socketio
            emit_network_data(socketio, network_data)
        except ImportError as e:
            logger.warning(f"Could not emit network data: {str(e)}")
            # Continue processing even if emit fails

        # Convert to dictionary while still in session
        network_data_dict = network_data.to_dict()

    return network_data_dict

def enqueue_network_data(data, flow_features_dict):
    """
    Enqueue network data for processing

    Args:
        data (dict): The preprocessed data for the model
        flow_features_dict (dict): The original flow features dictionary

    Returns:
        str: The job ID
    """
    logger.info("Enqueueing network data for processing")

    try:
        # Enqueue the job
        job = queue.enqueue(
            process_network_data,
            args=(data, flow_features_dict),
            job_timeout='5m'  # 5 minutes timeout
        )

        logger.info(f"Job enqueued with ID: {job.id}")
        return job.id
    except Exception as e:
        logger.error(f"Error enqueueing job: {str(e)}", exc_info=True)
        raise

def get_queue_stats():
    """
    Get statistics about the queue

    Returns:
        dict: Queue statistics
    """
    logger.debug("Getting queue statistics")

    try:
        # Get count of active workers
        worker_count = len(Worker.all(connection=redis_conn))

        stats = {
            'queued_jobs': queue.count,
            'failed_jobs': len(queue.failed_job_registry),
            'completed_jobs': len(queue.finished_job_registry),
            'workers': worker_count,
            'queue_name': queue.name
        }

        logger.debug(f"Queue stats: {stats}")
        return stats
    except Exception as e:
        logger.error(f"Error getting queue stats: {str(e)}", exc_info=True)
        # Return minimal stats in case of error
        return {
            'error': str(e),
            'queue_name': queue.name
        }
