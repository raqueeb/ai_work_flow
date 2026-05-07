# Why Local Inference?

In traditional enterprise applications, we often rely on **rule-based systems** — long lists of `if-else` statements, regular expressions, and hardcoded logic. These systems work well for predictable patterns, but they struggle when language gets messy, synonyms appear, or edge cases arise.

**Local LLM inference** changes that. Instead of writing rules for every scenario, we give the model a description of the task and let it *reason* like a human brain. The LLM becomes the "brain" of the application, understanding context, nuance, and intent.

## Rule‑Based vs. LLM‑Based

| Aspect | Rule‑Based | LLM‑Based |
|--------|-------------|-------------|
| **Logic** | Hard‑coded rules | Semantic understanding |
| **Maintenance** | Add/modify rules constantly | Update prompt or fine‑tune |
| **Handles ambiguity** | Poorly | Very well |
| **Data privacy** | Depends on implementation | Excellent when run locally |
| **Setup** | Simple scripts | Requires local LLM server |

## Why Run LLMs Locally?

1. **Privacy** – Customer complaints, employee records, and sales leads never leave your machine. No third‑party APIs see your data.
2. **Speed** – Sub‑second inference on consumer GPUs or modern CPUs. No network latency.
3. **Cost** – No per‑token billing. Run 24/7 for free after the initial model download.
4. **Offline** – Works without internet, perfect for internal enterprise networks.
5. **Control** – You decide which model to use, when to update it, and how to prompt it.

## The Link3 Approach

At Link3 Technologies, we use **hybrid systems**:

- **Keyword rules** catch obvious patterns instantly (e.g., “red light” → `ISP‑001`).
- **Local LLM** (Qwen2.5‑1.5B or Gemma 4 E4B) handles the rest, providing semantic understanding and reasoning.

This gives us the best of both worlds: deterministic speed for clear cases, and brain‑like flexibility for everything else.

## Streamlit: Turning Scripts into Interactive Apps

Many of our demos are built with **Streamlit**, a Python framework that lets you create web‑based dashboards with almost no front‑end code. If you can write a Python script, you can build a Streamlit app.

**Why Streamlit?**

- **No web development needed** – Just script in Python, Streamlit handles the UI.
- **Interactive widgets** – Sliders, buttons, text inputs, and more out of the box.
- **Fast prototyping** – See changes live as you save your script.
- **Easy sharing** – Run with `streamlit run your_app.py` and open the local URL.

Throughout this documentation, whenever you see a script that imports `streamlit`, launch it with:

```bash
streamlit run script_name.py
```

The app will open in your browser, giving you a point‑and‑click interface to the underlying LLM logic.

## Next Steps

Now that you understand the "why", let’s set up your environment and run your first local LLM script.

*Continue to [Getting Started with Qwen 2.5](getting-started-qwen.md).*