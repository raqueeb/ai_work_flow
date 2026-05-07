# Traditional vs AI Comparison

**Author:** Rakibul Hassan  
**Company:** Link3 Technologies  
**Date:** January 2025

---

## Overview

This document compares traditional rule-based classification with AI-powered LLM classification for ISP customer complaints.

## Side-by-Side Comparison

| Aspect | Traditional (Baseline) | AI (LLM) |
|--------|----------------------|----------|
| **Approach** | If-else rules | Neural network |
| **Training Data** | Manual curation | Pre-trained + fine-tune |
| **Context Understanding** | Keyword matching | Full context |
| **Error Handling** | Explicit conditions | Implicit understanding |
| **Maintenance** | Manual updates | Continuous learning |

## Test Results

From the stress test on 55 complaints:

| Metric | Baseline | LLM (Qwen) | LLM (Gemma) |
|--------|----------|------------|-------------|
| **Accuracy** | 45.5% | 32.7% | 58.2% |
| **Avg Time (ms)** | 5 | 2973 | 4500 |
| **Avg Tokens** | N/A | 792.7 | 1200 |

> Note: Qwen performed better in speed, Gemma in accuracy

## Code Comparison

### Traditional Approach

```python
def classify_traditional(complaint):
    if "red light" in complaint.lower():
        return "ISP-001"
    elif "wifi" in complaint.lower():
        return "ISP-002"
    elif "rain" in complaint.lower():
        return "ISP-006"
    else:
        return "ISP-999"
```

### AI Approach

```python
def classify_ai(complaint):
    prompt = f"""Classify this complaint into diagnostic code.
    Complaint: {complaint}
    Codes: ISP-001 (ONT), ISP-002 (WiFi), ISP-006 (Weather), etc."""
    
    response = llm.chat(prompt)
    return parse_code(response)
```

## When to Use Each

### Use Traditional When:
- Simple, predictable complaint patterns
- Need deterministic results
- Resource constraints
- Audit trail requirements

### Use AI When:
- Complex, nuanced complaints
- Need high accuracy
- Handling variations
- Self-improving system needed

## Migration Path

1. **Phase 1**: Deploy baseline alongside AI
2. **Phase 2**: Route uncertain cases to baseline
3. **Phase 3**: Full AI deployment
4. **Phase 4**: Continuous improvement

---

## Related Documentation

- [ISP Classifier Overview](index.md)
- [Baseline Classifier](baseline.md)
- [LLM Classifier](llm-classifier.md)