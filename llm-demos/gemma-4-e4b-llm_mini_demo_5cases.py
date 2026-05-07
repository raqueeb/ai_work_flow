"""
Mini demo: 5 cases, compares FLAT vs HIERARCHICAL LLM prompting: Link3 AI
"""
import requests
import re
import time

URL = "http://localhost:1234/v1/chat/completions"
MODEL = "google/gemma-4-e4b"  # Gemma 4 E4B model - matching LM Studio


FLAT = (
    "You are an ISP ticket classifier. Match complaint to exactly one ISP code.\n"
    "ISP-001 Red light / Physical Fiber Cut\n"
    "ISP-006 Rain issues / Moisture in Fiber Closure\n"
    "ISP-008 DNS error / DNS Server Unreachable\n"
    "ISP-009 Router rebooting / Power Adapter Fault\n"
    "ISP-010 Paid but inactive / API Sync Failure\n"
    "ISP-015 -25dBm or lower / High Optical Loss\n"
    "ISP-023 Broken drop cable / Physical Cable Damage\n"
    "ISP-025 Zoom Teams lag / Jitter Upstream Congestion\n"
    "ISP-035 Sparking wire / Induction on Messenger Wire\n"
    "ISP-037 Smart TV buffering / DNS Caching Issue\n"
    "ISP-047 Low signal -30dBm / Splicing Joint Failure\n"
    "Respond with ONLY the ISP code."
)

STAGE1 = (
    "Classify into ONE category. Respond with ONLY the category name.\n"
    "PHYSICAL = red light, rain, cable damage, sparks, signal loss\n"
    "NETWORK  = Netflix, DNS, zoom, websites\n"
    "ACCOUNT  = billing, payment, inactive\n"
    "WIFI_HW  = router reboot, wifi weak, tv buffering\n"
)

STAGE2 = {
    "PHYSICAL": (
        "Match to exactly one code. Respond with ONLY the code.\n"
        "ISP-001 Red light / Physical Fiber Cut\n"
        "ISP-006 Rain issues / Moisture in Fiber Closure\n"
        "ISP-023 Broken drop cable / Physical Cable Damage\n"
        "ISP-035 Sparking wire / Induction on Messenger Wire\n"
        "ISP-047 Low signal -30dBm / Splicing Joint Failure"
    ),
    "NETWORK": (
        "Match to exactly one code. Respond with ONLY the code.\n"
        "ISP-008 DNS error / DNS Server Unreachable\n"
        "ISP-025 Zoom Teams lag / Jitter Upstream Congestion"
    ),
    "ACCOUNT": (
        "Match to exactly one code. Respond with ONLY the code.\n"
        "ISP-010 Paid but inactive / API Sync Failure"
    ),
    "WIFI_HW": (
        "Match to exactly one code. Respond with ONLY the code.\n"
        "ISP-009 Router rebooting / Power Adapter Fault\n"
        "ISP-037 Smart TV buffering / DNS Caching Issue"
    ),
}


def query(system, user):
    r = requests.post(URL, json={
        "model": MODEL,
        "messages": [{"role": "system", "content": system},
                     {"role": "user", "content": user}],
        "temperature": 0.0,
        "max_tokens": 10
    }, timeout=60).json()
    return r["choices"][0]["message"]["content"].strip()


def flat_classify(c):
    raw = query(FLAT, c)
    m = re.search(r'ISP-\d+', raw)
    return m.group(0) if m else "INVALID"


def hi_classify(c):
    cat = query(STAGE1, c).upper()
    matched = None
    for k in STAGE2:
        if k in cat:
            matched = k
            break
    stage2 = STAGE2.get(matched, "\n".join(STAGE2.values()))
    raw = query(stage2, c)
    m = re.search(r'ISP-\d+', raw)
    return m.group(0) if m else "INVALID"


CASES = [
    ("my onu has a red light", "ISP-001"),
    ("it rained and internet is gone", "ISP-006"),
    ("zoom calls freeze", "ISP-025"),
    ("paid bill but still inactive", "ISP-010"),
    ("smart tv buffers on all apps", "ISP-037"),
]

print("=" * 70)
print("MINI DEMO: FLAT vs HIERARCHICAL")
print("=" * 70)

print("\n--- FLAT (11 codes at once) ---")
for c, e in CASES:
    p = flat_classify(c)
    ok = "PASS" if p == e else "FAIL"
    print(f"  {ok} | '{c}' -> {p} (exp {e})")

print("\n--- HIERARCHICAL (category first, then small list) ---")
for c, e in CASES:
    p = hi_classify(c)
    ok = "PASS" if p == e else "FAIL"
    print(f"  {ok} | '{c}' -> {p} (exp {e})")

print("\nDone!")
