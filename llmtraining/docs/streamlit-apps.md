# Streamlit Applications

Streamlit lets you turn any Python script that imports `streamlit` into an interactive web dashboard with a single command. This makes it possible for non‑developers to explore LLM‑driven tools, adjust parameters, and see results instantly.

## Why Streamlit?

- **Zero front‑end code** – Write pure Python; Streamlit builds the UI.
- **Live reloading** – Save the script and the browser updates automatically.
- **Widgets out of the box** – Text boxes, sliders, buttons, file uploaders, and more.
- **Easy sharing** – Run `streamlit run your_app.py` and share the local URL (or deploy to a server).

## How to launch

```bash
# Install dependencies if you haven't already
pip install streamlit requests

# Run any Streamlit app
streamlit run app-baseline-class.py
```

## Available Streamlit Apps

| Script | Description |
|--------|-------------|
| `app-baseline-class.py` | Baseline CTO dashboard – shows ticket classification and field dispatch logic |
| `app-classifier1.py` – `app-classifier9.py` | Iterative classifier demos with increasing model complexity |
| `app-optimized-classifiers.py` | Production‑ready optimized version using Gemma 4 E4B |
| `app-reasoning1.py` / `app-reasoning2.py` | Chain‑of‑thought reasoning demos |
| `apps-slm.py` | Service Level Management dashboard |
| `apps-standard.py` | Standard dashboard template |
| `ERP_AI_Approval_Assistant.py` | ERP workflow approval assistant |
| `gemma-4-e4b-app-optimized-classifiers.py` | Gemma‑optimized classifier |
| `gemma-4-e4b-app-reasoning2.py` | Gemma reasoning demo |
| `gemma-4-e4b-model_use_class.py` | Model usage explorer for Gemma |
| `Link3_Sales_Funnel_AI_Closer.py` | Sales funnel AI assistant |
| `model_use_class.py` | Generic model usage explorer |
| `SmartGift_AI_Admin.py` | SmartGift product recommendation dashboard |

Run any of the above with `streamlit run <script_name>.py`. The app will start a local web server (usually at `http://localhost:8501`) and open your default browser.

## Example

```bash
streamlit run app-reasoning2.py
```

You’ll see a clean UI where you can paste a ticket description, click **Analyze Ticket**, and the LLM will return the predicted ISP code, confidence score, and a short justification. If the result is a field‑dispatch case, a button appears to simulate dispatching a technician.

---

*All Streamlit apps share a common layout: a sidebar for inputs, a main panel for results, and optional sections for debugging or advanced options. Feel free to modify the scripts to add new widgets or change the prompts.*