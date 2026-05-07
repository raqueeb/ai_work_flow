# ISP Classification (Qwen 2.5)

This guide explains how to use the **Qwen 2.5‑1.5B** model to classify ISP support tickets into one of 50 predefined ISP codes. The classification logic combines fast keyword rules with the LLM for ambiguous cases, providing a hybrid approach that balances speed and accuracy.

## Overview

- **Keyword Rules** – Deterministic matching for obvious patterns (e.g., “red light”, “fiber cut”).  
- **LLM Fallback** – For tickets that don’t match any rule, the LLM analyzes the text and returns the most appropriate ISP code.  
- **Streamlit UI** – An interactive dashboard (`app-baseline-class.py`) lets you paste a ticket, run the classifier, and see the result instantly.

## How It Works

1. **Pre‑processing** – The ticket text is lower‑cased and stripped of special characters.  
2. **Keyword Matching** – The script iterates through a list of high‑priority keywords. If a match is found, the corresponding ISP code is returned with 99% confidence.  
3. **LLM Classification** – If no keyword matches, the script sends a prompt to the Qwen model via LM Studio:

   ```
   You are an ISP support ticket classifier. Choose the most appropriate ISP‑XXX code for the following complaint:
   {ticket_text}
   ```

   The model returns a single code (e.g., `ISP‑001`).  
4. **Result Display** – The Streamlit UI shows the code, a short justification, and a confidence score. If the issue is a field‑dispatch case (L2 or higher), a red alert appears with a **Dispatch Field Team** button.

## Running the Classifier

```bash
# Install dependencies if you haven’t already
pip install streamlit requests

# Launch the Streamlit dashboard
streamlit run app-baseline-class.py
```

Open your browser at `http://localhost:8501`, paste a ticket description, and click **Analyze Ticket**.

### Example

**Ticket:** “My ONT shows a red light and the internet is down.”  

**Result:**  
- **ISP Code:** `ISP‑001` – Red light / Physical Fiber Cut  
- **Confidence:** 99% (keyword match)  
- **Action:** Field dispatch required (L2)

## Extending the Classifier

- **Add New Keywords** – Edit the `FIELD_ISP_CODES` list in `app-baseline-class.py`.  
- **Custom Prompts** – Modify the system prompt in `model_use_class.py` to ask for additional details (e.g., suggested troubleshooting steps).  
- **Switch to Gemma** – Change `MODEL_NAME = "qwen2.5-coder-1.5b-instruct"` to `MODEL_NAME = "gemma-4b-instruct"` and restart the app.

## Next Steps

- Review the **Qwen Demos** page for more examples of how the model can be used in other contexts.  
- Upgrade to **Gemma 4 E4B** for deeper reasoning on complex tickets (see the [Upgrading to Gemma 4 E4B](upgrading-to-gemma.md) guide).

*Happy classifying!*