import os
import json
from redis import Redis
from rq import Queue
from models import ModelService
from database import DatabaseService

# Initialize Redis connection
redis_url = os.environ.get('REDIS_URL', 'redis://:root123@localhost:6379/0')
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
    # Get model service instance
    model_service = ModelService()

    # Make prediction
    prediction_result = model_service.predict(data)

    # Check if prediction contains an error
    if "error" in prediction_result:
        print(f"Error in prediction: {prediction_result['error']}")
        return None

    # Store data and prediction in database
    network_data = DatabaseService.add_network_data(data, prediction_result)

    # Emit network data to connected clients - use lazy import to avoid circular dependency
    try:
        # Import only when needed to avoid circular imports
        from app import emit_network_data
        emit_network_data(network_data)
    except ImportError as e:
        print(f"Warning: Could not emit network data: {str(e)}")
        # Continue processing even if emit fails

    return network_data.to_dict()

def enqueue_network_data(data, flow_features_dict):
    """
    Enqueue network data for processing

    Args:
        data (dict): The preprocessed data for the model
        flow_features_dict (dict): The original flow features dictionary

    Returns:
        str: The job ID
    """
    # Enqueue the job
    job = queue.enqueue(
        process_network_data,
        args=(data, flow_features_dict),
        job_timeout='5m'  # 5 minutes timeout
    )

    return job.id

def get_queue_stats():
    """
    Get statistics about the queue

    Returns:
        dict: Queue statistics
    """
    return {
        'queued_jobs': queue.count,
        'failed_jobs': len(queue.failed_job_registry),
        'completed_jobs': len(queue.finished_job_registry),
        'workers': len(queue.workers),
        'queue_name': queue.name
    }
