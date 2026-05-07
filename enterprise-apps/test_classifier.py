import requests
import re

LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"
MODEL_NAME = "qwen2.5-coder-1.5b-instruct"

KEYWORD_RULES = [
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

KB_CODES = [f"ISP-{i:03d}" for i in range(1, 51)]

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


def keyword_classify(text):
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


def llm_classify(complaint):
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
            m = re.search(r'ISP-\d+', raw)
            if m and m.group(0) in KB_CODES:
                return m.group(0)
    except Exception:
        pass
    return None


def classify_ticket(complaint):
    kw_code, _ = keyword_classify(complaint)
    if kw_code:
        return kw_code, "keyword"
    llm_code = llm_classify(complaint)
    if llm_code:
        return llm_code, "llm"
    return "ISP-001", "fallback"


TEST_CASES = [
    ("my tv is buffering when watching youtube", "ISP-037"),
    ("red light on my onu", "ISP-001"),
    ("its raining and internet keeps dropping", "ISP-006"),
    ("signal is -30 dbm", "ISP-047"),
    ("signal is -26 dbm", "ISP-015"),
    ("my drop cable is broken", "ISP-023"),
    ("wire is sparking outside", "ISP-035"),
    ("netflix keeps buffering", "ISP-002"),
    ("wifi signal is weak in my room", "ISP-005"),
    ("cannot login to router", "ISP-014"),
    ("paid bill but still inactive", "ISP-010"),
    ("router keeps rebooting", "ISP-009"),
    ("speed is capped at 10mbps", "ISP-038"),
    ("torrent download is very slow", "ISP-019"),
    ("customer says there is red light on the ONT", "ISP-001"),
    ("my smart tv buffers a lot", "ISP-037"),
    ("rain outside and net is down", "ISP-006"),
]

print("=" * 70)
print("TESTING KEYWORD CLASSIFIER ONLY")
print("=" * 70)
kw_correct = 0
for complaint, expected in TEST_CASES:
    code, _ = keyword_classify(complaint)
    ok = code == expected
    if ok:
        kw_correct += 1
    print(f"{'OK' if ok else 'FAIL'} | '{complaint}' -> {code} (expected: {expected})")
print(f"\nKeyword Accuracy: {kw_correct}/{len(TEST_CASES)} = {100*kw_correct/len(TEST_CASES):.1f}%")

print("\n" + "=" * 70)
print("TESTING FULL CLASSIFIER (Keyword + LLM fallback)")
print("=" * 70)
full_correct = 0
for complaint, expected in TEST_CASES:
    code, src = classify_ticket(complaint)
    ok = code == expected
    if ok:
        full_correct += 1
    print(f"{'OK' if ok else 'FAIL'} [{src}] | '{complaint}' -> {code} (expected: {expected})")
print(f"\nFull Accuracy: {full_correct}/{len(TEST_CASES)} = {100*full_correct/len(TEST_CASES):.1f}%")
