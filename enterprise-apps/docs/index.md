# Enterprise Apps

**Author:** Rakibul Hassan  
**Company:** Link3 Technologies  
**Date:** January 2025

---

## Overview

Enterprise Apps collection provides production-ready applications for business operations, including model management, testing frameworks, and utility scripts.

## Scripts

| Script | Description |
|--------|-------------|
| `model_use_class.py` | Model usage and management |
| `test_classifier.py` | Classifier testing framework |
| `test_one.py` | Single case testing |
| `test_llm_ISP_ticket_classifier.py` | ISP ticket classifier tests |

## Model Use Class

```python
from model_use_class import ModelManager

manager = ModelManager()

# Initialize models
manager.load_model("qwen2.5-coder-1.5b-instruct")
manager.load_model("gemma-4-e4b")

# Switch models
manager.use_model("gemma-4-e4b")

# Generate
response = manager.generate("What is fiber optic troubleshooting?")

# Track usage
stats = manager.get_stats()
print(f"Tokens used: {stats['total_tokens']}")
```

## Testing Framework

```python
from test_classifier import ClassifierTest

test = ClassifierTest()

# Run test suite
results = test.run_suite([
    "test_accuracy",
    "test_latency",
    "test_edge_cases"
])

# Generate report
test.generate_report(results, format="json")
```

## Features

| Feature | Description |
|---------|-------------|
| Multi-model Support | Switch between Qwen and Gemma |
| Usage Tracking | Monitor token consumption |
| Performance Metrics | Track accuracy and latency |
| Test Framework | Comprehensive testing suite |
| Reporting | Generate detailed reports |

## Architecture

```
┌─────────────────────────────────────────┐
│           Enterprise Apps               │
├─────────────────┬───────────────────────┤
│  Model Manager  │    Test Framework    │
├─────────────────┼───────────────────────┤
│ Load/Unload     │ Unit Tests            │
│ Token Tracking   │ Integration Tests    │
│ Performance      │ Stress Tests          │
└─────────────────┴───────────────────────┘
                    │
                    ▼
              ┌──────────┐
              │  LLM     │
              │ (Qwen/   │
              │ Gemma)   │
              └──────────┘
```

---

## Related Documentation

- [Getting Started](../getting-started/index.md)
- [MLOps](../mlops/index.md)
- [SLA System](../sla-system/index.md)