"""
Link3 AI Autonomous Dispatcher - Production Upgrade (Full Script)
Handles truncated JSON, network failures, and provides rule-based fallback.
"""

import streamlit as st
import requests
import json
import re
import time
import logging
from typing import Dict, Optional, Tuple, Any
from dataclasses import dataclass
from datetime import datetime

# ------------------------------
# Configuration
# ------------------------------
@dataclass
class AppConfig:
    lm_studio_url: str = "http://localhost:1234/v1/chat/completions"
    model_name: str = "local-model"
    timeout_sec: int = 60
    max_retries: int = 2
    retry_backoff_factor: float = 1.5
    temperature: float = 0.1          # Lower for stricter JSON output
    max_tokens: int = 400              # Increased to avoid truncation
    confidence_threshold: int = 70

config = AppConfig()

# ------------------------------
# Logging
# ------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Link3Dispatcher")

# ------------------------------
# Department Mapping
# ------------------------------
DEPARTMENTS = {
    "Field Support": {"icon": "🛠️", "color": "orange", "desc": "Physical repair, Fiber cuts, ONT replacement"},
    "NOC/Routing": {"icon": "🌐", "color": "blue", "desc": "Latency, BGP, DNS, Peering issues"},
    "Billing": {"icon": "💳", "color": "green", "desc": "Payments, Refunds, Suspensions"},
    "Sales": {"icon": "💰", "color": "purple", "desc": "New connections, Plan upgrades"},
    "Marketing": {"icon": "📣", "color": "red", "desc": "Brand feedback, Promotions, Social sentiment"},
    "Supply Chain": {"icon": "📦", "color": "grey", "desc": "Router stock, ONU inventory, Logistics"}
}

# ------------------------------
# Enhanced System Prompt (explicit JSON requirement)
# ------------------------------
SYSTEM_PROMPT = """
You are the Link3 Autonomous Dispatcher. Analyze the customer complaint and route it.

DEPARTMENTS & RULES:
- Field Support: physical damage, red lights, splicing, fiber cuts, low signal power (-25dBm or lower)
- NOC/Routing: high ping, buffering, DNS, BGP, latency
- Billing: money, double charges, suspension
- Sales: new packages, connections, upgrades
- Marketing: brand feedback, social sentiment
- Supply Chain: hardware failure (PSU dead, box humming)

STRICT: signal values like '-25db' or '-30db' → Field Support, NOT NOC.

Respond ONLY in the exact JSON format below. Include the closing brace. No extra text, no markdown.

{
  "dept": "Department Name",
  "reason": "Short logic for this choice",
  "urgency": "Low|Med|High|Critical",
  "confidence": 0-100
}
"""

# ------------------------------
# Rule-Based Fallback
# ------------------------------
def rule_based_router(text: str) -> Dict[str, Any]:
    text_lower = text.lower()
    if any(kw in text_lower for kw in ["fiber cut", "red light", "splicing", "signal -", "dbm"]):
        return {"dept": "Field Support", "reason": "Physical infrastructure keyword", "urgency": "High", "confidence": 85}
    if any(kw in text_lower for kw in ["charge", "bill", "payment", "refund", "suspended"]):
        return {"dept": "Billing", "reason": "Financial keyword", "urgency": "Med", "confidence": 90}
    if any(kw in text_lower for kw in ["ping", "latency", "buffer", "dns", "slow internet"]):
        return {"dept": "NOC/Routing", "reason": "Network performance keyword", "urgency": "Med", "confidence": 80}
    if any(kw in text_lower for kw in ["upgrade", "new connection", "plan", "package"]):
        return {"dept": "Sales", "reason": "Sales intent", "urgency": "Low", "confidence": 85}
    if any(kw in text_lower for kw in ["ad", "facebook", "promotion", "brand"]):
        return {"dept": "Marketing", "reason": "Marketing feedback", "urgency": "Low", "confidence": 75}
    if any(kw in text_lower for kw in ["router dead", "ont broken", "power supply"]):
        return {"dept": "Supply Chain", "reason": "Hardware failure", "urgency": "Med", "confidence": 80}
    return {"dept": "NOC/Routing", "reason": "Default fallback", "urgency": "Med", "confidence": 60}

