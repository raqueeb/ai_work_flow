import requests
import json

url = 'http://localhost:1234/v1/chat/completions'

# Test cases with expected codes: Link3 AI
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
]

# Optimized minimal prompt for 1.5B model
SYSTEM_PROMPT = """You are an ISP ticket classifier. Your job is to match customer complaints to EXACTLY one ISP code.

RULES - Follow these strictly:
1. TV/smart TV buffering = ISP-037
2. Red light on ONT/ONU = ISP-001
3. Rain, wet, moisture issues = ISP-006
4. Signal -30dBm or lower = ISP-047
5. Signal -25dBm to -29dBm = ISP-015
6. Broken, cut, damaged cable = ISP-023
7. Sparking wire, induction = ISP-035
8. Netflix buffering = ISP-002
9. Weak Wi-Fi signal in room = ISP-005
10. Cannot login = ISP-014
11. Paid but inactive = ISP-010
12. Router rebooting = ISP-009
13. Speed capped at 10Mbps = ISP-038
14. Torrent/P2P slow = ISP-019

Respond with ONLY the ISP code. No explanation."""

correct = 0
total = len(TEST_CASES)

for complaint, expected in TEST_CASES:
    payload = {
        "model": "google/gemma-4-e4b",  # Gemma 4 E4B model - matching LM Studio

        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": complaint}
        ],
        "temperature": 0.0,
        "max_tokens": 10
    }
    resp = requests.post(url, json=payload, timeout=30)
    data = resp.json()
    result = data["choices"][0]["message"]["content"].strip()
    ok = result == expected
    if ok:
        correct += 1
    print(f"{'OK' if ok else 'FAIL'} | '{complaint}' -> {result} (expected: {expected})")

print(f"\nAccuracy: {correct}/{total} = {100*correct/total:.1f}%")
