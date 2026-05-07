"""
Model Registry for MLOps
========================
Author: Rakibul Hassan
Company: Link3 Technologies
Purpose: Track and manage ML model versions and their performance
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path

class ModelRegistry:
    """
    Central registry for tracking ML model versions, metrics, and deployments.
    Supports model versioning, performance tracking, and promotion workflows.
    """
    
    def __init__(self, registry_path: str = "mlops/config/models.json"):
        self.registry_path = Path(registry_path)
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)
        self.models = self._load_registry()
    
    def _load_registry(self) -> Dict:
        """Load existing registry or create new one"""
        if self.registry_path.exists():
            with open(self.registry_path, 'r') as f:
                return json.load(f)
        return {
            'models': {},
            'deployment_history': [],
            'last_updated': datetime.now().isoformat()
        }
    
    def _save_registry(self):
        """Persist registry to disk"""
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.registry_path, 'w') as f:
            json.dump(self.models, f, indent=2)
    
    def register_model(self, model_name: str, model_info: Dict) -> str:
        """Register a new model version"""
        if model_name not in self.models['models']:
            self.models['models'][model_name] = {'versions': {}}
        
        version_id = f"v{int(datetime.now().timestamp())}"
        
        model_entry = {
            'version_id': version_id,
            'registered_at': datetime.now().isoformat(),
            'model_type': model_info.get('type', 'unknown'),
            'base_model': model_info.get('base_model', 'unknown'),
            'metrics': model_info.get('metrics', {}),
            'parameters': model_info.get('parameters', {}),
            'status': 'staging',
            'deployed_at': None,
            'metadata': model_info.get('metadata', {})
        }
        
        self.models['models'][model_name]['versions'][version_id] = model_entry
        self.models['last_updated'] = datetime.now().isoformat()
        self._save_registry()
        
        print(f"✓ Registered {model_name} as {version_id}")
        return version_id
    
    def update_metrics(self, model_name: str, version_id: str, metrics: Dict):
        """Update performance metrics for a model version"""
        if model_name in self.models['models']:
            if version_id in self.models['models'][model_name]['versions']:
                self.models['models'][model_name]['versions'][version_id]['metrics'] = metrics
                self.models['last_updated'] = datetime.now().isoformat()
                self._save_registry()
                print(f"✓ Updated metrics for {model_name} {version_id}")
    
    def promote_to_production(self, model_name: str, version_id: str):
        """Promote a model version to production"""
        if model_name not in self.models['models']:
            print(f"✗ Model {model_name} not found")
            return False
        
        # Demote current production version
        for vid, vdata in self.models['models'][model_name]['versions'].items():
            if vdata['status'] == 'production':
                vdata['status'] = 'archived'
                vdata['archived_at'] = datetime.now().isoformat()
        
        # Promote new version
        self.models['models'][model_name]['versions'][version_id]['status'] = 'production'
        self.models['models'][model_name]['versions'][version_id]['deployed_at'] = datetime.now().isoformat()
        
        # Record deployment history
        self.models['deployment_history'].append({
            'model_name': model_name,
            'version_id': version_id,
            'deployed_at': datetime.now().isoformat(),
            'previous_version': self._get_previous_production(model_name, version_id)
        })
        
        self.models['last_updated'] = datetime.now().isoformat()
        self._save_registry()
        
        print(f"✓ Promoted {model_name} {version_id} to production")
        return True
    
    def _get_previous_production(self, model_name: str, current_version: str) -> Optional[str]:
        """Get the previous production version"""
        for vid, vdata in self.models['models'][model_name]['versions'].items():
            if vid != current_version and vdata.get('status') == 'production':
                return vid
        return None
    
    def get_production_model(self, model_name: str) -> Optional[Dict]:
        """Get the current production version of a model"""
        if model_name in self.models['models']:
            for vdata in self.models['models'][model_name]['versions'].values():
                if vdata.get('status') == 'production':
                    return vdata
        return None
    
    def list_models(self) -> List[str]:
        """List all registered models"""
        return list(self.models['models'].keys())
    
    def list_versions(self, model_name: str) -> List[Dict]:
        """List all versions of a model"""
        if model_name in self.models['models']:
            return [
                {'version_id': vid, **vdata}
                for vid, vdata in self.models['models'][model_name]['versions'].items()
            ]
        return []
    
    def get_deployment_history(self, model_name: Optional[str] = None) -> List[Dict]:
        """Get deployment history, optionally filtered by model"""
        history = self.models['deployment_history']
        if model_name:
            history = [h for h in history if h['model_name'] == model_name]
        return history
    
    def rollback(self, model_name: str) -> bool:
        """Rollback to previous model version"""
        history = [h for h in self.models['deployment_history'] 
                  if h['model_name'] == model_name]
        
        if len(history) < 2:
            print(f"✗ No previous version available for {model_name}")
            return False
        
        current = history[-1]['version_id']
        previous = history[-2]['version_id']
        
        # Demote current
        if current in self.models['models'][model_name]['versions']:
            self.models['models'][model_name]['versions'][current]['status'] = 'archived'
        
        # Restore previous
        if previous in self.models['models'][model_name]['versions']:
            self.models['models'][model_name]['versions'][previous]['status'] = 'production'
            self.models['models'][model_name]['versions'][previous]['deployed_at'] = datetime.now().isoformat()
        
        self.models['last_updated'] = datetime.now().isoformat()
        self._save_registry()
        
        print(f"✓ Rolled back {model_name} from {current} to {previous}")
        return True
