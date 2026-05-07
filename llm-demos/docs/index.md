# LLM Demos

**Author:** Rakibul Hassan  
**Company:** Link3 Technologies  
**Date:** January 2025

---

## Overview

LLM Demos collection contains various demonstration scripts showcasing different LLM capabilities and use cases.

## Demo Categories

### 1. Basic Demos

Simple, foundational examples for beginners.

| Script | Description |
|--------|-------------|
| `llm_quick_demo_base.py` | Quick baseline demonstration |
| `llm_mini_demo_5cases.py` | 5-case mini demonstration |
| `llm_demo_small_10case.py` | 10-case small demonstration |

### 2. Hierarchical Demos

Multi-level classification and decision-making examples.

| Script | Description |
|--------|-------------|
| `llm_hierarchical_demo.py` | Hierarchical classification |
| `llm_hierarchical_class.py` | Class-based hierarchy |

### 3. Stress Testing

Performance and accuracy testing under load.

| Script | Description |
|--------|-------------|
| `llm_stress_test_class.py` | Stress testing framework |
| `llm_stress_test_report.json` | Test results |

## Quick Start

```python
from llm_demos import QuickDemo

demo = QuickDemo(model="qwen2.5-coder-1.5b-instruct")

# Run quick demo
results = demo.run(n_cases=5)
print(f"Accuracy: {results['accuracy']:.1%}")
```

## Hierarchical Demo

```python
from llm_demos import HierarchicalDemo

demo = HierarchicalDemo()

# Multi-level classification
result = demo.classify(
    "My internet stopped after the storm",
    levels=["category", "subcategory", "code"]
)

print(result)
# {'category': 'outage', 'subcategory': 'weather', 'code': 'ISP-006'}
```

## Stress Testing

```python
from llm_stress_test import StressTest

test = StressTest(model="gemma-4-e4b")
results = test.run(
    test_cases=complaints,
    expected_codes=codes,
    max_tokens=1000
)

print(f"Accuracy: {results['accuracy']:.1%}")
print(f"Avg Time: {results['avg_time_ms']:.0f}ms")
```

## Performance Metrics

| Demo | Cases | Avg Accuracy | Avg Time |
|------|-------|--------------|----------|
| Mini (5) | 5 | 85% | 2.5s |
| Small (10) | 10 | 78% | 3.1s |
| Stress (55) | 55 | 58% | 4.5s |

---

## Related Documentation

- [Getting Started](../getting-started/index.md)
- [ISP Classifier](../isp-classifier/index.md)
- [Gemma E4B](../gemma-e4b/index.md)