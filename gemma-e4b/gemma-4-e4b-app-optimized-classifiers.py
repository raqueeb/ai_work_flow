import streamlit as st
import requests
import re

# Configuration Link3 AI
LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"
MODEL_NAME = "google/gemma-4-e4b"  # Gemma 4 E4B model - matching LM Studio


st.set_page_config(page_title="Link3 CTO Dashboard", page_icon="🎫", layout="wide")

# Field dispatch trigger codes — physical/outside plant issues only
FIELD_ISP_CODES = ["ISP-015", "ISP-023", "ISP-035", "ISP-047"]

# --- KNOWLEDGE BASE ---
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

def parse_knowledge_base(kb_str):
    kb_dict = {}
    kb_codes = []
    for line in kb_str.strip().splitlines():
        line = line.strip()
        if not line or not line.startswith("ISP-"):
            continue
        match = re.match(r'(ISP-\d+):\s*(.+?)\s*->\s*(.+?)\s*\[(.+?)\]', line)
        if match:
            code = match.group(1)
            kb_dict[code] = {
                "category": match.group(2).strip(),
                "diagnosis": match.group(3).strip(),
                "urgency": match.group(4).strip()
            }
            kb_codes.append(code)
    return kb_dict, kb_codes

KB_DICT, KB_CODES = parse_knowledge_base(LINK3_KB)

# =====================================================================
# HYBRID CLASSIFIER: Keyword rules (deterministic) + LLM (semantic)
# =====================================================================
KEYWORD_RULES = [
    # (list of keywords, ISP code, priority)
    # Highest priority: explicit codes or very specific terms
    (["red light", "red led", "pon red", "los red"], "ISP-001", 100),
    (["los light", "los blinking", "los flashing"], "ISP-011", 100),
    (["sparking", "sparks", "induction", "messenger wire"], "ISP-035", 100),
    (["broken cable", "cut cable", "damaged cable", "drop cable", "cable cut", "cable is broken"], "ISP-023", 100),
    (["bending fiber", "bend fiber", "macro-bend"], "ISP-042", 100),
    (["lightning", "thunder", "surge"], "ISP-031", 100),
    ("-30", "ISP-047", 95),
    ("-31", "ISP-047", 95),
    ("-32", "ISP-047", 95),
    ("-33", "ISP-047", 95),
    ("-34", "ISP-047", 95),
    ("-35", "ISP-047", 95),
    ("-36", "ISP-047", 95),
    ("-37", "ISP-047", 95),
    ("-38", "ISP-047", 95),
    ("-39", "ISP-047", 95),
    ("-40", "ISP-047", 95),
    ("-25", "ISP-015", 95),
    ("-26", "ISP-015", 95),
    ("-27", "ISP-015", 95),
    ("-28", "ISP-015", 95),
    ("-29", "ISP-015", 95),
    (["rain", "raining", "wet", "moisture", "water", "damp"], "ISP-006", 95),
    (["netflix buffer", "netflix slow", "netflix lag", "netflix"], "ISP-002", 95),
    (["smart tv buffer", "tv buffer", "tv slow", "television buffer", "tv buffering", "tv buffers", "buffering on tv", "buffering", "tv is buffering"], "ISP-037", 95),
    (["youtube slow", "facebook slow", "fb slow"], "ISP-004", 90),
    (["wifi weak", "signal weak", "room signal", "attenuation", "weak signal", "weak wifi", "wifi is weak", "signal is weak"], "ISP-005", 90),
    (["gaming ping", "game lag", "high ping"], "ISP-007", 90),
    (["dns error", "dns issue", "dns problem"], "ISP-008", 90),
    (["router reboot", "router restart", "router keeps turning", "router keeps rebooting"], "ISP-009", 90),
    (["paid but", "paid inactive", "auto-pay", "autopay", "paid bill"], "ISP-010", 90),
    (["cannot login", "can't login", "cant login", "login fail"], "ISP-014", 90),
    (["slow 2.4", "2.4ghz slow", "2.4 ghz"], "ISP-012", 90),
    (["site unreachable", "website down"], "ISP-013", 90),
    (["partial browse", "some site work", "some page load"], "ISP-016", 90),
    (["static ip", "fixed ip"], "ISP-017", 90),
    (["ont power off", "ont dead", "ont no power"], "ISP-018", 90),
    (["torrent", "p2p", "peer to peer"], "ISP-019", 90),
    (["voip drop", "sip", "voice drop", "call drop"], "ISP-020", 90),
    (["port forward", "portforward"], "ISP-021", 90),
    (["wifi drop", "frequent disconnect", "dhcp conflict"], "ISP-022", 90),
    (["lan slow", "ethernet slow", "cat5"], "ISP-024", 90),
    (["zoom lag", "teams lag", "meeting lag", "jitter"], "ISP-025", 90),
    (["bill overcharge", "billing wrong", "charged extra"], "ISP-026", 90),
    (["router overheat", "hot router"], "ISP-027", 90),
    (["high latency global", "submarine cable", "international slow"], "ISP-028", 90),
    (["5ghz missing", "5g ssid gone", "dfs channel"], "ISP-029", 90),
    (["auto-pay fail", "payment fail", "gateway timeout"], "ISP-030", 90),
    (["cctv remote", "camera remote", "public ip"], "ISP-032", 90),
    (["pppoe", "radius", "auth error", "authentication"], "ISP-033", 90),
    (["vpn block", "vpn not work", "gre", "ipsec"], "ISP-034", 90),
    (["forgot wifi", "wifi password", "wpa2 reset", "wifi pass"], "ISP-036", 90),
    (["speed cap", "capped at 10", "10mbps", "10 mbps"], "ISP-038", 90),
    (["humming", "buzzing switch", "fan noise", "cooling fan"], "ISP-039", 90),
    (["plan upgrade", "upgrade pending", "provision"], "ISP-040", 90),
    (["google work only", "only google", "ipv6 mismatch"], "ISP-041", 90),
    (["microwave", "em interference", "emi noise"], "ISP-043", 90),
    (["duplicate invoice", "double bill", "same invoice"], "ISP-044", 90),
    (["ont no power", "ont dead", "psu dead", "adapter dead"], "ISP-045", 90),
    (["website redirect", "redirect malware", "dns hijack"], "ISP-046", 90),
    (["all led green", "led green no net", "ip pool"], "ISP-049", 90),
    (["firmware fail", "bootloader", "batch firmware"], "ISP-050", 90),
    (["subscription expire", "account suspend", "expire"], "ISP-003", 90),
    (["connection shift", "relocation", "moving connection"], "ISP-048", 90),
]


