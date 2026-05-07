import requests
import re
import time
import json

LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"
MODEL_NAME = "google/gemma-4-e4b"  # Gemma 4 E4B model - matching LM Studio: Link3 AI


# Full knowledge base for reference
KB_CODES = [f"ISP-{i:03d}" for i in range(1, 51)]

SYSTEM_PROMPT = (
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


def llm_classify(complaint):
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
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
                return m.group(0), data["usage"]["total_tokens"]
    except Exception as e:
        return f"ERROR: {e}", 0
    return "INVALID", 0


# Comprehensive test cases covering all categories and edge cases
TEST_CASES = [
    # Physical / L2 issues
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

    # L3 Network issues
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

    # L1 Account/Billing issues
    ("subscription expired yesterday", "ISP-003"),
    ("paid the bill but service still down", "ISP-010"),
    ("billed twice this month", "ISP-044"),
    ("auto-pay failed on card", "ISP-030"),
    ("plan upgrade not reflected", "ISP-040"),
    ("speed is locked at 10mbps", "ISP-038"),
    ("static ip stopped working", "ISP-017"),
    ("bill amount is wrong", "ISP-026"),

    # L4 Wi-Fi / Hardware issues
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


def run_stress_test():
    print("=" * 80)
    print("  LLM STRESS TEST - ISP TICKET CLASSIFICATION")
    print("  Model:", MODEL_NAME)
    print("  Total Queries:", len(TEST_CASES))
    print("=" * 80)

    correct = 0
    total_tokens = 0
    total_time = 0
    results = []

    for idx, (complaint, expected) in enumerate(TEST_CASES, 1):
        start = time.time()
        predicted, tokens = llm_classify(complaint)
        elapsed = time.time() - start

        total_tokens += tokens
        total_time += elapsed

        ok = predicted == expected
        if ok:
            correct += 1

        status = "PASS" if ok else "FAIL"
        results.append({
            "idx": idx,
            "complaint": complaint,
            "expected": expected,
            "predicted": predicted,
            "status": status,
            "tokens": tokens,
            "time_ms": round(elapsed * 1000, 1)
        })

        print(f"[{idx:02d}/{len(TEST_CASES)}] {status} | '{complaint[:50]:50s}' -> {predicted} (exp: {expected}) [{elapsed*1000:.0f}ms]")

    accuracy = 100 * correct / len(TEST_CASES)
    avg_time = total_time / len(TEST_CASES)
    avg_tokens = total_tokens / len(TEST_CASES)

    print("\n" + "=" * 80)
    print("  RESULTS SUMMARY")
    print("=" * 80)
    print(f"  Correct:     {correct}/{len(TEST_CASES)}")
    print(f"  Accuracy:    {accuracy:.1f}%")
    print(f"  Total Time:  {total_time:.1f}s")
    print(f"  Avg Time:    {avg_time*1000:.0f}ms per query")
    print(f"  Total Tokens:{total_tokens}")
    print(f"  Avg Tokens:  {avg_tokens:.0f} per query")
    print("=" * 80)

    # Show failures in detail
    failures = [r for r in results if r["status"] == "FAIL"]
    if failures:
        print("\n  FAILURE DETAILS:")
        for r in failures:
            print(f"    - '{r['complaint']}'")
            print(f"      Expected: {r['expected']} | Got: {r['predicted']}")
    else:
        print("\n  ALL TESTS PASSED!")

    # Save JSON report
    report_path = "C:\\Downloads\\llm_stress_test_report.json"
    with open(report_path, "w") as f:
        json.dump({
            "model": MODEL_NAME,
            "total_tests": len(TEST_CASES),
            "correct": correct,
            "accuracy_percent": round(accuracy, 1),
            "avg_time_ms": round(avg_time * 1000, 1),
            "avg_tokens": round(avg_tokens, 1),
            "results": results
        }, f, indent=2)
    print(f"\n  Report saved to: {report_path}")


if __name__ == "__main__":
    run_stress_test()
