"""
Customer Churn Prediction Demo
===============================
Author: Rakibul Hassan
Company: Link3 Technologies
Purpose: Demonstrates MLOps pipeline for ISP customer churn prediction

This demo showcases:
- End-to-end ML pipeline with local LLMs (Qwen/Gemma)
- Model registry for version management
- Performance monitoring and health checks
- A/B testing for model comparison
- Automated retraining triggers

Run: python churn_prediction_demo.py
"""

import json
import time
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from mlops import ChurnPipeline, ModelRegistry, PerformanceMonitor, ABTester, RetrainTrigger


def load_sample_customers():
    """Load sample customer data"""
    data_path = Path(__file__).parent / "data" / "sample_customers.json"
    if data_path.exists():
        with open(data_path, 'r') as f:
            return json.load(f)
    return []


def demo_basic_prediction():
    """Demo 1: Basic churn prediction pipeline"""
    print("\n" + "=" * 70)
    print("DEMO 1: Basic Customer Churn Prediction Pipeline")
    print("=" * 70)
    
    pipeline = ChurnPipeline()
    
    # Sample customer data
    customer = {
        'customer_id': 'CUST-2024-001',
        'name': 'Abdul Karim',
        'plan': 'Business Pro 50Mbps',
        'complaints': [
            {'date': '2024-01-05', 'category': 'network', 'description': 'Frequent disconnections'},
            {'date': '2024-01-10', 'category': 'technical', 'description': 'Slow speeds during peak hours'},
            {'date': '2024-01-15', 'category': 'service', 'description': 'Support response time poor'}
        ],
        'billing_history': {
            'months': 18,
            'delays': 1,
            'downgrades': 0
        },
        'support_tickets': [
            {'id': 'TKT-1001', 'status': 'resolved', 'resolution_hours': 36},
            {'id': 'TKT-1002', 'status': 'open', 'resolution_hours': None}
        ]
    }
    
    result = pipeline.run_pipeline(customer)
    
    print(f"\n📊 Prediction Result:")
    print(f"   Risk Level: {result['prediction']['risk_level']}")
    print(f"   Risk Score: {result['prediction']['risk_score']:.2f}")
    print(f"   Key Factors: {', '.join(result['prediction']['factors'])}")
    
    return result


def demo_model_registry():
    """Demo 2: Model registry and version management"""
    print("\n" + "=" * 70)
    print("DEMO 2: Model Registry & Version Management")
    print("=" * 70)
    
    registry = ModelRegistry()
    
    # Register new model versions
    models_to_register = [
        {
            'name': 'churn-classifier-v1',
            'type': 'classification',
            'base_model': 'qwen2.5-1.5b',
            'metrics': {'accuracy': 0.82, 'precision': 0.78, 'recall': 0.85}
        },
        {
            'name': 'churn-classifier-v2',
            'type': 'classification',
            'base_model': 'qwen2.5-1.5b',
            'metrics': {'accuracy': 0.85, 'precision': 0.82, 'recall': 0.87}
        },
        {
            'name': 'churn-classifier-gemma',
            'type': 'classification',
            'base_model': 'gemma-4-e4b',
            'metrics': {'accuracy': 0.88, 'precision': 0.85, 'recall': 0.90}
        }
    ]
    
    print("\n📋 Registering Models:")
    version_ids = {}
    for model in models_to_register:
        vid = registry.register_model(model['name'], model)
        version_ids[model['name']] = vid
    
    # List all models
    print("\n📋 Registered Models:")
    for model_name in registry.list_models():
        print(f"   - {model_name}")
        versions = registry.list_versions(model_name)
        for v in versions:
            print(f"     • {v['version_id']} ({v['status']}) - Accuracy: {v['metrics'].get('accuracy', 'N/A')}")
    
    # Promote best model to production
    print("\n🚀 Promoting best model to production...")
    registry.promote_to_production('churn-classifier-gemma', version_ids['churn-classifier-gemma'])
    
    # Show deployment history
    print("\n📜 Deployment History:")
    history = registry.get_deployment_history()
    for h in history[-3:]:
        print(f"   • {h['deployed_at'][:10]}: {h['model_name']} {h['version_id']}")
    
    return registry


