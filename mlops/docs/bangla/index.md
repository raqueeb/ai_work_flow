# MLOps - Bangla

**লেখক:** রাকিবুল হাসান  
**প্রতিষ্ঠান:** লিংক3 টেকনোলজিস  
**তারিখ:** জানুয়ারি ২০২৫

---

## ওভারভিউ

MLOps মডিউলে production-grade machine learning operations আছে। এতে model registry, monitoring, A/B testing এবং automatic retraining আছে।

## কম্পোনেন্টগুলো

### ১. Model Registry

কেন্দ্রীভূত model versioning এবং management।

```python
from mlops.registry import ModelRegistry

registry = ModelRegistry("./models")

# নতুন model register করুন
registry.register(
    model=classifier,
    version="1.2.0",
    metrics={"accuracy": 0.92, "latency": 4500},
    metadata={"framework": "pytorch", "quantization": "4bit"}
)

# Models list করুন
models = registry.list_models()
for m in models:
    print(f"{m.version}: {m.metrics['accuracy']:.1%}")

# specific version load করুন
model = registry.load("gemma-4-e4b", version="1.2.0")
```

এভাবে model version manage করা যায়।

### ২. Monitoring

Real-time model performance tracking।

```python
from mlops.monitor import ModelMonitor

monitor = ModelMonitor()

# prediction log করুন
monitor.log_prediction(
    model_id="gemma-4-e4b",
    input=complaint,
    output=code,
    latency=4500,
    confidence=0.92
)

# metrics পান
metrics = monitor.get_metrics(
    model_id="gemma-4-e4b",
    time_range="24h"
)

print(f"Accuracy: {metrics['accuracy']:.1%}")
print(f"Avg Latency: {metrics['avg_latency']}ms")
```

সব সময় performance monitor করা যায়।

### ৩. A/B Testing

Production-এ model performance compare করুন।

```python
from mlops.ab_test import ABTester

tester = ABTester()

# experiment create করুন
tester.create_experiment(
    name="qwen_vs_gemma",
    model_a="qwen2.5-coder-1.5b-instruct",
    model_b="gemma-4-e4b",
    traffic_split=0.5
)

# results log করুন
tester.log_result(
    experiment="qwen_vs_gemma",
    model_id="model_a",
    correct=True,
    latency=2973
)

# analysis পান
analysis = tester.analyze("qwen_vs_gemma")
print(f"Model A accuracy: {analysis['model_a_accuracy']:.1%}")
print(f"Model B accuracy: {analysis['model_b_accuracy']:.1%}")
```

### ৪. Automatic Retraining

Performance degradation-এর উপর ভিত্তি করে retraining trigger করুন।

```python
from mlops.retrain import RetrainTrigger

trigger = RetrainTrigger(threshold=0.85)

# performance check করুন
trigger.check_and_trigger(
    model_id="gemma-4-e4b",
    current_accuracy=0.82  # Threshold-এর নিচে
)

# Result: Retraining job automatically queue হয়ে যাবে
```

## বৈশিষ্ট্যগুলো

| বৈশিষ্ট্য | বিবরণ |
|---------|-------------|
| Version Control | সব model iterations track করুন |
| Performance Tracking | Real-time accuracy monitoring |
| Traffic Splitting | Downtime ছাড়া A/B test করুন |
| Auto-Retraining | degradation-এ training trigger করুন |
| Rollback | আগের model version-এ revert করুন |

## Customer Churn Prediction Example

Customer churn-এর জন্য end-to-end ML pipeline:

```python
from mlops.pipeline import ChurnPipeline

pipeline = ChurnPipeline()

# Data prepare করুন
pipeline.prepare_data("./data/customer_history.csv")

# Model train করুন
model = pipeline.train(
    features=["usage", "support_calls", "tenure"],
    target="churned"
)

# Register করুন
pipeline.register_model(model, version="1.0.0")

# Deploy করুন
pipeline.deploy("production", version="1.0.0")

# Monitor করুন
monitor = pipeline.get_monitor()
print(f"Accuracy: {monitor.current_accuracy():.1%}")
```

---

## সম্পর্কিত ডকুমেন্টেশন

- [Enterprise Apps](../enterprise-apps/index.md)
- [শুরু করুন](../getting-started/index.md)
- [Gemma E4B](../gemma-e4b/index.md)