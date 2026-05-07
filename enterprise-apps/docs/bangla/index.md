# Enterprise Apps - Bangla

**লেখক:** রাকিবুল হাসান  
**প্রতিষ্ঠান:** লিংক3 টেকনোলজিস  
**তারিখ:** জানুয়ারি ২০২৫

---

## ওভারভিউ

Enterprise Apps collection-এ business operations এর জন্য production-ready applications আছে। এতে model management, testing frameworks এবং utility scripts আছে।

## স্ক্রিপ্টগুলো

| স্ক্রিপ্ট | বিবরণ |
|--------|-------------|
| `model_use_class.py` | Model usage এবং management |
| `test_classifier.py` | Classifier testing framework |
| `test_one.py` | Single case testing |
| `test_llm_ISP_ticket_classifier.py` | ISP ticket classifier tests |

## Model Use Class

```python
from model_use_class import ModelManager

manager = ModelManager()

# Models initialize করুন
manager.load_model("qwen2.5-coder-1.5b-instruct")
manager.load_model("gemma-4-e4b")

# Models switch করুন
manager.use_model("gemma-4-e4b")

# Generate করুন
response = manager.generate("Fiber optic troubleshooting কি?")

# Usage track করুন
stats = manager.get_stats()
print(f"Token ব্যবহার: {stats['total_tokens']}")
```

সহজ এবং effective.

## Testing Framework

```python
from test_classifier import ClassifierTest

test = ClassifierTest()

# Test suite run করুন
results = test.run_suite([
    "test_accuracy",
    "test_latency",
    "test_edge_cases"
])

# Report generate করুন
test.generate_report(results, format="json")
```

## বৈশিষ্ট্যগুলো

| বৈশিষ্ট্য | বিবরণ |
|---------|-------------|
| Multi-model Support | Qwen এবং Gemma-র মধ্যে switch করুন |
| Usage Tracking | Token consumption monitor করুন |
| Performance Metrics | Accuracy এবং latency track করুন |
| Test Framework | Comprehensive testing suite |
| Reporting | বিস্তারিত reports generate করুন |

---

## সম্পর্কিত ডকুমেন্টেশন

- [শুরু করুন](../getting-started/index.md)
- [MLOps](../mlops/index.md)
- [SLA System](../sla-system/index.md)