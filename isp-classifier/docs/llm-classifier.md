# LLM Classifier

**Author:** Rakibul Hassan  
**Company:** Link3 Technologies  
**Date:** January 2025

---

## Overview

The LLM Classifier uses local LLMs (Qwen 2.5 1.5B or Gemma 4 E4B) to classify customer complaints with higher accuracy and context understanding.

## How It Works

```python
import requests

class LLMClassifier:
    def __init__(self, model: str = "qwen2.5-coder-1.5b-instruct"):
        self.model = model
        self.base_url = "http://localhost:1234/v1"
    
    def classify(self, complaint: str) -> dict:
        prompt = f"""Classify this ISP customer complaint:
        
        Complaint: {complaint}
        
        Return a JSON with:
        - code: The diagnostic code (e.g., ISP-001)
        - category: Problem category
        - confidence: Confidence score (0-1)
        - action: Recommended action
        """
        
        response = requests.post(
            f"{self.base_url}/chat/completions",
            json={
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3
            },
            timeout=60
        )
        
        return self.parse_response(response.json())
```

## Features

- **Context Understanding** - Understands complaint intent
- **Fuzzy Matching** - Handles typos and variations
- **Confidence Scores** - Provides accuracy estimates
- **Recommended Actions** - Suggests troubleshooting steps

## Usage

```python
classifier = LLMClassifier()

# Single classification
result = classifier.classify("My internet stopped working after the rain last night")
print(f"Code: {result['code']}, Action: {result['action']}")

# Batch classification
results = classifier.classify_batch(complaints)
```

## Model Comparison

| Model | Accuracy | Speed | Best For |
|-------|----------|-------|----------|
| Qwen 2.5 1.5B | 85% | Fast | General classification |
| Gemma 4 E4B | 92% | Medium | Complex complaints |

---

## Related Documentation

- [ISP Classifier Overview](index.md)
- [Baseline Classifier](baseline.md)
- [Comparison](comparison.md)