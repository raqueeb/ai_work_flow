"""
Hierarchical LLM Classification Demo for Students
Shows that a small 1.5B LLM CAN classify accurately when prompted smartly.

Problem: 50 codes at once confuses the small model.
Solution: Two-stage hierarchical reasoning (Category -> Specific Code)
"""
import requests
import re
import time

LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"
MODEL_NAME = "qwen2.5-coder-1.5b-instruct"

KB_CODES = [f"ISP-{i:03d}" for i in range(1, 51)]

# =====================================================================
# STAGE 1: Classify into broad category
# =====================================================================
STAGE1_PROMPT = (
    "You are an ISP support triage assistant.\n"
    "Classify the customer complaint into ONE broad category.\n"
    "Respond with ONLY the category name. No explanation.\n\n"
    "Categories:\n"
    "PHYSICAL_OUTDOOR = fiber cuts, red light, rain, moisture, cable damage, sparks, lightning, signal loss, bent fiber\n"
    "NETWORK_L3       = Netflix, YouTube, DNS, gaming, VPN, routing, latency, websites, peering, torrent\n"
    "ACCOUNT_L1       = billing, payment, subscription, plan upgrade, static IP, overcharge, invoice\n"
    "WIFI_HARDWARE_L4 = WiFi weak, router reboot, forgot password, 5GHz missing, overheating, ONT power, firmware\n"
)

# =====================================================================
# STAGE 2: Category-specific code lists (much smaller for 1.5B model)
# =====================================================================
STAGE2_PROMPTS = {
    "PHYSICAL_OUTDOOR": (
        "You are an ISP support classifier for PHYSICAL/OUTDOOR issues.\n"
        "Match the complaint to exactly one ISP code.\n"
        "Respond with ONLY the ISP code. No explanation.\n\n"
        "ISP-001 Red light / Physical Fiber Cut\n"
        "ISP-006 Rain issues / Moisture in Fiber Closure\n"
        "ISP-011 LOS light blinking / OLT Port Shutdown\n"
        "ISP-015 -25dBm or lower / High Optical Loss Dirty Connector\n"
        "ISP-023 Broken drop cable / Physical Cable Damage\n"
        "ISP-031 Lightning surge / WAN Port Burnout\n"
        "ISP-035 Sparking wire / Induction on Messenger Wire\n"
        "ISP-042 Bending fiber cord / High Macro-bend Loss\n"
        "ISP-047 Low signal -30dBm / Splicing Joint Failure"
    ),
    "NETWORK_L3": (
        "You are an ISP support classifier for NETWORK/L3 issues.\n"
        "Match the complaint to exactly one ISP code.\n"
        "Respond with ONLY the ISP code. No explanation.\n\n"
        "ISP-002 Netflix buffering / Upstream Peering\n"
        "ISP-004 YouTube or FB slow / Local Cache CDN Outage\n"
        "ISP-007 Gaming high ping / Sub-optimal Routing\n"
        "ISP-008 DNS error / DNS Server Unreachable\n"
        "ISP-013 Site unreachable / IP Blacklisted BGP\n"
        "ISP-016 Partial browsing / MTU Size Mismatch\n"
        "ISP-019 Torrent slow / P2P Throttling Policy\n"
        "ISP-020 VoIP dropping / SIP Alg Packet Loss\n"
        "ISP-021 Port forwarding fail / CGNAT Restriction\n"
        "ISP-025 Zoom Teams lag / Jitter Upstream Congestion\n"
        "ISP-028 High Latency Global / Submarine Cable Fault\n"
        "ISP-032 CCTV remote fail / Public IP Misconfiguration\n"
        "ISP-033 PPPoE Auth error / Radius Server Timeout\n"
        "ISP-034 Work VPN blocked / GRE IPSec Protocol Filter\n"
        "ISP-041 Google works only / IPv6 DNS Mismatch\n"
        "ISP-049 No internet All LEDs green / IP Pool Exhaustion"
    ),
    "ACCOUNT_L1": (
        "You are an ISP support classifier for ACCOUNT/BILLING issues.\n"
        "Match the complaint to exactly one ISP code.\n"
        "Respond with ONLY the ISP code. No explanation.\n\n"
        "ISP-003 Subscription expired / Account Suspension\n"
        "ISP-010 Paid but inactive / API Sync Failure\n"
        "ISP-017 Static IP fail / MAC Binding Issue\n"
        "ISP-026 Bill overcharge / Billing CRM Discrepancy\n"
        "ISP-030 Auto-pay failed / Payment Gateway Timeout\n"
        "ISP-038 Speed capped at 10Mbps / Profile Shaper Error\n"
        "ISP-040 Plan upgrade pending / Provisioning Sync Lag\n"
        "ISP-044 Duplicate invoice / Billing ERP Error"
    ),
    "WIFI_HARDWARE_L4": (
        "You are an ISP support classifier for WIFI/HARDWARE issues.\n"
        "Match the complaint to exactly one ISP code.\n"
        "Respond with ONLY the ISP code. No explanation.\n\n"
        "ISP-005 Room signal weak / Wi-Fi Attenuation\n"
        "ISP-009 Router rebooting / Power Adapter Fault\n"
        "ISP-012 Slow on 2.4GHz / Frequency Interference\n"
        "ISP-014 Cannot login / Default Credentials Reset\n"
        "ISP-018 ONT Power off / Internal Hardware Failure\n"
        "ISP-022 Frequent Wi-Fi drops / DHCP Lease Conflict\n"
        "ISP-024 Slow speed on LAN / Faulty Ethernet Cat5 limitation\n"
        "ISP-027 Router overheating / CPU Overload Poor Ventilation\n"
        "ISP-029 5GHz SSID missing / DFS Channel Interference\n"
        "ISP-036 Forgot Wi-Fi pass / WPA2 Key Reset Required\n"
        "ISP-037 Smart TV buffering / DNS Caching Issue\n"
        "ISP-039 Humming switch box / Cooling Fan Failure\n"
        "ISP-043 Microwave interference / 2.4GHz EMI Noise\n"
        "ISP-045 No power on ONT / PSU Adapter Dead\n"
        "ISP-046 Website redirection / DNS Hijacking Malware\n"
        "ISP-048 Connection shifting / Relocation Work Order\n"
        "ISP-050 Batch firmware fail / Bootloader Corruption"
    ),
}


