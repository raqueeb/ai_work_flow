import streamlit as st
import requests
import json

# Configuration
LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"

st.set_page_config(page_title="SmartGift AI Admin", page_icon="🎁", layout="wide")

# --- INVENTORY DATA (20+ Products in BDT) ---
INVENTORY = """
PROD-001: Mechanical Keyboard -> RGB Backlit, Blue Switches [Price: 4,500 BDT, Stock: 15]
PROD-002: Instant Camera -> Fujifilm Instax Mini 12 [Price: 9,500 BDT, Stock: 8]
PROD-003: Wireless Earbuds -> Noise Cancelling, TWS [Price: 3,200 BDT, Stock: 25]
PROD-004: Smart Watch -> AMOLED Display, Heart Rate [Price: 5,500 BDT, Stock: 10]
PROD-005: Leather Journal -> Handmade, Refillable [Price: 1,200 BDT, Stock: 40]
PROD-006: Desktop Ring Light -> 10-inch, Tripod included [Price: 1,800 BDT, Stock: 30]
PROD-007: Power Bank -> 20,000mAh, Fast Charging [Price: 2,800 BDT, Stock: 50]
PROD-008: Laptop Stand -> Aluminum, Ergonomic [Price: 1,500 BDT, Stock: 20]
PROD-009: Bluetooth Speaker -> Waterproof, Deep Bass [Price: 4,000 BDT, Stock: 12]
PROD-010: USB-C Hub -> 7-in-1, 4K HDMI support [Price: 3,500 BDT, Stock: 18]
PROD-011: Gaming Mouse -> 12,000 DPI, Programmable [Price: 2,500 BDT, Stock: 22]
PROD-012: Webcam -> 1080p Full HD, Dual Mic [Price: 3,800 BDT, Stock: 15]
PROD-013: Electric Kettle -> Stainless Steel, 1.5L [Price: 2,200 BDT, Stock: 10]
PROD-014: Table Lamp -> LED, Eye Protection Mode [Price: 1,900 BDT, Stock: 25]
PROD-015: Backpack -> Anti-theft, Laptop Compartment [Price: 3,000 BDT, Stock: 35]
PROD-016: Drawing Tablet -> 8192 Pressure Levels [Price: 7,500 BDT, Stock: 5]
PROD-017: Smart Plug -> Wi-Fi enabled, App control [Price: 1,100 BDT, Stock: 45]
PROD-018: External Hard Drive -> 1TB USB 3.0 [Price: 6,200 BDT, Stock: 9]
PROD-019: Wireless Charger -> 15W Qi Charging [Price: 1,400 BDT, Stock: 30]
PROD-020: Coffee Grinder -> Ceramic Burrs, Manual [Price: 2,600 BDT, Stock: 14]
"""

SYSTEM_PROMPT = f"""
You are a Sales Expert for an electronics gift shop.
Inventory:
{INVENTORY}

Task: Analyze the customer's request and find the SINGLE best matching product from the Inventory.
Rules:
1. If they mention music or audio, pick PROD-003.
2. If they mention typing, gaming, or office, pick PROD-001.
3. If they mention photos, memories, or sisters, pick PROD-002.
4. If they mention fitness or health, pick PROD-004.

Return ONLY a JSON object:
{{
  "id": "PROD-XXX",
  "reason": "Short explanation why this fits",
  "confidence": 0-100
}}
"""

st.title("🎁 SmartGift AI: Customer-to-Product Mapper")
st.info("Demonstrating how a 1.5B LLM can drive a local retail business by mapping fuzzy human requests to hard database IDs.")

col1, col2 = st.columns([1, 1])

with col1:
    customer_voice = st.text_area("What is the customer looking for?", 
                                 placeholder="e.g. My brother just started a YouTube channel and needs better lighting.")
    
    if st.button("Generate Recommendation"):
        payload = {
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": customer_voice}
            ],
            "temperature": 0.2
        }
        
        with st.spinner("Qwen is searching inventory..."):
            try:
                response = requests.post(LM_STUDIO_URL, json=payload)
                result = response.json()['choices'][0]['message']['content']
                # Clean JSON in case LLM adds markdown
                result = result.replace("```json", "").replace("```", "").strip()
                data = json.loads(result)
                
                st.session_state.rec = data
            except Exception as e:
                st.error(f"Error: {e}")

with col2:
    if 'rec' in st.session_state:
        rec = st.session_state['rec']
        st.success(f"### Match Found: {rec['id']}")
        st.metric("Confidence Score", f"{rec['confidence']}%")
        st.write(f"**AI Logic:** {rec['reason']}")
        
        # Simulated Business Action
        if rec['confidence'] > 80:
            st.button(f"🛒 Add {rec['id']} to Invoice", type="primary")
        else:
            st.warning("Low confidence. Suggesting manual review.")