# ------------------------------
# Robust JSON Extraction (repairs truncation)
# ------------------------------
def extract_json_from_text(text: str) -> Optional[Dict]:
    """Extract JSON, auto-repair missing braces or quotes from truncated output."""
    # Remove markdown code fences
    text = re.sub(r'```json\s*|```', '', text)
    # Find first '{' and last '}'
    start = text.find('{')
    end = text.rfind('}')
    
    if start == -1:
        return None
    
    # If no closing brace, add one
    if end == -1 or end <= start:
        json_str = text[start:] + '}'
    else:
        json_str = text[start:end+1]
    
    # Fix common truncation issues
    # 1. Remove trailing comma before a likely missing field
    json_str = re.sub(r',\s*}', '}', json_str)
    # 2. Add missing closing quote on last string value if needed
    if json_str.rstrip().endswith('"') is False:
        last_colon = json_str.rfind(':')
        if last_colon != -1:
            # Assume the value after colon is unquoted or truncated
            json_str = json_str[:last_colon+1] + '"' + json_str[last_colon+1:].strip() + '"'
    
    # Try to parse
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        return None

# ------------------------------
# LLM Router with Retry
# ------------------------------
def call_llm_router(user_input: str) -> Tuple[Optional[Dict], Optional[str]]:
    """Call LM Studio with retries. Returns (result_dict, error_message)."""
    payload = {
        "model": config.model_name,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ],
        "temperature": config.temperature,
        "max_tokens": config.max_tokens,
        "stream": False
    }
    
    for attempt in range(config.max_retries):
        try:
            response = requests.post(
                config.lm_studio_url,
                json=payload,
                timeout=config.timeout_sec
            )
            if response.status_code == 200:
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                logger.info(f"LLM raw response (attempt {attempt+1}): {content[:300]}")
                parsed = extract_json_from_text(content)
                if parsed and all(k in parsed for k in ("dept", "reason", "urgency", "confidence")):
                    return parsed, None
                else:
                    logger.warning("LLM returned incomplete or invalid JSON")
                    return None, "Incomplete JSON from LLM"
            else:
                logger.warning(f"HTTP {response.status_code}: {response.text}")
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
            logger.warning(f"Attempt {attempt+1} failed: {e}")
            if attempt < config.max_retries - 1:
                time.sleep(config.retry_backoff_factor ** attempt)
            else:
                return None, f"Connection error after {config.max_retries} attempts: {e}"
    return None, "Max retries exceeded"

