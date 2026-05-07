# ISP Classifier Reasoning - Bangla

**লেখক:** রাকিবুল হাসান  
**প্রতিষ্ঠান:** লিংক3 টেকনোলজিস  
**তারিখ:** জানুয়ারি ২০২৫

---

## ওভারভিউ

ISP Classifier Reasoning মডিউলে classification সিস্টেমে explanation যোগ করা হয়েছে। এটা শুধু complaint classify করে না, ব্যাখ্যাও করে কেন একটা নির্দিষ্ট diagnostic code বেছে নেওয়া হয়েছে।

## কেন Reasoning দরকার

| Reasoning ছাড়া | Reasoning সহ |
|-------------------|-----------------|
| "ISP-001" | "ISP-001 - ONT/fiber সমস্যা ধরা পড়েছে" |
| কোনো ব্যাখ্যা নেই | "লাল বাতির প্যাটার্ন ONT failure-এর সাথে মিলে যাচ্ছে" |
| ব্ল্যাক বক্স | স্বচ্ছ সিদ্ধান্ত নেওয়া |
| ডিবাগ করা কঠিন | অডিট করা সহজ |

## কিভাবে কাজ করে

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

## উদাহরণ আউটপুট

```
অভিযোগ: "আমার ONT-এ লাল বাতি জ্বলছে এবং ইন্টারনেট বন্ধ হয়ে গেছে"

{
  "code": "ISP-001",
  "reasoning": "ONT-এ 'লাল বাতি' হলো fiber disconnection বা 
               ONT hardware failure-এর একটা ক্লাসিক ইন্ডিকেটর।
               অভিযোগে স্পষ্টভাবে 'ইন্টারনেট বন্ধ হয়ে গেছে' 
               বলা হয়েছে যা connectivity loss নিশ্চিত করে।",
  "confidence": 0.92,
  "evidence": ["লাল বাতি", "ONT", "ইন্টারনেট বন্ধ"],
  "action": "ONT-এ fiber connection চেক করুন, ONT রিবুট করুন, 
            যদি চলতে থাকে তাহলে এসকেলেট করুন"
}
```

## স্ক্রিপ্টগুলো

| স্ক্রিপ্ট | বিবরণ |
|--------|-------------|
| `app_reasoning1.py` | Qwen দিয়ে বেসিক reasoning |
| `app_reasoning2.py` | Gemma দিয়ে এনহ্যান্সড reasoning |

## সুবিধাগুলো

1. **স্বচ্ছতা** - কেন সিদ্ধান্ত নেওয়া হয়েছে সেটা জানা যায়
2. **বিশ্বাস** - অপারেটররা classification verify করতে পারে
3. **ডিবাগিং** - classification error খুঁজে বের করা সহজ
4. **কমপ্লায়েন্স** - রেগুলেটরি প্রয়োজনীয়তার জন্য audit trail

---

## সম্পর্কিত ডকুমেন্টেশন

- [ISP Classifier](../isp-classifier/index.md)
- [LLM Classifier](../isp-classifier/llm-classifier.md)
- [Qwen + RAG](../qwen-rag/index.md)