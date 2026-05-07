# শুরু করুন

**লেখক:** রাকিবুল হাসান  
**প্রতিষ্ঠান:** লিংক3 টেকনোলজিস  
**তারিখ:** জানুয়ারি ২০২৫

---

## স্বাগতম

এই সেকশনে আপনি প্রথম পদক্ষেপ নেবেন। LM Studio-এর সাথে কথা বলা শিখবেন। প্রথম AI পাওয়ার স্ক্রিপ্ট চালাবেন। এটা কোনো কঠিন ব্যাপার না। ধীরে ধীরে এগিয়ে যেতে হবে মাত্র।

## কী কী লাগবে

শুরু করার আগে নিশ্চিত করতে হবে:

- **LM Studio** ইনস্টল করা আছে এবং চলছে
- **Qwen 2.5 1.5B** অথবা **Gemma 4 E4B** মডেল লোড করা আছে
- **Python 3.8+** ইনস্টল করা আছে
- Python-এর বেসিক জ্ঞান আছে

## দ্রুত সেটআপ

```bash
# প্যাকেজ ইনস্টল করুন
pip install requests

# LM Studio চালু করুন
# ১. LM Studio খুলুন
# ২. Qwen 2.5 1.5B মডেল লোড করুন
# ৩. ডিফল্ট পোর্টে (1234) সার্ভার চালু করুন
```

## প্রথম স্ক্রিপ্ট

একটা ফাইল বানান `talk_to_llm.py`:

```python
import requests

def talk_to_llm(prompt: str) -> str:
    """LM Studio-এ পাঠাবে এবং রেসপন্স পাবে।"""
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

# টেস্ট করুন
result = talk_to_llm("হ্যালো, আপনি কেমন আছেন?")
print(result)
```

এখানে দেখবেন কীভাবে প্রশ্ন পাঠানো যায়। সিস্টেম সেটা প্রসেস করে রেসপন্স দেয়। সেই রেসপন্স থেকে বুঝতে হবে AI কী বলতে চাইছে।

## পরবর্তী ধাপ

যখন LLM-এর সাথে কথা বলা শিখে যাবেন, তখন এগিয়ে যেতে পারেন:

১. **ISP Classifier** - বাস্তব classification-এ LLM ব্যবহার
২. **Basic Reasoning** - লজিক এবং ডিসিশন মেকিং যোগ করা
৩. **Advanced Reasoning** - চেইন অফ থট প্রম্পটিং

একটা একটা করে এগিয়ে যেতে হবে। তাড়াহুড়ো করার দরকার নেই।

---

## সম্পর্কিত ডকুমেন্টেশন

- [ISP Classifier Overview](../isp-classifier/index.md)
- [Qwen + RAG](../qwen-rag/index.md)
- [Reasoning কেন গুরুত্বপূর্ণ](../reasoning-importance.md)