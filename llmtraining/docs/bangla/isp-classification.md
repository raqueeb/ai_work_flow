# ISP ক্লাসিফিকেশন (লিগেসি)

এই গাইডটি পুরনো ফাইল নাম ব্যবহার করে ISP টিকিট ক্লাসিফিকেশন প্রক্রিয়া বর্ণনা করে। এটি Qwen 2.5‑1.5B অথবা Gemma 4 E4B মডেল ব্যবহার করে টিকিটকে ৫০টি পূর্বনির্ধারিত কোডে ম্যাপ করে।

## চালানোর পদ্ধতি

```bash
# Streamlit UI (Qwen)
streamlit run app-baseline-class.py

# পিউর পাইথন ডেমো
python app-reasoning1.py   # কীওয়ার্ড + Qwen ফ্যালব্যাক
python app-reasoning2.py   # চেইন‑অফ‑থট (CoT) ডেমো
```

## কাস্টমাইজেশন

- **নতুন কীওয়ার্ড যোগ** – `app-baseline-class.py`‑এর `FIELD_ISP_CODES` ডিকশনারি আপডেট করুন।  
- **মডেল সুইচ** – `MODEL_NAME = "gemma-4b-instruct"` করে Gemma‑এ পরিবর্তন করুন।  

*লিগেসি সিস্টেম রক্ষণাবেক্ষণ ও আপডেটের জন্য রেফারেন্স।*