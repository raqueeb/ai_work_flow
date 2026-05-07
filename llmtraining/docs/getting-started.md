# Getting Started (Legacy)

> **Note:** This guide covers the original setup using the Qwen 2.5‑1.5B model. For a more structured learning path, see [Getting Started with Qwen 2.5](getting-started-qwen.md) and [Upgrading to Gemma 4 E4B](upgrading-to-gemma.md).

This page provides a quick‑start for running the original demos that shipped with the repository.

## Prerequisites

- **Python 3.11+** – Ensure `python` is in your `PATH`.  
- **Git** – To clone the repository (optional if you already have the files).  
- **LM Studio** – Download from https://lmstudio.ai/ and install.

## Installation

```bash
# Clone the repository (skip if you already have the folder)
git clone https://github.com/raqueeb/link3_ai_cases.git
cd classifier-app

# Install Python dependencies
pip install streamlit requests playwright
```

## Setting Up LM Studio

1. **Download and Install LM Studio** – Follow the installer prompts.  
2. **Launch LM Studio** – Open the application.  
3. **Search for Qwen2.5‑1.5B** – Click the “Discover” icon, type `Qwen2.5-1.5B-Instruct`, and download the GGUF version (Q4_K_M recommended).  
4. **Load the Model** – Go to the “Models” tab, select the model, and click **Load**.  
5. **Start the Server** – LM Studio will start a local server at `http://localhost:1234/v1`.

## Running Your First Demo

```bash
# Quick demo (original Qwen version)
python app-reasoning2.py
```

You should see output similar to:

```
======================================================================
 QWEN2.5-1.5B LLM QUICK DEMO
======================================================================
...
```

## Running a Streamlit App

```bash
streamlit run app-baseline-class.py
```

This opens a browser at `http://localhost:8501` with an interactive ticket classifier.

## Next Steps

- Explore the **Qwen Demos** page for a list of all original demos.  
- Upgrade to **Gemma 4 E4B** for better reasoning (see the [Upgrading to Gemma 4 E4B](upgrading-to-gemma.md) guide).  
- Check the **Model Comparison** page to decide which model fits your use‑case.

*This legacy guide is kept for reference; the new learning path is recommended for beginners.*