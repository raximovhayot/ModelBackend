# DDoS Detection System

A web application that uses machine learning to detect and classify DDoS (Distributed Denial of Service) attacks in network traffic.

## Features

- **Real-time detection**: Analyze network traffic data in real-time to detect DDoS attacks
- **Multi-class classification**: Identify various types of DDoS attacks (Syn, UDP, LDAP, and others)
- **Interactive dashboard**: Visualize network traffic and attack statistics
- **Historical data**: View and filter historical network data and detections
- **REST API**: Receive network data and return predictions via RESTful API

## Architecture

The application consists of the following components:

### Backend
- **REST API**: Receives network data and returns predictions
- **Prediction service**: Uses a Random Forest model to classify network traffic
- **Database**: Stores network data and prediction results
- **WebSocket Server**: Provides real-time updates to the UI
- **Queue Service**: Queues and processes prediction tasks
- **Utils**: Common functionality and helper functions

### Frontend
- **Dashboard**: Shows network traffic and attack detection in real-time
- **History**: Shows historical network data and detections
- **Charts**: Visualizes detection statistics and trends

## Installation

### Requirements
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd ddos_detection_app
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Place the trained model file (`random_forest_model.pkl`) in the application directory.

4. Run the application:

   To run only the Flask application:
   ```
   python app.py
   ```

   To run only the worker process:
   ```
   python worker.py
   ```

   To run both the Flask application and worker process simultaneously:
   ```
   python run.py
   ```

5. Access the application in your web browser at `http://localhost:5000`

### Docker Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd ddos_detection_app
   ```

2. Start the application using Docker Compose:
   ```
   docker-compose up -d
   ```

3. Access the application in your web browser at `http://localhost:5000`

4. To stop the application:
   ```
   docker-compose down
   ```

#### Docker Environment Configuration

The Docker Compose file includes the following services:

- **app**: Main application (Flask and worker processes)
- **redis**: Redis for queue service

To configure the environment, modify the environment variables in the `docker-compose.yml` file.

### Detailed Installation Guide

For a comprehensive guide on installing and deploying the application, please refer to the [DEPLOYMENT.md](DEPLOYMENT.md) file. This document includes detailed information on local and Docker installation, production deployment, and troubleshooting.

## Usage

### Dashboard

The dashboard shows network traffic analysis and DDoS attack detection in real-time. It includes:

- Latest detection with details
- Detection statistics chart
- Table of recent detections

### History

The history page allows viewing and filtering historical network data and detections:

1. Select filters (attack type, limit)
2. Click "Apply Filters" to update results
3. Click the Data button to view detection details

### API

The application provides a REST API for submitting network data and making predictions:

#### Endpoints

- `POST /api/network-data`: Submit network data for prediction
- `GET /api/network-data/list`: Get all network data
- `GET /api/network-data/<id>`: Get network data by ID
- `GET /api/network-data/label/<label>`: Get network data by predicted label

#### Sample Request

```json
POST /api/network-data
Content-Type: application/json

{
  "protocol": 6,
  "flow_duration": 1234,
  "total_fwd_packets": 10,
  "total_backward_packets": 5,
  "fwd_packets_length_total": 1500.0,
  "bwd_packets_length_total": 500.0,
  "fwd_packet_length_max": 150.0,
  "fwd_packet_length_min": 60.0,
  "fwd_packet_length_std": 20.0,
  "bwd_packet_length_max": 100.0,
  "bwd_packet_length_min": 40.0,
  "flow_bytes_per_s": 1000.5,
  "flow_packets_per_s": 10.5,
  "bwd_packets_per_s": 5.0,
  "flow_iat_mean": 100.0,
  "flow_iat_min": 10.0,
  "fwd_iat_total": 500.0,
  "fwd_iat_mean": 50.0,
  "fwd_iat_min": 5.0,
  "bwd_iat_total": 400.0,
  "bwd_iat_mean": 80.0,
  "bwd_iat_min": 8.0,
  "fwd_header_length": 200,
  "bwd_header_length": 100,
  "packet_length_max": 150.0,
  "packet_length_mean": 100.2,
  "syn_flag_count": 1,
  "ack_flag_count": 1,
  "urg_flag_count": 0,
  "down_up_ratio": 0.5,
  "active_mean": 100.0,
  "active_std": 10.0,
  "active_max": 200.0,
  "active_min": 50.0,
  "idle_mean": 50.0,
  "idle_std": 5.0,
  "idle_max": 100.0,
  "idle_min": 10.0,
  "source_ip": "192.168.1.1",
  "destination_ip": "10.0.0.1",
  "source_port": 12345,
  "destination_port": 80
}
```

#### Sample Response

```json
{
  "id": 1,
  "timestamp": "2023-07-01T12:34:56.789Z",
  "prediction": {
    "class": 0,
    "label": "Benign",
    "confidence": 0.95,
    "probabilities": {
      "Benign": 0.95,
      "Syn": 0.01,
      "UDP": 0.01,
      "UDPLag": 0.01,
      "LDAP": 0.005,
      "MSSQL": 0.005,
      "NetBIOS": 0.005,
      "Portmap": 0.005
    }
  },
  "data": {
    "flow_duration": 1234,
    "protocol": 6,
    "flow_bytes_s": 1000.5,
    "flow_packets_s": 10.5,
    "packet_length_mean": 100.2,
    "packet_length_std": 10.0,
    "packet_length_min": 60.0,
    "packet_length_max": 150.0,
    "source_ip": "192.168.1.1",
    "destination_ip": "10.0.0.1",
    "source_port": 12345,
    "destination_port": 80,
    "predicted_class": 0,
    "predicted_label": "Benign",
    "prediction_confidence": 0.95
  }
}
```

## Machine Learning Model

The system uses a **Random Forest** classifier trained on the **CICDDoS2019** dataset to detect and classify DDoS attacks. The model can identify the following attack types:

- **Benign**: Normal, non-attack traffic
- **Syn**: SYN flood attack
- **UDP**: General UDP flood attack
- **UDPLag**: UDP-based DDoS with lag
- **LDAP**: Lightweight Directory Access Protocol-based attack
- **MSSQL**: MSSQL-specific DDoS attack
- **NetBIOS**: NetBIOS-related DDoS attack
- **Portmap**: Portmapper-based DDoS attack

## Technologies Used

### Backend
- Python
- Flask
- Flask-RESTful
- Flask-SQLAlchemy
- Flask-SocketIO
- scikit-learn

### Frontend
- HTML/CSS/JavaScript
- Bootstrap 5
- Chart.js
- Socket.IO
- Font Awesome

### Data Processing
- pandas
- NumPy
- Matplotlib
- seaborn

## License

This project is licensed under the MIT License - see the LICENSE file for details.