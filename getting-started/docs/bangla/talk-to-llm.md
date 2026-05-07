# LM Studio-এর সাথে কথা বলা

**লেখক:** রাকিবুল হাসান  
**প্রতিষ্ঠান:** লিংক3 টেকনোলজিস  
**তারিখ:** জানুয়ারি ২০২৫

---

## ওভারভিউ

এই গাইডে দেখাব কীভাবে Python দিয়ে LM Studio-এর সাথে কথা বলা যায়। LM Studio একটা লোকাল API সার্ভার হিসেবে কাজ করে। সেখানে LLM মডেল রাখা থাকে।

## সেটআপ

```python
import requests

BASE_URL = "http://localhost:1234/v1"
MODEL = "qwen2.5-coder-1.5b-instruct"
```

## বেসিক রিকোয়েস্ট

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

সহজ কথায়, প্রশ্ন পাঠাব, রেসপন্স পাব। এটাই মূল ব্যাপার।

## স্ট্রিমিং রেসপন্স

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

স্ট্রিমিং হলো যখন সার্ভার থেকে অল্প অল্প করে টেক্সট আসে। ধীরে ধীরে দেখা যায়। কোনো বড় রেসপন্সের জন্য এটা ভালো।

## সম্পূর্ণ উদাহরণ

```python
import requests
import json

def talk_to_llm(prompt: str, model: str = MODEL) -> dict:
    """LM Studio-এর সাথে পূর্ণ কথোপকথন।"""
    try:
        response = requests.post(
            f"{BASE_URL}/chat/completions",
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": "আপনি একজন সহায়ক অ্যাসিস্ট্যান্ট।"},
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

# চালান
if __name__ == "__main__":
    result = talk_to_llm("বাংলাদেশের রাজধানী কোথায়?")
    print(result["response"])
```

## সমস্যা সমাধান

| সমস্যা | সমাধান |
|-------|--------|
| Connection refused | LM Studio সার্ভার চলছে কিনা দেখুন |
| Timeout | timeout বাড়ান অথবা ছোট মডেল ব্যবহার করুন |
| খালি রেসপন্স | মডেল ঠিকমতো লোড হয়েছে কিনা চেক করুন |

একটা একটা করে সমাধান করতে হবে। কোনো সমস্যা হলে ধীরে ধীরে ঠিক করতে হবে।

---

## সম্পর্কিত ডকুমেন্টেশন

- [শুরু করুন](index.md)
- [ISP Classifier](../isp-classifier/index.md)