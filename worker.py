import os
import sys
import time
import logging
from redis import Redis
from rq import Worker, Queue, Connection

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
redis_url = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
# Get Redis password from environment variable if available
redis_password = os.environ.get('REDIS_PASSWORD', 'root123')
if redis_password and 'redis://:' not in redis_url:
    # Insert password into URL if not already present
    parts = redis_url.split('://')
    if len(parts) == 2:
        redis_url = f"{parts[0]}://:{redis_password}@{parts[1]}"

redis_conn = Redis.from_url(redis_url)

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
