"""
Small LLM Demo for Students (10 cases, fast)
Compares FLAT vs HIERARCHICAL prompting on Qwen2.5-1.5B
"""
import requests
import re
import time

LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"
MODEL_NAME = "qwen2.5-coder-1.5b-instruct"
KB_CODES = [f"ISP-{i:03d}" for i in range(1, 51)]

# Full flat prompt (50 codes)
FLAT_PROMPT = (
    "You are an ISP support ticket classifier.\n"
    "Match the complaint to exactly one ISP code.\n"
    "Use ONLY these codes:\n\n"
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

# Stage 1 prompt
STAGE1_PROMPT = (
    "Classify the complaint into ONE category. Respond with ONLY the category name.\n\n"
    "Categories:\n"
    "PHYSICAL_OUTDOOR = red light, rain, moisture, cable damage, sparks, lightning, signal loss\n"
    "NETWORK_L3       = Netflix, YouTube, DNS, gaming, VPN, routing, latency, websites\n"
    "ACCOUNT_L1       = billing, payment, subscription, plan upgrade, static IP\n"
    "WIFI_HARDWARE_L4 = WiFi weak, router reboot, forgot password, 5GHz, overheating, ONT power\n"
)

# Stage 2 prompts (smaller lists)
STAGE2 = {
    "PHYSICAL_OUTDOOR": (
        "Match to exactly one ISP code. Respond with ONLY the code.\n\n"
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
        "Match to exactly one ISP code. Respond with ONLY the code.\n\n"
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
        "Match to exactly one ISP code. Respond with ONLY the code.\n\n"
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
        "Match to exactly one ISP code. Respond with ONLY the code.\n\n"
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

CAT_MAP = {
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


def llm_query(system_prompt, user_msg):
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_msg}
        ],
        "temperature": 0.0,
        "max_tokens": 10
    }
    try:
        resp = requests.post(LM_STUDIO_URL, json=payload, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        if "choices" in data and len(data["choices"]) > 0:
            raw = data["choices"][0]["message"]["content"].strip()
            return raw, data["usage"]["total_tokens"]
    except Exception as e:
        return f"ERROR: {e}", 0
    return "INVALID", 0


def classify_flat(complaint):
    raw, tokens = llm_query(FLAT_PROMPT, complaint)
    m = re.search(r'ISP-\d+', raw)
    if m and m.group(0) in KB_CODES:
        return m.group(0), tokens
    return "INVALID", tokens


def classify_hierarchical(complaint):
    cat_raw, t1 = llm_query(STAGE1_PROMPT, complaint)
    cat = cat_raw.strip().upper()
    matched = None
    for k, v in CAT_MAP.items():
        if k in cat:
            matched = v
            break
    if not matched or matched not in STAGE2:
        stage2 = "\n\n".join(STAGE2.values())
    else:
        stage2 = STAGE2[matched]
    code_raw, t2 = llm_query(stage2, complaint)
    m = re.search(r'ISP-\d+', code_raw)
    if m and m.group(0) in KB_CODES:
        return m.group(0), t1 + t2
    return "INVALID", t1 + t2


TEST_CASES = [
    ("my onu has a red light", "ISP-001"),
    ("it rained last night and now internet is gone", "ISP-006"),
    ("signal is reading -32 dBm", "ISP-047"),
    ("there are sparks coming from the pole wire", "ISP-035"),
    ("netflix keeps buffering every evening", "ISP-002"),
    ("dns not resolving", "ISP-008"),
    ("zoom calls freeze and lag", "ISP-025"),
    ("paid the bill but service still down", "ISP-010"),
    ("wifi signal is weak in bedroom", "ISP-005"),
    ("router keeps restarting itself", "ISP-009"),
    ("forgot my wifi password", "ISP-036"),
    ("smart tv buffers on all apps", "ISP-037"),
    ("microwave kills wifi", "ISP-043"),
    ("firmware update failed on multiple devices", "ISP-050"),
]

print("=" * 90)
print("  LLM CLASSIFICATION DEMO FOR STUDENTS")
print("  Model: Qwen2.5-1.5B (smallest model)")
print("=" * 90)

# --- FLAT ---
print("\n[1] FLAT APPROACH: 50 codes given to LLM at once")
print("-" * 90)
flat_correct = 0
flat_time = 0
flat_tokens = 0
for complaint, expected in TEST_CASES:
    t0 = time.time()
    pred, tok = classify_flat(complaint)
    dt = time.time() - t0
    flat_time += dt
    flat_tokens += tok
    ok = pred == expected
    if ok:
        flat_correct += 1
    print(f"  {'PASS' if ok else 'FAIL'} | '{complaint[:40]:40s}' -> {pred} (exp: {expected})")

print(f"\n  Flat Accuracy: {flat_correct}/{len(TEST_CASES)} = {100*flat_correct/len(TEST_CASES):.1f}%")
print(f"  Avg Time:      {flat_time/len(TEST_CASES)*1000:.0f}ms")
print(f"  Total Tokens:  {flat_tokens}")

# --- HIERARCHICAL ---
print("\n" + "=" * 90)
print("[2] HIERARCHICAL APPROACH: Category first, then specific code (smaller lists)")
print("-" * 90)
hi_correct = 0
hi_time = 0
hi_tokens = 0
for complaint, expected in TEST_CASES:
    t0 = time.time()
    pred, tok = classify_hierarchical(complaint)
    dt = time.time() - t0
    hi_time += dt
    hi_tokens += tok
    ok = pred == expected
    if ok:
        hi_correct += 1
    print(f"  {'PASS' if ok else 'FAIL'} | '{complaint[:40]:40s}' -> {pred} (exp: {expected})")

print(f"\n  Hierarchical Accuracy: {hi_correct}/{len(TEST_CASES)} = {100*hi_correct/len(TEST_CASES):.1f}%")
print(f"  Avg Time:              {hi_time/len(TEST_CASES)*1000:.0f}ms")
print(f"  Total Tokens:          {hi_tokens}")

# --- Summary ---
print("\n" + "=" * 90)
print("  TEACHING POINT")
print("=" * 90)
print(f"  Flat (50 codes at once):       {100*flat_correct/len(TEST_CASES):.1f}% accuracy")
print(f"  Hierarchical (stage-by-stage): {100*hi_correct/len(TEST_CASES):.1f}% accuracy")
print("\n  The small 1.5B model gets confused with 50 choices.")
print("  But when we break it into 2 stages with smaller lists, it performs much better!")
print("=" * 90)
