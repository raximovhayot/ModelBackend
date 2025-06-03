import requests
import json
import time
import random
from datetime import datetime

# API endpoint
API_URL = "http://localhost:5000/api/network-data"

# Sample data for different attack types
SAMPLE_DATA = [
    # Benign traffic
    {
        "Flow Duration": 1234,
        "Protocol": "TCP",
        "Flow Bytes/s": 1000.5,
        "Flow Packets/s": 10.5,
        "Packet Length Mean": 100.2,
        "Packet Length Std": 10.5,
        "Packet Length Min": 60,
        "Packet Length Max": 1500,
        "Source IP": "192.168.1.1",
        "Destination IP": "10.0.0.1",
        "Source Port": 12345,
        "Destination Port": 80
    },
    # SYN flood attack
    {
        "Flow Duration": 500,
        "Protocol": "TCP",
        "Flow Bytes/s": 5000.0,
        "Flow Packets/s": 100.0,
        "Packet Length Mean": 60.0,
        "Packet Length Std": 5.0,
        "Packet Length Min": 54,
        "Packet Length Max": 66,
        "Source IP": "192.168.1.2",
        "Destination IP": "10.0.0.2",
        "Source Port": 54321,
        "Destination Port": 80
    },
    # UDP flood attack
    {
        "Flow Duration": 800,
        "Protocol": "UDP",
        "Flow Bytes/s": 8000.0,
        "Flow Packets/s": 150.0,
        "Packet Length Mean": 200.0,
        "Packet Length Std": 20.0,
        "Packet Length Min": 150,
        "Packet Length Max": 250,
        "Source IP": "192.168.1.3",
        "Destination IP": "10.0.0.3",
        "Source Port": 33333,
        "Destination Port": 53
    }
]

def send_data(data):
    """
    Send data to the API and print the response
    """
    try:
        response = requests.post(API_URL, json=data)
        
        if response.status_code == 201:
            result = response.json()
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Data sent successfully!")
            print(f"Prediction: {result['prediction']['label']} with {result['prediction']['confidence']*100:.2f}% confidence")
            print("-" * 50)
            return True
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return False
    
    except Exception as e:
        print(f"Exception: {str(e)}")
        return False

def generate_random_data():
    """
    Generate random network data based on the sample data
    """
    # Choose a random sample as base
    base = random.choice(SAMPLE_DATA)
    
    # Create a copy and add some randomness
    data = base.copy()
    data["Flow Duration"] = base["Flow Duration"] * (0.8 + 0.4 * random.random())
    data["Flow Bytes/s"] = base["Flow Bytes/s"] * (0.8 + 0.4 * random.random())
    data["Flow Packets/s"] = base["Flow Packets/s"] * (0.8 + 0.4 * random.random())
    data["Packet Length Mean"] = base["Packet Length Mean"] * (0.9 + 0.2 * random.random())
    data["Packet Length Std"] = base["Packet Length Std"] * (0.9 + 0.2 * random.random())
    
    # Randomize IP addresses slightly
    ip_parts = data["Source IP"].split('.')
    ip_parts[3] = str(random.randint(1, 254))
    data["Source IP"] = '.'.join(ip_parts)
    
    ip_parts = data["Destination IP"].split('.')
    ip_parts[3] = str(random.randint(1, 254))
    data["Destination IP"] = '.'.join(ip_parts)
    
    # Randomize ports
    data["Source Port"] = random.randint(10000, 65535)
    data["Destination Port"] = random.choice([80, 443, 22, 53, 8080])
    
    return data

def main():
    """
    Main function to test the API
    """
    print("DDoS Detection API Test")
    print("=" * 50)
    print(f"API URL: {API_URL}")
    print("=" * 50)
    
    # Test with predefined samples
    print("Testing with predefined samples...")
    for i, data in enumerate(SAMPLE_DATA):
        print(f"Sample {i+1}:")
        send_data(data)
    
    # Test with random data
    print("\nTesting with random data (press Ctrl+C to stop)...")
    try:
        while True:
            data = generate_random_data()
            send_data(data)
            time.sleep(2)  # Wait 2 seconds between requests
    
    except KeyboardInterrupt:
        print("\nTest stopped by user.")

if __name__ == "__main__":
    main()