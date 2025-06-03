import logging
import os
import sys

from rq import Worker, Connection

from utils.redis_utils import get_redis_connection

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.environ.get('WORKER_LOG_FILE', 'worker.log'))
    ]
)
logger = logging.getLogger(__name__)

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Initialize Redis connection
redis_conn = get_redis_connection()

# Define the queue name
queue_name = 'prediction_queue'

def main():
    """
    Start the worker to process jobs from the queue
    """
    logger.info(f"Starting worker for queue: {queue_name}")

    try:
        with Connection(redis_conn):
            worker = Worker([queue_name])
            logger.info(f"Worker initialized for queue: {queue_name}")
            worker.work(with_scheduler=True)
    except Exception as e:
        logger.error(f"Worker error: {str(e)}", exc_info=True)
        raise

if __name__ == '__main__':
    main()
