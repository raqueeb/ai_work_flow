# বেসিক ডেমো (লিগেসি)

এই পৃষ্ঠায় লিঙ্ক৩‑এর প্রাথমিক ডেমোগুলো তালিকাভুক্ত করা হয়েছে, যা **Qwen 2.5‑1.5B** মডেল ব্যবহার করে তৈরি।

## ডেমো তালিকা

| ডেমো | বর্ণনা | চালানোর পদ্ধতি |
|------|--------|----------------|
| `app-reasoning1.py` | কীওয়ার্ড‑ভিত্তিক ক্লাসিফিকেশন + দ্রুত Qwen ফ্যালব্যাক | `python app-reasoning1.py` |
| `app-reasoning2.py` | চেইন‑অফ‑থট (CoT) ডেমো | `python app-reasoning2.py` |
| `app-baseline-class.py` | Streamlit ড্যাশবোর্ড | `streamlit run app-baseline-class.py` |
| `apps-slm.py` | SLA চেক ডেমো | `streamlit run apps-slm.py` |
| `ERP_AI_Approval_Assistant.py` | ERP ওয়ার্কফ্লো সহকারী | `streamlit run ERP_AI_Approval_Assistant.py` |

## চালানোর ধাপ

1. **LM Studio** চালু করুন এবং পছন্দের মডেল (Qwen অথবা Gemma) লোড করুন।  
2. টার্মিনালে `cd c:\Downloads\classifier-app` লিখে প্রকল্প ফোল্ডারে যান।  
3. উপরের **চালানোর পদ্ধতি** কলাম থেকে কমান্ড চালান।  
4. ব্রাউজার স্বয়ংক্রিয়ভাবে `http://localhost:8501` খুলবে।

## কাস্টমাইজেশন

- `model_use_class.py` (Qwen) অথবা `gemma-4-e4b-model_use_class.py` (Gemma) এ সিস্টেম প্রম্পট পরিবর্তন করে আউটপুটের টোন ও বিস্তারিততা নিয়ন্ত্রণ করুন।  
- `app-baseline-class.py`‑এর `FIELD_ISP_CODES` ডিকশনারি আপডেট করে নতুন কীওয়ার্ড যোগ করুন।  
- Docker ব্যবহার করে অ্যাপগুলোকে কন্টেইনারে প্যাকেজ করুন, যাতে পরিবেশ পুনরুত্পাদন সহজ হয়।

*এই লিগেসি গাইডটি বিদ্যমান ডিপ্লয়মেন্ট রক্ষণাবেক্ষণ ও আপডেটের জন্য রেফারেন্স।*