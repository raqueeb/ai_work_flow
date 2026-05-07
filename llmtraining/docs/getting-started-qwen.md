# Getting Started with Qwen 2.5

This guide walks you through setting up the environment to run the **Qwen 2.5‑1.5B** model for local LLM inference. All steps are designed for a fresh Windows machine, but they also work on macOS and Linux with minor path adjustments.

## Prerequisites

- **Python 3.11+** – Make sure `python` is in your `PATH`.
- **Git** – To clone the repository (optional if you already have the files).
- **LM Studio** – Download and install from https://lmstudio.ai/. This provides a local OpenAI‑compatible server for the model.

## Installation

```bash
# Clone the repository (skip if you already have the folder)
git clone https://github.com/raqueeb/link3_ai_cases.git
cd classifier-app

# Install Python dependencies
pip install -r requirements.txt   # If a requirements.txt exists
# Or install the core packages manually
pip install streamlit requests playwright
```

## Setting Up LM Studio with Qwen 2.5‑1.5B

1. **Download and Install LM Studio**
   - Go to https://lmstudio.ai/ and download the installer for your operating system.
   - Run the installer and follow the prompts.

2. **Launch LM Studio**
   - Open LM Studio from your applications menu.

3. **Search for and Download Qwen2.5‑1.5B**
   - Click the "Discover" icon (magnifying glass) in the left sidebar.
   - In the search bar, type: `Qwen2.5-1.5B-Instruct`.
   - Look for the model by Qwen/Qwen2.5-1.5B-Instruct-GGUF.
   - Click on the model and select a quantized version (Q4_K_M is recommended for a balance of quality and size).
   - Click "Download".

4. **Load the Model**
   - After the download completes, go to the "Models" tab on the left.
   - You should see Qwen2.5-1.5B-Instruct listed.
   - Click the "Load" button to load the model into memory.
   - LM Studio will start a local server at `http://localhost:1234/v1`.

5. **Verify the Server is Running**
   - In LM Studio, go to the "Developer" tab.
   - You should see "Local Server: Running" at the bottom.
   - The API endpoint will be shown as `http://localhost:1234/v1`.

## Running Your First Script

Now let's run a basic LLM demo to verify everything is working:

```bash
# Run the Qwen version of the quick demo
python app-reasoning2.py  # This is the original Qwen version
```

Or, if you prefer to use the explicitly named version:

```bash
# Note: We'll create a Qwen-specific version shortly.
# For now, the original files are the Qwen versions.
```

You should see output similar to:

```
======================================================================
 QWEN2.5-1.5B LLM QUICK DEMO
======================================================================

This demo shows how to use the Qwen2.5-1.5B model for local, private LLM inference.
All processing is done locally via LM Studio.

Asking LLM to analyze...
LLM RESPONSE:
[The model's response to your prompt]
```

## Running a Streamlit App

Many of our tools are interactive web apps built with Streamlit. To launch one:

```bash
streamlit run app-baseline-class.py
```

This will open a browser window with a dashboard where you can paste a customer complaint, click **Analyze Ticket**, and see the LLM's classification in real time.

## Understanding the File Structure

In this repository, you will find:

- **Original files** (no prefix): These are the Qwen2.5-1.5B versions.
- **Gemma-prefixed files** (`gemma-4-e4b-*.py`): These are the Google Gemma 4 E4B versions.

For this learning path, which focuses on starting with Qwen, we will primarily work with the original files first.

---

*Next: [Qwen 2.5 Demos](qwen-demos.md)*