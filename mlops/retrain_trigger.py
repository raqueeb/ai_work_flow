"""
Auto-Retraining Trigger for MLOps
===================================
Author: Rakibul Hassan
Company: Link3 Technologies
Purpose: Automatically detect model drift and trigger retraining pipelines
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable
from pathlib import Path

class RetrainTrigger:
    """
    Automated retraining trigger system for ML models.
    Monitors performance metrics, detects drift, and triggers retraining workflows.
    """
    
    def __init__(self, config_path: str = "mlops/config/retrain_config.json"):
        self.config_path = Path(config_path)
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        self.config = self._load_config()
        self.trigger_history = self._load_history()
    
    def _load_config(self) -> Dict:
        """Load retraining configuration"""
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                return json.load(f)
        
        # Default configuration
        return {
            'triggers': {
                'performance_drift': {
                    'enabled': True,
                    'threshold': 0.1,  # 10% degradation triggers retraining
                    'metric': 'accuracy',
                    'window_days': 7
                },
                'latency_degradation': {
                    'enabled': True,
                    'threshold': 2000,  # ms
                    'consecutive_breaches': 3
                },
                'error_rate_spike': {
                    'enabled': True,
                    'threshold': 0.05,  # 5% error rate
                    'window_hours': 1
                },
                'data_drift': {
                    'enabled': True,
                    'threshold': 0.15,  # 15% feature distribution change
                    'check_interval_hours': 24
                },
                'scheduled': {
                    'enabled': True,
                    'interval_days': 30  # Monthly retraining
                }
            },
            'notification_webhooks': [],
            'auto_approve_small_changes': True,
            'max_retrains_per_week': 3
        }
    
    def _load_history(self) -> Dict:
        """Load trigger history"""
        history_path = Path("mlops/config/trigger_history.json")
        if history_path.exists():
            with open(history_path, 'r') as f:
                return json.load(f)
        return {'triggers': [], 'retrain_requests': []}
    
    def _save_history(self):
        """Persist trigger history"""
        with open("mlops/config/trigger_history.json", 'w') as f:
            json.dump(self.trigger_history, f, indent=2)
    
    def check_performance_drift(self, current_metrics: Dict, 
                                baseline_metrics: Dict) -> Optional[Dict]:
        """Check for performance degradation"""
        if not self.config['triggers']['performance_drift']['enabled']:
            return None
        
        trigger = self.config['triggers']['performance_drift']
        metric = trigger['metric']
        
        if metric not in current_metrics or metric not in baseline_metrics:
            return None
        
        current = current_metrics[metric]
        baseline = baseline_metrics[metric]
        
        if baseline == 0:
            return None
        
        degradation = (baseline - current) / baseline
        
        if degradation >= trigger['threshold']:
            return {
                'trigger_type': 'performance_drift',
                'detected_at': datetime.now().isoformat(),
                'metric': metric,
                'baseline_value': baseline,
                'current_value': current,
                'degradation_percent': degradation * 100,
                'threshold': trigger['threshold'] * 100,
                'severity': 'high' if degradation > 0.2 else 'medium',
                'action_required': 'retrain'
            }
        
        return None
    
    def check_latency_degradation(self, latencies: List[float]) -> Optional[Dict]:
        """Check for latency degradation"""
        if not self.config['triggers']['latency_degradation']['enabled']:
            return None
        
        trigger = self.config['triggers']['latency_degradation']
        threshold = trigger['threshold']
        consecutive = trigger['consecutive_breaches']
        
        if len(latencies) < consecutive:
            return None
        
        # Check last N predictions
        recent = latencies[-consecutive:]
        breaches = sum(1 for lat in recent if lat > threshold)
        
        if breaches >= consecutive:
            avg_latency = sum(recent) / len(recent)
            return {
                'trigger_type': 'latency_degradation',
                'detected_at': datetime.now().isoformat(),
                'threshold_ms': threshold,
                'current_avg_ms': avg_latency,
                'consecutive_breaches': breaches,
                'severity': 'high' if avg_latency > threshold * 1.5 else 'medium',
                'action_required': 'investigate'
            }
        
        return None
    
    def check_error_rate(self, metrics_summary: Dict) -> Optional[Dict]:
        """Check for error rate spike"""
        if not self.config['triggers']['error_rate_spike']['enabled']:
            return None
        
        trigger = self.config['triggers']['error_rate_spike']
        error_rate = metrics_summary.get('error_rate', 0)
        
        if error_rate >= trigger['threshold']:
            return {
                'trigger_type': 'error_rate_spike',
                'detected_at': datetime.now().isoformat(),
                'current_error_rate': error_rate,
                'threshold': trigger['threshold'],
                'severity': 'critical' if error_rate > 0.1 else 'high',
                'action_required': 'retrain'
            }
        
        return None
    
    def check_scheduled_retrain(self, last_retrain: str) -> Optional[Dict]:
        """Check if scheduled retraining is due"""
        if not self.config['triggers']['scheduled']['enabled']:
            return None
        
        if not last_retrain:
            return {
                'trigger_type': 'scheduled',
                'detected_at': datetime.now().isoformat(),
                'reason': 'No previous retraining found',
                'severity': 'low',
                'action_required': 'retrain'
            }
        
        last_date = datetime.fromisoformat(last_retrain.replace('Z', '+00:00')).replace(tzinfo=None)
        days_since = (datetime.now() - last_date).days
        
        if days_since >= self.config['triggers']['scheduled']['interval_days']:
            return {
                'trigger_type': 'scheduled',
                'detected_at': datetime.now().isoformat(),
                'last_retrain': last_retrain,
                'days_since': days_since,
                'interval_days': self.config['triggers']['scheduled']['interval_days'],
                'severity': 'medium',
                'action_required': 'retrain'
            }
        
        return None
    
    def evaluate_all_triggers(self, current_metrics: Dict,
                             baseline_metrics: Dict,
                             latencies: List[float],
                             last_retrain: str = None) -> List[Dict]:
        """Evaluate all enabled triggers"""
        triggers = []
        
        # Performance drift check
        drift = self.check_performance_drift(current_metrics, baseline_metrics)
        if drift:
            triggers.append(drift)
        
        # Latency check
        latency_issue = self.check_latency_degradation(latencies)
        if latency_issue:
            triggers.append(latency_issue)
        
        # Error rate check
        error_issue = self.check_error_rate(current_metrics)
        if error_issue:
            triggers.append(error_issue)
        
        # Scheduled check
        scheduled = self.check_scheduled_retrain(last_retrain)
        if scheduled:
            triggers.append(scheduled)
        
        # Record all detected triggers
        for trigger in triggers:
            self.trigger_history['triggers'].append(trigger)
        self._save_history()
        
        return triggers
    
    def create_retrain_request(self, model_name: str, 
                              trigger_reason: Dict,
                              priority: str = 'normal') -> str:
        """Create a formal retraining request"""
        # Check retrain rate limit
        if self._check_rate_limit():
            return None
        
        request_id = f"retrain_{int(datetime.now().timestamp())}"
        
        request = {
            'request_id': request_id,
            'model_name': model_name,
            'created_at': datetime.now().isoformat(),
            'trigger_reason': trigger_reason,
            'priority': priority,
            'status': 'pending_approval',
            'approved': False,
            'approved_by': None,
            'approved_at': None,
            'pipeline_started': None,
            'completed_at': None
        }
        
        self.trigger_history['retrain_requests'].append(request)
        self._save_history()
        
        return request_id
    
    def _check_rate_limit(self) -> bool:
        """Check if retrain rate limit is exceeded"""
        max_retrains = self.config.get('max_retrains_per_week', 3)
        
        # Count retrains in last 7 days
        one_week_ago = datetime.now() - timedelta(days=7)
        recent_retrains = sum(
            1 for r in self.trigger_history['retrain_requests']
            if datetime.fromisoformat(r['created_at'].replace('Z', '+00:00')).replace(tzinfo=None) > one_week_ago
            and r.get('completed_at')
        )
        
        return recent_retrains >= max_retrains
    
    def approve_retrain(self, request_id: str, approver: str = 'system') -> bool:
        """Approve a retraining request"""
        for request in self.trigger_history['retrain_requests']:
            if request['request_id'] == request_id:
                request['approved'] = True
                request['approved_by'] = approver
                request['approved_at'] = datetime.now().isoformat()
                request['status'] = 'approved'
                self._save_history()
                return True
        return False
    
    def get_pending_requests(self) -> List[Dict]:
        """Get all pending retrain requests"""
        return [
            r for r in self.trigger_history['retrain_requests']
            if r['status'] == 'pending_approval'
        ]
    
    def get_trigger_summary(self) -> Dict:
        """Get summary of all triggers"""
        triggers = self.trigger_history['triggers']
        requests = self.trigger_history['retrain_requests']
        
        return {
            'total_triggers': len(triggers),
            'by_type': {
                trigger_type: sum(1 for t in triggers if t['trigger_type'] == trigger_type)
                for trigger_type in set(t['trigger_type'] for t in triggers)
            },
            'pending_requests': len([r for r in requests if r['status'] == 'pending_approval']),
            'approved_requests': len([r for r in requests if r['approved']])
        }
