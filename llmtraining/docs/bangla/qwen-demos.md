# Qwen 2.5 ডেমো

এই পৃষ্ঠায় **Qwen 2.5‑1.5B** মডেল ব্যবহার করে তৈরি করা ডেমোগুলোর তালিকা ও চালানোর নির্দেশনা রয়েছে। সব ডেমো লোকালভাবে LM Studio‑এর মাধ্যমে চালানো হয়।

## ডেমো তালিকা

| ডেমো | বর্ণনা | চালানোর পদ্ধতি |
|------|--------|----------------|
| `app-reasoning1.py` | কীওয়ার্ড রুল + Qwen‑এর দ্রুত ক্লাসিফিকেশন। | `python app-reasoning1.py` |
| `app-reasoning2.py` | চেইন‑অফ‑থট (CoT) ডেমো – মডেল ধাপ‑ধাপে ব্যাখ্যা করে। | `python app-reasoning2.py` |
| `app-baseline-class.py` | Streamlit ড্যাশবোর্ড – রিয়েল‑টাইম টিকিট ক্লাসিফিকেশন। | `streamlit run app-baseline-class.py` |
| `app-classifier1.py` – `app-classifier9.py` | ধাপে ধাপে প্রম্পট উন্নয়ন ও মডেল ব্যবহার। | `streamlit run app-classifierX.py` (X = 1‑9) |
| `apps-slm.py` | সার্ভিস লেভেল ম্যানেজমেন্ট – SLA চেকের জন্য LLM ব্যবহার। | `streamlit run apps-slm.py` |
| `ERP_AI_Approval_Assistant.py` | ERP ওয়ার্কফ্লো সহকারী – লিভ ও পারচেজ অর্ডার অনুমোদন। | `streamlit run ERP_AI_Approval_Assistant.py` |

## চালানোর ধাপ

1. **LM Studio** চালু করুন এবং Qwen 2.5‑1.5B মডেল লোড করুন (উপরের **Upgrading to Gemma** গাইডে দেখুন)।  
2. টার্মিনালে `cd c:\Downloads\classifier-app` লিখে প্রকল্প ফোল্ডারে যান।  
3. উপরের **চালানোর পদ্ধতি** কলাম থেকে কমান্ড চালান।  
4. Streamlit ডেমোর জন্য ব্রাউজার স্বয়ংক্রিয়ভাবে `http://localhost:8501` খুলবে।

## কাস্টমাইজেশন

- `model_use_class.py`‑এ সিস্টেম প্রম্পট পরিবর্তন করে আউটপুটের টোন ও বিস্তারিততা নিয়ন্ত্রণ করুন।  
- কীওয়ার্ড রুল আপডেট করতে `app-baseline-class.py`‑এর `FIELD_ISP_CODES` ডিকশনারি সম্পাদনা করুন।  
- Gemma‑এ পরিবর্তন করতে `MODEL_NAME = "gemma-4b-instruct"` করে স্ক্রিপ্ট রিস্টার্ট করুন।

*এই ডেমোগুলো Qwen 2.5‑এর গতি ও নির্ভুলতা দ্রুত অভিজ্ঞতা করার জন্য আদর্শ।*