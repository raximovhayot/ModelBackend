import pickle
import numpy as np
import pandas as pd

class ModelService:
    def __init__(self, model_path='random_forest_model.pkl', scaler_path=None):
        """
        Initialize the model service

        Args:
            model_path (str): Path to the saved model file
            scaler_path (str, optional): Path to the saved scaler file
        """
        # Load the model
        try:
            with open(model_path, 'rb') as f:
                self.model = pickle.load(f)
            print(f"Model loaded successfully from {model_path}")
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model = None

        # Load the scaler if provided
        self.scaler = None
        if scaler_path:
            try:
                with open(scaler_path, 'rb') as f:
                    self.scaler = pickle.load(f)
                print(f"Scaler loaded successfully from {scaler_path}")
            except Exception as e:
                print(f"Error loading scaler: {e}")

        # Define the label mapping (from the notebook)
        self.label_map = {
            0: 'Benign',
            1: 'LDAP',
            2: 'MSSQL',
            3: 'NetBIOS',
            4: 'Portmap',
            5: 'Syn',
            6: 'UDP',
            7: 'UDPLag'
        }

    def preprocess_data(self, data):
        """
        Preprocess the input data before prediction

        Args:
            data (dict or pd.DataFrame): Input data to preprocess

        Returns:
            np.ndarray: Preprocessed data ready for prediction
        """
        # Convert to DataFrame if it's a dictionary
        if isinstance(data, dict):
            data = pd.DataFrame([data])

        # Get the features that the model was trained on
        # These are all the features that the model was trained on (32 features)
        model_features = [
            'Flow Duration', 'Protocol', 'Total Fwd Packets', 'Total Backward Packets',
            'Fwd Packet Length Total', 'Bwd Packet Length Total', 'Fwd Packet Length Max',
            'Fwd Packet Length Min', 'Fwd Packet Length Std', 'Bwd Packet Length Max',
            'Bwd Packet Length Min', 'Packet Length Max', 'Packet Length Mean',
            'Flow Bytes/s', 'Flow Packets/s', 'Bwd Packets/s',
            'Flow IAT Mean', 'Flow IAT Min', 'Fwd IAT Total', 'Fwd IAT Mean',
            'Fwd IAT Min', 'Bwd IAT Total', 'Bwd IAT Mean', 'Bwd IAT Min',
            'Fwd Header Length', 'Bwd Header Length', 'SYN Flag Count', 'ACK Flag Count',
            'URG Flag Count', 'Down/Up Ratio', 'Active Mean', 'Active Std'
        ]

        # Filter the data to include only the features that the model was trained on
        # If a feature is missing, it will be filled with 0
        for feature in model_features:
            if feature not in data.columns:
                data[feature] = 0

        # Select only the features that the model was trained on, in the correct order
        data = data[model_features]

        # Apply scaling if scaler is available
        if self.scaler:
            return self.scaler.transform(data)

        # If no scaler, just return the values as numpy array
        return data.values

    def predict(self, data):
        """
        Make a prediction using the loaded model

        Args:
            data (dict or pd.DataFrame): Input data for prediction

        Returns:
            dict: Prediction results including class label and probabilities
        """
        if self.model is None:
            return {"error": "Model not loaded"}

        # Preprocess the data
        processed_data = self.preprocess_data(data)

        # Make prediction
        prediction = self.model.predict(processed_data)
        probabilities = self.model.predict_proba(processed_data)

        # Get the predicted class label
        predicted_class = prediction[0]
        predicted_label = self.label_map.get(predicted_class, f"Unknown class {predicted_class}")

        # Create a dictionary of class probabilities
        class_probs = {self.label_map.get(i, f"Class {i}"): float(prob) 
                      for i, prob in enumerate(probabilities[0])}

        # Return the results
        return {
            "predicted_class": int(predicted_class),
            "predicted_label": predicted_label,
            "probabilities": class_probs
        }
