from flask import request, jsonify
from flask_restful import Resource
import json

from models import ModelService
from database import DatabaseService
from flow.flow_features import FlowFeatures
from queue_service import enqueue_network_data, get_queue_stats

class NetworkDataAPI(Resource):
    """
    API for receiving network data and making predictions
    """
    def __init__(self, model_service):
        self.model_service = model_service

    def post(self):
        """
        Receive network data, enqueue for processing, and return job ID
        """
        try:
            # Get data from request
            json_data = request.get_json()

            if not json_data:
                return {"error": "No data provided"}, 400

            # Convert JSON data to FlowFeatures instance
            try:
                flow_features = FlowFeatures.from_json(json_data)
                # Convert FlowFeatures to dictionary format expected by the model and database service
                data = flow_features.to_model_dict()
            except Exception as e:
                return {"error": f"Invalid flow features data: {str(e)}"}, 400

            # Enqueue data for processing
            job_id = enqueue_network_data(data, flow_features.to_dict())

            # Return job ID and status
            return {
                "success": True,
                "message": "Network data enqueued for processing",
                "job_id": job_id,
                "queue_stats": get_queue_stats()
            }, 202

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

class QueueStatsAPI(Resource):
    """
    API for retrieving queue statistics
    """
    def get(self):
        """
        Get queue statistics
        """
        try:
            # Get queue statistics
            stats = get_queue_stats()

            return stats, 200

        except Exception as e:
            return {"error": str(e)}, 500
