# DDoS Detection Application - Deployment Guide

This document provides comprehensive instructions for deploying the DDoS Detection Application in various environments.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Local Deployment](#local-deployment)
- [Docker Deployment](#docker-deployment)
- [Production Deployment](#production-deployment)
- [Troubleshooting](#troubleshooting)

## Prerequisites

Before deploying the application, ensure you have the following:

### For Local Deployment
- Python 3.8 or higher
- pip (Python package manager)
- Git

### For Docker Deployment
- Docker
- Docker Compose
- Git

## Local Deployment

Follow these steps to deploy the application locally:

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ddos_detection_app
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Place the trained model file**
   
   Ensure the `random_forest_model.pkl` file is in the application directory.

4. **Run the application**

   You have several options to run the application:

   a. Run only the Flask application:
   ```bash
   python app.py
   ```

   b. Run only the worker process:
   ```bash
   python worker.py
   ```

   c. Run both the Flask application and worker process simultaneously:
   ```bash
   python run.py
   ```

5. **Access the application**
   
   Open your web browser and navigate to `http://localhost:5000`

## Docker Deployment

Docker provides an isolated environment for running the application with all its dependencies:

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ddos_detection_app
   ```

2. **Build and start the containers**
   ```bash
   docker-compose up -d
   ```
   This command builds the application image and starts both the app and Redis containers in detached mode.

3. **Access the application**
   
   Open your web browser and navigate to `http://localhost:5000`

4. **Stop the application**
   ```bash
   docker-compose down
   ```

### Docker Environment Configuration

The Docker Compose file includes the following services:

- **app**: The main application (Flask and worker processes)
- **redis**: Redis service for queue functionality

You can customize the environment by modifying the environment variables in the `docker-compose.yml` file.

## Production Deployment

For production environments, consider the following additional steps:

### Security Considerations

1. **Change default passwords**
   
   Update the Redis password in `docker-compose.yml` and ensure it's reflected in the application's environment variables.

2. **Use HTTPS**
   
   Configure a reverse proxy (like Nginx) in front of the application to handle HTTPS.

### Scaling

1. **Separate services**
   
   For high-load environments, consider running the Flask application and worker processes on separate containers or servers.

2. **Database scaling**
   
   Consider using a more robust database solution instead of SQLite for production.

### Example Nginx Configuration

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Troubleshooting

### Common Issues

1. **Application not starting**
   
   Check the logs for errors:
   ```bash
   # For local deployment
   cat ddos_detection.log
   
   # For Docker deployment
   docker-compose logs app
   ```

2. **Redis connection issues**
   
   Ensure Redis is running and accessible:
   ```bash
   # For local deployment
   redis-cli ping
   
   # For Docker deployment
   docker-compose logs redis
   ```

3. **Model not found**
   
   Ensure the `random_forest_model.pkl` file is in the correct location.

### Logs

The application generates several log files:

- `ddos_detection.log`: Main application logs
- `queue.log`: Queue service logs
- `worker.log`: Worker process logs

Review these logs when troubleshooting issues.