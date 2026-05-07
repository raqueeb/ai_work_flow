# ISP Classifier Reasoning

**Author:** Rakibul Hassan  
**Company:** Link3 Technologies  
**Date:** January 2025

---

## Overview

The ISP Classifier Reasoning module adds explanation capabilities to the classification system. It not only classifies complaints but also explains WHY it chose a particular diagnostic code.

## Why Reasoning Matters

| Without Reasoning | With Reasoning |
|-------------------|-----------------|
| "ISP-001" | "ISP-001 - ONT/fiber issue detected" |
| No explanation | "Red light pattern matches ONT failure" |
| Black box | Transparent decision-making |
| Hard to debug | Easy to audit and improve |

## How It Works

```python
class ReasoningClassifier:
    def __init__(self, model="gemma-4-e4b"):
        self.model = model
    
    def classify_with_reasoning(self, complaint: str) -> dict:
        prompt = f"""Analyze this ISP complaint and provide:
        
        1. Primary classification with code
        2. Secondary possibilities
        3. Reasoning for the choice
        4. Supporting evidence from complaint
        5. Recommended action
        
        Complaint: {complaint}
        """
        
        response = self.llm.generate(prompt)
        return self.parse_reasoned_response(response)
```

## Example Output

```
Complaint: "My ONT has a red light and internet stopped working"

{
  "code": "ISP-001",
  "reasoning": "The 'red light' on ONT is a classic indicator of 
               fiber disconnection or ONT hardware failure. The 
               complaint explicitly mentions 'internet stopped 
               working' which confirms loss of connectivity.",
  "confidence": 0.92,
  "evidence": ["red light", "ONT", "internet stopped"],
  "action": "Check fiber connection at ONT, reboot ONT, 
            escalate if persists"
}
```

## Scripts

| Script | Description |
|--------|-------------|
| `app_reasoning1.py` | Basic reasoning with Qwen |
| `app_reasoning2.py` | Enhanced reasoning with Gemma |

## Benefits

1. **Transparency** - Know why a decision was made
2. **Trust** - Operators can verify classifications
3. **Debugging** - Easy to find classification errors
4. **Compliance** - Audit trail for regulatory requirements

---

## Related Documentation

- [ISP Classifier Overview](../isp-classifier/index.md)
- [LLM Classifier](../isp-classifier/llm-classifier.md)
- [Qwen + RAG](../qwen-rag/index.md)