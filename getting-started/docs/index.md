# Getting Started

**Author:** Rakibul Hassan  
**Company:** Link3 Technologies  
**Date:** January 2025

---

## Welcome

This section helps you take your first steps with local LLM development. You will learn how to communicate with LM Studio and run your first AI-powered scripts.

## What You Need

Before starting, make sure you have:

- **LM Studio** installed and running
- **Qwen 2.5 1.5B** or **Gemma 4 E4B** model loaded
- **Python 3.8+** installed
- Basic understanding of Python

## Quick Setup

```bash
# Install required packages
pip install requests

# Start LM Studio
# 1. Open LM Studio
# 2. Load Qwen 2.5 1.5B model
# 3. Start server on default port (1234)
```

## Your First Script

Create a file named `talk_to_llm.py`:

```python
import requests

def talk_to_llm(prompt: str) -> str:
    """Send a prompt to LM Studio and get response."""
    response = requests.post(
        "http://localhost:1234/v1/chat/completions",
        json={
            "model": "qwen2.5-coder-1.5b-instruct",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        },
        timeout=30
    )
    return response.json()["choices"][0]["message"]["content"]

# Test it
result = talk_to_llm("Hello, how are you?")
print(result)
```

## Next Steps

Once you understand how to communicate with the LLM, proceed to:

1. **ISP Classifier** - Apply LLM to real-world classification
2. **Basic Reasoning** - Add logic and decision making
3. **Advanced Reasoning** - Chain of thought prompting

---

## Related Documentation

- [ISP Classifier Overview](../isp-classifier/index.md)
- [Qwen + RAG](../qwen-rag/index.md)
- [Why Reasoning Matters](../reasoning-importance.md)