def keyword_classify(text: str) -> tuple[str, int]:
    """
    Returns (isp_code, priority) or (None, 0) if no keyword matches.
    Higher priority wins. For same priority, first match wins.
    """
    text_lower = text.lower()
    best_code = None
    best_priority = 0
    for entry in KEYWORD_RULES:
        if len(entry) == 3:
            keywords, code, priority = entry
        else:
            continue
        if isinstance(keywords, str):
            keywords = [keywords]
        matched = any(kw in text_lower for kw in keywords)
        if matched and priority > best_priority:
            best_code = code
            best_priority = priority
    return best_code, best_priority


# Minimal system prompt for the 1.5B model — only covers remaining cases
SYSTEM_PROMPT_LLM = (
    "You are an ISP support ticket classifier.\n"
    "Match the customer complaint to exactly one ISP code.\n"
    "Use ONLY these codes and their meanings:\n\n"
    "ISP-001 Red light / Physical Fiber Cut\n"
    "ISP-002 Netflix buffering / Upstream Peering\n"
    "ISP-003 Subscription expired / Account Suspension\n"
    "ISP-004 YouTube or FB slow / Local Cache CDN Outage\n"
    "ISP-005 Room signal weak / Wi-Fi Attenuation\n"
    "ISP-006 Rain issues / Moisture in Fiber Closure\n"
    "ISP-007 Gaming high ping / Sub-optimal Routing\n"
    "ISP-008 DNS error / DNS Server Unreachable\n"
    "ISP-009 Router rebooting / Power Adapter Fault\n"
    "ISP-010 Paid but inactive / API Sync Failure\n"
    "ISP-011 LOS light blinking / OLT Port Shutdown\n"
    "ISP-012 Slow on 2.4GHz / Frequency Interference\n"
    "ISP-013 Site unreachable / IP Blacklisted BGP\n"
    "ISP-014 Cannot login / Default Credentials Reset\n"
    "ISP-015 -25dBm or lower / High Optical Loss Dirty Connector\n"
    "ISP-016 Partial browsing / MTU Size Mismatch\n"
    "ISP-017 Static IP fail / MAC Binding Issue\n"
    "ISP-018 ONT Power off / Internal Hardware Failure\n"
    "ISP-019 Torrent slow / P2P Throttling Policy\n"
    "ISP-020 VoIP dropping / SIP Alg Packet Loss\n"
    "ISP-021 Port forwarding fail / CGNAT Restriction\n"
    "ISP-022 Frequent Wi-Fi drops / DHCP Lease Conflict\n"
    "ISP-023 Broken drop cable / Physical Cable Damage\n"
    "ISP-024 Slow speed on LAN / Faulty Ethernet Cat5 limitation\n"
    "ISP-025 Zoom Teams lag / Jitter Upstream Congestion\n"
    "ISP-026 Bill overcharge / Billing CRM Discrepancy\n"
    "ISP-027 Router overheating / CPU Overload Poor Ventilation\n"
    "ISP-028 High Latency Global / Submarine Cable Fault\n"
    "ISP-029 5GHz SSID missing / DFS Channel Interference\n"
    "ISP-030 Auto-pay failed / Payment Gateway Timeout\n"
    "ISP-031 Lightning surge / WAN Port Burnout\n"
    "ISP-032 CCTV remote fail / Public IP Misconfiguration\n"
    "ISP-033 PPPoE Auth error / Radius Server Timeout\n"
    "ISP-034 Work VPN blocked / GRE IPSec Protocol Filter\n"
    "ISP-035 Sparking wire / Induction on Messenger Wire\n"
    "ISP-036 Forgot Wi-Fi pass / WPA2 Key Reset Required\n"
    "ISP-037 Smart TV buffering / DNS Caching Issue\n"
    "ISP-038 Speed capped at 10Mbps / Profile Shaper Error\n"
    "ISP-039 Humming switch box / Cooling Fan Failure\n"
    "ISP-040 Plan upgrade pending / Provisioning Sync Lag\n"
    "ISP-041 Google works only / IPv6 DNS Mismatch\n"
    "ISP-042 Bending fiber cord / High Macro-bend Loss\n"
    "ISP-043 Microwave interference / 2.4GHz EMI Noise\n"
    "ISP-044 Duplicate invoice / Billing ERP Error\n"
    "ISP-045 No power on ONT / PSU Adapter Dead\n"
    "ISP-046 Website redirection / DNS Hijacking Malware\n"
    "ISP-047 Low signal -30dBm / Splicing Joint Failure\n"
    "ISP-048 Connection shifting / Relocation Work Order\n"
    "ISP-049 No internet All LEDs green / IP Pool Exhaustion\n"
    "ISP-050 Batch firmware fail / Bootloader Corruption\n\n"
    "Respond with ONLY the ISP code. No explanation."
)


