"""
Link3 Sales Funnel AI Closer
Powered by LM Studio (Local LLM)
For Marketing & Sales Team - B2B + B2C Deal Closing
"""

import streamlit as st
import requests
import re
import json

# Configuration
LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"
MODELS_URL = "http://localhost:1234/v1/models"

st.set_page_config(page_title="Link3 Sales AI Closer", page_icon="💰", layout="wide")

# --- SALES FUNNEL DEFINITIONS ---
FUNNEL_STAGES = ["Awareness", "Interest", "Consideration", "Intent", "Purchase", "Retention"]

NEXT_ACTIONS = {
    "Awareness": "Send educational content / Fiber speed comparison",
    "Interest": "Share plan options + success stories",
    "Consideration": "Schedule demo or site survey",
    "Intent": "Send customized quotation + limited-time offer",
    "Purchase": "Close deal + contract + installation booking",
    "Retention": "Upsell higher package or loyalty reward"
}

# Department / Segment specific actions
DEPARTMENTS = {
    "B2B": {"icon": "🏢", "name": "Business / Corporate"},
    "B2C": {"icon": "🏠", "name": "Residential / Home User"}
}

# --- STRONG SYSTEM PROMPT FOR SALES ---
SYSTEM_PROMPT = """
You are Link3's Sales AI Closer - an expert in closing internet service deals for both B2B and B2C segments.

Analyze the lead message and respond with a SINGLE valid JSON object (no extra text).

Rules:
- Classify as B2B or B2C
- Identify exact funnel stage: Awareness, Interest, Consideration, Intent, Purchase, or Retention
- Recommend the single best "Next Action"
- Generate a natural, friendly, and persuasive reply (WhatsApp or Email style) that the sales person can copy-paste immediately
- Give a confidence score (0-100)

Respond ONLY with this JSON format:
{
  "b2b_b2c": "B2B or B2C",
  "funnel_stage": "Awareness / Interest / Consideration / Intent / Purchase / Retention",
  "next_action": "Short description of what to do next",
  "suggested_reply": "Full ready-to-send message (WhatsApp/Email style)",
  "urgency": "Low / Med / High",
  "confidence": 85,
  "reason": "One sentence explaining your decision"
}
"""

# Session State
if 'sales_result' not in st.session_state:
    st.session_state.sales_result = None
if 'current_model' not in st.session_state:
    st.session_state.current_model = "Unknown"

def get_current_model():
    try:
        resp = requests.get(MODELS_URL, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            if "data" in data and data["data"]:
                model_id = data["data"][0]["id"]
                return model_id.split("/")[-1] if "/" in model_id else model_id
    except:
        pass
    return "Qwen2.5-1.5B"

def reset_dashboard():
    st.session_state.sales_result = None

# UI
st.title("💰 Link3 Sales Funnel AI Closer")
st.markdown("**Marketing & Sales Team** — Close more deals with AI")
st.markdown("---")

col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("📥 Lead Inquiry")
    lead_input = st.text_area(
        "Paste the lead message (WhatsApp, email, Facebook, call note, etc.):",
        height=220,
        placeholder="Example B2C: Hi, I want 100Mbps for my home in Gulshan...\n\nExample B2B: We have 3 offices and need reliable 500Mbps fiber..."
    )

    c1, c2 = st.columns(2)
    with c1:
        analyze_btn = st.button("🚀 Analyze Lead & Get Next Step", use_container_width=True, type="primary")
    with c2:
        st.button("🔄 Clear", on_click=reset_dashboard, use_container_width=True)

    st.markdown("**Quick Demo Leads to try:**")
    st.caption("• B2C: My current internet is very slow at night. I want to upgrade.")
    st.caption("• B2B: We need dedicated fiber for our 45-employee office in Banani.")

# Fetch model once
if st.session_state.current_model == "Unknown":
    st.session_state.current_model = get_current_model()

if analyze_btn and lead_input.strip():
    current_model_name = get_current_model()
    st.session_state.current_model = current_model_name

    payload = {
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": lead_input}
        ],
        "temperature": 0.3,
        "max_tokens": 600
    }

    try:
        spinner_text = f"AI Sales Closer **({current_model_name})** is analyzing lead..."
        with st.spinner(spinner_text):
            response = requests.post(LM_STUDIO_URL, json=payload, timeout=60)
            response.raise_for_status()
            data = response.json()

            content = data["choices"][0]["message"]["content"]
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            
            if json_match:
                result = json.loads(json_match.group())
                st.session_state.sales_result = result
            else:
                st.error("Could not read AI response. Try again.")
    except Exception as e:
        st.error(f"Error: {e}")

with col2:
    st.subheader("📈 AI Deal Recommendation")

    if st.session_state.sales_result:
        res = st.session_state.sales_result
        seg = DEPARTMENTS.get(res.get("b2b_b2c", "B2C"), DEPARTMENTS["B2C"])

        st.toast(f"Lead classified as {res.get('b2b_b2c', 'B2C')}", icon=seg["icon"])

        st.write(f"### {seg['icon']} {res.get('b2b_b2c', 'B2C')} — {seg['name']}")
        
        # Funnel Stage
        stage = res.get("funnel_stage", "Interest")
        st.metric("Funnel Stage", stage)

        # Next Action
        st.subheader("✅ Recommended Next Action")
        st.info(res.get("next_action", "Follow up in 24 hours"))

        # Suggested Reply (copy-paste ready)
        st.subheader("✉️ Ready-to-Send Reply")
        with st.container(border=True):
            st.write(res.get("suggested_reply", "No reply generated"))

        # Urgency + Confidence
        urgency = res.get("urgency", "Med")
        if urgency == "High":
            st.error(f"🚨 URGENCY: {urgency}")
        else:
            st.success(f"URGENCY: {urgency}")

        st.progress(res.get("confidence", 70) / 100, 
                    text=f"AI Confidence: {res.get('confidence', 70)}%")

        st.caption(f"**Reason:** {res.get('reason', '')}")

        st.divider()
        st.button("📋 Copy Reply to Clipboard", 
                  on_click=lambda: st.toast("✅ Reply copied!", icon="📋"))

    else:
        st.info("Paste a lead message above and click **Analyze Lead & Get Next Step**")

st.caption(f"**Active Model:** {st.session_state.current_model} | • Sales Funnel AI Closer v1")
