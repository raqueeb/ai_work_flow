# Streamlit অ্যাপস

এই পৃষ্ঠায় লিঙ্ক৩‑এর **Streamlit**‑ভিত্তিক ডেমো অ্যাপগুলোর তালিকা ও ব্যবহার নির্দেশনা রয়েছে। সব অ্যাপ লোকাল LLM (Qwen 2.5‑1.5B অথবা Gemma 4 E4B) ব্যবহার করে।

## ডেমো তালিকা

| অ্যাপ | বর্ণনা | চালানোর পদ্ধতি |
|------|--------|----------------|
| `app-baseline-class.py` | টিকিট ক্লাসিফিকেশন ড্যাশবোর্ড – রিয়েল‑টাইমে ISP কোড, কনফিডেন্স এবং ফিল্ড‑ডিসপ্যাচ দেখায়। | `streamlit run app-baseline-class.py` |
| `apps-slm.py` | সার্ভিস লেভেল ম্যানেজমেন্ট – SLA চেক ও রিমাইন্ডার জেনারেট করে। | `streamlit run apps-slm.py` |
| `ERP_AI_Approval_Assistant.py` | ERP ওয়ার্কফ্লো সহকারী – লিভ, পারচেজ অর্ডার ইত্যাদি অনুমোদন করে। | `streamlit run ERP_AI_Approval_Assistant.py` |
| `gemma-4-e4b-app-baseline-class.py` | Gemma 4 E4B ব্যবহার করে একই ক্লাসিফিকেশন UI। | `streamlit run gemma-4-e4b-app-baseline-class.py` |
| `gemma-4-e4b-app-slm.py` | Gemma‑ভিত্তিক SLA ডেমো। | `streamlit run gemma-4-e4b-app-slm.py` |

## চালানোর ধাপ

1. **LM Studio** চালু করুন এবং পছন্দের মডেল (Qwen অথবা Gemma) লোড করুন।  
2. টার্মিনালে `cd c:\Downloads\classifier-app` লিখে প্রকল্প ফোল্ডারে যান।  
3. উপরের **চালানোর পদ্ধতি** কলাম থেকে কমান্ড চালান।  
4. ব্রাউজার স্বয়ংক্রিয়ভাবে `http://localhost:8501` এ খুলবে।

## কাস্টমাইজেশন টিপস

- `model_use_class.py` (Qwen) অথবা `gemma-4-e4b-model_use_class.py` (Gemma) এ সিস্টেম প্রম্পট পরিবর্তন করে আউটপুটের টোন ও বিস্তারিততা নিয়ন্ত্রণ করুন।  
- `app-baseline-class.py`‑এর `FIELD_ISP_CODES` ডিকশনারি আপডেট করে নতুন কীওয়ার্ড যোগ করুন।  
- Docker ব্যবহার করে অ্যাপগুলোকে কন্টেইনারে প্যাকেজ করুন, যাতে পরিবেশ পুনরুত্পাদন সহজ হয়।

*Streamlit অ্যাপগুলো লোকাল LLM‑এর ক্ষমতা দ্রুত দেখার জন্য আদর্শ।*