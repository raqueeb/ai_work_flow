# ISP Classification (Legacy)

This legacy guide describes the original ISP ticket classification workflow that predates the structured learning path. It is kept for reference and for users who prefer the older naming conventions.

## Overview

The classification system maps a free‑form customer complaint to one of 50 predefined ISP codes (e.g., `ISP‑001` for “Red light / Physical fiber cut”). The workflow combines:

1. **Fast keyword rules** – Deterministic matching for obvious patterns.  
2. **LLM fallback** – When no rule matches, the LLM (Qwen 2.5‑1.5B or Gemma 4 E4B) is queried to infer the most appropriate code.

## Running the Legacy Classifier

```bash
# Install dependencies if needed
pip install streamlit requests

# Launch the Streamlit UI (Qwen version)
streamlit run app-baseline-class.py
```

Or run the pure Python version:

```bash
python app-reasoning1.py   # Keyword + Qwen fallback
python app-reasoning2.py   # Chain‑of‑thought version
```

## Expected Input

Paste the raw ticket text into the **Ticket** field. The classifier will output:

- **Predicted ISP code** (e.g., `ISP‑023`).  
- **Confidence score** (0‑100).  
- **Justification** – a short sentence explaining the decision.  
- **Field dispatch flag** – highlighted in red if the issue is critical (L2+).

## Extending the Legacy System

- **Add new keywords** – Edit the `FIELD_ISP_CODES` dictionary in `app-baseline-class.py`.  
- **Custom prompts** – Modify the system prompt in `model_use_class.py` to request additional details (e.g., suggested troubleshooting steps).  
- **Switch models** – Change `MODEL_NAME = "gemma-4b-instruct"` to use Gemma instead of Qwen.

## When to Use This Legacy Guide

- You are maintaining an existing deployment that still references the old file names.  
- You need a quick reference without the newer learning‑path structure.  

For a more modern, step‑by‑step onboarding experience, see the **Getting Started with Qwen 2.5** and **Upgrading to Gemma 4 E4B** guides.

*The core logic remains the same; only the documentation layout has changed.*