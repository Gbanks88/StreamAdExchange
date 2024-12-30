import logging
from typing import Dict, List, Optional
from datetime import datetime
import json
from pathlib import Path
import time
import threading
from queue import Queue
from dataclasses import dataclass
import requests
from collections import defaultdict

@dataclass
class StreamData:
    timestamp: float
    peer_id: str
    data_type: str
    value: any
    metadata: Dict

class StatefulDataStore:
    """Manages reference data for stateful joins"""
    
    def __init__(self):
        self.reference_data = {
            'exchange_rates': {},
            'peer_details': {},
            'network_topology': {},
            'service_catalog': {}
        }
        self.update_timestamps = {}
        self.refresh_intervals = {
            'exchange_rates': 3600,  # 1 hour
            'peer_details': 86400,   # 1 day
            'network_topology': 3600, # 1 hour
            'service_catalog': 86400  # 1 day
        }

    def update_reference_data(self, data_type: str, data: Dict):
        """Update reference data of a specific type"""
        self.reference_data[data_type] = data
        self.update_timestamps[data_type] = time.time()

    def get_reference_data(self, data_type: str) -> Dict:
        """Get reference data with refresh check"""
        if self._needs_refresh(data_type):
            self._refresh_data(data_type)
        return self.reference_data.get(data_type, {})

    def _needs_refresh(self, data_type: str) -> bool:
        """Check if reference data needs refresh"""
        last_update = self.update_timestamps.get(data_type, 0)
        refresh_interval = self.refresh_intervals.get(data_type, 3600)
        return (time.time() - last_update) > refresh_interval

    def _refresh_data(self, data_type: str):
        """Refresh reference data from source"""
        try:
            if data_type == 'exchange_rates':
                self._fetch_exchange_rates()
            elif data_type == 'peer_details':
                self._fetch_peer_details()
            elif data_type == 'network_topology':
                self._fetch_network_topology()
            elif data_type == 'service_catalog':
                self._fetch_service_catalog()
        except Exception as e:
            self.logger.error(f"Error refreshing {data_type}: {e}")

    def _fetch_exchange_rates(self):
        """Fetch current exchange rates"""
        try:
            # Example: Fetch from an API
            response = requests.get('https://api.exchangerate-api.com/v4/latest/USD')
            if response.status_code == 200:
                self.update_reference_data('exchange_rates', response.json()['rates'])
        except Exception as e:
            self.logger.error(f"Error fetching exchange rates: {e}")

    def _fetch_peer_details(self):
        """Fetch peer network details"""
        try:
            # Example: Load from local database or configuration
            peer_details = {
                'AS12345': {
                    'name': 'Example ISP',
                    'country': 'US',
                    'peering_policy': 'open',
                    'capacity_tier': 'premium'
                }
                # Add more peer details
            }
            self.update_reference_data('peer_details', peer_details)
        except Exception as e:
            self.logger.error(f"Error fetching peer details: {e}")

    def _fetch_network_topology(self):
        """Fetch current network topology"""
        try:
            # Example: Load from network management system
            topology = {
                'nodes': ['ix1', 'ix2', 'ix3'],
                'links': [
                    {'source': 'ix1', 'target': 'ix2', 'capacity': '100G'},
                    {'source': 'ix2', 'target': 'ix3', 'capacity': '100G'}
                ]
            }
            self.update_reference_data('network_topology', topology)
        except Exception as e:
            self.logger.error(f"Error fetching network topology: {e}")

    def _fetch_service_catalog(self):
        """Fetch service catalog"""
        try:
            # Example: Load from service management system
            catalog = {
                'transit': {
                    'tiers': ['basic', 'premium', 'enterprise'],
                    'features': ['ddos-protection', 'redundancy', 'sla']
                },
                'peering': {
                    'types': ['direct', 'route-server', 'private-vlan'],
                    'ports': ['1G', '10G', '100G']
                }
            }
            self.update_reference_data('service_catalog', catalog)
        except Exception as e:
            self.logger.error(f"Error fetching service catalog: {e}")

