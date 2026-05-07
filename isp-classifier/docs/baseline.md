# ISP Classifier Baseline

**Author:** Rakibul Hassan  
**Company:** Link3 Technologies  
**Date:** January 2025

---

## Overview

The baseline classifier uses rule-based logic to categorize customer complaints. This is the traditional approach before introducing LLM-based classification.

## How It Works

```python
import re

class BaselineClassifier:
    def __init__(self):
        self.rules = {
            "ont": ["red light", "pon led", "onu", "fiber"],
            "wifi": ["wifi", "router", "connection", "ssid"],
            "weather": ["rain", "storm", "flood", "water"]
        }
    
    def classify(self, complaint: str) -> dict:
        complaint_lower = complaint.lower()
        
        for category, keywords in self.rules.items():
            for keyword in keywords:
                if keyword in complaint_lower:
                    return {
                        "category": category,
                        "code": self.get_code(category),
                        "confidence": 0.7
                    }
        
        return {"category": "unknown", "code": "ISP-999", "confidence": 0.1}
    
    def get_code(self, category: str) -> str:
        codes = {
            "ont": "ISP-001",
            "wifi": "ISP-002",
            "weather": "ISP-006",
            "fiber": "ISP-036"
        }
        return codes.get(category, "ISP-999")
```

## Limitations

| Limitation | Description |
|------------|-------------|
| Keyword matching | Misses nuanced complaints |
| No context | Cannot understand intent |
| Static rules | Requires manual updates |
| Low accuracy | High misclassification rate |

## Comparison with LLM

| Aspect | Baseline | LLM |
|--------|----------|-----|
| Accuracy | 60-70% | 85-95% |
| Speed | Fast | Medium |
| Maintenance | Manual | Self-learning |
| Context understanding | None | Full |

---

## Related Documentation

- [ISP Classifier Overview](index.md)
- [LLM Classifier](llm-classifier.md)
- [Traditional vs AI](traditional-vs-ai.md)