import json
from flow.flow_features import FlowFeatures

def test_flow_features_serialization():
    """
    Test serialization and deserialization of FlowFeatures
    """
    # Create a sample FlowFeatures instance
    flow_features = FlowFeatures(
        protocol=6,  # TCP
        flow_duration=1000,
        total_fwd_packets=10,
        total_backward_packets=5,
        fwd_packets_length_total=1500.0,
        bwd_packets_length_total=750.0,
        fwd_packet_length_max=200.0,
        fwd_packet_length_min=50.0,
        fwd_packet_length_std=25.0,
        bwd_packet_length_max=150.0,
        bwd_packet_length_min=40.0,
        flow_bytes_per_s=2250.0,
        flow_packets_per_s=15.0,
        bwd_packets_per_s=5.0,
        packet_length_mean=150.0,
        syn_flag_count=1,
        ack_flag_count=10,
        urg_flag_count=0
    )
    
    # Convert to JSON
    json_str = flow_features.to_json()
    print(f"JSON representation: {json_str}")
    
    # Convert back to FlowFeatures
    flow_features2 = FlowFeatures.from_json(json_str)
    
    # Verify that the two instances are equal
    assert flow_features.protocol == flow_features2.protocol
    assert flow_features.flow_duration == flow_features2.flow_duration
    assert flow_features.total_fwd_packets == flow_features2.total_fwd_packets
    assert flow_features.total_backward_packets == flow_features2.total_backward_packets
    assert flow_features.fwd_packets_length_total == flow_features2.fwd_packets_length_total
    assert flow_features.bwd_packets_length_total == flow_features2.bwd_packets_length_total
    assert flow_features.flow_bytes_per_s == flow_features2.flow_bytes_per_s
    assert flow_features.flow_packets_per_s == flow_features2.flow_packets_per_s
    assert flow_features.syn_flag_count == flow_features2.syn_flag_count
    assert flow_features.ack_flag_count == flow_features2.ack_flag_count
    assert flow_features.urg_flag_count == flow_features2.urg_flag_count
    
    print("Serialization test passed!")
    
    # Test to_model_dict
    model_dict = flow_features.to_model_dict()
    print(f"Model dictionary: {model_dict}")
    
    # Verify that the model dictionary has the expected keys
    assert 'Flow Duration' in model_dict
    assert 'Protocol' in model_dict
    assert 'Flow Bytes/s' in model_dict
    assert 'Flow Packets/s' in model_dict
    assert 'Packet Length Mean' in model_dict
    assert 'Packet Length Std' in model_dict
    assert 'Packet Length Min' in model_dict
    assert 'Packet Length Max' in model_dict
    
    # Verify that the values are correct
    assert model_dict['Flow Duration'] == flow_features.flow_duration
    assert model_dict['Protocol'] == str(flow_features.protocol)
    assert model_dict['Flow Bytes/s'] == flow_features.flow_bytes_per_s
    assert model_dict['Flow Packets/s'] == flow_features.flow_packets_per_s
    assert model_dict['Packet Length Mean'] == flow_features.packet_length_mean
    assert model_dict['Packet Length Std'] == flow_features.fwd_packet_length_std
    assert model_dict['Packet Length Min'] == flow_features.fwd_packet_length_min
    assert model_dict['Packet Length Max'] == flow_features.packet_length_max
    
    print("to_model_dict test passed!")

def test_flow_features_from_java():
    """
    Test deserialization of FlowFeatures from Java JSON format
    """
    # Sample JSON data from Java application
    java_json = {
        "protocol": 6,
        "flow_duration": 1000,
        "total_fwd_packets": 10,
        "total_backward_packets": 5,
        "fwd_packets_length_total": 1500.0,
        "bwd_packets_length_total": 750.0,
        "fwd_packet_length_max": 200.0,
        "fwd_packet_length_min": 50.0,
        "fwd_packet_length_std": 25.0,
        "bwd_packet_length_max": 150.0,
        "bwd_packet_length_min": 40.0,
        "flow_bytes_per_s": 2250.0,
        "flow_packets_per_s": 15.0,
        "bwd_packets_per_s": 5.0,
        "flow_iat_mean": 100.0,
        "flow_iat_min": 50.0,
        "fwd_iat_total": 900.0,
        "fwd_iat_mean": 100.0,
        "fwd_iat_min": 50.0,
        "bwd_iat_total": 400.0,
        "bwd_iat_mean": 100.0,
        "bwd_iat_min": 50.0,
        "fwd_header_length": 200,
        "bwd_header_length": 100,
        "packet_length_max": 200.0,
        "packet_length_mean": 150.0,
        "syn_flag_count": 1,
        "ack_flag_count": 10,
        "urg_flag_count": 0,
        "down_up_ratio": 0.5,
        "active_mean": 100.0,
        "active_std": 25.0,
        "active_max": 150.0,
        "active_min": 50.0,
        "idle_mean": 200.0,
        "idle_std": 50.0,
        "idle_max": 300.0,
        "idle_min": 100.0
    }
    
    # Convert to FlowFeatures
    flow_features = FlowFeatures.from_json(java_json)
    
    # Verify that the values are correct
    assert flow_features.protocol == java_json["protocol"]
    assert flow_features.flow_duration == java_json["flow_duration"]
    assert flow_features.total_fwd_packets == java_json["total_fwd_packets"]
    assert flow_features.total_backward_packets == java_json["total_backward_packets"]
    assert flow_features.fwd_packets_length_total == java_json["fwd_packets_length_total"]
    assert flow_features.bwd_packets_length_total == java_json["bwd_packets_length_total"]
    assert flow_features.flow_bytes_per_s == java_json["flow_bytes_per_s"]
    assert flow_features.flow_packets_per_s == java_json["flow_packets_per_s"]
    assert flow_features.syn_flag_count == java_json["syn_flag_count"]
    assert flow_features.ack_flag_count == java_json["ack_flag_count"]
    assert flow_features.urg_flag_count == java_json["urg_flag_count"]
    
    print("Deserialization from Java JSON test passed!")
    
    # Test to_model_dict
    model_dict = flow_features.to_model_dict()
    print(f"Model dictionary from Java JSON: {model_dict}")
    
    # Verify that the model dictionary has the expected keys and values
    assert model_dict['Flow Duration'] == flow_features.flow_duration
    assert model_dict['Protocol'] == str(flow_features.protocol)
    assert model_dict['Flow Bytes/s'] == flow_features.flow_bytes_per_s
    assert model_dict['Flow Packets/s'] == flow_features.flow_packets_per_s
    assert model_dict['Packet Length Mean'] == flow_features.packet_length_mean
    
    print("to_model_dict from Java JSON test passed!")

if __name__ == "__main__":
    print("Testing FlowFeatures serialization...")
    test_flow_features_serialization()
    
    print("\nTesting FlowFeatures deserialization from Java JSON...")
    test_flow_features_from_java()
    
    print("\nAll tests passed!")