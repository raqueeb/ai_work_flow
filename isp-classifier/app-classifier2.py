import streamlit as st
import requests
import re

# Configuration
LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"

st.set_page_config(page_title="Link3 CTO Dashboard", page_icon="🎫", layout="wide")

# --- EXPANDED KNOWLEDGE BASE (ISP-001 to ISP-020) ---
# Derived from provided PDF and common ISP scenarios
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
ISP-012: Slow speed on 2.4GHz -> Frequency Interference [L4, Low]
ISP-013: Site unreachable (403/404) -> IP Blacklisted/BGP [L3, Med]
ISP-014: Cannot login to Router -> Default Credentials Reset [L4, Low]
ISP-015: Frequent disconnection -> Dirty Patch Cord/Connector [L2, High]
ISP-016: Partial browsing -> MTU Size Mismatch [L3, Med]
ISP-017: Static IP not working -> MAC Binding Issue [L1, High]
ISP-018: ONT Power light off -> Internal Hardware Failure [L4, High]
ISP-019: Torrent speed slow -> P2P Throttling/Policy [L3, Low]
ISP-020: Voice/VoIP dropping -> SIP Alg/Packet Loss [L3, Med]
"""

# --- SESSION STATE INITIALIZATION ---
if 'diagnosis' not in st.session_state:
    st.session_state.diagnosis = ""
if 'show_dispatch' not in st.session_state:
    st.session_state.show_dispatch = False

def reset_dashboard():
    st.session_state.diagnosis = ""
    st.session_state.show_dispatch = False
    st.rerun()

# --- UI LAYOUT ---
st.title("🎫 Link3 Support Ticket Classifier")
st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Input Ticket")
    ticket_input = st.text_area("Customer Complaint:", height=150, placeholder="e.g. My internet stops working when it rains...")
    
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        analyze_btn = st.button("🚀 Analyze Ticket", use_container_width=True)
    with btn_col2:
        st.button("🔄 Reset Dashboard", on_click=reset_dashboard, use_container_width=True)

# --- LOGIC ---
if analyze_btn:
    if not ticket_input.strip():
        st.warning("Please enter a ticket description.")
    else:
        # Check for dBm status manually for speed
        db_match = re.search(r'(-?\d+)\s*db', ticket_input.lower())
        if db_match and int(db_match.group(1)) <= -25:
            st.error(f"⚠️ CRITICAL: Signal is {db_match.group(1)}dBm. Immediate Physical Layer failure detected.")

        payload = {
            "messages": [
                {"role": "system", "content": f"Use this Link3 Knowledge Base:\n{LINK3_KB}\nClassify and respond in format: ID, CATEGORY, DIAGNOSIS, URGENCY."},
                {"role": "user", "content": ticket_input}
            ],
            "temperature": 0.1,
            "max_tokens": 200
        }

        try:
            with st.spinner('Gemma 4B is classifying...'):
                response = requests.post(LM_STUDIO_URL, json=payload, timeout=90)
                data = response.json()
                
                # Robust list-index check
                if "choices" in data and len(data["choices"]) > 0:
                    raw_content = data["choices"][0]["message"]["content"]
                    st.session_state.diagnosis = raw_content
                    # Trigger dispatch button for Physical (L2) or Hardware (L4)
                    if any(kw in raw_content.upper() for kw in ["L2", "L4", "PHYSICAL", "FIBER", "ROUTER"]):
                        st.session_state.show_dispatch = True
                else:
                    st.error("Server Error: Check if model is loaded in LM Studio.")
        except Exception as e:
            st.error(f"Connection Failed: {e}")

with col2:
    st.subheader("Automated Diagnosis")
    if st.session_state.diagnosis:
        st.info(st.session_state.diagnosis)
        
        if st.session_state.show_dispatch:
            st.warning("🚨 This issue requires on-site attention.")
            if st.button("🛠️ Dispatch Field Support Team"):
                st.balloons()
                st.success("SUCCESS: Ticket assigned to the nearest Link3 Field Technician.")
    else:
        st.write("Results will appear here after analysis.")
