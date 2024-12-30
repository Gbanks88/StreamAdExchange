import socket
import subprocess
import requests
import time
from pathlib import Path
import json
from typing import Dict, List, Optional
import logging
from app.balt_ix_cost import BALTIXCostManager
from app.cortex_integration import CortexProcessor, StreamData

class BALTIX:
    """BALT-IX Internet Exchange Platform Manager"""
    
    def __init__(self):
        self.logger = logging.getLogger('balt_ix')
        self.config_path = Path("/Volumes/Learn_Space/StreamAdExchange/config/balt_ix.json")
        self.peers = self._load_peers()
        self.metrics = {
            'latency': {},
            'throughput': {},
            'packet_loss': {}
        }
        self.cost_manager = BALTIXCostManager()
        self.cortex = CortexProcessor()
        self.cortex.start_processing()

    def _load_peers(self) -> Dict:
        """Load peer configuration"""
        try:
            if self.config_path.exists():
                with open(self.config_path) as f:
                    return json.load(f)
            return {
                "peers": {
                    "default": {
                        "ip": "192.168.1.1",
                        "asn": "AS12345",
                        "capacity": "10G",
                        "enabled": True
                    }
                },
                "settings": {
                    "max_latency": 10,  # ms
                    "min_throughput": 1000,  # Mbps
                    "max_packet_loss": 0.1  # %
                }
            }
        except Exception as e:
            self.logger.error(f"Error loading peer configuration: {e}")
            return {}

    def check_connectivity(self, peer_id: str = "default") -> Dict:
        """Check connectivity with a specific peer"""
        if peer_id not in self.peers.get("peers", {}):
            return {"status": "error", "message": f"Peer {peer_id} not found"}

        peer = self.peers["peers"][peer_id]
        if not peer.get("enabled", False):
            return {"status": "disabled", "message": f"Peer {peer_id} is disabled"}

        results = {
            "peer_id": peer_id,
            "timestamp": time.time(),
            "metrics": {}
        }

        try:
            # Check latency
            latency = self._measure_latency(peer["ip"])
            results["metrics"]["latency"] = latency

            # Check throughput
            throughput = self._measure_throughput(peer["ip"])
            results["metrics"]["throughput"] = throughput

            # Check packet loss
            packet_loss = self._measure_packet_loss(peer["ip"])
            results["metrics"]["packet_loss"] = packet_loss

            # Update metrics history
            self._update_metrics(peer_id, results["metrics"])

            # Check against thresholds
            status = self._check_thresholds(results["metrics"])
            results.update(status)

            return results

        except Exception as e:
            self.logger.error(f"Error checking connectivity for peer {peer_id}: {e}")
            return {"status": "error", "message": str(e)}

    def _measure_latency(self, ip: str) -> float:
        """Measure latency to peer"""
        try:
            result = subprocess.run(
                ['ping', '-c', '5', ip],
                capture_output=True,
                text=True
            )
            # Extract average latency from ping output
            for line in result.stdout.splitlines():
                if "avg" in line:
                    return float(line.split('/')[-3])
            return -1
        except Exception as e:
            self.logger.error(f"Error measuring latency: {e}")
            return -1

    def _measure_throughput(self, ip: str) -> float:
        """Measure throughput to peer"""
        try:
            # Implement throughput measurement
            # This is a placeholder - you'd want to use iperf3 or similar
            return 1000.0  # Mbps
        except Exception as e:
            self.logger.error(f"Error measuring throughput: {e}")
            return -1

    def _measure_packet_loss(self, ip: str) -> float:
        """Measure packet loss to peer"""
        try:
            result = subprocess.run(
                ['ping', '-c', '100', ip],
                capture_output=True,
                text=True
            )
            # Extract packet loss percentage
            for line in result.stdout.splitlines():
                if "packet loss" in line:
                    return float(line.split('%')[0].split()[-1])
            return 100.0
        except Exception as e:
            self.logger.error(f"Error measuring packet loss: {e}")
            return 100.0

    def _update_metrics(self, peer_id: str, new_metrics: Dict):
        """Update metrics history"""
        for metric_type, value in new_metrics.items():
            if peer_id not in self.metrics[metric_type]:
                self.metrics[metric_type][peer_id] = []
            self.metrics[metric_type][peer_id].append({
                "timestamp": time.time(),
                "value": value
            })
            # Keep last 1000 measurements
            self.metrics[metric_type][peer_id] = self.metrics[metric_type][peer_id][-1000:]

    def _check_thresholds(self, metrics: Dict) -> Dict:
        """Check metrics against thresholds"""
        settings = self.peers.get("settings", {})
        status = "healthy"
        issues = []

        if metrics["latency"] > settings.get("max_latency", 10):
            status = "degraded"
            issues.append(f"High latency: {metrics['latency']}ms")

        if metrics["throughput"] < settings.get("min_throughput", 1000):
            status = "degraded"
            issues.append(f"Low throughput: {metrics['throughput']}Mbps")

        if metrics["packet_loss"] > settings.get("max_packet_loss", 0.1):
            status = "degraded"
            issues.append(f"High packet loss: {metrics['packet_loss']}%")

        return {
            "status": status,
            "issues": issues
        }

    def get_metrics_history(self, peer_id: str = "default") -> Dict:
        """Get historical metrics for a peer"""
        return {
            metric_type: data.get(peer_id, [])
            for metric_type, data in self.metrics.items()
        } 

    def get_cost_analysis(self, peer_id: str = "default") -> Dict:
        """Get cost analysis for a peer"""
        try:
            # Get basic connectivity metrics
            connectivity = self.check_connectivity(peer_id)
            
            # Get cost analysis
            cost_savings = self.cost_manager.calculate_cost_savings(peer_id)
            
            # Get optimization recommendations
            optimizations = self.cost_manager.optimize_peer_allocation()
            
            return {
                "connectivity": connectivity,
                "cost_savings": cost_savings,
                "optimizations": optimizations,
                "status": "success"
            }
        except Exception as e:
            self.logger.error(f"Error getting cost analysis: {e}")
            return {"status": "error", "message": str(e)} 

    def monitor_traffic(self, peer_id: str = "default"):
        """Monitor real-time traffic for a peer"""
        try:
            peer = self.peers["peers"].get(peer_id)
            if not peer or not peer.get("enabled"):
                return
            
            # Get traffic stats using iftop or similar
            result = subprocess.run(
                ['iftop', '-t', '-s', '1', '-N', '-n', '-i', 'any', 
                 '-F', peer['ip'] + '/32', '-B'],
                capture_output=True,
                text=True,
                timeout=2
            )
            
            if result.returncode == 0:
                # Parse traffic data
                lines = result.stdout.splitlines()
                for line in lines:
                    if peer['ip'] in line:
                        # Extract bytes transferred
                        bytes_in = int(line.split()[1])
                        bytes_out = int(line.split()[2])
                        total_bytes = bytes_in + bytes_out
                        
                        # Track traffic for cost analysis
                        self.cost_manager.track_traffic(peer_id, total_bytes)
                        
                        # Update metrics
                        self._update_metrics(peer_id, {
                            'bytes_transferred': total_bytes,
                            'timestamp': time.time()
                        })
                        
            # Send data to Cortex for processing with additional context
            stream_data = StreamData(
                timestamp=time.time(),
                peer_id=peer_id,
                data_type="traffic_metrics",
                value=total_bytes,
                metadata={
                    "bytes_transferred": total_bytes,
                    "cost_per_gb": self.cost_manager.get_current_cost(peer_id),
                    "latency": metrics.get("latency"),
                    "throughput": metrics.get("throughput"),
                    "packet_loss": metrics.get("packet_loss"),
                    "asn": peer.get("asn"),
                    "capacity": peer.get("capacity"),
                    "location": peer.get("location", "unknown"),
                    "service_type": peer.get("service_type", "standard"),
                    "currency": peer.get("billing_currency", "USD")
                }
            )
            self.cortex.ingest_data(stream_data)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error monitoring traffic: {e}")
            return False 