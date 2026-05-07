"""Cybersecurity Analysis with Gemma 4 E4B Reasoning
This script demonstrates how to use the Gemma 4 E4B model for local, private cybersecurity analysis.
It can process security logs, port scan results, or suspicious network activity and provide reasoning
about potential threats, risk levels, and remediation steps.
Intended for educational use to show students how LLM reasoning can be applied to cybersecurity tasks.
"""

import requests
import sys
import json
from typing import List, Dict, Any# ----------------------------------------------------------------------
# Configuration Link3 AI
# ----------------------------------------------------------------------
LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"
MODEL_NAME = "google/gemma-4-e4b"   # Must match LM Studio
TIMEOUT = 320                       # Seconds for HTTP requests
MAX_TOKENS = 800                   # Allow detailed analysis
TEMPERATURE = 0.0                  # Deterministic output

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
# Example security data
# ----------------------------------------------------------------------
def demo_port_scan():
    """Example: Analyze a port scan result."""
    scan_result = """ Port Scan Report for 192.168.1.100 (scan performed 2026-04-29)
Open ports:
22/tcp open ssh
23/tcp open telnet
80/tcp open http
443/tcp open https
3306/tcp open mysql
8080/tcp open http-proxy """
    system_prompt = """You are a cybersecurity analyst. Analyze the provided port scan data.
Identify potential security risks, explain why each open port might be a concern, and suggest remediation steps.
Be concise but thorough."""
    user_prompt = f"""Here is a port scan result:
{scan_result}
Provide a risk assessment and recommendations."""
    print("=" * 70)
    print(" CYBERSECURITY ANALYSIS: PORT SCAN")
    print("=" * 70)
    print("\nScan Data:\n", scan_result)
    print("\nAsking LLM to analyze...")
    analysis = ask_llm(system_prompt, user_prompt)
    print("\nLLM ANALYSIS:\n")
    print(analysis)

def demo_suspicious_log():
    """Example: Analyze a suspicious log entry."""
    log_entry = """ [2026-04-29 10:15:23] Failed password for invalid user 'admin' from 203.0.113.42 port 22 ssh2[2026-04-29 10:15:25] Failed password for invalid user 'root' from 203.0.113.42 port 22 ssh2[2026-04-29 10:15:27] Failed password for invalid user 'administrator' from 203.0.113.42 port 22 ssh2
[2026-04-29 10:15:30] Failed password for invalid user 'user' from 203.0.113.42 port 22 ssh2
[2026-04-29 10:15:35] Connection closed by 203.0.113.42 port 22
[2026-04-29 10:15:40] Invalid user 'test' from 203.0.113.42 port 22 """
    system_prompt = """You are a cybersecurity analyst. Analyze the provided authentication log entries.
Determine if this indicates a brute-force attack, explain the evidence, assess the threat level, and suggest immediate actions."""
    user_prompt = f"""Here are SSH log entries:
{log_entry}
What is your analysis?"""
    print("\n" + "=" * 70)
    print(" CYBERSECURITY ANALYSIS: SUSPICIOUS LOG")
    print("=" * 70)
    print("\nLog Data:\n", log_entry)
    print("\nAsking LLM to analyze...")
    analysis = ask_llm(system_prompt, user_prompt)
    print("\nLLM ANALYSIS:\n")
    print(analysis)

def demo_malware_traffic():
    """Example: Analyze a malware communication pattern."""
    traffic_desc = """ Observed network traffic:
- Multiple DNS queries for random-looking subdomains of 'evil.example.com' (e.g., 'a8f3.evil.example.com', '9c2d.evil.example.com')
- Responses are small, varying IP addresses
- Followed by HTTPS connections to those IPs on port 443
- Traffic occurs every 60 seconds, even when no user activity """
    system_prompt = """You are a cybersecurity analyst. Analyze the described network traffic pattern.
Determine if this matches known malware communication (e.g., botnet C2), explain the indicators, assess the severity, and recommend containment steps."""
    user_prompt = f"""Network traffic description:
{traffic_desc}
Provide your analysis."""
    print("\n" + "=" * 70)
    print(" CYBERSECURITY ANALYSIS: MALWARE TRAFFIC PATTERN")
    print("=" * 70)
    print("\nTraffic Description:\n", traffic_desc)
    print("\nAsking LLM to analyze...")
    analysis = ask_llm(system_prompt, user_prompt)
    print("\nLLM ANALYSIS:\n")
    print(analysis)

# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------
def main():
    print("\n" + "=" * 70)
    print(" CYBERSECURITY ANALYSIS WITH GEMMA 4 E4B REASONING")
    print("=" * 70)
    print("\nThis demo shows how local LLM reasoning can be applied to cybersecurity tasks.")
    print("All analysis is performed locally using the Gemma 4 E4B model via LM Studio.\n")
    demo_port_scan()
    demo_suspicious_log()
    demo_malware_traffic()
    print("\n" + "=" * 70)
    print(" DEMO COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    main()