class CortexProcessor:
    """Real-time data processing using Cortex"""
    
    def __init__(self):
        self.logger = logging.getLogger('cortex_processor')
        self.config_path = Path("/Volumes/Learn_Space/StreamAdExchange/config/cortex.json")
        self.data_queue = Queue()
        self.stream_processors = {}
        self.enrichment_rules = self._load_enrichment_rules()
        self.is_processing = False
        self.stateful_store = StatefulDataStore()
        self.temporal_processor = TemporalJoinProcessor()
        
    def _load_enrichment_rules(self) -> Dict:
        """Load data enrichment rules"""
        try:
            if self.config_path.exists():
                with open(self.config_path) as f:
                    return json.load(f)
            return {
                "traffic_analysis": {
                    "join_fields": ["peer_id", "timestamp"],
                    "enrichment": {
                        "cost_metrics": ["bytes_transferred", "cost_per_gb"],
                        "performance_metrics": ["latency", "throughput", "packet_loss"],
                        "peer_info": ["asn", "capacity", "location"]
                    }
                },
                "stream_processing": {
                    "window_size": 300,  # 5 minutes
                    "batch_size": 100,
                    "triggers": {
                        "cost_anomaly": "deviation > 2.0",
                        "performance_degradation": "latency_increase > 50%",
                        "capacity_warning": "utilization > 80%"
                    }
                }
            }
        except Exception as e:
            self.logger.error(f"Error loading enrichment rules: {e}")
            return {}

    def start_processing(self):
        """Start the stream processing engine"""
        self.is_processing = True
        self.process_thread = threading.Thread(target=self._process_stream)
        self.process_thread.daemon = True
        self.process_thread.start()
        self.logger.info("Cortex stream processing started")

    def stop_processing(self):
        """Stop the stream processing engine"""
        self.is_processing = False
        if hasattr(self, 'process_thread'):
            self.process_thread.join()
        self.logger.info("Cortex stream processing stopped")

    def ingest_data(self, data: StreamData):
        """Ingest data into the processing pipeline"""
        try:
            # Add to regular processing queue
            self.data_queue.put(data)
            
            # Process temporal joins
            joined_events = self.temporal_processor.process_event(data)
            
            # Handle joined events
            for event in joined_events:
                self._handle_joined_event(event)
                
        except Exception as e:
            self.logger.error(f"Error ingesting data: {e}")
            
    def _handle_joined_event(self, event: Dict):
        """Handle temporally joined events"""
        try:
            if 'traffic_data' in event and 'cost_data' in event:
                self._analyze_traffic_cost_correlation(event)
            elif 'performance_data' in event and 'error_data' in event:
                self._analyze_performance_correlation(event)
                
        except Exception as e:
            self.logger.error(f"Error handling joined event: {e}")
            
    def _analyze_traffic_cost_correlation(self, event: Dict):
        """Analyze correlation between traffic and cost"""
        try:
            traffic_data = event['traffic_data']
            cost_data = event['cost_data']
            
            # Calculate cost efficiency
            total_traffic = traffic_data.get('bytes_transferred', 0)
            total_cost = sum(cost['cost_per_gb'] for cost in cost_data)
            
            if total_traffic > 0:
                efficiency = total_cost / (total_traffic / 1e9)  # Cost per GB
                
                # Log significant cost variations
                if efficiency > 0.10:  # $0.10 per GB threshold
                    self.logger.warning(
                        f"High cost efficiency detected for peer {event['peer_id']}: "
                        f"${efficiency:.3f}/GB"
                    )
                    
        except Exception as e:
            self.logger.error(f"Error analyzing traffic-cost correlation: {e}")
            
    def _analyze_performance_correlation(self, event: Dict):
        """Analyze correlation between performance issues and errors"""
        try:
            perf_data = event['performance_data']
            error_data = event['error_data']
            
            # Check for error patterns during performance issues
            error_types = [error.get('type') for error in error_data]
            if len(error_types) >= 3:  # Multiple errors threshold
                self.logger.warning(
                    f"Performance correlation detected for peer {event['peer_id']}: "
                    f"Latency: {perf_data.get('latency')}ms, "
                    f"Errors: {', '.join(error_types)}"
                )
                
        except Exception as e:
            self.logger.error(f"Error analyzing performance correlation: {e}")

    def _process_stream(self):
        """Main stream processing loop"""
        while self.is_processing:
            try:
                batch = []
                while len(batch) < self.enrichment_rules["stream_processing"]["batch_size"]:
                    try:
                        data = self.data_queue.get(timeout=1)
                        batch.append(data)
                    except Queue.Empty:
                        break

                if batch:
                    enriched_data = self._enrich_batch(batch)
                    self._analyze_batch(enriched_data)
                    
            except Exception as e:
                self.logger.error(f"Error in stream processing: {e}")
                time.sleep(1)

    def _enrich_batch(self, batch: List[StreamData]) -> List[Dict]:
        """Enrich a batch of data with additional context and reference data"""
        enriched_batch = []
        try:
            # Get latest reference data
            peer_details = self.stateful_store.get_reference_data('peer_details')
            exchange_rates = self.stateful_store.get_reference_data('exchange_rates')
            service_catalog = self.stateful_store.get_reference_data('service_catalog')
            
            for data in batch:
                enriched_data = {
                    "timestamp": data.timestamp,
                    "peer_id": data.peer_id,
                    "data_type": data.data_type,
                    "value": data.value,
                    **data.metadata
                }
                
                # Enrich with peer details
                if data.peer_id in peer_details:
                    enriched_data.update({
                        "peer_name": peer_details[data.peer_id]["name"],
                        "peer_country": peer_details[data.peer_id]["country"],
                        "peering_policy": peer_details[data.peer_id]["peering_policy"]
                    })
                
                # Convert costs to different currencies
                if "cost_per_gb" in data.metadata:
                    cost_usd = data.metadata["cost_per_gb"]
                    enriched_data["costs"] = {
                        currency: cost_usd * rate 
                        for currency, rate in exchange_rates.items()
                    }
                
                # Add service tier information
                if "capacity" in data.metadata:
                    capacity = data.metadata["capacity"]
                    for service_type, details in service_catalog.items():
                        if capacity in details.get("ports", []):
                            enriched_data["service_tier"] = service_type
                
                # Apply standard enrichment rules
                for category, fields in self.enrichment_rules["traffic_analysis"]["enrichment"].items():
                    for field in fields:
                        if field in data.metadata:
                            enriched_data[f"{category}_{field}"] = data.metadata[field]
                
                enriched_batch.append(enriched_data)
                
        except Exception as e:
            self.logger.error(f"Error enriching batch: {e}")
            
        return enriched_batch

    def _analyze_batch(self, batch: List[Dict]):
        """Analyze enriched data batch"""
        try:
            window_size = self.enrichment_rules["stream_processing"]["window_size"]
            current_time = time.time()
            
            # Group by peer
            peer_data = {}
            for item in batch:
                peer_id = item["peer_id"]
                if peer_id not in peer_data:
                    peer_data[peer_id] = []
                peer_data[peer_id].append(item)
            
            # Analyze each peer's data
            for peer_id, data in peer_data.items():
                # Filter to window
                window_data = [
                    d for d in data 
                    if current_time - d["timestamp"] <= window_size
                ]
                
                if window_data:
                    self._check_triggers(peer_id, window_data)
                    
        except Exception as e:
            self.logger.error(f"Error analyzing batch: {e}")

    def _check_triggers(self, peer_id: str, window_data: List[Dict]):
        """Check if any triggers should fire based on the data"""
        try:
            triggers = self.enrichment_rules["stream_processing"]["triggers"]
            
            # Calculate metrics
            metrics = self._calculate_metrics(window_data)
            
            # Check triggers
            for trigger_name, condition in triggers.items():
                if self._evaluate_trigger(condition, metrics):
                    self._handle_trigger(trigger_name, peer_id, metrics)
                    
        except Exception as e:
            self.logger.error(f"Error checking triggers: {e}")

    def _calculate_metrics(self, window_data: List[Dict]) -> Dict:
        """Calculate metrics from window data"""
        metrics = {
            "utilization": 0,
            "latency_increase": 0,
            "deviation": 0
        }
        
        try:
            if window_data:
                # Calculate utilization
                if "performance_metrics_throughput" in window_data[0]:
                    throughputs = [d["performance_metrics_throughput"] for d in window_data]
                    capacity = float(window_data[0]["peer_info_capacity"].rstrip("G"))
                    metrics["utilization"] = max(throughputs) / (capacity * 1000)
                
                # Calculate latency increase
                if "performance_metrics_latency" in window_data[0]:
                    latencies = [d["performance_metrics_latency"] for d in window_data]
                    if len(latencies) > 1:
                        metrics["latency_increase"] = (
                            (latencies[-1] - latencies[0]) / latencies[0] * 100
                        )
                
                # Calculate cost deviation
                if "cost_metrics_cost_per_gb" in window_data[0]:
                    costs = [d["cost_metrics_cost_per_gb"] for d in window_data]
                    avg_cost = sum(costs) / len(costs)
                    if avg_cost > 0:
                        max_deviation = max(abs(c - avg_cost) for c in costs)
                        metrics["deviation"] = max_deviation / avg_cost
                    
        except Exception as e:
            self.logger.error(f"Error calculating metrics: {e}")
            
        return metrics

    def _evaluate_trigger(self, condition: str, metrics: Dict) -> bool:
        """Evaluate if a trigger condition is met"""
        try:
            # Parse condition
            metric, op, value = condition.split()
            metric_value = metrics.get(metric, 0)
            
            # Evaluate
            if op == '>':
                return metric_value > float(value)
            elif op == '<':
                return metric_value < float(value)
            
        except Exception as e:
            self.logger.error(f"Error evaluating trigger: {e}")
            
        return False

    def _handle_trigger(self, trigger_name: str, peer_id: str, metrics: Dict):
        """Handle triggered events"""
        try:
            event = {
                "timestamp": time.time(),
                "trigger": trigger_name,
                "peer_id": peer_id,
                "metrics": metrics
            }
            
            # Log the event
            self.logger.info(f"Trigger fired: {json.dumps(event)}")
            
            # Add your event handling logic here
            # For example, send to monitoring system, alert, etc.
            
        except Exception as e:
            self.logger.error(f"Error handling trigger: {e}")

