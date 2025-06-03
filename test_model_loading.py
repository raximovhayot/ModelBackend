from models import ModelService

def test_model_loading():
    """
    Test that the model loads successfully with the compatibility fix
    """
    print("Testing model loading...")
    model_service = ModelService()
    
    if model_service.model is None:
        print("Error: Model not loaded")
        return False
    
    print("Success: Model loaded successfully")
    return True

if __name__ == "__main__":
    test_model_loading()