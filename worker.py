import os
import sys
import time
from redis import Redis
from rq import Worker, Queue, Connection

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Initialize Redis connection
redis_url = os.environ.get('REDIS_URL', 'redis://:root123@localhost:6379/0')
redis_conn = Redis.from_url(redis_url)

# Define the queue name
queue_name = 'prediction_queue'

def main():
    """
    Start the worker to process jobs from the queue
    """
    print(f"Starting worker for queue: {queue_name}")
    
    with Connection(redis_conn):
        worker = Worker([queue_name])
        worker.work(with_scheduler=True)

if __name__ == '__main__':
    main()