# ISP Classification (Gemma 4 E4B)

The **Gemma 4 E4B** model offers deeper reasoning and higher accuracy for ISP ticket classification, especially for ambiguous or multi‑step tickets. The workflow is identical to the Qwen version, but the model can ask clarifying questions and provide a more detailed justification.

## How It Works

1. **Keyword Rules** – The same deterministic rules are applied first.  
2. **Gemma Fallback** – If no rule matches, the script sends a prompt to Gemma:

   ```
   You are an ISP support ticket classifier.  
   Analyze the following complaint and return the most appropriate ISP‑XXX code, a short justification, and a confidence score (0‑100).  
   {ticket_text}
   ```

   Gemma returns a structured response, e.g.,

   ```
   ISP‑023 – Broken drop cable – Physical cable damage
   Confidence: 92
   ```

3. **Result Display** – The Streamlit UI shows the code, justification, confidence, and a field‑dispatch button if the issue is critical.

## Running the Classifier

```bash
# Install dependencies if needed
pip install streamlit requests

# Launch the Streamlit dashboard
streamlit run app-baseline-class.py
```

Open `http://localhost:8501`, paste a ticket, and click **Analyze Ticket**.

### Example

**Ticket:** “I can’t connect to the internet, the router shows a blinking red LED.”  

**Result:**  
- **ISP Code:** `ISP‑001` – Red light / Physical Fiber Cut  
- **Confidence:** 95% (Gemma reasoning)  
- **Action:** Field dispatch required (L2)

## Extending the Classifier

- **Add New Keywords** – Update `FIELD_ISP_CODES` in `app-baseline-class.py`.  
- **Custom Prompts** – Modify the system prompt in `model_use_class.py` to ask for troubleshooting steps.  
- **Switch Models** – Change `MODEL_NAME = "gemma-4b-instruct"` to use a different Gemma variant.

## Next Steps

- Compare the Qwen and Gemma results side‑by‑side in the **Model Comparison** guide.  
- Explore the **Advanced Reasoning** page for chain‑of‑thought examples that leverage Gemma’s reasoning depth.

*Happy classifying with the brain of a large LLM!*