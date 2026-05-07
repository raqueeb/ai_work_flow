import time
import requests
from playwright.sync_api import Playwright, sync_playwright

# --- CONFIGURATION ---
LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"

def ask_qwen(reason):
    """Asks your local 1.5B model to evaluate the reason if needed."""
    try:
        payload = {
            "model": "qwen2.5-1.5b-instruct",
            "messages": [
                {"role": "system", "content": "You are an HR manager. Approve leave if the reason is professional and valid. Answer ONLY 'APPROVE' or 'REJECT'."},
                {"role": "user", "content": f"Reason: {reason}"}
            ],
            "temperature": 0.1 # Keep it focused
        }
        response = requests.post(LM_STUDIO_URL, json=payload, timeout=10)
        return response.json()['choices'][0]['message']['content'].strip()
    except:
        return "REJECT" # Default to safety if model is off

def run_automation():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False) # Keep False to watch the demo
        context = browser.new_context()
        page = context.new_page()
        
        # --- LOGIN ---
        page.goto("https://office.link3.net/login")
        page.get_by_role("textbox", name="email@link3.net").fill("rakibul.hassan")
        page.get_by_role("textbox", name="password").fill("########")
        page.get_by_role("button", name="Log In").click()
        
        # --- NAVIGATE TO APPROVALS ---
        page.get_by_role("link", name="Leave Application").click()
        page.get_by_role("link", name="Leave Approval Pending").click() 

        # --- DATA EXTRACTION ---
        # Note: You need to find the correct text selectors for 'Days' and 'Balance' 
        # For now, let's assume variables based on your rule:
        days_requested = 2  # Replace with: float(page.locator("YOUR_SELECTOR").inner_text())
        balance_remaining = 12 # Replace with: float(page.locator("YOUR_SELECTOR").inner_text())
        reason_text = "Family emergency" # Replace with: page.locator("YOUR_SELECTOR").inner_text()

        # --- APPLY YOUR RULES ---
        print(f"Checking: {days_requested} days, {balance_remaining} balance.")
        
        if days_requested < 3 and balance_remaining >= 10:
            print("Rule Match: Auto-approving based on days/balance.")
            page.get_by_role("link", name="Select").click()
            page.get_by_role("button", name="Approve").click()
            page.locator("#ctl00_ContentPlaceHolder1_ConfirmBox1_btnOk").click()
        else:
            print("Consulting Qwen 2.5 for reason...")
            decision = ask_qwen(reason_text)
            if "APPROVE" in decision:
                page.get_by_role("link", name="Select").click()
                page.get_by_role("button", name="Approve").click()
                page.locator("#ctl00_ContentPlaceHolder1_ConfirmBox1_btnOk").click()
            else:
                print("Leave rejected by AI or needs manual review.")

        # --- LOGOUT ---
        page.get_by_role("link", name="Log Out").click()
        context.close()
        browser.close()

# Start the bot
if __name__ == "__main__":
    run_automation()