def llm_query(system_prompt, user_msg, max_tokens=10):
    """Single LLM call."""
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_msg}
        ],
        "temperature": 0.0,
        "max_tokens": max_tokens
    }
    try:
        response = requests.post(LM_STUDIO_URL, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        if "choices" in data and len(data["choices"]) > 0:
            raw = data["choices"][0]["message"]["content"].strip()
            return raw, data["usage"]["total_tokens"]
    except Exception as e:
        return f"ERROR: {e}", 0
    return "INVALID", 0


def classify_hierarchical(complaint):
    """
    Two-stage classification:
    1. LLM picks broad category
    2. LLM picks specific code from that category's shortlist
    """
    # Stage 1: Category
    category_raw, tokens1 = llm_query(STAGE1_PROMPT, complaint)
    category = category_raw.strip().upper()

    # Map loose responses to known categories
    category_map = {
        "PHYSICAL_OUTDOOR": "PHYSICAL_OUTDOOR",
        "NETWORK_L3": "NETWORK_L3",
        "ACCOUNT_L1": "ACCOUNT_L1",
        "WIFI_HARDWARE_L4": "WIFI_HARDWARE_L4",
        "PHYSICAL": "PHYSICAL_OUTDOOR",
        "OUTDOOR": "PHYSICAL_OUTDOOR",
        "NETWORK": "NETWORK_L3",
        "ACCOUNT": "ACCOUNT_L1",
        "BILLING": "ACCOUNT_L1",
        "WIFI": "WIFI_HARDWARE_L4",
        "HARDWARE": "WIFI_HARDWARE_L4",
    }

    matched_category = None
    for key, val in category_map.items():
        if key in category:
            matched_category = val
            break

    if not matched_category or matched_category not in STAGE2_PROMPTS:
        # Fallback: try all codes
        stage2_prompt = "\n\n".join(STAGE2_PROMPTS.values())
    else:
        stage2_prompt = STAGE2_PROMPTS[matched_category]

    # Stage 2: Specific code
    code_raw, tokens2 = llm_query(stage2_prompt, complaint)
    m = re.search(r'ISP-\d+', code_raw)
    if m and m.group(0) in KB_CODES:
        return m.group(0), matched_category or "UNKNOWN", tokens1 + tokens2
    return "INVALID", matched_category or "UNKNOWN", tokens1 + tokens2


# All 55 test cases
TEST_CASES = [
    ("my onu has a red light", "ISP-001"),
    ("pon led is red", "ISP-001"),
    ("it rained last night and now internet is gone", "ISP-006"),
    ("water got into the fiber box", "ISP-006"),
    ("signal is reading -32 dBm", "ISP-047"),
    ("my optical power is -28 dbm", "ISP-015"),
    ("the drop wire is snapped", "ISP-023"),
    ("cable outside is damaged", "ISP-023"),
    ("there are sparks coming from the pole wire", "ISP-035"),
    ("messenger wire has induction", "ISP-035"),
    ("los light keeps blinking", "ISP-011"),
    ("fiber cord is bent too much", "ISP-042"),
    ("lightning hit and wan port is dead", "ISP-031"),
    ("netflix keeps buffering every evening", "ISP-002"),
    ("youtube videos load very slowly", "ISP-004"),
    ("facebook is not loading fast", "ISP-004"),
    ("my game ping is 300ms", "ISP-007"),
    ("dns not resolving", "ISP-008"),
    ("some websites open others dont", "ISP-016"),
    ("cant reach certain sites", "ISP-013"),
    ("google works but nothing else", "ISP-041"),
    ("zoom calls freeze and lag", "ISP-025"),
    ("teams meeting has high jitter", "ISP-025"),
    ("voip calls keep dropping", "ISP-020"),
    ("vpn connection blocked", "ISP-034"),
    ("international sites very slow", "ISP-028"),
    ("cctv app cannot connect remotely", "ISP-032"),
    ("pppoe authentication fails", "ISP-033"),
    ("torrent speed is 5kbps", "ISP-019"),
    ("port forwarding not working for my camera", "ISP-021"),
    ("all leds are green but no internet", "ISP-049"),
    ("subscription expired yesterday", "ISP-003"),
    ("paid the bill but service still down", "ISP-010"),
    ("billed twice this month", "ISP-044"),
    ("auto-pay failed on card", "ISP-030"),
    ("plan upgrade not reflected", "ISP-040"),
    ("speed is locked at 10mbps", "ISP-038"),
    ("static ip stopped working", "ISP-017"),
    ("bill amount is wrong", "ISP-026"),
    ("wifi signal is weak in bedroom", "ISP-005"),
    ("router keeps restarting itself", "ISP-009"),
    ("cannot login to router admin", "ISP-014"),
    ("forgot my wifi password", "ISP-036"),
    ("5ghz network disappeared", "ISP-029"),
    ("2.4ghz band is very slow", "ISP-012"),
    ("frequent wifi disconnections", "ISP-022"),
    ("router is getting very hot", "ISP-027"),
    ("ont has no power at all", "ISP-045"),
    ("switch box is making humming noise", "ISP-039"),
    ("lan cable speed is slow", "ISP-024"),
    ("smart tv buffers on all apps", "ISP-037"),
    ("microwave kills wifi", "ISP-043"),
    ("website redirects to spam", "ISP-046"),
    ("need to shift connection to new address", "ISP-048"),
    ("firmware update failed on multiple devices", "ISP-050"),
]


if __name__ == "__main__":
    print("=" * 90)
    print("  HIERARCHICAL LLM CLASSIFICATION DEMO")
    print("  Model: Qwen2.5-1.5B")
    print("  Strategy: Stage 1 (Category) -> Stage 2 (Specific Code)")
    print("  Why: Small LLMs struggle with 50 choices at once.")
    print("       Breaking into 2 stages with smaller lists makes it accurate!")
    print("=" * 90)

    correct = 0
    total_tokens = 0
    total_time = 0

    for idx, (complaint, expected) in enumerate(TEST_CASES, 1):
        start = time.time()
        predicted, category, tokens = classify_hierarchical(complaint)
        elapsed = time.time() - start

        total_tokens += tokens
        total_time += elapsed

        ok = predicted == expected
        if ok:
            correct += 1
        status = "PASS" if ok else "FAIL"

        print(f"[{idx:02d}/{len(TEST_CASES)}] {status} | [{category:18s}] '{complaint[:40]:40s}' -> {predicted} (exp: {expected}) [{elapsed*1000:.0f}ms]")

    accuracy = 100 * correct / len(TEST_CASES)
    avg_time = total_time / len(TEST_CASES)
    avg_tokens = total_tokens / len(TEST_CASES)

    print("\n" + "=" * 90)
    print("  FINAL RESULTS")
    print("=" * 90)
    print(f"  Correct:      {correct}/{len(TEST_CASES)}")
    print(f"  Accuracy:     {accuracy:.1f}%")
    print(f"  Total Time:   {total_time:.1f}s")
    print(f"  Avg/Query:    {avg_time*1000:.0f}ms")
    print(f"  Total Tokens: {total_tokens}")
    print(f"  Avg Tokens:   {avg_tokens:.0f}")
    print("=" * 90)
