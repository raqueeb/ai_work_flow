# Upgrading to Gemma 4 E4B

After you have explored the Qwen 2.5‑1.5B workflow, you may want to try a larger model with stronger reasoning capabilities. **Gemma 4 E4B** (4 billion parameters) provides better performance on complex tickets while still running locally on a consumer‑grade GPU or CPU.

## Why Upgrade?

| Reason | Qwen 2.5‑1.5B | Gemma 4 E4B |
|--------|---------------|------------|
| Parameter count | 1.5 B | 4 B |
| Reasoning depth | Good for straightforward classification | Superior for nuanced, multi‑turn reasoning |
| Speed (CPU) | Faster | Slightly slower, but still sub‑second on modern CPUs |
| Memory usage | ~2 GB VRAM | ~4 GB VRAM (or ~6 GB RAM on CPU) |
| Ideal use‑case | Simple ISP ticket classification | Complex ticket classification, chain‑of‑thought demos, network diagnostics |

## Prerequisites

- All the same prerequisites from the Qwen guide (Python 3.11+, Git, LM Studio).
- A machine with at least **4 GB VRAM** (or 8 GB RAM) to load the model comfortably.

## Installation Steps

1. **Install the same Python dependencies** (if you already did this for Qwen, you can skip):

   ```bash
   pip install streamlit requests playwright
   ```

2. **Open LM Studio** (if it is already running, keep it open).

3. **Search for Gemma 4 E4B**  
   - Click the **Discover** icon (magnifying glass) on the left.  
   - In the search bar type: `Gemma-4B-Instruct`.  
   - Choose the **Google Gemma 4 E4B‑Instruct‑GGUF** model.  
   - Pick a quantized version – **Q4_K_M** is a good balance of size and quality.

4. **Download and Load**  
   - Click **Download** and wait for the model to finish.  
   - After download, go to the **Models** tab, locate **Gemma‑4B‑Instruct**, and click **Load**.  
   - LM Studio will start a local server at `http://localhost:1234/v1`.

5. **Verify the Server**  
   - Switch to the **Developer** tab. You should see **Local Server: Running** and the endpoint `http://localhost:1234/v1`.

## Running Gemma‑Based Scripts

All Gemma‑specific scripts are prefixed with `gemma-4-e4b-`. For example:

```bash
# Run the optimized classifier that uses Gemma
python gemma-4-e4b-app-optimized-classifiers.py
```

Or launch the interactive Streamlit version:

```bash
streamlit run gemma-4-e4b-app-optimized-classifiers.py
```

The UI is identical to the Qwen version; only the underlying model changes, giving you richer explanations and higher accuracy on ambiguous tickets.

## Updating Existing Scripts

If you have a Qwen‑based script and want to switch to Gemma without rewriting the whole file:

1. Locate the line that defines the model name, e.g.:

   ```python
   MODEL_NAME = "qwen2.5-coder-1.5b-instruct"
   ```

2. Replace it with the Gemma model name:

   ```python
   MODEL_NAME = "gemma-4b-instruct"
   ```

3. Save the file and re‑run. The rest of the code works unchanged because both models follow the OpenAI‑compatible API.

## Quick Test

Run the quick demo to see the difference:

```bash
python gemma-4-e4b-app-reasoning2.py
```

You should see a more detailed reasoning trace, with the model breaking down the problem step‑by‑step before giving the final ISP code.

## Next Steps

- Explore the **Gemma Demos** page for more advanced use‑cases (chain‑of‑thought, hierarchical classification, network monitoring).  
- Compare results side‑by‑side with the Qwen version to see the improvement in accuracy and explanation quality.

*Happy upgrading! The same local‑only, privacy‑first workflow applies – just a more powerful brain.*