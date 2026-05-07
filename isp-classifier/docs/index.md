# ISP Classifier

**Author:** Rakibul Hassan  
**Company:** Link3 Technologies  
**Date:** January 2025

---

## Overview

The ISP Classifier is a customer complaint classification system built with local LLMs. It maps customer complaints to diagnostic codes for efficient troubleshooting.

## Features

- **Rule-based Classification** - Traditional approach with if-else logic
- **LLM-based Classification** - AI-powered classification using Qwen/Gemma
- **Comparison Mode** - Side-by-side comparison of both approaches
- **Batch Processing** - Process multiple complaints at once

## Scripts

| Script | Description |
|--------|-------------|
| `app_baseline_class.py` | Baseline rule-based classifier |
| `app_optimize_classifier.py` | Optimized classifier |
| `app_classifier_1.py` to `app_classifier_9.py` | Various classifier versions |
| `llm_classifier.py` | LLM-powered classifier |
| `traditional_vs_ai_workflow.py` | Comparison script |

## Architecture

```
Customer Complaint
       │
       ▼
┌──────────────┐
│ Preprocessing│
└──────────────┘
       │
       ▼
┌──────────────┐    ┌──────────────┐
│    Rules     │ or │     LLM      │
│  (Baseline)  │    │  (Qwen/Gemma)│
└──────────────┘    └──────────────┘
       │                  │
       └────────┬─────────┘
                ▼
         Diagnostic Code
```

## Usage

```python
from isp_classifier import LLMClassifier

classifier = LLMClassifier()
complaint = "My ONT has a red light, internet is not working"
result = classifier.classify(complaint)
print(f"Code: {result['code']}, Confidence: {result['confidence']}")
```

## Diagnostic Codes

| Code | Description |
|------|-------------|
| ISP-001 | ONT/Fiber issues |
| ISP-002 | WiFi/Router issues |
| ISP-006 | Weather-related outages |
| ISP-036 | Fiber cut/damage |
| ISP-047 | Signal level issues |

---

## Related Documentation

- [Getting Started](../getting-started/index.md)
- [ISP Reasoning](../isp-classifier-reasoning/index.md)
- [Qwen + RAG](../qwen-rag/index.md)