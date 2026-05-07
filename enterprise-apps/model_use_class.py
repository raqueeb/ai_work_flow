"""
The AI is trained to read between the lines of customer complaints, 
identify the underlying issue, and route it to the correct department 
with a confidence score. This allows Link3 to provide lightning-fast 
resolutions and personalized service at scale.
"""

import streamlit as st
import requests
import re
import json

# Configuration
LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"
MODELS_URL = "http://localhost:1234/v1/models"   # New endpoint to fetch current model

st.set_page_config(page_title="Link3 AI Orchestrator", page_icon="🧠", layout="wide")

# --- DEPARTMENT MAPPING ---
DEPARTMENTS = {
    "Field Support": {"icon": "🛠️", "color": "orange", "desc": "Physical repair, Fiber cuts, ONT replacement"},
    "NOC/Routing": {"icon": "🌐", "color": "blue", "desc": "Latency, BGP, DNS, Peering issues"},
    "Billing": {"icon": "💳", "color": "green", "desc": "Payments, Refunds, Suspensions"},
    "Sales": {"icon": "💰", "color": "purple", "desc": "New connections, Plan upgrades"},
    "Marketing": {"icon": "📣", "color": "red", "desc": "Brand feedback, Promotions, Social sentiment"},
    "Supply Chain": {"icon": "📦", "color": "grey", "desc": "Router stock, ONU inventory, Logistics"}
}

# --- ENHANCED SYSTEM PROMPT ---
SYSTEM_PROMPT = """
You are the Link3 Autonomous Dispatcher. Analyze the customer complaint and route it.
Your response must be a single JSON object.

DEPARTMENTS & OPERATIONAL RULES:
- Field Support: Use this for physical damage, red lights, wifi onu red signal, splicing, fiber cuts, or low signal power (-25dBm or lower, e.g., -30dBm).
- NOC/Routing: Use this for logical network issues, high ping, buffering, DNS, or BGP.
- Billing: Issues about money, double charges, or account suspension.
- Sales: Inquiries about new packages, connections, Link3 connections or upgrades.
- Marketing: Brand feedback or general sentiment.
- Supply Chain: Equipment hardware failure (PSU dead, box humming).

STRICT RULE: If you see signal values like '-25db', '-30db', or '-28db', you MUST route to Field Support, NOT NOC.

Respond ONLY in this format (valid JSON, no extra text):
{
  "dept": "Department Name",
  "reason": "Short logic for this choice",
  "urgency": "Low/Med/High/Critical",
  "confidence": 0-100
}
"""

# Initialize session state
if 'ai_result' not in st.session_state:
    st.session_state.ai_result = None
if 'current_model' not in st.session_state:
    st.session_state.current_model = "Unknown Model"

def get_current_model():
    """Fetch the currently loaded model from LM Studio"""
    try:
        resp = requests.get(MODELS_URL, timeout=5)
        if resp.status_code == 200:
            models_data = resp.json()
            if "data" in models_data and len(models_data["data"]) > 0:
                # Take the first loaded model (usually the active one)
                model_id = models_data["data"][0]["id"]
                # Clean up common long names for display
                display_name = model_id.split("/")[-1] if "/" in model_id else model_id
                return display_name
    except:
        pass
    return "Qwen2.5-1.5B"  # Fallback

def reset_dashboard():
    st.session_state.ai_result = None

st.title("🎫 Link3 Autonomous Service Orchestrator")
st.markdown("---")

col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("📥 Customer Input")
    ticket_input = st.text_area("Live Complaint Stream:", height=200, 
                               placeholder="e.g. I want to upgrade to the 100Mbps plan...")

    c1, c2 = st.columns(2)
    with c1:
        analyze_btn = st.button("🚀 Dispatch Ticket", use_container_width=True)
    with c2:
        st.button("🔄 Clear System", on_click=reset_dashboard, use_container_width=True)

    st.markdown("""
    **Demo Scenarios to try:**
    1. *'My fiber is disconnected near the electric pole.'* (Field Support)
    2. *'Why was I charged twice this month?'* (Billing)
    3. *'The latency in gaming is too high tonight.'* (NOC)
    4. *'I saw your ad in facebook, I want to take Link3.'* (Sales)
    """)

# Fetch model name once at startup / on refresh
if st.session_state.current_model == "Unknown Model":
    st.session_state.current_model = get_current_model()

if analyze_btn and ticket_input.strip():
    # Get fresh model name before calling
    current_model_name = get_current_model()
    st.session_state.current_model = current_model_name

    payload = {
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": ticket_input}
        ],
        "temperature": 0.2,
        "max_tokens": 250
    }

    try:
        spinner_text = f"AI Model **({current_model_name})** is routing..."
        with st.spinner(spinner_text):
            response = requests.post(LM_STUDIO_URL, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if "choices" in data and len(data["choices"]) > 0:
                content = data["choices"][0]["message"]["content"]
                # Extract JSON safely
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    json_str = json_match.group()
                    st.session_state.ai_result = json.loads(json_str)
                else:
                    st.error("Could not parse JSON from model response.")
            else:
                st.error("Model Error: Ensure LLM is loaded in LM Studio.")
    except Exception as e:
        st.error(f"Routing Error: {e}")

with col2:
    st.subheader("📡 Autonomous Dispatcher Output")
    
    if st.session_state.ai_result:
        res = st.session_state.ai_result
        dept_name = res.get("dept", "NOC/Routing")
        dept_info = DEPARTMENTS.get(dept_name, DEPARTMENTS["NOC/Routing"])
        
        st.toast(f"Ticket Routed to {dept_name}")
        
        st.write(f"### {dept_info['icon']} {dept_name}")
        
        urgency = res.get("urgency", "Med").upper()
        if urgency in ["HIGH", "CRITICAL"]:
            st.error(f"URGENCY: {urgency}")
        else:
            st.info(f"URGENCY: {urgency}")

        with st.container(border=True):
            st.write(f"**AI Reasoning:** {res.get('reason', 'No reasoning provided')}")
            st.progress(res.get("confidence", 0) / 100, 
                        text=f"Match Confidence: {res.get('confidence', 0)}%")

        st.divider()
        st.subheader(f"Next Steps for {dept_name}")
        
        if dept_name == "Field Support":
            st.warning("⚠️ Action: Generating Ticket for Local Splicing Team.")
            st.button("🛠️ Notify Field Supervisor")
        elif dept_name == "Billing":
            st.success("✅ Action: Fetching Ledger from ERP for comparison.")
            st.button("💳 Open Billing Portal")
        elif dept_name == "Sales":
            st.balloons()
            st.success("💰 Action: Forwarding to Lead Management System.")
            st.button("📞 Assign to Sales Agent")
        else:
            st.write(f"Status: Ticket held in {dept_name} queue.")
            
    else:
        st.info("Awaiting input to initiate autonomous routing.")

st.caption(f"**Active Model:** {st.session_state.current_model}")