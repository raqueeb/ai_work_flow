# Enterprise AI Automations

> Privacy-first AI agents for real-world ISP operations. No cloud. No data leaks. Pure local intelligence.

---

## 🏗️ Architecture Philosophy

**Privacy First** - All data stays on-premises. No cloud API calls for sensitive data. Complete data sovereignty ensures your customer information never leaves your infrastructure.

**Locality Only** - Run entirely on your own hardware. No internet dependency. Systems work offline when needed, giving you complete control over your AI operations.

**Speed Matters** - Small, efficient models (1.5B - 7B parameters) deliver fast inference times. Real-time responses for customer support without long wait times.

**Modular Design** - Each project is self-contained and easy to extend. Standalone functionality means you can pick and choose what you need without adopting everything at once.

**Production Ready** - Built with MLOps pipelines, monitoring, and A/B testing capabilities from the start. These aren't just demos - they're ready for real deployment.

**Human Centric** - AI assists but humans decide. All decisions are explainable with complete audit trails. Your team stays in control of every automated process.

---

## 🔄 System Workflow

### Complete AI Pipeline

```
User Input ──▶ Local Server (LM Studio) ──▶ AI Model (Qwen/Gemma) ──▶ Response
     ▲                                                                    │
     └────────────────────────────────────────────────────────────────────┘
                              Feedback Loop
```

### Classification Workflow (ISP Classifier)

```
Customer Complaint
        │
        ▼
Text Preprocessing (normalize, clean)
        │
        ▼
Local LLM (Qwen 2.5 1.5B) ──▶ Classification (ISP-001, ISP-006, ISP-047, etc.)
        │
        ▼
Response Generation
        │
        ▼
Customer Notified with ETA/Solution
```

### RAG Workflow (Qwen + RAG)

```
Documents (PDF, TXT, CSV) ──▶ Text Chunker ──▶ Embedding Model (Local)
                                              │
Query Input ◀──────────────────────────────────┘
        │
        ▼
Vector Similarity Search (Top-K Chunks)
        │
        ▼
Context + Query ──▶ LLM (Qwen 2.5) ──▶ Grounded Response with Citations
```

### MLOps Pipeline Workflow

```
Train ──▶ Validate ──▶ Register ──▶ Deploy ──▶ Monitor ──▶ Alert (if drift) ──▶ Retrain
                                                      │
                                                      ◀─────────────────────────┘
```

---

## 📁 Project Groups

### 1. Getting Started
এই ফোল্ডারটি দিয়ে শুরু করুন যদি আপনি এই repository-তে নতুন হন। এখানে LM Studio-র সাথে কথা বলার প্রথম স্ক্রিপ্ট আছে যা দেখায় কিভাবে local LLM-এর সাথে যোগাযোগ করতে হয়। এটা সবচেয়ে simple এবং basic উদাহরণ - এটা বুঝলে বাকি সব কিছু সহজ হয়ে যাবে। আপনি এখান থেকে শিখবেন কিভাবে API call করতে হয় এবং AI-র কাছ থেকে response পেতে হয়।

### 2. ISP Classifier
এটা হলো আমাদের মূল classification system যা customer complaints গুলোকে diagnostic codes-এ ভাগ করে। যখন কোনো গ্রাহক সমস্যা রিপোর্ট করে, এই সিস্টেম complaint টাকে analyze করে এবং সঠিক ISP code assign করে - যেমন ISP-001 (ONT issue) বা ISP-006 (weather-related outage)। ১২টি Python script আছে যা বিভিন্ন classification approach দেখায়, rule-based থেকে শুরু করে AI-powered পর্যন্ত। আপনি baseline compare করতে পারবেন modern AI approach-এর সাথে।

### 3. ISP Classifier Reasoning
এই মডিউলে classification-এর পাশাপাশি explanation-ও আছে। এটা শুধু নির্দিষ্ট কোড দেয় না, ব্যাখ্যাও করে কেন ওই কোড বেছে নেওয়া হয়েছে। যখন আপনার support team-কে জানাতে হবে কেন একটা particular classification হয়েছে, এই system transparent reasoning provide করে। Chain-of-thought approach ব্যবহার করে complex complaints গুলোকে ভালোভাবে বোঝে এবং appropriate solutions recommend করে।

