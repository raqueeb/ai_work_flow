import streamlit as st
import requests
import re

# Configuration
LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"

st.set_page_config(page_title="Link3 CTO Dashboard", page_icon="🎫")
st.title("🎫 Link3 Support Ticket Classifier")
st.markdown("### CTO Dashboard: Automated Diagnosis via Gemma 4B")

SYSTEM_PROMPT = """
You are a Link3 ISP Technical Assistant. Categorize the user's problem.
FORMAT:
CATEGORY: [L1/L2/L3/L4]
DIAGNOSIS: [Reason]
URGENCY: [High/Med/Low]
"""

# Initialize session state for the button so it doesn't disappear
if 'diagnosis_ready' not in st.session_state:
    st.session_state.diagnosis_ready = False
if 'current_diagnosis' not in st.session_state:
    st.session_state.current_diagnosis = ""

ticket_text = st.text_area("Enter Customer Complaint:", placeholder="e.g., My router has a red light", height=100)

if st.button("🚀 Analyze Ticket"):
    if ticket_text.strip():
        payload = {
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": ticket_text}
            ],
            "temperature": 0.1,
            "max_tokens": 150
        }

        try:
            with st.spinner('Gemma is processing...'):
                response = requests.post(LM_STUDIO_URL, json=payload, timeout=120)
                data = response.json()
                
                # SAFE CHECK: Ensure 'choices' exists in the response
                if "choices" in data and len(data["choices"]) > 0:
                    choice = data["choices"][0]["message"]
                    st.session_state.current_diagnosis = choice.get("content") or choice.get("reasoning_content") or "No output."
                    st.session_state.diagnosis_ready = True
                else:
                    # Log the actual error from LM Studio for debugging
                    st.error(f"LM Studio Error: {data.get('error', 'Unknown server error')}")
                    
        except Exception as e:
            st.error(f"Connection Error: {e}")
    else:
        st.warning("Please enter a ticket description.")

# Display Results & Assignment Button
if st.session_state.diagnosis_ready:
    st.success("Analysis Complete")
    st.info(f"**Gemma's Diagnosis:**\n\n{st.session_state.current_diagnosis}")
    
    # Show "Assign" button if it's a Physical (L2) or Hardware (L4) issue
    if any(x in st.session_state.current_diagnosis.upper() for x in ["L2", "L4", "PHYSICAL", "RED LIGHT"]):
        st.divider()
        st.error("🚨 **Field Support Required**")
        if st.button("🛠️ Click to Assign Field Team"):
            st.balloons()
            st.success("✅ DISPATCHED: A technician has been assigned to this Link3 client.")
