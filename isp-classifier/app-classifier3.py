## gemma 4, 20 cases, 2k tokens, 0.1 temp, 120s timeout, reasoning_content, updated KB with 20 cases (ISP-001 to ISP-020)

import streamlit as st
import requests
import re

# Configuration
LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"

st.set_page_config(page_title="Link3 CTO Dashboard", page_icon="🎫", layout="wide")

# --- UPDATED KNOWLEDGE BASE (ISP-001 to ISP-020) ---
LINK3_KB = """
ISP-001: Red light -> Physical Fiber Cut [L2, High]
ISP-002: Netflix buffering -> Upstream/Peering Issue [L3, Med]
ISP-003: Subscription expired -> Account Suspension [L1, Med]
ISP-004: YouTube/FB slow -> Local Cache/CDN Outage [L3, Med]
ISP-005: Room signal weak -> Wi-Fi Attenuation [L4, Low]
ISP-006: Rain issues -> Moisture in Fiber Closure [L2, High]
ISP-007: Gaming high ping -> Sub-optimal Routing [L3, Med]
ISP-008: DNS error -> DNS Server Unreachable [L3, High]
ISP-009: Router rebooting -> Power Adapter Fault [L4, Med]
ISP-010: Paid but inactive -> API Sync Failure [L1, High]
ISP-011: LOS light blinking -> OLT Port Shutdown [L2, High]
ISP-012: Slow on 2.4GHz -> Frequency Interference [L4, Low]
ISP-013: Site unreachable -> IP Blacklisted/BGP [L3, Med]
ISP-014: Cannot login -> Default Credentials Reset [L4, Low]
ISP-015: -25dBm or lower -> High Optical Loss/Dirty Connector [L2, High]
ISP-016: Partial browsing -> MTU Size Mismatch [L3, Med]
ISP-017: Static IP fail -> MAC Binding Issue [L1, High]
ISP-018: ONT Power off -> Internal Hardware Failure [L4, High]
ISP-019: Torrent slow -> P2P Throttling Policy [L3, Low]
ISP-020: VoIP dropping -> SIP Alg/Packet Loss [L3, Med]
"""

# Initialize session state
if 'diagnosis' not in st.session_state:
    st.session_state.diagnosis = ""
if 'show_dispatch' not in st.session_state:
    st.session_state.show_dispatch = False

def reset_dashboard():
    st.session_state.diagnosis = ""
    st.session_state.show_dispatch = False
    # No rerun needed here as button will trigger it

st.title("🎫 Link3 Support Ticket Classifier")
st.markdown("---")

# FIXED: Added the required argument '2' to st.columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("Input Ticket")
    ticket_input = st.text_area("Customer Complaint:", height=150, placeholder="e.g. my onu is -30 db")
    
    c1, c2 = st.columns(2)
    with c1:
        analyze_btn = st.button("🚀 Analyze Ticket", use_container_width=True)
    with c2:
        st.button("🔄 Reset Dashboard", on_click=reset_dashboard, use_container_width=True)

    # Manual Hardware Check
    db_match = re.search(r'(-?\d+)\s*db', ticket_input.lower())
    if db_match and int(db_match.group(1)) <= -25:
        st.error(f"⚠️ CRITICAL SIGNAL ALERT: {db_match.group(1)}dBm detected. (Link3 Limit: -25dBm)")

if analyze_btn and ticket_input.strip():
    payload = {
        "messages": [
            {"role": "system", "content": f"Knowledge Base:\n{LINK3_KB}\nTask: Classify ticket. Respond ONLY in format: ID, CATEGORY, DIAGNOSIS, URGENCY."},
            {"role": "user", "content": ticket_input}
        ],
        "temperature": 0.1,
        "max_tokens": 1024 # High enough for Gemma's thinking tokens
    }

    try:
        with st.spinner('Gemma [google/gemma-4-e4b] is processing...'):
            response = requests.post(LM_STUDIO_URL, json=payload, timeout=120)
            data = response.json()
            
            if "choices" in data:
                msg = data["choices"][0]["message"]
                # Catcher for both standard content and reasoning content
                raw_text = msg.get("content") or msg.get("reasoning_content") or "No output generated."
                st.session_state.diagnosis = raw_text
                
                # Logic to trigger dispatch button
                if any(kw in raw_text.upper() for kw in ["L2", "L4", "PHYSICAL", "HARDWARE", "ISP-015"]):
                    st.session_state.show_dispatch = True
            else:
                st.error("Model Error: Ensure Gemma is active in LM Studio.")
    except Exception as e:
        st.error(f"Connection Failed: {e}")

with col2:
    st.subheader("Automated Diagnosis")
    if st.session_state.diagnosis:
        # Display the result (cleans up thinking tags if present)
        st.info(st.session_state.diagnosis.replace("<thought>", "").replace("</thought>", ""))
        
        if st.session_state.show_dispatch:
            st.divider()
            st.error("🚨 Field Support Required")
            if st.button("🛠️ Dispatch Field Team"):
                st.balloons()
                st.success("✅ DISPATCHED: Ticket sent to Field Technician.")
    else:
        st.write("Results will appear here.")