### 4. Qwen + RAG
RAG (Retrieval-Augmented Generation) হলো একটা powerful technique যা AI responses-কে আরো accurate করে। এই ফোল্ডারে Qwen 2.5 1.5B model দিয়ে knowledge-augmented responses তৈরির উদাহরণ আছে। সিস্টেমটা প্রথমে আপনার documents থেকে relevant information retrieve করে, তারপর সেটা context হিসেবে ব্যবহার করে response generate করে। এটা especially useful যখন আপনি internal policies, technical documentation, বা training materials-এর উপর ভিত্তি করে answers দিতে চান।

### 5. Gemma E4B
Google-এর Gemma 4-bit quantized model এর capabilities দেখায় এই ফোল্ডার। এটা complex reasoning এবং classification tasks-এ বেশি accurate, তবে একটু slower। Qwen-এর সাথে তুলনা করলে Gemma বেশি quality দেয় কিন্তু speed sacrifice করে। আপনি এখানে various demonstrations পাবেন - cybersecurity analysis থেকে network monitoring পর্যন্ত, সব Gemma model দিয়ে implement করা।

### 6. HR Assistant
Human Resources automation এর জন্য তৈরি করা হয়েছে এই section। তিনটি main components আছে - HR Manager যা leave approvals automate করে, HR Assistant যা employee queries handle করে, এবং Sales Funnel AI যা customer leads manage করে। যখন কোনো employee leave request করে, AI সেটা review করে balance check করে এবং appropriate action নেয়। এটা HR operations-কে significantly faster এবং consistent করে তোলে।

### 7. SLA System
Service Level Agreement monitoring এবং violation detection এর জন্য এই system। যখন একটা support ticket create হয়, SLA timer শুরু হয় এবং different priority levels-এর জন্য different thresholds আছে - P1 critical issues এর জন্য 4 ঘন্টা, P4 general inquiries এর জন্য 72 ঘন্টা। যখন SLA risk-এ চলে যায়, system automatically escalate করে এবং appropriate teams-কে notify করে। এটা service quality maintain করতে এবং SLA breaches এড়াতে সাহায্য করে।

### 8. Smart Gift AI
AI-powered gift recommendation system এই ফোল্ডারে। এটা customer preferences analyze করে এবং personalized gift suggestions দেয়। Admin interface দিয়ে products manage করা যায় এবং promotional campaigns automate করা যায়। যখন কোনো customer birthday বা anniversary approach করে, system automatically appropriate recommendations generate করে based on past behavior এবং budget।

### 9. LLM Demos
Experiments এবং benchmarking এর জন্য এই collection। এখানে বিভিন্ন size-এর test cases আছে - 5 case mini demo থেকে শুরু করে 55 case stress test পর্যন্ত। আপনি দেখতে পাবেন কিভাবে different models perform করে বিভিন্ন workloads-এ। Stress test results দেখায় কোন model কোন situation-এ ভালো এবং average response times কত। এটা আপনাকে decide করতে সাহায্য করে কোন model আপনার use case-এর জন্য best।

### 10. Enterprise Apps
Production-ready enterprise automation examples এই ফোল্ডারে। Model management থেকে testing frameworks পর্যন্ত সব আছে। আপনি এখানে learn করবেন কিভাবে models load/unload করতে হয়, token usage track করতে হয়, এবং comprehensive testing suites run করতে হয়। এগুলো actual business operations-এ use করার জন্য designed, just demos না।

### 11. MLOps
Production ML pipelines এই section-এর main focus। Customer churn prediction থেকে শুরু করে auto-retraining triggers পর্যন্ত সব included। Model registry আপনার trained models track করে, monitoring dashboard real-time performance দেখায়, এবং A/B testing framework different versions compare করার সুযোগ দেয়। যখন model drift detect হয়, system automatically retraining trigger করে। এটা complete MLOps lifecycle manage করে।

---

## 📁 Project Structure