def demo_performance_monitoring():
    """Demo 3: Performance monitoring"""
    print("\n" + "=" * 70)
    print("DEMO 3: Performance Monitoring")
    print("=" * 70)
    
    monitor = PerformanceMonitor()
    pipeline = ChurnPipeline()
    
    # Simulate multiple predictions
    print("\n📡 Recording predictions...")
    customers = load_sample_customers()[:5]
    
    for i, customer in enumerate(customers):
        start = time.time()
        result = pipeline.run_pipeline(customer)
        latency = (time.time() - start) * 1000
        
        monitor.record_prediction(
            model_name='qwen-classifier',
            version='v1.0',
            latency_ms=latency,
            prediction=result['prediction'],
            customer_id=customer['customer_id']
        )
        
        print(f"   ✓ {customer['customer_id']}: {result['prediction']['risk_level']} ({latency:.0f}ms)")
    
    # Health check
    print("\n🏥 Running Health Check...")
    health = monitor.health_check('qwen-classifier')
    
    print(f"\n   Status: {health['status'].upper()}")
    print(f"   Average Latency: {health['avg_latency_ms']:.0f}ms")
    print(f"   Error Rate: {health['error_rate']:.2%}")
    print(f"   Success Rate: {health['success_rate']:.2%}")
    
    # Performance summary
    print("\n📊 Performance Summary:")
    summary = monitor.get_summary('qwen-classifier')
    for key, value in summary.items():
        if isinstance(value, float):
            print(f"   • {key}: {value:.2f}" if 'rate' in key or 'ms' in key else f"   • {key}: {value}")
        else:
            print(f"   • {key}: {value}")
    
    return monitor


def demo_ab_testing():
    """Demo 4: A/B testing framework"""
    print("\n" + "=" * 70)
    print("DEMO 4: A/B Testing for Model Comparison")
    print("=" * 70)
    
    ab_tester = ABTester()
    pipeline = ChurnPipeline()
    
    # Create experiment comparing Qwen vs Gemma
    print("\n🧪 Creating A/B Experiment...")
    experiment_id = ab_tester.create_experiment(
        name="Qwen vs Gemma Churn Classifier",
        model_a={'name': 'qwen-classifier', 'version': 'v1.0', 'type': 'qwen'},
        model_b={'name': 'gemma-classifier', 'version': 'v1.0', 'type': 'gemma'},
        traffic_split=0.5,
        min_samples=20
    )
    
    # Simulate predictions
    print("\n📊 Running experiment predictions...")
    customers = load_sample_customers()
    
    for i, customer in enumerate(customers[:25]):
        # Select model based on traffic split
        variant = ab_tester.select_model(experiment_id)
        
        start = time.time()
        result = pipeline.run_pipeline(customer)
        latency = (time.time() - start) * 1000
        
        # Simulate actual churn (ground truth)
        actual_churn = customer.get('churned', False)
        
        # Record result
        ab_tester.record_result(
            experiment_id=experiment_id,
            model_variant=variant,
            prediction=result['prediction'],
            actual=actual_churn or result['prediction']['risk_level'] == 'HIGH',
            latency_ms=latency
        )
        
        model_name = "Qwen" if variant == 'model_a' else "Gemma"
        print(f"   [{model_name}] {customer['customer_id']}: {result['prediction']['risk_level']}")
    
    # Get experiment status
    status = ab_tester.get_experiment_status(experiment_id)
    print(f"\n📈 Final Results:")
    print(f"   Status: {status['status']}")
    print(f"   Model A ({status['model_a']}): {status['results_a']} predictions")
    print(f"   Model B ({status['model_b']}): {status['results_b']} predictions")
    
    return ab_tester


