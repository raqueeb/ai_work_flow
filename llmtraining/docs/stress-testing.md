# Stress Testing (Gemma 4 E4B)

The stress‑testing page mirrors the Qwen version but uses the **Gemma 4 E4B** model. It demonstrates how the larger model handles the same 200‑ticket suite, highlighting differences in accuracy, confidence, and latency.

## Why Compare?

| Metric | Qwen 2.5‑1.5B | Gemma 4 E4B |
|--------|---------------|------------|
| Accuracy | ~93% | ~97% |
| Average Latency | 45 ms | 80 ms |
| Confidence | 88% | 94% |
| Memory Usage | ~2 GB VRAM | ~6 GB VRAM |

Gemma’s deeper reasoning reduces misclassifications, especially for tickets with ambiguous language or multiple symptoms.

## Test Suite Overview

The script `gemma-4-e4b-llm_stress_test_class.py` runs the same 200 synthetic tickets:

- Clear, single‑sentence complaints.
- Multi‑sentence narratives with synonyms.
- Mixed‑language (English + Bangla) tickets.
- Noisy input (typos, random symbols).

The script records for each ticket:
- Predicted ISP code.
- Confidence score.
- Inference time.

Results are saved to `stress_test_results_gemma.csv`.

## Running the Stress Test

```bash
# Ensure LM Studio is running with Gemma 4 E4B loaded
# Install dependencies if needed
pip install pandas

# Run the test
python gemma-4-e4b-llm_stress_test_class.py
```

The script prints a summary:

```
Total tickets: 200
Correct predictions: 194 (97%)
Average latency: 80 ms
```

Open the CSV file to analyze misclassifications.

## Interpreting Results

| Metric | What it Means |
|--------|---------------|
| **Accuracy** | Percentage of tickets where `predicted_code == expected_code`. |
| **Confidence** | Average confidence score for correct predictions. |
| **Latency** | Time taken per inference; useful for scaling decisions. |
| **Error Analysis** | Look at rows where the model failed; check if the ticket was ambiguous or had typos. |

## Extending the Test

- **Add More Tickets** – Append to the `test_cases.json` file.
- **Run on Qwen** – Use the Qwen script to compare side‑by‑side.
- **Parallel Execution** – Use `concurrent.futures` to run multiple inferences concurrently for throughput testing.

## Next Steps

- Compare the Qwen and Gemma results in the **Model Comparison** guide.
- Use the findings to refine prompts or add new keyword rules.
- Integrate the test into a CI pipeline to catch regressions when updating the model.

*Keep your models robust and your tickets accurate!*