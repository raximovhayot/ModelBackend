from dataclasses import dataclass, field
from typing import Dict, Any
import json

@dataclass
class FlowFeatures:
    """
    Contains statistical features extracted from a network flow.
    These features can be used for traffic analysis and classification,
    such as detecting DDoS attacks or other anomalies.
    """
    # Protocol and basic flow information
    protocol: int = 0
    flow_duration: int = 0
    total_fwd_packets: int = 0
    total_backward_packets: int = 0

    # Packet length statistics
    fwd_packets_length_total: float = 0.0
    bwd_packets_length_total: float = 0.0
    fwd_packet_length_max: float = 0.0
    fwd_packet_length_min: float = 0.0
    fwd_packet_length_std: float = 0.0
    bwd_packet_length_max: float = 0.0
    bwd_packet_length_min: float = 0.0

    # Flow rate statistics
    flow_bytes_per_s: float = 0.0
    flow_packets_per_s: float = 0.0
    bwd_packets_per_s: float = 0.0

    # Inter-arrival time (IAT) statistics
    flow_iat_mean: float = 0.0
    flow_iat_min: float = 0.0
    fwd_iat_total: float = 0.0
    fwd_iat_mean: float = 0.0
    fwd_iat_min: float = 0.0
    bwd_iat_total: float = 0.0
    bwd_iat_mean: float = 0.0
    bwd_iat_min: float = 0.0

    # Header information
    fwd_header_length: int = 0
    bwd_header_length: int = 0

    # Packet statistics
    packet_length_max: float = 0.0
    packet_length_mean: float = 0.0

    # TCP flag counts
    syn_flag_count: int = 0
    ack_flag_count: int = 0
    urg_flag_count: int = 0

    # Ratio statistics
    down_up_ratio: float = 0.0

    # Activity statistics
    active_mean: float = 0.0
    active_std: float = 0.0
    active_max: float = 0.0
    active_min: float = 0.0

    # Idle statistics
    idle_mean: float = 0.0
    idle_std: float = 0.0
    idle_max: float = 0.0
    idle_min: float = 0.0

    @classmethod
    def from_json(cls, json_data: str) -> 'FlowFeatures':
        """
        Create a FlowFeatures instance from a JSON string.

        Args:
            json_data (str): JSON string representation of FlowFeatures

        Returns:
            FlowFeatures: A new FlowFeatures instance
        """
        if isinstance(json_data, str):
            data = json.loads(json_data)
        else:
            data = json_data

        return cls(
            protocol=data.get('protocol', 0),
            flow_duration=data.get('flow_duration', 0),
            total_fwd_packets=data.get('total_fwd_packets', 0),
            total_backward_packets=data.get('total_backward_packets', 0),
            fwd_packets_length_total=data.get('fwd_packets_length_total', 0.0),
            bwd_packets_length_total=data.get('bwd_packets_length_total', 0.0),
            fwd_packet_length_max=data.get('fwd_packet_length_max', 0.0),
            fwd_packet_length_min=data.get('fwd_packet_length_min', 0.0),
            fwd_packet_length_std=data.get('fwd_packet_length_std', 0.0),
            bwd_packet_length_max=data.get('bwd_packet_length_max', 0.0),
            bwd_packet_length_min=data.get('bwd_packet_length_min', 0.0),
            flow_bytes_per_s=data.get('flow_bytes_per_s', 0.0),
            flow_packets_per_s=data.get('flow_packets_per_s', 0.0),
            bwd_packets_per_s=data.get('bwd_packets_per_s', 0.0),
            flow_iat_mean=data.get('flow_iat_mean', 0.0),
            flow_iat_min=data.get('flow_iat_min', 0.0),
            fwd_iat_total=data.get('fwd_iat_total', 0.0),
            fwd_iat_mean=data.get('fwd_iat_mean', 0.0),
            fwd_iat_min=data.get('fwd_iat_min', 0.0),
            bwd_iat_total=data.get('bwd_iat_total', 0.0),
            bwd_iat_mean=data.get('bwd_iat_mean', 0.0),
            bwd_iat_min=data.get('bwd_iat_min', 0.0),
            fwd_header_length=data.get('fwd_header_length', 0),
            bwd_header_length=data.get('bwd_header_length', 0),
            packet_length_max=data.get('packet_length_max', 0.0),
            packet_length_mean=data.get('packet_length_mean', 0.0),
            syn_flag_count=data.get('syn_flag_count', 0),
            ack_flag_count=data.get('ack_flag_count', 0),
            urg_flag_count=data.get('urg_flag_count', 0),
            down_up_ratio=data.get('down_up_ratio', 0.0),
            active_mean=data.get('active_mean', 0.0),
            active_std=data.get('active_std', 0.0),
            active_max=data.get('active_max', 0.0),
            active_min=data.get('active_min', 0.0),
            idle_mean=data.get('idle_mean', 0.0),
            idle_std=data.get('idle_std', 0.0),
            idle_max=data.get('idle_max', 0.0),
            idle_min=data.get('idle_min', 0.0)
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the FlowFeatures instance to a dictionary.

        Returns:
            Dict[str, Any]: Dictionary representation of FlowFeatures
        """
        return {
            'protocol': self.protocol,
            'flow_duration': self.flow_duration,
            'total_fwd_packets': self.total_fwd_packets,
            'total_backward_packets': self.total_backward_packets,
            'fwd_packets_length_total': self.fwd_packets_length_total,
            'bwd_packets_length_total': self.bwd_packets_length_total,
            'fwd_packet_length_max': self.fwd_packet_length_max,
            'fwd_packet_length_min': self.fwd_packet_length_min,
            'fwd_packet_length_std': self.fwd_packet_length_std,
            'bwd_packet_length_max': self.bwd_packet_length_max,
            'bwd_packet_length_min': self.bwd_packet_length_min,
            'flow_bytes_per_s': self.flow_bytes_per_s,
            'flow_packets_per_s': self.flow_packets_per_s,
            'bwd_packets_per_s': self.bwd_packets_per_s,
            'flow_iat_mean': self.flow_iat_mean,
            'flow_iat_min': self.flow_iat_min,
            'fwd_iat_total': self.fwd_iat_total,
            'fwd_iat_mean': self.fwd_iat_mean,
            'fwd_iat_min': self.fwd_iat_min,
            'bwd_iat_total': self.bwd_iat_total,
            'bwd_iat_mean': self.bwd_iat_mean,
            'bwd_iat_min': self.bwd_iat_min,
            'fwd_header_length': self.fwd_header_length,
            'bwd_header_length': self.bwd_header_length,
            'packet_length_max': self.packet_length_max,
            'packet_length_mean': self.packet_length_mean,
            'syn_flag_count': self.syn_flag_count,
            'ack_flag_count': self.ack_flag_count,
            'urg_flag_count': self.urg_flag_count,
            'down_up_ratio': self.down_up_ratio,
            'active_mean': self.active_mean,
            'active_std': self.active_std,
            'active_max': self.active_max,
            'active_min': self.active_min,
            'idle_mean': self.idle_mean,
            'idle_std': self.idle_std,
            'idle_max': self.idle_max,
            'idle_min': self.idle_min
        }

    def to_json(self) -> str:
        """
        Convert the FlowFeatures instance to a JSON string.

        Returns:
            str: JSON string representation of FlowFeatures
        """
        return json.dumps(self.to_dict())

    def to_model_dict(self) -> Dict[str, Any]:
        """
        Convert the FlowFeatures instance to a dictionary format expected by the model and database service.

        This method includes all available features from the FlowFeatures class, even though the model
        might only use a subset of these features. The ModelService.preprocess_data method is responsible
        for selecting only the features that the model was trained on.

        Including all features here provides flexibility for future model updates that might use
        different feature sets, without requiring changes to this method.

        Some features like Source IP, Destination IP, Source Port, and Destination Port are not available in FlowFeatures
        and are included with default values.

        Returns:
            Dict[str, Any]: Dictionary with keys expected by the model and database service
        """
        return {
            # Basic flow information
            'Flow Duration': self.flow_duration,
            'Protocol': str(self.protocol),
            'Total Fwd Packets': self.total_fwd_packets,
            'Total Backward Packets': self.total_backward_packets,

            # Packet length statistics
            'Fwd Packet Length Total': self.fwd_packets_length_total,
            'Bwd Packet Length Total': self.bwd_packets_length_total,
            'Fwd Packet Length Max': self.fwd_packet_length_max,
            'Fwd Packet Length Min': self.fwd_packet_length_min,
            'Fwd Packet Length Std': self.fwd_packet_length_std,
            'Bwd Packet Length Max': self.bwd_packet_length_max,
            'Bwd Packet Length Min': self.bwd_packet_length_min,
            'Packet Length Max': self.packet_length_max,
            'Packet Length Mean': self.packet_length_mean,

            # Flow rate statistics
            'Flow Bytes/s': self.flow_bytes_per_s,
            'Flow Packets/s': self.flow_packets_per_s,
            'Bwd Packets/s': self.bwd_packets_per_s,

            # Inter-arrival time (IAT) statistics
            'Flow IAT Mean': self.flow_iat_mean,
            'Flow IAT Min': self.flow_iat_min,
            'Fwd IAT Total': self.fwd_iat_total,
            'Fwd IAT Mean': self.fwd_iat_mean,
            'Fwd IAT Min': self.fwd_iat_min,
            'Bwd IAT Total': self.bwd_iat_total,
            'Bwd IAT Mean': self.bwd_iat_mean,
            'Bwd IAT Min': self.bwd_iat_min,

            # Header information
            'Fwd Header Length': self.fwd_header_length,
            'Bwd Header Length': self.bwd_header_length,

            # TCP flag counts
            'SYN Flag Count': self.syn_flag_count,
            'ACK Flag Count': self.ack_flag_count,
            'URG Flag Count': self.urg_flag_count,

            # Ratio statistics
            'Down/Up Ratio': self.down_up_ratio,

            # Activity statistics
            'Active Mean': self.active_mean,
            'Active Std': self.active_std,
            'Active Max': self.active_max,
            'Active Min': self.active_min,

            # Idle statistics
            'Idle Mean': self.idle_mean,
            'Idle Std': self.idle_std,
            'Idle Max': self.idle_max,
            'Idle Min': self.idle_min,

            # Network identifiers (not available in FlowFeatures)
            'Source IP': '',  # Not available in FlowFeatures
            'Destination IP': '',  # Not available in FlowFeatures
            'Source Port': 0,  # Not available in FlowFeatures
            'Destination Port': 0  # Not available in FlowFeatures
        }

    def __str__(self) -> str:
        """
        String representation of FlowFeatures.

        Returns:
            str: String representation of FlowFeatures
        """
        return (
            f"FlowFeatures(protocol={self.protocol}, "
            f"flow_duration={self.flow_duration}, "
            f"total_fwd_packets={self.total_fwd_packets}, "
            f"total_backward_packets={self.total_backward_packets}, "
            f"fwd_packets_length_total={self.fwd_packets_length_total}, "
            f"bwd_packets_length_total={self.bwd_packets_length_total}, "
            f"flow_bytes_per_s={self.flow_bytes_per_s}, "
            f"flow_packets_per_s={self.flow_packets_per_s}, "
            f"syn_flag_count={self.syn_flag_count}, "
            f"ack_flag_count={self.ack_flag_count}, "
            f"urg_flag_count={self.urg_flag_count})"
        )
