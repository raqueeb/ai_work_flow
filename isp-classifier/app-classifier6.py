import streamlit as st
import requests
import re

# Configuration
LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"

st.set_page_config(page_title="Link3 CTO Dashboard", page_icon="🎫", layout="wide")

# --- UPDATED KNOWLEDGE BASE (ISP-001 to ISP-050) ---
# Field dispatch trigger codes — physical/outside plant issues only
FIELD_ISP_CODES = ["ISP-015", "ISP-023", "ISP-035", "ISP-047"]

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
ISP-021: Port forwarding fail -> CGNAT Restriction [L3, Med]
ISP-022: Frequent Wi-Fi drops -> DHCP Lease Conflict [L4, Med]
ISP-023: Broken drop cable -> Physical Cable Damage [L2, High]
ISP-024: Slow speed on LAN -> Faulty Ethernet/Cat5 limitation [L4, Med]
ISP-025: Zoom/Teams lag -> Jitter/Upstream Congestion [L3, Med]
ISP-026: Bill overcharge -> Billing CRM Discrepancy [L1, Low]
ISP-027: Router overheating -> CPU Overload/Poor Ventilation [L4, Med]
ISP-028: High Latency (Global) -> Submarine Cable Fault [L3, High]
ISP-029: 5GHz SSID missing -> DFS Channel Interference [L4, Low]
ISP-030: Auto-pay failed -> Payment Gateway Timeout [L1, Med]
ISP-031: Lightning surge -> WAN Port Burnout [L2, High]
ISP-032: CCTV remote fail -> Public IP Misconfiguration [L3, Med]
ISP-033: PPPoE Auth error -> Radius Server Timeout [L1, High]
ISP-034: Work VPN blocked -> GRE/IPSec Protocol Filter [L3, High]
ISP-035: Sparking wire -> Induction on Messenger Wire [L2, Critical]
ISP-036: Forgot Wi-Fi pass -> WPA2 Key Reset Required [L4, Low]
ISP-037: Smart TV buffering -> DNS Caching Issue [L4, Med]
ISP-038: Speed capped at 10Mbps -> Profile Shaper Error [L1, High]
ISP-039: Humming switch box -> Cooling Fan Failure [L2, Med]
ISP-040: Plan upgrade pending -> Provisioning Sync Lag [L1, Low]
ISP-041: Google works only -> IPv6/DNS Mismatch [L3, Med]
ISP-042: Bending fiber cord -> High Macro-bend Loss [L2, High]
ISP-043: Microwave interference -> 2.4GHz EMI Noise [L4, Low]
ISP-044: Duplicate invoice -> Billing ERP Error [L1, Low]
ISP-045: No power on ONT -> PSU/Adapter Dead [L4, Med]
ISP-046: Website redirection -> DNS Hijacking/Malware [L4, High]
ISP-047: Low signal (-30dBm) -> Splicing Joint Failure [L2, High]
ISP-048: Connection shifting -> Relocation Work Order [L1, Low]
ISP-049: No internet (All LEDs green) -> IP Pool Exhaustion [L3, High]
ISP-050: Batch firmware fail -> Bootloader Corruption [L4, High]
"""

# Initialize session state
if 'diagnosis' not in st.session_state:
    st.session_state.diagnosis = ""
if 'show_dispatch' not in st.session_state:
    st.session_state.show_dispatch = False

def reset_dashboard():
    st.session_state.diagnosis = ""
    st.session_state.show_dispatch = False

st.title("🎫 Link3 Support Ticket Classifier")
st.markdown("---")

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
        "max_tokens": 2048
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

                # --- FIELD DISPATCH LOGIC ---
                # Only L2 (physical/outside plant) issues require field operations.
                # L1 = Billing/Account (remote), L3 = Network/Routing (remote), L4 = CPE/Software (remote).
                is_field_issue = (
                    "L2" in raw_text.upper() or
                    any(code in raw_text for code in FIELD_ISP_CODES)
                )

                st.session_state.show_dispatch = is_field_issue

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
            if st.session_state.diagnosis:
                st.divider()
                st.success("✅ Remote Support — No Field Dispatch Needed")
    else:
        st.write("Results will appear here.")
