# Gemma 4 E4B Demos

The Gemma 4 E4B model provides richer reasoning and higher accuracy for complex ISP tickets. This page lists the Gemma‑specific demos that take advantage of the model's advanced capabilities.

## Demo List

| Demo | Description | How to Run |
|------|-------------|------------|
| `gemma-4-e4b-app-reasoning1.py` | Basic classification using Gemma with detailed reasoning. | `python gemma-4-e4b-app-reasoning1.py` |
| `gemma-4-e4b-app-reasoning2.py` | Chain‑of‑thought version with step‑by‑step explanations. | `python gemma-4-e4b-app-reasoning2.py` |
| `gemma-4-e4b-app-baseline-class.py` | Full Streamlit dashboard with confidence scoring and field dispatch. | `streamlit run gemma-4-e4b-app-baseline-class.py` |
| `gemma-4-e4b-app-classifier1.py` – `gemma-4-e4b-app-classifier9.py` | Progressive versions showing prompt engineering improvements. | `streamlit run gemma-4-e4b-app-classifierX.py` |
| `gemma-4-e4b-app-slm.py` | Service Level Management with SLA compliance checking. | `streamlit run gemma-4-e4b-app-slm.py` |
| `gemma-4-e4b-ERP_AI_Approval_Assistant.py` | ERP workflow with multi‑document processing. | `streamlit run gemma-4-e4b-ERP_AI_Approval_Assistant.py` |

## Running a Demo

1. **Start LM Studio** and load the **Gemma 4 E4B** model (see the [Upgrading to Gemma 4](upgrading-to-gemma.md) guide).  
2. Navigate to the `c:\Downloads\classifier-app` folder in your terminal.  
3. Run the command from the **Howto Run** column.

## What You'll See

The Gemma demos include all features of the Qwen demos plus:

- **Multi‑step reasoning display** – Watch the model break down complex tickets into logical components.  
- **Higher confidence scores** – Gemma typically produces confidence scores above 90% for clear cases.  
- **Better handling of ambiguous tickets** – The model asks clarifying questions when needed.  
- **Field dispatch automation** – Automatic escalation for critical issues (e.g., fiber cut, complete outage).

## Comparing Qwen vs. Gemma

| Feature | Qwen 2.5‑1.5B | Gemma 4 E4B |
|---------|---------------|-------------|
| Model size | 1.5 B parameters | ~4 B parameters |
| Reasoning depth | Single‑step | Multi‑step chain‑of‑thought |
| Speed | ~10 tokens/sec | ~5 tokens/sec |
| Accuracy on complex tickets | ~75% | ~92% |
| Memory usage | ~2 GB VRAM | ~6 GB VRAM |

## Next Steps

- Try the **ISP Classification** demos to see how both models handle specific ticket categories.  
- Explore **Advanced Reasoning** for tips on prompt engineering.  
- Compare performance side‑by‑side using the **Model Comparison** guide.