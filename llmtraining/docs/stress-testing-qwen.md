# Stress Testing (Qwen 2.5)

Stress testing evaluates how well the **Qwen 2.5‑1.5B** model handles a large variety of ISP tickets, including edge cases, ambiguous language, and noisy input. This guide shows how to run the built‑in stress‑test suite and interpret the results.

## Why Stress Test?

- **Validate Accuracy** – Ensure the model classifies tickets correctly across all 50 ISP codes.  
- **Measure Latency** – Check inference time per ticket on your hardware.  
- **Identify Weak Spots** – Find categories where the model frequently misclassifies or returns low confidence.

## Test Suite Overview

The script `llm_stress_test_class.py` contains a list of 200 synthetic tickets covering every ISP code, including:

- Clear, single‑sentence complaints.  
- Multi‑sentence narratives with synonyms.  
- Mixed‑language (English + Bangla) tickets.  
- Noisy input (typos, random symbols).

The script:

1. Loads the Qwen model via LM Studio.  
2. Sends each ticket to the model and records:
   - Predicted ISP code.  
   - Confidence score.  
   - Inference time.  
3. Generates a CSV report (`stress_test_results_qwen.csv`) with the following columns:
   - `ticket_id`, `ticket_text`, `expected_code`, `predicted_code`, `confidence`, `latency_ms`.

## Running the Stress Test

```bash
# Ensure LM Studio is running with Qwen 2.5
# Install dependencies if needed
pip install pandas

# Run the test
python llm_stress_test_class.py
```

The script will print a summary:

```
Total tickets: 200
Correct predictions: 186 (93%)
Average latency: 45 ms
```

Open the CSV file to drill down into misclassifications.

## Interpreting Results

| Metric | What it Means |
|--------|---------------|
| **Accuracy** | Percentage of tickets where `predicted_code == expected_code`. |
| **Confidence** | Average confidence score for correct predictions. |
| **Latency** | Time taken per inference; useful for scaling decisions. |
| **Error Analysis** | Look at rows where the model failed; check if the ticket was ambiguous or had typos. |

## Extending the Test

- **Add More Tickets** – Append to the `test_cases.json` file.  
- **Run on Gemma** – Copy the script to `gemma_stress_test_class.py` and change the `MODEL_NAME`.  
- **Parallel Execution** – Use `concurrent.futures` to run multiple inferences concurrently for throughput testing.

## Next Steps

- Compare the Qwen results with the **Gemma 4 E4B** stress test (see `stress-testing.md`).  
- Use the findings to refine prompts or add new keyword rules.  
- Integrate the test into a CI pipeline to catch regressions when updating the model.

*Keep your models robust and your tickets accurate!*