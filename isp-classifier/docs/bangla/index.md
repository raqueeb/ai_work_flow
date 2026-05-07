# ISP Classifier - Bangla

**লেখক:** রাকিবুল হাসান  
**প্রতিষ্ঠান:** লিংক3 টেকনোলজিস  
**তারিখ:** জানুয়ারি ২০২৫

---

## ওভারভিউ

ISP Classifier হলো একটা customer complaint classification সিস্টেম। এটা স্থানীয় LLM ব্যবহার করে বানানো। গ্রাহকের অভিযোগগুলো ডায়াগনস্টিক কোডে ভাগ করে দেয় যাতে সমস্যা সমাধান সহজ হয়।

## বৈশিষ্ট্য

- **Rule-based Classification** - ঐতিহ্যবাহী if-else লজিক
- **LLM-based Classification** - Qwen/Gemma দিয়ে AI-পাওয়ার্ড classification
- **Comparison Mode** - দুইটা অ্যাপ্রোচের সাইড-বাই-সাইড তুলনা
- **Batch Processing** - একসাথে অনেকগুলো অভিযোগ প্রসেস করা

## স্ক্রিপ্টগুলো

| স্ক্রিপ্ট | বিবরণ |
|---------|--------|
| `app_baseline_class.py` | বেসলাইন rule-based classifier |
| `app_optimize_classifier.py` | অপ্টিমাইজড classifier |
| `app_classifier_1.py` থেকে `app_classifier_9.py` | বিভিন্ন classifier ভার্সন |
| `llm_classifier.py` | LLM-পাওয়ার্ড classifier |
| `traditional_vs_ai_workflow.py` | তুলনা স্ক্রিপ্ট |

## আর্কিটেকচার

```
গ্রাহকের অভিযোগ
       │
       ▼
┌──────────────┐
│  প্রিপ্রসেসিং │
└──────────────┘
       │
       ▼
┌──────────────┐    ┌──────────────┐
│    রুলস      │ অথবা │     LLM      │
│  (বেসলাইন)   │    │  (Qwen/Gemma)│
└──────────────┘    └──────────────┘
       │                  │
       └────────┬─────────┘
                ▼
         ডায়াগনস্টিক কোড
```

## ব্যবহার

```python
from isp_classifier import LLMClassifier

classifier = LLMClassifier()
complaint = "আমার ONT-এ লাল বাতি জ্বলছে, ইন্টারনেট কাজ করছে না"
result = classifier.classify(complaint)
print(f"কোড: {result['code']}, বিশ্বাসযোগ্যতা: {result['confidence']}")
```

এভাবে classification কাজ করে। সহজ এবং দ্রুত।

## ডায়াগনস্টিক কোড

| কোড | বিবরণ |
|------|-------------|
| ISP-001 | ONT/Fiber সমস্যা |
| ISP-002 | WiFi/Router সমস্যা |
| ISP-006 | আবহাওয়াজনিত বিদ্যুৎ বিভ্রাট |
| ISP-036 | Fiber কাটা/ক্ষতি |
| ISP-047 | সিগন্যাল লেভেল সমস্যা |

---

## সম্পর্কিত ডকুমেন্টেশন

- [শুরু করুন](../getting-started/index.md)
- [ISP Reasoning](../isp-classifier-reasoning/index.md)
- [Qwen + RAG](../qwen-rag/index.md)