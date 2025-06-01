import os
import json
from flask import Flask, render_template, jsonify, redirect, url_for, flash
from flask_restful import Api
from flask_socketio import SocketIO

from models import ModelService
from database import init_db, DatabaseService
from api import NetworkDataAPI, NetworkDataListAPI, NetworkDataDetailAPI, NetworkDataByLabelAPI

# Create Flask app
app = Flask(__name__)

# Configure app
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///ddos_detection.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
init_db(app)

# Initialize SocketIO for real-time updates
socketio = SocketIO(app)

# Initialize model service
model_service = ModelService(
    model_path=os.environ.get('MODEL_PATH', 'random_forest_model.pkl'),
    scaler_path=os.environ.get('SCALER_PATH', None)
)

# Initialize API
api = Api(app)

# Register API endpoints
api.add_resource(
    NetworkDataAPI, 
    '/api/network-data', 
    resource_class_kwargs={'model_service': model_service}
)
api.add_resource(NetworkDataListAPI, '/api/network-data/list')
api.add_resource(NetworkDataDetailAPI, '/api/network-data/<int:id>')
api.add_resource(NetworkDataByLabelAPI, '/api/network-data/label/<string:label>')

# Frontend routes
@app.route('/')
def index():
    """
    Render the main dashboard page
    """
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """
    Render the dashboard page
    """
    return render_template('dashboard.html')

@app.route('/history')
def history():
    """
    Render the history page
    """
    return render_template('history.html')

@app.route('/about')
def about():
    """
    Render the about page
    """
    return render_template('about.html')

@app.route('/clear', methods=['POST'])
def clear_application():
    """
    Clear all network data from the database
    """
    try:
        count = DatabaseService.clear_all_network_data()
        return jsonify({
            'success': True,
            'message': f'Successfully cleared {count} records from the database'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error clearing database: {str(e)}'
        }), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    """
    Handle 404 errors
    """
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    """
    Handle 500 errors
    """
    return render_template('500.html'), 500

# SocketIO event handlers
@socketio.on('connect')
def handle_connect():
    """
    Handle client connection
    """
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    """
    Handle client disconnection
    """
    print('Client disconnected')

# Function to emit network data to connected clients
def emit_network_data(network_data):
    """
    Emit network data to connected clients

    Args:
        network_data (NetworkData): Network data to emit
    """
    # Convert to dictionary
    data = network_data.to_dict()

    # Parse class probabilities
    if data['class_probabilities']:
        probabilities = json.loads(data['class_probabilities'])
    else:
        probabilities = {}

    # Create prediction object
    prediction = {
        'class': data['predicted_class'],
        'label': data['predicted_label'],
        'confidence': data['prediction_confidence'],
        'probabilities': probabilities
    }

    # Create data object
    network_data_dict = {
        'id': data['id'],
        'timestamp': data['timestamp'],
        'prediction': prediction,
        'data': {
            'flow_duration': data['flow_duration'],
            'protocol': data['protocol'],
            'flow_bytes_s': data['flow_bytes_s'],
            'flow_packets_s': data['flow_packets_s'],
            'packet_length_mean': data['packet_length_mean'],
            'packet_length_std': data['packet_length_std'],
            'packet_length_min': data['packet_length_min'],
            'packet_length_max': data['packet_length_max'],
            'source_ip': data['source_ip'],
            'destination_ip': data['destination_ip'],
            'source_port': data['source_port'],
            'destination_port': data['destination_port']
        }
    }

    # Emit to all connected clients
    socketio.emit('new_network_data', network_data_dict)

# Run the app
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    # Using eventlet as the async mode for better performance
    socketio.run(app, host='0.0.0.0', port=port, debug=True, use_reloader=True)