def llm_classify(complaint: str) -> str | None:
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT_LLM},
            {"role": "user", "content": complaint}
        ],
        "temperature": 0.0,
        "max_tokens": 10
    }
    try:
        response = requests.post(LM_STUDIO_URL, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        if "choices" in data and len(data["choices"]) > 0:
            raw = data["choices"][0]["message"]["content"].strip()
            # Extract first ISP-XXX pattern
            m = re.search(r'ISP-\d+', raw)
            if m and m.group(0) in KB_DICT:
                return m.group(0)
    except Exception:
        pass
    return None


def classify_ticket(complaint: str) -> tuple[str, str]:
    """
    Hybrid classification:
    1. Try LLM first (leverage Gemma 4 E4B reasoning capabilities)
    2. Fall back to keyword rules if LLM fails
    Returns (isp_code, source) where source is 'llm' or 'keyword'
    """
    # 1. LLM match (prioritize LLM reasoning)
    llm_code = llm_classify(complaint)
    if llm_code:
        return llm_code, "llm"

    # 2. Keyword match (fallback)
    kw_code, kw_priority = keyword_classify(complaint)
    if kw_code:
        return kw_code, "keyword"

    # 3. Ultimate fallback
    return "ISP-001", "fallback"


# --- Streamlit UI ---
if 'model_isp_code' not in st.session_state:
    st.session_state.model_isp_code = ""
if 'model_confidence' not in st.session_state:
    st.session_state.model_confidence = 0
if 'selected_isp_code' not in st.session_state:
    st.session_state.selected_isp_code = ""
if 'show_dispatch' not in st.session_state:
    st.session_state.show_dispatch = False
if 'classification_source' not in st.session_state:
    st.session_state.classification_source = ""


def reset_dashboard():
    st.session_state.model_isp_code = ""
    st.session_state.model_confidence = 0
    st.session_state.selected_isp_code = ""
    st.session_state.show_dispatch = False
    st.session_state.classification_source = ""


st.title("🎫 Link3 Support Ticket Classifier")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Input Ticket")
    ticket_input = st.text_area("Customer Complaint:", height=150,
                                placeholder="e.g. my onu is -30 db or smart tv is buffering")

    c1, c2 = st.columns(2)
    with c1:
        analyze_btn = st.button("🚀 Analyze Ticket", use_container_width=True)
    with c2:
        st.button("🔄 Reset Dashboard", on_click=reset_dashboard, use_container_width=True)

    # Manual Hardware Check for critical signal
    db_match = re.search(r'(-?\d+)\s*db', ticket_input.lower())
    if db_match and int(db_match.group(1)) <= -25:
        st.error(f"⚠️ CRITICAL SIGNAL ALERT: {db_match.group(1)}dBm detected. (Link3 Limit: -25dBm)")

if analyze_btn and ticket_input.strip():
    code, source = classify_ticket(ticket_input.strip())
    st.session_state.model_isp_code = code
    st.session_state.selected_isp_code = code
    st.session_state.classification_source = source

    # Confidence: keyword = 99, llm = 85, fallback = 50
    conf_map = {"keyword": 99, "llm": 85, "fallback": 50}
    st.session_state.model_confidence = conf_map.get(source, 50)

    data = KB_DICT[code]
    is_field_issue = (
        code in FIELD_ISP_CODES or
        "L2" in data["urgency"].upper() or
        "CRITICAL" in data["urgency"].upper()
    )
    st.session_state.show_dispatch = is_field_issue

with col2:
    st.subheader("Automated Diagnosis")

    if st.session_state.selected_isp_code and st.session_state.selected_isp_code in KB_DICT:
        src_label = st.session_state.classification_source.upper()
        st.markdown(
            f"**🤖 Model selected:** {st.session_state.model_isp_code} — "
            f"**{st.session_state.model_confidence}%** confidence ({src_label})"
        )

        selected_code = st.selectbox(
            "👤 Correct the ISP code if needed (from 1 of 50 cases):",
            options=KB_CODES,
            index=KB_CODES.index(st.session_state.selected_isp_code),
            format_func=lambda c: f"{c} — {KB_DICT[c]['category']}",
            key="isp_selector_key"
        )

        st.session_state.selected_isp_code = selected_code

        data = KB_DICT[selected_code]
        display_text = f"{data['category']}, {data['diagnosis']}, {data['urgency']}"
        st.info(display_text)

        is_field_issue = (
            selected_code in FIELD_ISP_CODES or
            "L2" in data["urgency"].upper() or
            "CRITICAL" in data["urgency"].upper()
        )
        st.session_state.show_dispatch = is_field_issue

        if st.session_state.show_dispatch:
            st.divider()
            st.error("🚨 Field Support Required")
            if st.button("🛠️ Dispatch Field Team", use_container_width=True):
                st.balloons()
                st.success(f"✅ DISPATCHED: Ticket sent to Field Technician (Code: {selected_code})")
        else:
            st.divider()
            st.success("✅ Remote Support — No Field Dispatch Needed")

    else:
        st.write("Analysis results will appear here after clicking **Analyze Ticket**.")

st.markdown("---")
st.caption("Link3 CTO Dashboard | Powered by Local Google Gemma 4 E4B via LM Studio | LLM-First Hybrid Classification")
