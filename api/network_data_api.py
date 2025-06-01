from flask import request, jsonify
from flask_restful import Resource
import json

from models import ModelService
from database import DatabaseService

class NetworkDataAPI(Resource):
    """
    API for receiving network data and making predictions
    """
    def __init__(self, model_service):
        self.model_service = model_service

    def post(self):
        """
        Receive network data, make prediction, and store in database
        """
        try:
            # Get data from request
            data = request.get_json()

            if not data:
                return {"error": "No data provided"}, 400

            # Make prediction
            prediction_result = self.model_service.predict(data)

            # Check if prediction contains an error
            if "error" in prediction_result:
                return {"error": prediction_result["error"]}, 500

            # Store data and prediction in database
            network_data = DatabaseService.add_network_data(data, prediction_result)

            # Emit network data to connected clients
            from app import emit_network_data
            emit_network_data(network_data)

            # Return prediction result
            return {
                "id": network_data.id,
                "timestamp": network_data.timestamp.isoformat(),
                "prediction": {
                    "class": network_data.predicted_class,
                    "label": network_data.predicted_label,
                    "confidence": network_data.prediction_confidence,
                    "probabilities": json.loads(network_data.class_probabilities)
                },
                "data": {
                    "flow_duration": network_data.flow_duration,
                    "protocol": network_data.protocol,
                    "flow_bytes_s": network_data.flow_bytes_s,
                    "flow_packets_s": network_data.flow_packets_s,
                    "packet_length_mean": network_data.packet_length_mean,
                    "packet_length_std": network_data.packet_length_std,
                    "packet_length_min": network_data.packet_length_min,
                    "packet_length_max": network_data.packet_length_max,
                    "source_ip": network_data.source_ip,
                    "destination_ip": network_data.destination_ip,
                    "source_port": network_data.source_port,
                    "destination_port": network_data.destination_port
                }
            }, 201

        except Exception as e:
            return {"error": str(e)}, 500

class NetworkDataListAPI(Resource):
    """
    API for retrieving network data
    """
    def get(self):
        """
        Get all network data
        """
        try:
            # Get limit parameter from query string
            limit = request.args.get('limit', default=100, type=int)

            # Get network data from database
            network_data_list = DatabaseService.get_all_network_data(limit=limit)

            # Convert to list of dictionaries
            result = [data.to_dict() for data in network_data_list]

            return {"data": result, "count": len(result)}, 200

        except Exception as e:
            return {"error": str(e)}, 500

class NetworkDataDetailAPI(Resource):
    """
    API for retrieving network data by ID
    """
    def get(self, id):
        """
        Get network data by ID
        """
        try:
            # Get network data from database
            network_data = DatabaseService.get_network_data_by_id(id)

            if not network_data:
                return {"error": f"Network data with ID {id} not found"}, 404

            # Convert to dictionary
            result = network_data.to_dict()

            return result, 200

        except Exception as e:
            return {"error": str(e)}, 500

class NetworkDataByLabelAPI(Resource):
    """
    API for retrieving network data by predicted label
    """
    def get(self, label):
        """
        Get network data by predicted label
        """
        try:
            # Get limit parameter from query string
            limit = request.args.get('limit', default=100, type=int)

            # Get network data from database
            network_data_list = DatabaseService.get_network_data_by_label(label, limit=limit)

            # Convert to list of dictionaries
            result = [data.to_dict() for data in network_data_list]

            return {"data": result, "count": len(result)}, 200

        except Exception as e:
            return {"error": str(e)}, 500
