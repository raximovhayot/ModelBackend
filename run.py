import os
import sys
import multiprocessing
from app import app, socketio
from worker import main as worker_main

def run_flask_app():
    """
    Run the Flask application with SocketIO
    """
    port = int(os.environ.get('PORT', 5000))
    # Use debug mode only in development environment
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    socketio.run(app, host='0.0.0.0', port=port, debug=debug_mode, use_reloader=False)

def run_worker():
    """
    Run the worker process
    """
    worker_main()

if __name__ == '__main__':
    # Create processes
    flask_process = multiprocessing.Process(target=run_flask_app)
    worker_process = multiprocessing.Process(target=run_worker)

    try:
        # Start processes
        print("Starting Flask application...")
        flask_process.start()

        print("Starting worker process...")
        worker_process.start()

        # Wait for processes to complete
        flask_process.join()
        worker_process.join()
    except KeyboardInterrupt:
        print("Shutting down...")
        # Terminate processes on keyboard interrupt
        flask_process.terminate()
        worker_process.terminate()

        # Wait for processes to terminate
        flask_process.join()
        worker_process.join()

        print("Application shut down successfully")
    except Exception as e:
        print(f"Error: {str(e)}")
        # Ensure processes are terminated in case of error
        if flask_process.is_alive():
            flask_process.terminate()
        if worker_process.is_alive():
            worker_process.terminate()
