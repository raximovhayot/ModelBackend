# Test script to verify that the circular import issue is resolved
print("Testing imports to verify circular import issue is resolved...")

try:
    # Import app from app.py (this was failing before due to circular import)
    print("Importing app from app.py...")
    from app import app, socketio
    print("Successfully imported app and socketio from app.py")
    
    # Import queue_service functions
    print("Importing functions from queue_service.py...")
    from queue_service import enqueue_network_data, get_queue_stats
    print("Successfully imported functions from queue_service.py")
    
    # Import API classes
    print("Importing API classes...")
    from api import NetworkDataAPI, NetworkDataListAPI, NetworkDataDetailAPI, NetworkDataByLabelAPI
    print("Successfully imported API classes")
    
    print("\nAll imports successful! The circular import issue is resolved.")
except ImportError as e:
    print(f"\nImport error: {str(e)}")
    print("The circular import issue is still present.")