# Basic Demos

This page lists the simple, entry‑level demos that showcase how to use the local LLMs for common ISP tasks. All demos are self‑contained Python scripts and can be run directly from the repository root.

## Qwen 2.5 (1.5 B) Demos

| Demo | Description | How to Run |
|------|-------------|------------|
| `app-reasoning1.py` | Keyword‑based classification with a quick LLM fallback. | `python app-reasoning1.py` |
| `app-reasoning2.py` | Chain‑of‑thought reasoning demo – the model explains each step before giving the final ISP code. | `python app-reasoning2.py` |
| `app-baseline-class.py` | Streamlit dashboard for interactive ticket classification. | `streamlit run app-baseline-class.py` |
| `apps-slm.py` | Service Level Management demo – query the LLM for SLA compliance. | `streamlit run apps-slm.py` |
| `ERP_AI_Approval_Assistant.py` | Simple ERP workflow assistant (leave requests, purchase orders). | `streamlit run ERP_AI_Approval_Assistant.py` |

## Gemma 4 E4B Demos

| Demo | Description | How to Run |
|------|-------------|------------|
| `gemma-4-e4b-app-reasoning1.py` | Same as Qwen’s `app-reasoning1.py` but using Gemma. | `python gemma-4-e4b-app-reasoning1.py` |
| `gemma-4-e4b-app-reasoning2.py` | Chain‑of‑thought demo with deeper reasoning. | `python gemma-4-e4b-app-reasoning2.py` |
| `gemma-4-e4b-app-baseline-class.py` | Streamlit UI powered by Gemma. | `streamlit run gemma-4-e4b-app-baseline-class.py` |
| `gemma-4-e4b-app-slm.py` | Service Level Management demo using Gemma. | `streamlit run gemma-4-e4b-app-slm.py` |
| `gemma-4-e4b-ERP_AI_Approval_Assistant.py` | ERP assistant demo with Gemma’s richer explanations. | `streamlit run gemma-4-e4b-ERP_AI_Approval_Assistant.py` |

## Running a Demo

1. **Start LM Studio** and load the appropriate model (Qwen 2.5‑1.5B or Gemma 4 E4B).  
2. Open a terminal in `c:\Downloads\classifier-app`.  
3. Execute the command from the **How to Run** column.  
4. For Streamlit demos, a browser window will open at `http://localhost:8501`.

## Extending the Demos

- Add custom prompts in the `model_use_class.py` (Qwen) or `gemma-4-e4b-model_use_class.py` (Gemma) helper files.  
- Replace the model name in the script to switch between Qwen and Gemma instantly.  
- Wrap any demo in Docker for reproducible deployment.

*These basic demos are ideal for newcomers to get hands‑on experience with local LLM inference.*