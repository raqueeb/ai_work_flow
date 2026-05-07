# LLM Demos - Bangla

**লেখক:** রাকিবুল হাসান  
**প্রতিষ্ঠান:** লিংক3 টেকনোলজিস  
**তারিখ:** জানুয়ারি ২০২৫

---

## ওভারভিউ

LLM Demos collection-এ বিভিন্ন demonstration scripts আছে যা different LLM capabilities এবং use cases দেখায়।

## Demo ক্যাটাগরি

### ১. বেসিক ডেমো

শিখার জন্য সহজ, foundational examples।

| স্ক্রিপ্ট | বিবরণ |
|--------|-------------|
| `llm_quick_demo_base.py` | দ্রুত baseline demonstration |
| `llm_mini_demo_5cases.py` | ৫-কেসের mini demonstration |
| `llm_demo_small_10case.py` | ১০-কেসের small demonstration |

### ২. Hierarchical ডেমো

Multi-level classification এবং decision-making examples।

| স্ক্রিপ্ট | বিবরণ |
|--------|-------------|
| `llm_hierarchical_demo.py` | Hierarchical classification |
| `llm_hierarchical_class.py` | Class-based hierarchy |

### ৩. Stress Testing

Load-এর নিচে performance এবং accuracy testing।

| স্ক্রিপ্ট | বিবরণ |
|--------|-------------|
| `llm_stress_test_class.py` | Stress testing framework |
| `llm_stress_test_report.json` | Test results |

## দ্রুত শুরু

```python
from llm_demos import QuickDemo

demo = QuickDemo(model="qwen2.5-coder-1.5b-instruct")

# Quick demo run করুন
results = demo.run(n_cases=5)
print(f"Accuracy: {results['accuracy']:.1%}")
```

সহজ এবং straightforward.

## Hierarchical ডেমো

```python
from llm_demos import HierarchicalDemo

demo = HierarchicalDemo()

# Multi-level classification
result = demo.classify(
    "বৃষ্টির পরে ইন্টারনেট বন্ধ হয়ে গেছে",
    levels=["category", "subcategory", "code"]
)

print(result)
# {'category': 'outage', 'subcategory': 'weather', 'code': 'ISP-006'}
```

## Performance Metrics

| Demo | Cases | Avg Accuracy | Avg Time |
|------|-------|--------------|----------|
| Mini (5) | 5 | 85% | 2.5s |
| Small (10) | 10 | 78% | 3.1s |
| Stress (55) | 55 | 58% | 4.5s |

---

## সম্পর্কিত ডকুমেন্টেশন

- [শুরু করুন](../getting-started/index.md)
- [ISP Classifier](../isp-classifier/index.md)
- [Gemma E4B](../gemma-e4b/index.md)