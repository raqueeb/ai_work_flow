"""
Performance Monitor for MLOps
===============================
Author: Rakibul Hassan
Company: Link3 Technologies
Purpose: Monitor ML model performance, latency, and health metrics
"""

import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pathlib import Path
from collections import deque

class PerformanceMonitor:
    """
    Real-time performance monitoring for ML models.
    Tracks latency, throughput, accuracy, and system health.
    """
    
    def __init__(self, metrics_path: str = "mlops/config/metrics.json", window_size: int = 100):
        self.metrics_path = Path(metrics_path)
        self.metrics_path.parent.mkdir(parents=True, exist_ok=True)
        self.window_size = window_size
        self.metrics = self._load_metrics()
        self.prediction_buffer = deque(maxlen=window_size)
    
    def _load_metrics(self) -> Dict:
        """Load existing metrics or create new tracking"""
        if self.metrics_path.exists():
            with open(self.metrics_path, 'r') as f:
                return json.load(f)
        return {
            'predictions': [],
            'latencies': [],
            'errors': [],
            'alerts': [],
            'health_checks': [],
            'last_updated': datetime.now().isoformat()
        }
    
    def _save_metrics(self):
        """Persist metrics to disk"""
        with open(self.metrics_path, 'w') as f:
            json.dump(self.metrics, f, indent=2)
    
    def record_prediction(self, model_name: str, version: str, 
                         latency_ms: float, prediction: Dict,
                         customer_id: str = None):
        """Record a prediction event"""
        event = {
            'timestamp': datetime.now().isoformat(),
            'model_name': model_name,
            'version': version,
            'latency_ms': latency_ms,
            'customer_id': customer_id,
            'prediction': prediction.get('risk_level', 'unknown'),
            'risk_score': prediction.get('risk_score', 0.0)
        }
        
        self.prediction_buffer.append(event)
        self.metrics['predictions'].append(event)
        self.metrics['latencies'].append(latency_ms)
        self.metrics['last_updated'] = datetime.now().isoformat()
        self._save_metrics()
    
    def record_error(self, model_name: str, error_type: str, error_message: str):
        """Record an error event"""
        error = {
            'timestamp': datetime.now().isoformat(),
            'model_name': model_name,
            'error_type': error_type,
            'message': error_message
        }
        
        self.metrics['errors'].append(error)
        self.metrics['last_updated'] = datetime.now().isoformat()
        self._save_metrics()
        
        # Trigger alert if error rate is high
        self._check_error_threshold()
    
    def health_check(self, model_name: str) -> Dict:
        """Perform health check on model"""
        now = datetime.now()
        
        # Calculate metrics for last hour
        recent_predictions = [
            p for p in self.metrics['predictions']
            if datetime.fromisoformat(p['timestamp'].replace('Z', '+00:00')).replace(tzinfo=None) > now - timedelta(hours=1)
        ]
        
        recent_errors = [
            e for e in self.metrics['errors']
            if datetime.fromisoformat(e['timestamp'].replace('Z', '+00:00')).replace(tzinfo=None) > now - timedelta(hours=1)
        ]
        
        latencies = [
            p['latency_ms'] for p in recent_predictions
            if p['model_name'] == model_name
        ]
        
        error_rate = len(recent_errors) / max(1, len(recent_predictions)) if recent_predictions else 0
        avg_latency = sum(latencies) / max(1, len(latencies))
        
        # Determine health status
        if error_rate > 0.1 or avg_latency > 5000:
            status = 'degraded'
        elif error_rate > 0.05 or avg_latency > 2000:
            status = 'warning'
        else:
            status = 'healthy'
        
        health_report = {
            'timestamp': now.isoformat(),
            'model_name': model_name,
            'status': status,
            'error_rate': error_rate,
            'avg_latency_ms': avg_latency,
            'predictions_last_hour': len(recent_predictions),
            'errors_last_hour': len(recent_errors),
            'success_rate': 1 - error_rate
        }
        
        self.metrics['health_checks'].append(health_report)
        self._save_metrics()
        
        if status != 'healthy':
            self._create_alert(model_name, status, health_report)
        
        return health_report
    
    def _check_error_threshold(self):
        """Check if error rate exceeds threshold"""
        recent_predictions = len(self.metrics['predictions'])
        recent_errors = len(self.metrics['errors'])
        
        if recent_predictions > 0:
            error_rate = recent_errors / recent_predictions
            if error_rate > 0.1:
                self._create_alert('system', 'critical', 
                                 f"Error rate {error_rate:.2%} exceeds 10% threshold")
    
    def _create_alert(self, model_name: str, severity: str, message):
        """Create and store an alert"""
        if isinstance(message, dict):
            msg = f"{message.get('status', 'unknown')}: {message.get('error_rate', 0):.2%} errors, {message.get('avg_latency_ms', 0):.0f}ms avg latency"
        else:
            msg = message
        
        alert = {
            'timestamp': datetime.now().isoformat(),
            'model_name': model_name,
            'severity': severity,
            'message': msg,
            'acknowledged': False
        }
        
        self.metrics['alerts'].append(alert)
        print(f"\n⚠️  ALERT [{severity.upper()}] {model_name}: {msg}")
    
    def acknowledge_alert(self, alert_index: int):
        """Acknowledge an alert"""
        if 0 <= alert_index < len(self.metrics['alerts']):
            self.metrics['alerts'][alert_index]['acknowledged'] = True
            self._save_metrics()
    
    def get_summary(self, model_name: Optional[str] = None) -> Dict:
        """Get performance summary"""
        predictions = self.metrics['predictions']
        if model_name:
            predictions = [p for p in predictions if p['model_name'] == model_name]
        
        if not predictions:
            return {'status': 'no_data', 'message': 'No predictions recorded'}
        
        latencies = [p['latency_ms'] for p in predictions]
        
        return {
            'total_predictions': len(predictions),
            'avg_latency_ms': sum(latencies) / len(latencies),
            'min_latency_ms': min(latencies),
            'max_latency_ms': max(latencies),
            'p95_latency_ms': sorted(latencies)[int(len(latencies) * 0.95)] if len(latencies) > 20 else max(latencies),
            'total_errors': len(self.metrics['errors']),
            'error_rate': len(self.metrics['errors']) / len(predictions),
            'active_alerts': sum(1 for a in self.metrics['alerts'] if not a['acknowledged'])
        }
    
    def get_recent_predictions(self, limit: int = 10) -> List[Dict]:
        """Get most recent predictions"""
        return sorted(self.metrics['predictions'], 
                     key=lambda x: x['timestamp'], 
                     reverse=True)[:limit]
    
    def get_unacknowledged_alerts(self) -> List[Dict]:
        """Get all unacknowledged alerts"""
        return [a for a in self.metrics['alerts'] if not a['acknowledged']]
