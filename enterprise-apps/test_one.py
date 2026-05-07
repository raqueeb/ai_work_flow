import requests
url = 'http://localhost:1234/v1/chat/completions'
payload = {
    "model": "qwen2.5-coder-1.5b-instruct",
    "messages": [
        {"role": "system", "content": "You are an ISP ticket classifier. Match complaints to exactly one ISP code.\n\nTV/smart TV buffering = ISP-037\nRed light on ONT/ONU = ISP-001\nRain/wet/moisture issues = ISP-006\nSignal -30dBm or lower = ISP-047\nSignal -25dBm to -29dBm = ISP-015\nBroken/cut cable = ISP-023\nSparking wire = ISP-035\nNetflix buffering = ISP-002\nWeak Wi-Fi in room = ISP-005\nCannot login = ISP-014\nPaid but inactive = ISP-010\nRouter rebooting = ISP-009\nSpeed capped at 10Mbps = ISP-038\nTorrent slow = ISP-019\n\nRespond with ONLY the ISP code."},
        {"role": "user", "content": "my smart tv is buffering when watching netflix"}
    ],
    "temperature": 0.0,
    "max_tokens": 10
}
resp = requests.post(url, json=payload, timeout=120)
print(resp.json()["choices"][0]["message"]["content"].strip())