```
classifier-app/
│
├── 📁 isp-classifier/              Customer complaint classification (12 scripts)
├── 📁 isp-classifier-reasoning/     AI reasoning for support tickets (3 scripts)
├── 📁 hr-assistant/                 HR automation tools (3 scripts)
├── 📁 qwen-rag/                     Qwen + RAG knowledge system (4 scripts)
├── 📁 gemma-e4b/                    Gemma 1.1 4B demonstrations (3 scripts)
├── 📁 sla-system/                   SLA monitoring & classification (2 scripts)
├── 📁 smart-gift/                   AI gift recommendation admin (1 script)
├── 📁 llm-demos/                    LLM experiments & benchmarking (5 scripts)
├── 📁 enterprise-apps/              Enterprise automation examples (5 scripts)
├── 📁 mlops/                        Production ML pipelines (6 scripts)
├── 📁 getting-started/              Learning path basics (3 scripts)
│
├── 📁 llmtraining/                  Documentation root (mkdocs)
└── translate_to_bangla.py          Bangla translation utility
```

---

## 🚀 Quick Start

```bash
# 1. LM Studio start করুন Qwen 2.5 1.5B বা Gemma 4 E4B দিয়ে
# 2. প্রথম AI script run করুন
python getting-started/talk_to_llm.py
```

---

## 🛤️ Learning Path

এই path টা follow করুন beginner থেকে advanced:

```
1. Getting Started ──────────────────────────────────────────────────────────▶
│   └── শিখুন: LM Studio-র সাথে যোগাযোগ, প্রথম AI response

2. ISP Classifier ─────────────────────────────────────────────────────────────▶
│   └── শিখুন: Basic classification, rule-based থেকে AI

3. ISP Reasoning ──────────────────────────────────────────────────────────────▶
│   └── শিখুন: Chain of thought, advanced reasoning

4. Qwen + RAG ─────────────────────────────────────────────────────────────────▶
│   └── শিখুন: Retrieval-augmented generation

5. Gemma E4B ───────────────────────────────────────────────────────────────────▶
│   └── শিখুন: Google's efficient 4-bit model

6. HR Assistant ───────────────────────────────────────────────────────────────▶
│   └── শিখুন: Real-world HR automation

7. SLA System ─────────────────────────────────────────────────────────────────▶
│   └── শিখুন: Enterprise SLA management

8. Smart Gift AI ─────────────────────────────────────────────────────────────▶
│   └── শিখুন: AI admin systems

9. LLM Demos ─────────────────────────────────────────────────────────────────▶
│   └── শিখুন: Experiments and benchmarking

10. Enterprise Apps ───────────────────────────────────────────────────────────▶
│   └── শিখুন: Production-ready applications

11. MLOps ──────────────────────────────────────────────────────────────────────
    └── শিখুন: Production pipelines and monitoring
```

---

## 🤖 Available Models

| Model | Size | Purpose | Best For | Speed |
|-------|------|---------|----------|-------|
| **Qwen 2.5 1.5B** | 1.5B | Classification, Reasoning | Speed, General tasks | ⚡⚡⚡⚡ |
| **Gemma 4 E4B** | 4B | Complex reasoning, Analysis | Accuracy, Quality | ⚡⚡ |

---

## 📊 Tech Stack

```
Language: Python 3.10+
LLM Runtime: LM Studio
Vector DB: ChromaDB
Embeddings: sentence-transformers
Framework: LangChain, LlamaIndex
API Server: FastAPI, Flask
Database: PostgreSQL, MongoDB
Monitoring: Grafana, Prometheus
Deployment: Docker, Kubernetes
```

---

## 📈 Benchmark Results

llm_stress_test_report.json এর উপর ভিত্তি করে:

```
qwen2.5-coder-1.5b-instruct Results
─────────────────────────────────────────
Accuracy: 32.7% (18/55 tests passed)
Avg Time: 2973ms
Avg Tokens: 792.7
```

---

## 📚 Documentation

| Language | Link |
|----------|------|
| English | [docs/](llmtraining/docs/index.md) |
| Bangla | [বাংলা ডক্স](llmtraining/docs/bangla/index.md) |

---

## 🔧 Configuration

```env
# LM Studio Configuration
LM_STUDIO_URL=http://localhost:1234/v1/chat/completions
MODEL_NAME=qwen2.5-coder-1.5b-instruct

# Vector Database
CHROMA_PERSIST_DIR=./chroma_db

# Logging
LOG_LEVEL=INFO
```

---

## 🤝 Contributing

Contributions welcome! Please read the documentation and follow the project structure.

---

## 📄 License

MIT License - See LICENSE for details.

---

## 👤 Author

**Rakibul Hassan**, CTO - Link3 Technologies