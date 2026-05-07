"""
Link3 ERP AI Approval Assistant
Local LLM + Human-in-the-loop (inspired by the article)
"""

import streamlit as st
import requests
import re
import json
from datetime import datetime

# Configuration
LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"
MODELS_URL = "http://localhost:1234/v1/models"

st.set_page_config(page_title="ERP AI Approver", page_icon="🤖", layout="wide")

# Your custom rules (edit these according to your office policy)
SYSTEM_PROMPT = """
You are an intelligent ERP Approval Assistant for our company.
You follow strict company rules for approvals.

Current Rules (follow exactly):
- Leave Approval: Auto-approve if balance >= requested days AND not during peak festival period (Eid, Puja, etc.). Escalate if >5 days or balance low.
- Purchase Order: Approve if amount <= 50,000 BDT. Escalate if >50,000 BDT or unusual vendor.
- HR Onboarding: Approve standard cases. Escalate if salary >80,000 or special position.
- General: Reject if policy violation. Always explain reason.

Analyze the pending request and respond ONLY with valid JSON:
{
  "decision": "Approve | Reject | Escalate to Human",
  "reason": "Short clear explanation in Bengali or English",
  "confidence": 0-100,
  "suggested_comment": "Comment to put in ERP (if approving)",
  "category": "Leave | Purchase Order | HR Onboarding | Other"
}
"""

# Session state
if 'ai_result' not in st.session_state:
    st.session_state.ai_result = None
if 'current_model' not in st.session_state:
    st.session_state.current_model = "Unknown"

def get_current_model():
    try:
        r = requests.get(MODELS_URL, timeout=5)
        if r.status_code == 200:
            data = r.json()
            if data.get("data"):
                return data["data"][0]["id"].split("/")[-1]
    except:
        pass
    return "Local LLM (1.5B or similar)"

st.title("🤖 ERP AI Approval Assistant")
st.markdown("**Local & Private** — No data leaves your laptop. Inspired by the article.")

col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("📥 Pending Approval Request")
    request_text = st.text_area(
        "Paste the full details from ERP (or type summary):",
        height=250,
        placeholder="Example:\nName: Rahim Khan\nType: Leave\nDays: 3\nBalance: 12 days\nReason: Personal\nPeriod: 20-22 April 2026"
    )

    c1, c2 = st.columns(2)
    with c1:
        analyze_btn = st.button("🚀 Let AI Decide", use_container_width=True, type="primary")
    with c2:
        if st.button("🔄 Clear", use_container_width=True):
            st.session_state.ai_result = None
            st.rerun()

with col2:
    st.subheader("📊 AI Decision")

    if analyze_btn and request_text.strip():
        current_model = get_current_model()
        st.session_state.current_model = current_model

        payload = {
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": request_text}
            ],
            "temperature": 0.1,
            "max_tokens": 400
        }

        try:
            with st.spinner(f"AI Approver ({current_model}) is thinking..."):
                resp = requests.post(LM_STUDIO_URL, json=payload, timeout=60)
                resp.raise_for_status()
                content = resp.json()["choices"][0]["message"]["content"]

                # Extract JSON
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group())
                    st.session_state.ai_result = result
                else:
                    st.error("Could not parse AI response. Try rephrasing the input.")
        except Exception as e:
            st.error(f"Error connecting to LM Studio: {e}")

    if st.session_state.ai_result:
        res = st.session_state.ai_result
        decision = res.get("decision", "Escalate")

        if decision == "Approve":
            st.success(f"✅ **{decision.upper()}**")
        elif decision == "Reject":
            st.error(f"❌ **{decision.upper()}**")
        else:
            st.warning(f"⏳ **{decision.upper()}**")

        st.metric("Confidence", f"{res.get('confidence', 0)}%")
        st.write(f"**Category:** {res.get('category', 'Other')}")
        st.write(f"**Reason:** {res.get('reason', '')}")

        if res.get("suggested_comment"):
            with st.expander("Suggested Comment for ERP", expanded=True):
                st.info(res["suggested_comment"])

        st.caption(f"Active Model: {st.session_state.current_model}")

# Footer tips
st.markdown("---")
st.markdown("""
**How to make it more powerful (like the article):**
1. Add your exact rules in the SYSTEM_PROMPT (leave thresholds, PO limits, etc.)
2. For real auto-approval: Integrate **Playwright** to login to ERP and click Approve button automatically (only for high-confidence cases).
3. Run this on an old laptop 24/7 with scheduled checks.

Want me to add the **Playwright automation version** next? 
It can read pending requests from ERP and act automatically (with your final confirmation).
""")

st.caption("Private • Local LLM • No internet required for decision making")