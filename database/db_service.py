import json
from .models import db, NetworkData

class DatabaseService:
    """
    Service for database operations
    """
    @staticmethod
    def add_network_data(data, prediction_result):
        """
        Add network data and prediction results to the database

        Args:
            data (dict): Network data
            prediction_result (dict): Prediction results from the model

        Returns:
            NetworkData: The created database record
        """
        # Extract prediction details
        predicted_class = prediction_result.get('predicted_class')
        predicted_label = prediction_result.get('predicted_label')
        probabilities = prediction_result.get('probabilities', {})

        # Find the highest probability
        prediction_confidence = max(probabilities.values()) if probabilities else None

        # Create a new NetworkData instance
        network_data = NetworkData(
            # Network data features
            flow_duration=data.get('Flow Duration'),
            protocol=data.get('Protocol'),
            flow_bytes_s=data.get('Flow Bytes/s'),
            flow_packets_s=data.get('Flow Packets/s'),
            packet_length_mean=data.get('Packet Length Mean'),
            packet_length_std=data.get('Packet Length Std'),
            packet_length_min=data.get('Packet Length Min'),
            packet_length_max=data.get('Packet Length Max'),

            # Source and destination information
            source_ip=data.get('Source IP'),
            destination_ip=data.get('Destination IP'),
            source_port=data.get('Source Port'),
            destination_port=data.get('Destination Port'),

            # Prediction results
            predicted_class=predicted_class,
            predicted_label=predicted_label,
            prediction_confidence=prediction_confidence,
            class_probabilities=json.dumps(probabilities)
        )

        # Add to database
        db.session.add(network_data)
        db.session.commit()

        return network_data

    @staticmethod
    def get_all_network_data(limit=100):
        """
        Get all network data from the database

        Args:
            limit (int): Maximum number of records to return

        Returns:
            list: List of NetworkData objects
        """
        return NetworkData.query.order_by(NetworkData.timestamp.desc()).limit(limit).all()

    @staticmethod
    def get_network_data_by_id(id):
        """
        Get network data by ID

        Args:
            id (int): ID of the network data record

        Returns:
            NetworkData: The network data record
        """
        return NetworkData.query.get(id)

    @staticmethod
    def get_network_data_by_label(label, limit=100):
        """
        Get network data by predicted label

        Args:
            label (str): Predicted label
            limit (int): Maximum number of records to return

        Returns:
            list: List of NetworkData objects
        """
        return NetworkData.query.filter_by(predicted_label=label).order_by(NetworkData.timestamp.desc()).limit(limit).all()

    @staticmethod
    def clear_all_network_data():
        """
        Clear all network data from the database

        Returns:
            int: Number of records deleted
        """
        count = NetworkData.query.delete()
        db.session.commit()
        return count

    @staticmethod
    def get_label_distribution():
        """
        Get the distribution of predicted labels in the database

        Returns:
            dict: Dictionary with label counts
        """
        from sqlalchemy import func

        # Query the database to count occurrences of each label
        result = db.session.query(
            NetworkData.predicted_label, 
            func.count(NetworkData.id)
        ).group_by(NetworkData.predicted_label).all()

        # Convert to dictionary
        distribution = {
            'Benign': 0,
            'Syn': 0,
            'UDP': 0,
            'UDPLag': 0,
            'LDAP': 0,
            'MSSQL': 0,
            'NetBIOS': 0,
            'Portmap': 0
        }

        # Update with actual counts
        for label, count in result:
            if label in distribution:
                distribution[label] = count

        return distribution
