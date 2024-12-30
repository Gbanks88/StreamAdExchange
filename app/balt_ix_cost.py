from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json
from pathlib import Path
import logging
import time

@dataclass
class TrafficCost:
    timestamp: float
    bytes_transferred: int
    cost_per_gb: float
    peer_id: str

class BALTIXCostManager:
    """Cost management and optimization for BALT-IX"""
    
    def __init__(self):
        self.logger = logging.getLogger('balt_ix_cost')
        self.config_path = Path("/Volumes/Learn_Space/StreamAdExchange/config/balt_ix_cost.json")
        self.cost_history: List[TrafficCost] = []
        self.config = self._load_config()
        
    def _load_config(self) -> Dict:
        """Load cost configuration"""
        try:
            if self.config_path.exists():
                with open(self.config_path) as f:
                    return json.load(f)
            return {
                "cost_tiers": {
                    "tier1": {
                        "threshold_gb": 1000,
                        "cost_per_gb": 0.08
                    },
                    "tier2": {
                        "threshold_gb": 5000,
                        "cost_per_gb": 0.06
                    },
                    "tier3": {
                        "threshold_gb": 10000,
                        "cost_per_gb": 0.04
                    }
                },
                "peers": {
                    "default": {
                        "cost_model": "tier1",
                        "committed_bandwidth": "1Gbps",
                        "overage_cost_per_gb": 0.10
                    }
                }
            }
        except Exception as e:
            self.logger.error(f"Error loading cost configuration: {e}")
            return {}

    def calculate_cost_savings(self, peer_id: str, period_days: int = 30) -> Dict:
        """Calculate cost savings from using BALT-IX vs direct transit"""
        try:
            # Get peer configuration
            peer_config = self.config["peers"].get(peer_id, self.config["peers"]["default"])
            cost_tier = self.config["cost_tiers"][peer_config["cost_model"]]
            
            # Calculate total traffic
            start_time = datetime.now() - timedelta(days=period_days)
            relevant_costs = [
                cost for cost in self.cost_history 
                if cost.peer_id == peer_id and cost.timestamp >= start_time.timestamp()
            ]
            
            total_gb = sum(cost.bytes_transferred for cost in relevant_costs) / (1024 * 1024 * 1024)
            
            # Calculate BALT-IX cost
            balt_ix_cost = total_gb * cost_tier["cost_per_gb"]
            
            # Estimate traditional transit cost (typically 2-3x more expensive)
            traditional_cost = total_gb * 0.15  # Assuming average market rate of $0.15/GB
            
            savings = traditional_cost - balt_ix_cost
            savings_percentage = (savings / traditional_cost) * 100 if traditional_cost > 0 else 0
            
            return {
                "period_days": period_days,
                "total_traffic_gb": round(total_gb, 2),
                "balt_ix_cost": round(balt_ix_cost, 2),
                "traditional_cost": round(traditional_cost, 2),
                "savings": round(savings, 2),
                "savings_percentage": round(savings_percentage, 2),
                "cost_tier": peer_config["cost_model"]
            }
            
        except Exception as e:
            self.logger.error(f"Error calculating cost savings: {e}")
            return {}

    def optimize_peer_allocation(self) -> Dict[str, List[str]]:
        """Optimize traffic allocation across peers for cost efficiency"""
        try:
            # Get current utilization
            peer_utilization = self._get_peer_utilization()
            
            # Sort peers by cost efficiency
            peers_by_cost = sorted(
                self.config["peers"].items(),
                key=lambda x: self.config["cost_tiers"][x[1]["cost_model"]]["cost_per_gb"]
            )
            
            recommendations = {
                "immediate_actions": [],
                "long_term_actions": [],
                "cost_saving_opportunities": []
            }
            
            for peer_id, peer_config in peers_by_cost:
                utilization = peer_utilization.get(peer_id, 0)
                committed_bw = self._parse_bandwidth(peer_config["committed_bandwidth"])
                
                if utilization < committed_bw * 0.5:
                    recommendations["immediate_actions"].append(
                        f"Reduce committed bandwidth for {peer_id} - currently underutilized"
                    )
                elif utilization > committed_bw * 0.8:
                    recommendations["immediate_actions"].append(
                        f"Consider upgrading {peer_id} to next tier - approaching capacity"
                    )
                
                # Check for cost-saving opportunities
                current_tier = peer_config["cost_model"]
                potential_tier = self._find_optimal_tier(utilization)
                if potential_tier != current_tier:
                    savings = self._calculate_tier_savings(peer_id, current_tier, potential_tier)
                    recommendations["cost_saving_opportunities"].append(
                        f"Switch {peer_id} from {current_tier} to {potential_tier} "
                        f"for estimated monthly savings of ${savings:.2f}"
                    )
            
            return recommendations
            
        except Exception as e:
            self.logger.error(f"Error optimizing peer allocation: {e}")
            return {}

    def _get_peer_utilization(self) -> Dict[str, float]:
        """Get current utilization for each peer"""
        # Implementation would integrate with your monitoring system
        return {"default": 500}  # Placeholder returning 500 Mbps

    def _parse_bandwidth(self, bandwidth_str: str) -> float:
        """Convert bandwidth string to Mbps"""
        multipliers = {'G': 1000, 'M': 1, 'K': 0.001}
        value = float(bandwidth_str[:-4])  # Remove 'bps'
        unit = bandwidth_str[-4:-3]  # Get G/M/K
        return value * multipliers[unit]

    def _find_optimal_tier(self, utilization: float) -> str:
        """Find the most cost-effective tier for given utilization"""
        gb_per_month = (utilization * 3600 * 24 * 30) / (8 * 1024)  # Convert Mbps to GB/month
        
        optimal_tier = "tier1"
        for tier, config in self.config["cost_tiers"].items():
            if gb_per_month <= config["threshold_gb"]:
                optimal_tier = tier
                break
                
        return optimal_tier

    def _calculate_tier_savings(self, peer_id: str, current_tier: str, new_tier: str) -> float:
        """Calculate monthly savings from tier change"""
        current_cost = self.config["cost_tiers"][current_tier]["cost_per_gb"]
        new_cost = self.config["cost_tiers"][new_tier]["cost_per_gb"]
        
        # Calculate based on last month's usage
        last_month_gb = sum(
            cost.bytes_transferred for cost in self.cost_history[-30:]
            if cost.peer_id == peer_id
        ) / (1024 * 1024 * 1024)
        
        return last_month_gb * (current_cost - new_cost) 

    def track_traffic(self, peer_id: str, bytes_transferred: int):
        """Track real-time traffic and update cost history"""
        try:
            peer_config = self.config["peers"].get(peer_id, self.config["peers"]["default"])
            cost_tier = self.config["cost_tiers"][peer_config["cost_model"]]
            
            cost_entry = TrafficCost(
                timestamp=time.time(),
                bytes_transferred=bytes_transferred,
                cost_per_gb=cost_tier["cost_per_gb"],
                peer_id=peer_id
            )
            
            self.cost_history.append(cost_entry)
            self._trim_history()  # Keep history manageable
            
            # Check if we should trigger tier optimization
            self._check_tier_optimization(peer_id)
            
        except Exception as e:
            self.logger.error(f"Error tracking traffic: {e}")

    def _trim_history(self):
        """Keep only last 90 days of history"""
        cutoff_time = time.time() - (90 * 24 * 3600)
        self.cost_history = [
            cost for cost in self.cost_history 
            if cost.timestamp > cutoff_time
        ]

    def _check_tier_optimization(self, peer_id: str):
        """Check if we should optimize the tier based on recent usage"""
        try:
            # Get last 30 days of traffic
            recent_traffic = [
                cost for cost in self.cost_history[-1000:]
                if cost.peer_id == peer_id and 
                cost.timestamp > (time.time() - 30 * 24 * 3600)
            ]
            
            if not recent_traffic:
                return
            
            total_bytes = sum(cost.bytes_transferred for cost in recent_traffic)
            avg_daily_bytes = total_bytes / 30
            projected_monthly_gb = (avg_daily_bytes * 30) / (1024 * 1024 * 1024)
            
            optimal_tier = self._find_optimal_tier(projected_monthly_gb * 8 / (30 * 24 * 3600))
            current_tier = self.config["peers"][peer_id]["cost_model"]
            
            if optimal_tier != current_tier:
                savings = self._calculate_tier_savings(peer_id, current_tier, optimal_tier)
                if savings > 100:  # Only suggest changes for significant savings
                    self.logger.info(
                        f"Tier optimization available for {peer_id}: "
                        f"Switch from {current_tier} to {optimal_tier} "
                        f"for monthly savings of ${savings:.2f}"
                    )
                
        except Exception as e:
            self.logger.error(f"Error checking tier optimization: {e}") 