import time
import requests
from playwright.sync_api import Playwright, sync_playwright

# --- 1. LM STUDIO SETTINGS ---
LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"

def ask_qwen_ai(reason):
    """Sends the leave reason to Qwen 2.5 1.5B for a decision."""
    try:
        payload = {
            "model": "qwen2.5-1.5b-instruct",
            "messages": [
                {"role": "system", "content": "You are an HR Assistant. Answer ONLY 'APPROVE' or 'REJECT'."},
                {"role": "user", "content": f"Should I approve this leave? Reason: {reason}"}
            ],
            "temperature": 0.3
        }
        response = requests.post(LM_STUDIO_URL, json=payload, timeout=10)
        return response.json()['choices']['message']['content'].strip()
    except Exception as e:
        print(f"LM Studio Error: {e}")
        return "REJECT" # Safety first

# --- 2. THE AUTOMATION LOGIC ---
def process_approvals(playwright: Playwright):
    # Launch browser (headless=True for background running)
    browser = playwright.chromium.launch(headless=False) 
    context = browser.new_context()
    page = context.new_page()

    try:
        # LOGIN
        print("Logging in to Link3 CRM...")
        page.goto("https://crm.link3.net/")
        page.get_by_role("textbox", name="ID or Name").fill("rakibul.hassan")
        page.get_by_role("textbox", name="Password").fill("YOUR_PASSWORD") # <--- PUT PASSWORD HERE
        page.get_by_role("button", name="Login").click() # Update if button name is different

        # NAVIGATE (Update these based on your actual CRM menu)
        # page.get_by_role("link", name="Leave Approvals").click()

        # --- DATA EXTRACTION (Example Logic) ---
        # Replace these selectors with the actual ones from your CRM table
        days = 2       # Example: float(page.locator(".days-cell").inner_text())
        balance = 12   # Example: float(page.locator(".balance-cell").inner_text())
        reason = "Visiting family"

        # APPLY THE RULES
        if days < 3 and balance >= 10:
            print(f"Rule Match: Auto-approving {days} days.")
            # page.get_by_role("button", name="Approve").click()
        else:
            print("Request needs AI review...")
            decision = ask_qwen_ai(reason)
            if "APPROVE" in decision:
                print("AI Decision: Approved.")
                # page.get_by_role("button", name="Approve").click()
            else:
                print("AI Decision: Rejected/Review Needed.")

    except Exception as e:
        print(f"Automation Error: {e}")
    finally:
        context.close()
        browser.close()

# --- 3. THE PERIODIC LOOP ---
if __name__ == "__main__":
    while True:
        print(f"\n--- Starting Sync at {time.strftime('%H:%M:%S')} ---")
        with sync_playwright() as playwright:
            process_approvals(playwright)
        
        print("Done. Waiting 15 minutes for next check...")
        time.sleep(900) # 15 minutes
