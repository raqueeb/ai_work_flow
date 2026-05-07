# Enterprise Applications

This section showcases how local LLMs can be embedded into real‑world enterprise workflows at Link3 Technologies. Each example is a self‑contained Python script (some with Streamlit UI) that runs entirely on‑premise, keeping data private and latency low.

## 1. Ticket Classification Dashboard

- **Script:** `app-baseline-class.py` (Qwen) / `gemma-4-e4b-app-baseline-class.py` (Gemma)  
- **Purpose:** Classify ISP support tickets into one of 50 ISP codes, display confidence, and trigger field dispatch for critical issues.  
- **Key Features:** Hybrid keyword + LLM logic, real‑time UI, automatic escalation.

## 2. ERP Approval Assistant

- **Script:** `ERP_AI_Approval_Assistant.py`  
- **Purpose:** Automate leave requests, purchase orders, and HR onboarding approvals.  
- **How it Works:** The LLM reads the request JSON, checks policy rules, and returns an approval decision with a short justification.

## 3. Sales Funnel AI Closer

- **Script:** `Link3_Sales_Funnel_AI_Closer.py`  
- **Purpose:** Classify leads, suggest next‑step actions, and generate a ready‑to‑send email draft.  
- **Benefit:** Reduces manual copy‑pasting and speeds up deal closure.

## 4. SmartGift Product Recommender

- **Script:** `SmartGift_AI_Admin.py`  
- **Purpose:** Map vague customer wishes (“something for my brother’s YouTube channel”) to exact inventory items using fuzzy matching and LLM reasoning.

## 5. Network Monitoring & Diagnostics

- **Script:** `gemma-4-e4b-network_monitor.py`  
- **Purpose:** Run ping, traceroute, DNS lookup, and let the LLM summarize health and suggest remediation.

## 6. Cybersecurity Log Analyzer

- **Script:** `gemma-4-e4b-cybersec_analysis.py`  
- **Purpose:** Analyze firewall/IDS logs, flag potential intrusions, and propose mitigation steps.

## 7. Stress‑Testing Suite

- **Script:** `llm_stress_test_class.py` (Qwen) / `gemma-4-e4b-llm_stress_test_class.py` (Gemma)  
- **Purpose:** Run 200 synthetic tickets, generate accuracy/latency reports, and help tune prompts.

## Deployment Tips

- **Containerize** – Wrap any script in a lightweight Docker container with LM Studio pre‑installed for reproducible environments.  
- **CI Integration** – Add the stress‑test scripts to your CI pipeline to catch regressions when updating models or prompts.  
- **Version Control** – Keep `mkdocs.yml` and the documentation in sync with code changes; the docs are automatically rebuilt on push.

## Next Steps

- Explore the **Model Comparison** page to see side‑by‑side performance of Qwen vs. Gemma.  
- Extend any demo with custom prompts or additional data sources (e.g., CRM APIs).  

*Local LLMs turn rule‑based scripts into brain‑powered assistants without sacrificing privacy.*