def demo_auto_retraining():
    """Demo 5: Automated retraining triggers"""
    print("\n" + "=" * 70)
    print("DEMO 5: Automated Retraining Triggers")
    print("=" * 70)
    
    retrain_trigger = RetrainTrigger()
    
    # Simulated metrics for demonstration
    baseline_metrics = {'accuracy': 0.85, 'precision': 0.82, 'recall': 0.87}
    degraded_metrics = {'accuracy': 0.72, 'precision': 0.75, 'recall': 0.68}
    
    print("\n🔍 Checking for retraining triggers...")
    
    # Check performance drift
    drift = retrain_trigger.check_performance_drift(degraded_metrics, baseline_metrics)
    if drift:
        print(f"\n⚠️  Performance Drift Detected:")
        print(f"   Metric: {drift['metric']}")
        print(f"   Baseline: {drift['baseline_value']:.2%}")
        print(f"   Current: {drift['current_value']:.2%}")
        print(f"   Degradation: {drift['degradation_percent']:.1f}%")
        print(f"   Severity: {drift['severity'].upper()}")
    
    # Check latency degradation
    latencies = [850, 920, 1100, 2400, 2600, 2800]  # Increasingly slow
    latency_issue = retrain_trigger.check_latency_degradation(latencies)
    if latency_issue:
        print(f"\n⚠️  Latency Degradation Detected:")
        print(f"   Current Avg: {latency_issue['current_avg_ms']:.0f}ms")
        print(f"   Threshold: {latency_issue['threshold_ms']}ms")
        print(f"   Severity: {latency_issue['severity'].upper()}")
    
    # Create retrain request
    print("\n📝 Creating Retraining Request...")
    if drift:
        request_id = retrain_trigger.create_retrain_request(
            model_name='churn-classifier',
            trigger_reason=drift,
            priority='high'
        )
        print(f"   Request ID: {request_id}")
        print(f"   Status: pending_approval")
        
        # Simulate approval
        retrain_trigger.approve_retrain(request_id, 'admin')
        print(f"   ✅ Approved by: admin")
    
    # Show pending requests
    print("\n📋 Retraining Summary:")
    summary = retrain_trigger.get_trigger_summary()
    print(f"   Total Triggers: {summary['total_triggers']}")
    print(f"   By Type: {summary['by_type']}")
    print(f"   Pending Requests: {summary['pending_requests']}")
    print(f"   Approved Requests: {summary['approved_requests']}")
    
    return retrain_trigger


def main():
    """Run all MLOps demos"""
    print("\n" + "=" * 70)
    print("🚀 MLOps Customer Churn Prediction Demo")
    print("   Author: Rakibul Hassan | Link3 Technologies")
    print("=" * 70)
    
    try:
        # Demo 1: Basic Pipeline
        demo_basic_prediction()
        
        # Demo 2: Model Registry
        registry = demo_model_registry()
        
        # Demo 3: Performance Monitoring
        monitor = demo_performance_monitoring()
        
        # Demo 4: A/B Testing
        ab_tester = demo_ab_testing()
        
        # Demo 5: Auto Retraining
        retrain_trigger = demo_auto_retraining()
        
        # Final Summary
        print("\n" + "=" * 70)
        print("📊 MLOps Pipeline Summary")
        print("=" * 70)
        print(f"""
   This demo showcased the complete MLOps lifecycle:
   
   1. 📥 Data Ingestion: Customer data collection & validation
   2. ⚙️  Feature Engineering: Extracted predictive features
   3. 🔮 Prediction: LLM-powered churn risk assessment
   4. 📝 Model Registry: Version tracking & deployment management
   5. 📡 Monitoring: Real-time performance & health tracking
   6. 🧪 A/B Testing: Data-driven model comparison
   7. 🔄 Auto-Retraining: Drift detection & automated triggers
   
   Key Benefits:
   • Traceable model versions
   • Automated performance monitoring
   • Data-driven deployment decisions
   • Proactive maintenance triggers
   
   Next Steps:
   • Integrate with production data pipelines
   • Set up notification webhooks
   • Implement CI/CD for model deployments
        """)
        
        print("=" * 70)
        print("✅ Demo Complete!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
