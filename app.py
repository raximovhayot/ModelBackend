import os
import json
from flask import Flask, render_template, jsonify, redirect, url_for, flash
from flask_restful import Api
from flask_socketio import SocketIO

from models import ModelService
from database import init_db, DatabaseService
from api import NetworkDataAPI, NetworkDataListAPI, NetworkDataDetailAPI, NetworkDataByLabelAPI
from api.network_data_api import QueueStatsAPI
from utils.socketio_utils import emit_network_data

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
api.add_resource(QueueStatsAPI, '/api/queue-stats')

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

@app.route('/explanation')
def explanation():
    """
    Render the explanation page
    """
    return render_template('explanation.html')

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


# Run the app if executed directly
if __name__ == '__main__':
    # This is for development only - use run.py for production
    port = int(os.environ.get('PORT', 5000))
    # Using eventlet as the async mode for better performance
    socketio.run(app, host='0.0.0.0', port=port, debug=True, use_reloader=True)
