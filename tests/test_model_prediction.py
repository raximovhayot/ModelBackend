from models import ModelService
from flow.flow_features import FlowFeatures
import numpy as np

def test_model_prediction():
    """
    Test that the model can make predictions with the correct number of features
    """
    print("Testing model prediction...")
    
    # Create a ModelService instance
    model_service = ModelService()
    
    if model_service.model is None:
        print("Error: Model not loaded")
        return False
    
    # Create a sample FlowFeatures instance with default values
    flow_features = FlowFeatures()
    
    # Convert to model dictionary format
    model_data = flow_features.to_model_dict()
    
    try:
        # Try to make a prediction
        prediction_result = model_service.predict(model_data)
        
        # Check if prediction was successful
        if "error" in prediction_result:
            print(f"Error in prediction: {prediction_result['error']}")
            return False
        
        print(f"Success: Model prediction successful")
        print(f"Predicted class: {prediction_result['predicted_class']}")
        print(f"Predicted label: {prediction_result['predicted_label']}")
        return True
    
    except Exception as e:
        print(f"Error during prediction: {str(e)}")
        return False

if __name__ == "__main__":
    test_model_prediction()