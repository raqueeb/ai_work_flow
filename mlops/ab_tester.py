"""
A/B Testing Framework for MLOps
=================================
Author: Rakibul Hassan
Company: Link3 Technologies
Purpose: Compare model performance and enable data-driven deployment decisions
"""

import json
import random
from datetime import datetime
from typing import Dict, List, Optional, Callable
from pathlib import Path

class ABTester:
    """
    A/B testing framework for comparing ML model performance.
    Supports traffic splitting, statistical analysis, and automated winner selection.
    """
    
    def __init__(self, experiment_path: str = "mlops/config/experiments.json"):
        self.experiment_path = Path(experiment_path)
        self.experiment_path.parent.mkdir(parents=True, exist_ok=True)
        self.experiments = self._load_experiments()
    
    def _load_experiments(self) -> Dict:
        """Load existing experiments or create new tracking"""
        if self.experiment_path.exists():
            with open(self.experiment_path, 'r') as f:
                return json.load(f)
        return {'experiments': {}, 'active_experiments': []}
    
    def _save_experiments(self):
        """Persist experiments to disk"""
        with open(self.experiment_path, 'w') as f:
            json.dump(self.experiments, f, indent=2)
    
    def create_experiment(self, name: str, model_a: Dict, model_b: Dict,
                         traffic_split: float = 0.5, 
                         min_samples: int = 100) -> str:
        """Create a new A/B test experiment"""
        experiment_id = f"exp_{int(datetime.now().timestamp())}"
        
        experiment = {
            'experiment_id': experiment_id,
            'name': name,
            'created_at': datetime.now().isoformat(),
            'status': 'running',
            'model_a': model_a,
            'model_b': model_b,
            'traffic_split': traffic_split,
            'min_samples': min_samples,
            'results_a': {'predictions': 0, 'successes': 0, 'latencies': []},
            'results_b': {'predictions': 0, 'successes': 0, 'latencies': []},
            'winner': None,
            'concluded_at': None
        }
        
        self.experiments['experiments'][experiment_id] = experiment
        self.experiments['active_experiments'].append(experiment_id)
        self._save_experiments()
        
        print(f"✓ Created experiment: {name} ({experiment_id})")
        print(f"  Model A: {model_a['name']} ({model_a['version']})")
        print(f"  Model B: {model_b['name']} ({model_b['version']})")
        print(f"  Traffic Split: {(1-traffic_split)*100:.0f}% / {traffic_split*100:.0f}%")
        
        return experiment_id
    
    def select_model(self, experiment_id: str) -> str:
        """Select which model variant for a prediction based on traffic split"""
        if experiment_id not in self.experiments['experiments']:
            raise ValueError(f"Experiment {experiment_id} not found")
        
        exp = self.experiments['experiments'][experiment_id]
        
        if exp['status'] != 'running':
            raise ValueError(f"Experiment {experiment_id} is not running")
        
        # Random selection based on traffic split
        if random.random() < exp['traffic_split']:
            return 'model_a'
        return 'model_b'
    
    def record_result(self, experiment_id: str, model_variant: str,
                     prediction: Dict, actual: bool, latency_ms: float):
        """Record a result for a model variant"""
        if experiment_id not in self.experiments['experiments']:
            return
        
        exp = self.experiments['experiments'][experiment_id]
        results = exp[f'results_{model_variant}']
        
        results['predictions'] += 1
        if actual:  # Assuming 'actual' means correct/high-risk correctly identified
            results['successes'] += 1
        results['latencies'].append(latency_ms)
        
        # Check if minimum samples reached
        total_samples = exp['results_a']['predictions'] + exp['results_b']['predictions']
        if total_samples >= exp['min_samples']:
            self._evaluate_experiment(experiment_id)
        
        self._save_experiments()
    
    def _evaluate_experiment(self, experiment_id: str):
        """Evaluate experiment results and determine winner"""
        exp = self.experiments['experiments'][experiment_id]
        
        # Calculate metrics
        metrics_a = self._calculate_metrics(exp['results_a'])
        metrics_b = self._calculate_metrics(exp['results_b'])
        
        # Simple winner determination based on success rate
        # In production, use proper statistical significance testing
        if metrics_a['success_rate'] > metrics_b['success_rate']:
            winner = 'model_a'
            confidence = abs(metrics_a['success_rate'] - metrics_b['success_rate'])
        elif metrics_b['success_rate'] > metrics_a['success_rate']:
            winner = 'model_b'
            confidence = abs(metrics_b['success_rate'] - metrics_a['success_rate'])
        else:
            winner = 'tie'
            confidence = 0
        
        exp['metrics_a'] = metrics_a
        exp['metrics_b'] = metrics_b
        exp['winner'] = winner
        exp['confidence'] = confidence
        exp['status'] = 'concluded'
        exp['concluded_at'] = datetime.now().isoformat()
        
        # Remove from active experiments
        if experiment_id in self.experiments['active_experiments']:
            self.experiments['active_experiments'].remove(experiment_id)
        
        self._save_experiments()
        
        print(f"\n📊 Experiment Concluded: {exp['name']}")
        print(f"  Model A Success Rate: {metrics_a['success_rate']:.2%}")
        print(f"  Model B Success Rate: {metrics_b['success_rate']:.2%}")
        print(f"  Winner: {winner.upper()} (confidence: {confidence:.2%})")
    
    def _calculate_metrics(self, results: Dict) -> Dict:
        """Calculate performance metrics for a variant"""
        predictions = results['predictions']
        successes = results['successes']
        latencies = results['latencies']
        
        return {
            'predictions': predictions,
            'success_rate': successes / predictions if predictions > 0 else 0,
            'avg_latency_ms': sum(latencies) / len(latencies) if latencies else 0,
            'min_latency_ms': min(latencies) if latencies else 0,
            'max_latency_ms': max(latencies) if latencies else 0
        }
    
    def get_experiment_status(self, experiment_id: str) -> Dict:
        """Get current status of an experiment"""
        if experiment_id not in self.experiments['experiments']:
            return {'error': 'Experiment not found'}
        
        exp = self.experiments['experiments'][experiment_id]
        
        return {
            'name': exp['name'],
            'status': exp['status'],
            'model_a': f"{exp['model_a']['name']} ({exp['model_a']['version']})",
            'model_b': f"{exp['model_b']['name']} ({exp['model_b']['version']})",
            'results_a': exp['results_a']['predictions'],
            'results_b': exp['results_b']['predictions'],
            'total_samples': exp['results_a']['predictions'] + exp['results_b']['predictions'],
            'min_samples_required': exp['min_samples'],
            'progress': (exp['results_a']['predictions'] + exp['results_b']['predictions']) / exp['min_samples']
        }
    
    def list_active_experiments(self) -> List[Dict]:
        """List all active experiments"""
        active = []
        for exp_id in self.experiments['active_experiments']:
            status = self.get_experiment_status(exp_id)
            status['experiment_id'] = exp_id
            active.append(status)
        return active
    
    def conclude_early(self, experiment_id: str) -> Dict:
        """Manually conclude an experiment early"""
        if experiment_id not in self.experiments['experiments']:
            return {'error': 'Experiment not found'}
        
        self._evaluate_experiment(experiment_id)
        
        exp = self.experiments['experiments'][experiment_id]
        return {
            'experiment_id': experiment_id,
            'winner': exp['winner'],
            'metrics_a': exp.get('metrics_a'),
            'metrics_b': exp.get('metrics_b')
        }
