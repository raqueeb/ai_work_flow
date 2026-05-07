# MCP সার্ভার

MCP (Model‑Control‑Protocol) সার্ভার লোকাল LLM‑কে একটি REST API হিসেবে প্রকাশ করে। এই গাইডে কিভাবে MCP সার্ভার সেটআপ ও ব্যবহার করবেন তা বর্ণনা করা হয়েছে।

## ইনস্টলেশন

```bash
pip install mcp-server
```

## কনফিগারেশন (`mcp_config.yaml`)

```yaml
model:
  name: qwen2.5-coder-1.5b-instruct   # অথবা gemma-4b-instruct
  endpoint: http://localhost:1234/v1
auth:
  token: YOUR_SECRET_TOKEN
```

## চালু করা

```bash
mcp-server --config mcp_config.yaml
```

## ব্যবহার উদাহরণ (Python)

```python
import requests
payload = {
    "model": "local-llm",
    "messages": [{"role": "system", "content": "You are an ISP assistant."},
                 {"role": "user", "content": "Customer reports red light on ONT."}]
}
response = requests.post("http://localhost:1234/v1/chat/completions", json=payload)
print(response.json()["choices"][0]["message"]["content"])
```

*Docker‑এ ডিপ্লয় করে টিমে শেয়ার করা যায়।*