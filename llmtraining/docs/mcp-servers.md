# MCP Servers

MCP (Model‑Control‑Protocol) servers provide a lightweight way to expose local LLM functionality as a REST API that other internal tools can call. In the Link3 ecosystem we use MCP servers to centralize model access, enforce security policies, and simplify version management.

## Why Use an MCP Server?

- **Single Point of Access** – All scripts (Streamlit apps, batch jobs, CI pipelines) talk to the same endpoint (`http://localhost:1234/v1`).  
- **Access Control** – You can add token‑based authentication or IP whitelisting to restrict who can query the model.  
- **Model Swapping** – Switch from Qwen to Gemma by changing the server configuration, without touching downstream code.  
- **Scalability** – Run multiple MCP instances on different ports to serve different teams or environments.

## Setting Up an MCP Server

1. **Install the MCP package** (if not already bundled with LM Studio):

   ```bash
   pip install mcp-server
   ```

2. **Create a config file** (`mcp_config.yaml`) in the project root:

   ```yaml
   model:
     name: qwen2.5-coder-1.5b-instruct   # or gemma-4b-instruct
     endpoint: http://localhost:1234/v1
   auth:
     token: YOUR_SECRET_TOKEN            # optional, for simple token auth
   ```

3. **Start the server**:

   ```bash
   mcp-server --config mcp_config.yaml
   ```

   The server will load the specified model via LM Studio and expose the OpenAI‑compatible `/v1/chat/completions` endpoint.

## Using the MCP Server from a Script

```python
import requests
import json

API_URL = "http://localhost:1234/v1/chat/completions"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer YOUR_SECRET_TOKEN"   # if auth enabled
}

def ask_llm(system_prompt, user_prompt):
    payload = {
        "model": "local-llm",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.0,
        "max_tokens": 200
    }
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

# Example usage
if __name__ == "__main__":
    system = "You are an ISP support assistant."
    user = "Customer reports a red light on the ONT."
    print(ask_llm(system, user))
```

## Deploying MCP in Production

- **Dockerize** – Create a Dockerfile that installs LM Studio, the MCP package, and copies `mcp_config.yaml`.  
- **Reverse Proxy** – Put Nginx in front of the MCP server to handle TLS termination and rate limiting.  
- **Monitoring** – Export Prometheus metrics from the MCP server (use `--metrics-port` flag) to track request latency and error rates.

## Switching Models

To move from Qwen to Gemma, simply edit `mcp_config.yaml`:

```yaml
model:
  name: gemma-4b-instruct
  endpoint: http://localhost:1234/v1
```

Restart the server and all downstream applications will automatically start using the new model.

## Security Considerations

- Keep the MCP port bound to `127.0.0.1` unless you explicitly need remote access.  
- Use strong tokens or mutual TLS for any external access.  
- Regularly audit the logs (`mcp_server.log`) for unexpected usage patterns.

## Next Steps

- Add the MCP server to your CI/CD pipeline to spin up a fresh instance for each test run.  
- Explore the **Model Comparison** page to see how Qwen and Gemma perform on the same tasks when accessed via MCP.

*The MCP server turns a local LLM into a reusable service for the whole organization.*