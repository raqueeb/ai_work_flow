# Gemma 4 E4B ডেমো#

এই পৃষ্ঠায় **Gemma 4 E4B** মডেল ব্যবহার করে তৈরি করা ডেমোগুলোর তালিকা ও চালানোর নির্দেশনা রয়েছে। Gemma‑এর গভীর রিজনিং ক্ষমতা ব্যবহার করে জটিল টিকিট বিশ্লেষণ করা যায়।

## ডেমো তালিকা

| ডেমো | বর্ণনা | চালানোর পদ্ধতি |
|------|--------|----------------|
| `gemma-4-e4b-app-reasoning1.py` | কীওয়ার্ড রুল + Gemma‑এর দ্রুত ক্লাসিফিকেশন। | `python gemma-4-e4b-app-reasoning1.py` |
| `gemma-4-e4b-app-reasoning2.py` | চেইন‑অফ‑থট (CoT) ডেমো – মডেল ধাপ‑ধাপে ব্যাখ্যা করে। | `python gemma-4-e4b-app-reasoning2.py` |
| `gemma-4-e4b-app-baseline-class.py` | Streamlit ড্যাশবোর্ড – Gemma‑এর রিজনিং দিয়ে রিয়েল‑টাইম টিকিট ক্লাসিফিকেশন। | `streamlit run gemma-4-e4b-app-baseline-class.py` |
| `gemma-4-e4b-app-classifier1.py` – `gemma-4-e4b-app-classifier9.py` | প্রম্পট ইমপ্রুভমেন্টের ধাপ‑ধাপ ডেমো। | `streamlit run gemma-4-e4b-app-classifierX.py` (X = 1‑9) |
| `gemma-4-e4b-app-slm.py` | সার্ভিস লেভেল ম্যানেজমেন্ট – Gemma‑এর মাধ্যমে SLA চেক। | `streamlit run gemma-4-e4b-app-slm.py` |
| `gemma-4-e4b-ERP_AI_Approval_Assistant.py` | ERP ওয়ার্কফ্লো সহকারী – Gemma‑এর সমৃদ্ধ ব্যাখ্যা। | `streamlit run gemma-4-e4b-ERP_AI_Approval_Assistant.py` |

## চালানোর ধাপ

1. **LM Studio** চালু করুন এবং **Gemma 4 E4B** মডেল লোড করুন (Upgrading to Gemma গাইডে দেখুন)।  
2. টার্মিনালে `cd c:\Downloads\classifier-app` লিখে প্রকল্প ফোল্ডারে যান।  
3. উপরের **চালানোর পদ্ধতি** কলাম থেকে কমান্ড চালান।  
4. Streamlit ডেমোর জন্য ব্রাউজার স্বয়ংক্রিয়ভাবে `http://localhost:8501` খুলবে।

## কাস্টমাইজেশন

- `gemma-4-e4b-model_use_class.py`‑এ সিস্টেম প্রম্পট পরিবর্তন করে রিজনিং স্টাইল ও আউটপুটের দৈর্ঘ্য নিয়ন্ত্রণ করুন।  
- কীওয়ার্ড রুল আপডেট করতে `gemma-4-e4b-app-baseline-class.py`‑এর `FIELD_ISP_CODES` ডিকশনারি সম্পাদনা করুন।  
- Qwen‑এ ফিরে যেতে `MODEL_NAME = "qwen2.5-coder-1.5b-instruct"` করে স্ক্রিপ্ট রিস্টার্ট করুন।

*Gemma 4 E4B‑এর গভীর রিজনিং দিয়ে জটিল ISP টিকিটের জন্য আরও সঠিক ও ব্যাখ্যামূলক ফলাফল পান।*