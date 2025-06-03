import json

def emit_network_data(socketio, network_data):
    """
    Emit network data to connected clients

    Args:
        socketio: The SocketIO instance
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