import argparse
import ipaddress
import os
import random
import time
from glob import glob

import pandas as pd
import requests

# Define attack types based on the CICDDoS2019 dataset
ATTACK_TYPES = {
    'LDAP': 1,
    'MSSQL': 2,
    'NetBIOS': 3,
    'Portmap': 4,
    'Syn': 5,
    'UDP': 6,
    'UDPLag': 7
}

# Define normal traffic type
NORMAL_TYPE = {'Benign': 0}

def generate_ip():
    """Generate a random IP address"""
    return str(ipaddress.IPv4Address(random.randint(0, 2**32 - 1)))

def generate_port():
    """Generate a random port number"""
    return random.randint(1, 65535)


def read_parquet_data(file_path):
    """
    Read network traffic data from a parquet file

    Args:
        file_path (str): Path to the parquet file

    Returns:
        list: A list of dictionaries containing network traffic features
    """
    try:
        # Read the parquet file
        df = pd.read_parquet(file_path)

        # Extract the attack type from the filename
        filename = os.path.basename(file_path)
        attack_type = filename.split('-')[0]

        # Convert DataFrame to list of dictionaries
        records = []
        for _, row in df.iterrows():
            # Convert row to dictionary with lowercase keys
            data = {
                'protocol': int(row['Protocol']),
                'flow_duration': int(row['Flow Duration']),
                'total_fwd_packets': int(row['Total Fwd Packets']),
                'total_backward_packets': int(row['Total Backward Packets']),
                'fwd_packets_length_total': float(row['Fwd Packets Length Total']),
                'bwd_packets_length_total': float(row['Bwd Packets Length Total']),
                'fwd_packet_length_max': float(row['Fwd Packet Length Max']),
                'fwd_packet_length_min': float(row['Fwd Packet Length Min']),
                'fwd_packet_length_std': float(row['Fwd Packet Length Std']),
                'bwd_packet_length_max': float(row['Bwd Packet Length Max']),
                'bwd_packet_length_min': float(row['Bwd Packet Length Min']),
                'flow_bytes_per_s': float(row['Flow Bytes/s']),
                'flow_packets_per_s': float(row['Flow Packets/s']),
                'bwd_packets_per_s': float(row.get('Bwd Packets/s', 0.0)),
                'flow_iat_mean': float(row['Flow IAT Mean']),
                'flow_iat_min': float(row['Flow IAT Min']),
                'fwd_iat_total': float(row.get('Fwd IAT Total', 0.0)),
                'fwd_iat_mean': float(row['Fwd IAT Mean']),
                'fwd_iat_min': float(row['Fwd IAT Min']),
                'bwd_iat_total': float(row.get('Bwd IAT Total', 0.0)),
                'bwd_iat_mean': float(row['Bwd IAT Mean']),
                'bwd_iat_min': float(row['Bwd IAT Min']),
                'fwd_header_length': int(row['Fwd Header Length']),
                'bwd_header_length': int(row['Bwd Header Length']),
                'packet_length_max': float(row['Packet Length Max']),
                'packet_length_mean': float(row['Packet Length Mean']),
                'syn_flag_count': int(row['SYN Flag Count']),
                'ack_flag_count': int(row['ACK Flag Count']),
                'urg_flag_count': int(row['URG Flag Count']),
                'down_up_ratio': float(row['Down/Up Ratio']),
                'active_mean': float(row['Active Mean']),
                'active_std': float(row['Active Std']),
                'active_max': float(row['Active Max']),
                'active_min': float(row['Active Min']),
                'idle_mean': float(row['Idle Mean']),
                'idle_std': float(row['Idle Std']),
                'idle_max': float(row['Idle Max']),
                'idle_min': float(row['Idle Min']),
                # Generate random IPs and ports since they're not in the dataset
                'source_ip': generate_ip(),
                'destination_ip': generate_ip(),
                'source_port': generate_port(),
                'destination_port': generate_port()
            }
            records.append(data)

        return records
    except Exception as e:
        print(f"Error reading parquet file {file_path}: {str(e)}")
        return []

def post_to_api(data, api_url):
    """
    Post data to the network data API

    Args:
        data (dict): Data to post
        api_url (str): URL of the API

    Returns:
        dict: Response from the API
    """
    try:
        response = requests.post(api_url, json=data)
        return {
            'status_code': response.status_code,
            'response': response.json() if response.status_code == 202 else response.text
        }
    except Exception as e:
        return {'error': str(e)}

def main():
    parser = argparse.ArgumentParser(description='Read and send network traffic data from parquet files')
    parser.add_argument('--api-url', type=str, default='http://localhost:5000/api/network-data',
                        help='URL of the network data API')
    parser.add_argument('--count', type=int, default=100,
                        help='Number of requests to send')
    parser.add_argument('--interval', type=float, default=1.0,
                        help='Interval between requests in seconds')
    parser.add_argument('--attack-types', type=str, nargs='+', 
                        default=['LDAP', 'MSSQL', 'NetBIOS', 'Portmap', 'Syn', 'UDP', 'UDPLag'],
                        help='Types of attacks to filter from parquet files')
    parser.add_argument('--data-dir', type=str, default='mock_data',
                        help='Directory containing parquet data files')

    args = parser.parse_args()

    print(f"Starting tester with {args.count} requests at {args.interval}s intervals")
    print(f"Reading data from {args.data_dir}")

    # Get all parquet files in the data directory
    data_files = glob(os.path.join(args.data_dir, '*.parquet'))
    if not data_files:
        print(f"No parquet files found in {args.data_dir}")
        return

    print(f"Found {len(data_files)} data files: {[os.path.basename(f) for f in data_files]}")

    # Read all data files
    all_records = []
    for file_path in data_files:
        attack_type = os.path.basename(file_path).split('-')[0]
        if attack_type in args.attack_types or not args.attack_types:
            records = read_parquet_data(file_path)
            if records:
                print(f"Loaded {len(records)} records from {os.path.basename(file_path)}")
                all_records.extend([(record, attack_type) for record in records])

    if not all_records:
        print("No records loaded from data files")
        return

    # Shuffle the records to randomize the order
    random.shuffle(all_records)

    # Limit to the requested count
    records_to_send = all_records[:args.count]

    print(f"Sending {len(records_to_send)} records to API at {args.api_url}")

    for i, (data, attack_type) in enumerate(records_to_send):
        # Post to API
        print(f"\nRequest {i+1}/{len(records_to_send)} - Attack ({attack_type})")
        response = post_to_api(data, args.api_url)

        if 'error' in response:
            print(f"Error: {response['error']}")
        else:
            print(f"Status: {response['status_code']}")
            print(f"Response: {response['response']}")

        # Wait for the specified interval
        if i < len(records_to_send) - 1:
            time.sleep(args.interval)

    print("\nTesting completed!")

if __name__ == "__main__":
    main()
