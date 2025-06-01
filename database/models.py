from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class NetworkData(db.Model):
    """
    Model for storing network data and predictions
    """
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Network data features
    flow_duration = db.Column(db.Float, nullable=True)
    protocol = db.Column(db.String(20), nullable=True)
    flow_bytes_s = db.Column(db.Float, nullable=True)
    flow_packets_s = db.Column(db.Float, nullable=True)
    packet_length_mean = db.Column(db.Float, nullable=True)
    packet_length_std = db.Column(db.Float, nullable=True)
    packet_length_min = db.Column(db.Float, nullable=True)
    packet_length_max = db.Column(db.Float, nullable=True)
    
    # Additional features can be added based on the model requirements
    
    # Prediction results
    predicted_class = db.Column(db.Integer, nullable=True)
    predicted_label = db.Column(db.String(50), nullable=True)
    prediction_confidence = db.Column(db.Float, nullable=True)  # Highest probability
    
    # JSON string of all class probabilities
    class_probabilities = db.Column(db.Text, nullable=True)
    
    # Source and destination information
    source_ip = db.Column(db.String(50), nullable=True)
    destination_ip = db.Column(db.String(50), nullable=True)
    source_port = db.Column(db.Integer, nullable=True)
    destination_port = db.Column(db.Integer, nullable=True)
    
    def __repr__(self):
        return f"<NetworkData {self.id}: {self.predicted_label} ({self.prediction_confidence:.2f})>"
    
    def to_dict(self):
        """
        Convert the model instance to a dictionary
        """
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'flow_duration': self.flow_duration,
            'protocol': self.protocol,
            'flow_bytes_s': self.flow_bytes_s,
            'flow_packets_s': self.flow_packets_s,
            'packet_length_mean': self.packet_length_mean,
            'packet_length_std': self.packet_length_std,
            'packet_length_min': self.packet_length_min,
            'packet_length_max': self.packet_length_max,
            'predicted_class': self.predicted_class,
            'predicted_label': self.predicted_label,
            'prediction_confidence': self.prediction_confidence,
            'class_probabilities': self.class_probabilities,
            'source_ip': self.source_ip,
            'destination_ip': self.destination_ip,
            'source_port': self.source_port,
            'destination_port': self.destination_port
        }

def init_db(app):
    """
    Initialize the database with the Flask app
    """
    db.init_app(app)
    
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()