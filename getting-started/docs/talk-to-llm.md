# Talk to LM Studio

**Author:** Rakibul Hassan  
**Company:** Link3 Technologies  
**Date:** January 2025

---

## Overview

This guide shows how to communicate with LM Studio using Python. LM Studio acts as a local API server that hosts your LLM models.

## Setup

```python
import requests

BASE_URL = "http://localhost:1234/v1"
MODEL = "qwen2.5-coder-1.5b-instruct"
```

## Basic Request

```python
def chat(prompt: str) -> str:
    response = requests.post(
        f"{BASE_URL}/chat/completions",
        json={
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 500
        },
        timeout=60
    )
    return response.json()["choices"][0]["message"]["content"]
```

## Streaming Response

```python
def chat_stream(prompt: str):
    response = requests.post(
        f"{BASE_URL}/chat/completions",
        json={
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "stream": True
        },
        stream=True
    )
    for line in response.iter_lines():
        if line:
            data = json.loads(line)
            if "content" in data.get("choices", [{}])[0].get("delta", {}):
                yield data["choices"][0]["delta"]["content"]
```

## Complete Example

```python
import requests
import json

def talk_to_llm(prompt: str, model: str = MODEL) -> dict:
    """Full conversation with LM Studio."""
    try:
        response = requests.post(
            f"{BASE_URL}/chat/completions",
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 500
            },
            timeout=60
        )
        
        result = response.json()
        return {
            "success": True,
            "response": result["choices"][0]["message"]["content"],
            "usage": result.get("usage", {})
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

# Run
if __name__ == "__main__":
    result = talk_to_llm("What is the capital of Bangladesh?")
    print(result["response"])
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Connection refused | Make sure LM Studio server is running |
| Timeout | Increase timeout or use smaller model |
| Empty response | Check model is loaded properly |

---

## Related Documentation

- [Getting Started Index](index.md)
- [ISP Classifier](../isp-classifier/index.md)