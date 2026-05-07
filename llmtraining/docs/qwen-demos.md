# Qwen 2.5 Demos

The Qwen 2.5‑1.5B model powers a set of interactive demos that showcase how a local LLM can be used for real‑world ISP automation tasks. Each demo is a self‑contained Python script (some with Streamlit UI) that you can run directly after setting up LM Studio.

## Demo List

| Demo | Description | How to Run |
|------|-------------|------------|
| `app-reasoning1.py` | Simple classification demo using keyword rules + Qwen LLM. | `python app-reasoning1.py` |
| `app-reasoning2.py` | Chain‑of‑thought (CoT) reasoning demo – the model explains each step before giving the final ISP code. | `python app-reasoning2.py` |
| `app-baseline-class.py` | Full dashboard with Streamlit UI for ticket classification, confidence scoring, and field‑dispatch handling. | `streamlit run app-baseline-class.py` |
| `app-classifier1.py` – `app-classifier9.py` | Incremental versions showing improvements in prompt engineering and model usage. | `streamlit run app-classifierX.py` (replace X with 1‑9) |
| `apps-slm.py` | Service Level Management demo – shows how to query the LLM for SLA compliance checks. | `streamlit run apps-slm.py` |
| `ERP_AI_Approval_Assistant.py` | ERP workflow assistant that classifies leave requests and purchase orders. | `streamlit run ERP_AI_Approval_Assistant.py` |

## Running a Demo

1. **Start LM Studio** and ensure the Qwen 2.5‑1.5B model is loaded (see the [Getting Started with Qwen 2.5](getting-started-qwen.md) guide).  
2. Open a terminal in the `c:\Downloads\classifier-app` folder.  
3. Execute the command from the **How to Run** column. For Streamlit apps, a browser window will open automatically at `http://localhost:8501`.

## What You’ll See

- **Input area** – Paste a customer complaint or ticket description.  
- **Analyze button** – Triggers the LLM to classify the ticket.  
- **Result panel** – Shows the predicted ISP code, a short justification, and a confidence score.  
- **Field dispatch** – If the issue is critical (e.g., signal loss below –25 dBm), a red alert appears with a **Dispatch Field Team** button.

## Extending the Demos

All demos share a common helper library (`model_use_class.py` for Qwen) that handles the API call to LM Studio. To experiment:

- Change the **system prompt** in the script to ask the model for additional details (e.g., “also suggest a troubleshooting step”).  
- Add new **Streamlit widgets** (e.g., a dropdown to select the model version).  
- Replace the model name with `gemma-4b-instruct` to compare performance side‑by‑side.

## Next Steps

After you’ve tried the Qwen demos, move on to the **Gemma Demos** page to see how a larger model handles more complex reasoning tasks.

*Happy experimenting!*