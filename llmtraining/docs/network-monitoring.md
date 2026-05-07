# Network Monitoring

Monitoring ISP network health is a classic use‑case for local LLMs. By feeding ping, traceroute, and DNS lookup results into a model, you can get human‑readable diagnostics and suggested remediation steps.

## What the Demo Does

- Runs a **ping** to a target host.  
- Performs a **traceroute** to map the path between the ISP node and the destination.  
- Executes a **DNS lookup** to verify name resolution.  
- Sends the raw output to the LLM, which summarizes the health of the connection and suggests next actions.

## Why Use an LLM for Monitoring?

- **Contextual Summaries** – Instead of reading raw ping statistics, the model tells you “high latency, possible congestion”.  
- **Root‑Cause Suggestions** – The LLM can recommend checking specific routers, ISP peering points, or DNS servers.  
- **Privacy‑First** – All network data stays on your machine; no external API calls are needed.

## Running the Demo

```bash
# Install dependencies if you haven’t already
pip install streamlit requests

# Run the script (Python version)
python gemma-4-e4b-network_monitor.py
```

Or launch the interactive Streamlit UI:

```bash
streamlit run gemma-4-e4b-network_monitor.py
```

Open `http://localhost:8501` and enter a hostname or IP address. The app will display:

1. **Ping Summary** – Packet loss, average latency, jitter.  
2. **Traceroute Path** – List of hops with latency per hop.  
3. **DNS Result** – Resolved IP addresses.  
4. **LLM Analysis** – A short paragraph explaining the overall health and any recommended actions (e.g., “Consider contacting upstream provider for hop 5 latency spikes”).

## Example Output

**Input:** `example.com`

**LLM Summary:**  
> The ping shows 0% packet loss but an average latency of 120 ms, which is higher than typical for a local ISP. The traceroute reveals a latency spike at hop 5 (≈ 250 ms), indicating a possible congestion point in the upstream network. DNS resolution succeeded with IP 93.184.216.34. Recommendation: Open a ticket with the upstream provider to investigate hop 5, and monitor latency over the next 24 hours.

## Extending the Demo

- **Add More Metrics** – Include `mtr` output or BGP route status.  
- **Custom Prompts** – Ask the model to generate a markdown report that can be emailed to the network team.  
- **Switch Models** – Change `MODEL_NAME` in `model_use_class.py` to use Qwen for faster but less detailed analysis.

## Next Steps

- Pair this monitoring tool with the **Cybersecurity Analysis** demo to get a combined view of performance and security alerts.  
- Use the **Advanced Reasoning** page to see how chain‑of‑thought prompts can break down complex network incidents step‑by‑step.

*Keep your network healthy, keep the data local.*