# ------------------------------
# Main Streamlit App
# ------------------------------
def main():
    st.set_page_config(page_title="Link3 AI Orchestrator Pro", page_icon="🧠", layout="wide")
    st.title("🎫 Link3 Autonomous Service Orchestrator (Upgraded)")
    st.markdown("---")
    
    # Session state
    if 'history' not in st.session_state:
        st.session_state.history = []
    if 'current_result' not in st.session_state:
        st.session_state.current_result = None
    if 'debug_logs' not in st.session_state:
        st.session_state.debug_logs = []
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        use_fallback = st.checkbox("Enable rule-based fallback", value=True)
        st.session_state.model_url = st.text_input("LM Studio URL", value=config.lm_studio_url)
        st.session_state.confidence_threshold = st.slider("Confidence threshold (%)", 0, 100, config.confidence_threshold)
        st.divider()
        st.header("📊 Session Stats")
        st.metric("Tickets routed", len(st.session_state.history))
        if st.button("🧹 Clear History"):
            st.session_state.history = []
            st.session_state.current_result = None
            st.rerun()
        st.divider()
        st.header("📋 Debug Panel")
        if st.button("Show Debug Logs"):
            st.json(st.session_state.debug_logs[-10:])
    
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.subheader("📥 Customer Input")
        ticket_input = st.text_area("Live Complaint Stream:", height=200,
                                   placeholder="e.g. My fiber is disconnected near the electric pole...")
        
        col_a, col_b = st.columns(2)
        with col_a:
            analyze_btn = st.button("🚀 Dispatch Ticket", use_container_width=True, type="primary")
        with col_b:
            st.button("🔄 Clear Current", on_click=lambda: st.session_state.update(current_result=None), use_container_width=True)
        
        st.markdown("**📌 Try these examples:**")
        examples = [
            "My fiber is disconnected near the electric pole.",
            "Why was I charged twice this month?",
            "The latency in gaming is too high tonight.",
            "I saw your ad on facebook, I want to take Link3."
        ]
        for ex in examples:
            if st.button(f"📋 {ex[:50]}...", key=ex):
                ticket_input = ex
                st.rerun()
    
    if analyze_btn and ticket_input.strip():
        # Update config from sidebar
        config.lm_studio_url = st.session_state.model_url
        config.confidence_threshold = st.session_state.confidence_threshold
        
        with st.spinner("AI is routing..."):
            result, error = call_llm_router(ticket_input)
            
            # Fallback if LLM fails
            if (result is None or error) and use_fallback:
                st.warning(f"LLM issue: {error or 'No valid JSON'}. Using rule-based engine.")
                result = rule_based_router(ticket_input)
                st.session_state.debug_logs.append({
                    "timestamp": datetime.now().isoformat(),
                    "event": "fallback_used",
                    "input": ticket_input[:100]
                })
            
            if result:
                # Validate department name
                if result["dept"] not in DEPARTMENTS:
                    result["dept"] = "NOC/Routing"
                    result["reason"] += " (corrected to existing department)"
                
                st.session_state.current_result = result
                st.session_state.history.append({
                    "timestamp": datetime.now().isoformat(),
                    "input": ticket_input,
                    "result": result
                })
                st.success(f"✅ Routed to {result['dept']} with {result['confidence']}% confidence")
            else:
                st.error(f"Routing failed: {error if error else 'Unknown error'}")
                st.session_state.debug_logs.append({
                    "timestamp": datetime.now().isoformat(),
                    "event": "routing_failed",
                    "error": error
                })
    
    with col2:
        st.subheader("📡 Dispatcher Output")
        
        if st.session_state.current_result:
            res = st.session_state.current_result
            dept_name = res.get("dept", "NOC/Routing")
            dept_info = DEPARTMENTS.get(dept_name, DEPARTMENTS["NOC/Routing"])
            
            st.toast(f"Ticket routed to {dept_name}", icon=dept_info["icon"])
            
            st.markdown(f"### {dept_info['icon']} {dept_name}")
            urgency = res.get("urgency", "Med").upper()
            if urgency in ["HIGH", "CRITICAL"]:
                st.error(f"🚨 URGENCY: {urgency}")
            else:
                st.info(f"⏱️ URGENCY: {urgency}")
            
            with st.container(border=True):
                st.write(f"**🤖 AI Reasoning:** {res.get('reason')}")
                conf = res.get("confidence", 0)
                st.progress(conf / 100, text=f"Match Confidence: {conf}%")
                if conf < config.confidence_threshold:
                    st.warning("⚠️ Low confidence – manual review recommended")
            
            st.divider()
            st.subheader(f"✅ Next Steps for {dept_name}")
            if dept_name == "Field Support":
                st.warning("🛠️ Action: Generate ticket for local splicing team")
                st.button("📡 Notify Field Supervisor")
            elif dept_name == "Billing":
                st.success("💳 Action: Fetch ledger from ERP for comparison")
                st.button("💰 Open Billing Portal")
            elif dept_name == "Sales":
                st.balloons()
                st.success("📈 Action: Forward to Lead Management System")
                st.button("📞 Assign to Sales Agent")
            else:
                st.write(f"Status: Ticket held in {dept_name} queue.")
            
            # Export button
            col_exp1, _ = st.columns([1, 4])
            with col_exp1:
                if st.button("📥 Export as JSON"):
                    st.download_button(
                        label="Download",
                        data=json.dumps(res, indent=2),
                        file_name=f"routing_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
        else:
            st.info("👈 Enter a customer complaint and click 'Dispatch Ticket' to see AI routing in action.")
    
    # Show recent history
    if st.session_state.history:
        with st.expander("📜 Recent Routing History"):
            for entry in st.session_state.history[-5:]:
                st.write(f"**{entry['timestamp'][:19]}** → {entry['result']['dept']} ({entry['result']['confidence']}%)")
                st.caption(f"Input: {entry['input'][:100]}...")

if __name__ == "__main__":
    main()