class TemporalJoinProcessor:
    """Handles temporal (time-windowed) joins of data streams"""
    
    def __init__(self):
        self.window_buffers = defaultdict(list)
        self.window_configs = {
            'traffic_cost': {
                'window_size': 300,  # 5 minutes
                'slide_interval': 60,  # 1 minute
                'streams': ['traffic_metrics', 'cost_events']
            },
            'performance_alerts': {
                'window_size': 600,  # 10 minutes
                'slide_interval': 120,  # 2 minutes
                'streams': ['latency_metrics', 'error_events']
            }
        }
        
    def process_event(self, event: StreamData) -> List[Dict]:
        """Process an event and perform temporal joins"""
        joined_events = []
        
        # Store event in appropriate windows
        for window_name, config in self.window_configs.items():
            if event.data_type in config['streams']:
                self._add_to_window(window_name, event)
                
                # Check if we should process this window
                if self._should_process_window(window_name):
                    joined_events.extend(
                        self._process_window(window_name)
                    )
                    
        return joined_events
    
    def _add_to_window(self, window_name: str, event: StreamData):
        """Add event to a specific window buffer"""
        self.window_buffers[window_name].append({
            'timestamp': event.timestamp,
            'data_type': event.data_type,
            'data': {
                'peer_id': event.peer_id,
                'value': event.value,
                **event.metadata
            }
        })
        
        # Clean up old events
        self._cleanup_window(window_name)
    
    def _cleanup_window(self, window_name: str):
        """Remove events outside the window"""
        config = self.window_configs[window_name]
        cutoff_time = time.time() - config['window_size']
        
        self.window_buffers[window_name] = [
            event for event in self.window_buffers[window_name]
            if event['timestamp'] > cutoff_time
        ]
    
    def _should_process_window(self, window_name: str) -> bool:
        """Check if we should process a window based on slide interval"""
        config = self.window_configs[window_name]
        buffer = self.window_buffers[window_name]
        
        if not buffer:
            return False
            
        last_event = max(event['timestamp'] for event in buffer)
        last_slide = getattr(self, f'_last_slide_{window_name}', 0)
        
        if last_event - last_slide >= config['slide_interval']:
            setattr(self, f'_last_slide_{window_name}', last_event)
            return True
            
        return False
    
    def _process_window(self, window_name: str) -> List[Dict]:
        """Process events in a window and perform temporal join"""
        config = self.window_configs[window_name]
        buffer = self.window_buffers[window_name]
        
        if window_name == 'traffic_cost':
            return self._join_traffic_cost(buffer, config)
        elif window_name == 'performance_alerts':
            return self._join_performance_alerts(buffer, config)
        
        return []
    
    def _join_traffic_cost(self, buffer: List[Dict], config: Dict) -> List[Dict]:
        """Join traffic metrics with cost events"""
        joined_events = []
        
        # Group events by peer
        peer_events = defaultdict(lambda: defaultdict(list))
        for event in buffer:
            peer_events[event['data']['peer_id']][event['data_type']].append(event)
        
        # Process each peer's events
        for peer_id, events in peer_events.items():
            traffic_metrics = events.get('traffic_metrics', [])
            cost_events = events.get('cost_events', [])
            
            if traffic_metrics and cost_events:
                # Find matching events within small time windows
                for traffic in traffic_metrics:
                    traffic_time = traffic['timestamp']
                    matching_costs = [
                        cost for cost in cost_events
                        if abs(cost['timestamp'] - traffic_time) <= 60  # 1-minute matching window
                    ]
                    
                    if matching_costs:
                        # Join the events
                        joined_events.append({
                            'timestamp': traffic_time,
                            'peer_id': peer_id,
                            'traffic_data': traffic['data'],
                            'cost_data': [cost['data'] for cost in matching_costs],
                            'window_size': config['window_size']
                        })
        
        return joined_events
    
    def _join_performance_alerts(self, buffer: List[Dict], config: Dict) -> List[Dict]:
        """Join performance metrics with error events"""
        joined_events = []
        
        # Group events by peer
        peer_events = defaultdict(lambda: defaultdict(list))
        for event in buffer:
            peer_events[event['data']['peer_id']][event['data_type']].append(event)
        
        # Process each peer's events
        for peer_id, events in peer_events.items():
            latency_metrics = events.get('latency_metrics', [])
            error_events = events.get('error_events', [])
            
            if latency_metrics and error_events:
                # Find correlated performance issues
                high_latency_periods = [
                    metric for metric in latency_metrics
                    if metric['data'].get('latency', 0) > 100  # High latency threshold
                ]
                
                for period in high_latency_periods:
                    period_time = period['timestamp']
                    related_errors = [
                        error for error in error_events
                        if abs(error['timestamp'] - period_time) <= 300  # 5-minute correlation window
                    ]
                    
                    if related_errors:
                        joined_events.append({
                            'timestamp': period_time,
                            'peer_id': peer_id,
                            'performance_data': period['data'],
                            'error_data': [error['data'] for error in related_errors],
                            'window_size': config['window_size']
                        })
        
        return joined_events
