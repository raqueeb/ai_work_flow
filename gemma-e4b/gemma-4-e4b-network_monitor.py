"""
Network Monitoring & Reasoning Tool: Link3 AI

This script demonstrates how to combine classic network diagnostics
(ping, traceroute, DNS lookup) with LLM reasoning using the
Gemma 4 E4B model loaded in LM Studio.

It is intended as an educational example for students to see how
raw network data can be fed to an LLM for higher-level analysis,
suggestions, and explanations.
"""

import subprocess
import sys
import json
import platform
import socket
import dns.resolver
import requests
from typing import List, Dict, Any

# ----------------------------------------------------------------------
# Configuration – adjust if your LM Studio runs on a different host/port
# ----------------------------------------------------------------------
LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"
MODEL_NAME = "google/gemma-4-e4b"   # Must match the model loaded in LM Studio
TIMEOUT = 300                       # Seconds for HTTP requests
MAX_TOKENS = 500                   # Allow a richer response from the LLM
TEMPERATURE = 0.0                  # Deterministic output for reproducibility

# ----------------------------------------------------------------------
# Helper: run a shell command and capture its output
# ----------------------------------------------------------------------
def run_cmd(cmd: List[str]) -> str:
    """Execute a command and return stdout (stderr merged)."""
    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=15,
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Error executing {' '.join(cmd)}: {e}"

# ----------------------------------------------------------------------
# Diagnostics
# ----------------------------------------------------------------------
def ping(host: str, count: int = 4) -> str:
    """Perform a ping to the host."""
    param = "-n" if platform.system().lower() == "windows" else "-c"
    cmd = ["ping", param, str(count), host]
    return run_cmd(cmd)

def traceroute(host: str) -> str:
    """Run a traceroute (or tracert on Windows)."""
    if platform.system().lower() == "windows":
        cmd = ["tracert", host]
    else:
        cmd = ["traceroute", host]
    return run_cmd(cmd)

def dns_lookup(host: str) -> str:
    """Resolve A records for the host using dnspython."""
    try:
        answers = dns.resolver.resolve(host, "A")
        ips = [rdata.to_text() for rdata in answers]
        return f"A records for {host}: {', '.join(ips)}"
    except Exception as e:
        return f"DNS lookup failed for {host}: {e}"

# ----------------------------------------------------------------------
# LLM Interaction
# ----------------------------------------------------------------------
def ask_llm(system_prompt: str, user_prompt: str) -> str:
    """Send a request to LM Studio and return the assistant's reply."""
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS,
    }
    try:
        resp = requests.post(LM_STUDIO_URL, json=payload, timeout=TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        if "choices" in data and data["choices"]:
            return data["choices"][0]["message"]["content"].strip()
        return "LLM returned no content."
    except Exception as e:
        return f"Error contacting LLM: {e}"

# ----------------------------------------------------------------------
# Main demonstration
# ----------------------------------------------------------------------
def main():
    # Target for diagnostics
    target_host = "8.8.8.8"
    domain = "google.com"

    print("=" * 70)
    print(" NETWORK MONITORING & LLM REASONING DEMO")
    print("=" * 70)

    # 1. Ping
    print("\n[1] Running ping to", target_host)
    ping_result = ping(target_host, count=4)
    print(ping_result[:500])  # Truncate if too long

    # 2. Traceroute
    print("\n[2] Running traceroute to", target_host)
    trace_result = traceroute(target_host)
    print(trace_result[:500])

    # 3. DNS lookup
    print("\n[3] Running DNS lookup for", domain)
    dns_result = dns_lookup(domain)
    print(dns_result)

    # 4. Combine data and ask LLM to reason
    system_prompt = """You are a network diagnostics assistant.
Analyze the provided network diagnostic data (ping, traceroute, DNS).
Provide a concise summary of what the data indicates about network health,
possible issues, and suggestions for further investigation.
Be factual and avoid speculation beyond the data."""

    user_prompt = f"""Here are network diagnostic results for target {target_host} and domain {domain}:

PING:
{ping_result}

TRACEROUTE:
{trace_result}

DNS LOOKUP:
{dns_result}

Based on this data, what is your analysis?"""

    print("\n[4] Asking LLM to analyze the data...")
    analysis = ask_llm(system_prompt, user_prompt)
    print("\nLLM ANALYSIS:\n")
    print(analysis)

    print("\n" + "=" * 70)
    print(" DEMO COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    main()