"""
ISP SLA Assistant - Service Level Agreement Tool with LLM
=========================================================
Uses a small LLM to classify customer SLA tiers, track compliance,
and detect potential breaches before they occur.

Author: Rakibul Hassan
Date: May 2026
"""

import json
import time
from datetime import datetime, timedelta
from typing import Optional

# ============================================================================
# CONFIGURATION - Update these based on your LM Studio setup
# ============================================================================
BASE_URL = "http://localhost:1234/v1/chat/completions"
# For LM Studio, use "local-model" as the model name, or check your loaded model name
# You can also try: "qwen2.5-coder-1.5b-instruct" or "gemma-4-2b-it"
MODEL_NAME = "local-model"

# ============================================================================
# SLA TIER DEFINITIONS
# ============================================================================
SLA_TIERS = {
    "Bronze": {
        "response_time_hours": 24,
        "resolution_time_hours": 72,
        "uptime_percent": 99.0,
        "support_hours": "Business Hours",
        "escalation_level": "Standard",
        "max_concurrent_tickets": 1,
        "price_monthly_usd": 29.99
    },
    "Silver": {
        "response_time_hours": 12,
        "resolution_time_hours": 48,
        "uptime_percent": 99.5,
        "support_hours": "Business Hours + Email",
        "escalation_level": "Priority",
        "max_concurrent_tickets": 3,
        "price_monthly_usd": 79.99
    },
    "Gold": {
        "response_time_hours": 4,
        "resolution_time_hours": 24,
        "uptime_percent": 99.9,
        "support_hours": "24/7 Phone + Email",
        "escalation_level": "VIP",
        "max_concurrent_tickets": 5,
        "price_monthly_usd": 199.99
    },
    "Platinum": {
        "response_time_hours": 1,
        "resolution_time_hours": 8,
        "uptime_percent": 99.99,
        "support_hours": "24/7 Dedicated Line",
        "escalation_level": "Critical",
        "max_concurrent_tickets": 10,
        "price_monthly_usd": 499.99
    }
}

# ============================================================================
# TICKET PRIORITY MAPPING
# ============================================================================
PRIORITY_LEVELS = {
    "Critical": {"response_hours": 1, "resolution_hours": 4},
    "High": {"response_hours": 4, "resolution_hours": 12},
    "Medium": {"response_hours": 8, "resolution_hours": 24},
    "Low": {"response_hours": 24, "resolution_hours": 48}
}


# ============================================================================
# LLM INTERACTION FUNCTIONS
# ============================================================================
def call_llm(messages: list) -> str:
    """Make API call to local LLM via LM Studio."""
    import urllib.request
    
    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "temperature": 0.3,
        "max_tokens": 512
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        BASE_URL,
        data=data,
        headers={"Content-Type": "application/json"}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result["choices"][0]["message"]["content"]
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else str(e)
        print(f"   ⚠️  HTTP Error {e.code}: {error_body[:200]}")
        return None
    except Exception as e:
        print(f"   ⚠️  LLM Call Error: {e}")
        return None


def classify_customer_sla(customer_description: str) -> dict:
    """
    Use LLM to classify customer into appropriate SLA tier.
    Instead of hardcoded rules, the LLM analyzes the business needs.
    """
    system_prompt = """You are an ISP SLA Classifier. Analyze the customer's business description 
and classify them into one of these tiers: Bronze, Silver, Gold, or Platinum.

Consider these factors:
- Business size and complexity
- Criticality of internet connectivity
- Budget constraints
- Compliance requirements

Return ONLY a JSON object with this structure:
{
    "tier": "Bronze|Silver|Gold|Platinum",
    "confidence": 0.0-1.0,
    "reasoning": "brief explanation",
    "recommended_features": ["feature1", "feature2"]
}

Be concise. Return only the JSON."""
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Customer description: {customer_description}"}
    ]
    
    response = call_llm(messages)
    
    if response is None:
        return {"tier": "Bronze", "confidence": 0.5, "reasoning": "Fallback due to LLM error", "recommended_features": []}
    
    try:
        # Parse JSON from response
        if "{" in response:
            json_str = response[response.find("{"):response.rfind("}")+1]
            return json.loads(json_str)
    except:
        pass
    
    # Fallback to Bronze
    return {"tier": "Bronze", "confidence": 0.5, "reasoning": "Fallback", "recommended_features": []}


def assess_ticket_priority(ticket_text: str) -> dict:
    """
    Use LLM to assess ticket priority based on business impact.
    This replaces complex if-else rules with natural language understanding.
    """
    system_prompt = """You are an ISP Ticket Priority Analyzer. 
Analyze the ticket description and determine its priority and SLA requirements.

Consider:
- Business impact (revenue, operations)
- Number of affected users
- Service type affected
- Time sensitivity
- Potential escalation risk

Return ONLY a JSON object:
{
    "priority": "Critical|High|Medium|Low",
    "response_deadline_hours": number,
    "resolution_deadline_hours": number,
    "sla_breach_risk": "High|Medium|Low",
    "justification": "brief explanation"
}"""
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Ticket description: {ticket_text}"}
    ]
    
    response = call_llm(messages)
    
    if response is None:
        return {"priority": "Medium", "response_deadline_hours": 8, 
                "resolution_deadline_hours": 24, "sla_breach_risk": "Medium", 
                "justification": "Fallback due to LLM error"}
    
    try:
        if "{" in response:
            json_str = response[response.find("{"):response.rfind("}")+1]
            return json.loads(json_str)
    except:
        pass
    
    return {"priority": "Medium", "response_deadline_hours": 8, 
            "resolution_deadline_hours": 24, "sla_breach_risk": "Medium", 
            "justification": "Fallback"}


def check_sla_breach_risk(ticket: dict, customer_tier: str) -> dict:
    """
    Use LLM to analyze if a ticket is at risk of SLA breach.
    Combines ticket age, priority, and customer tier guarantees.
    """
    system_prompt = """You are an SLA Compliance Analyst. 
Analyze this ticket and customer tier to determine breach risk.

Calculate:
- Time since ticket opened vs SLA response/resolution time
- Customer tier guarantees vs actual performance
- Risk factors (weekends, holidays, complexity)
- Recommended actions to prevent breach

Return ONLY a JSON:
{
    "at_risk": true/false,
    "breach_type": "Response|Resolution|Both|None",
    "hours_until_breach": number or -1 if safe,
    "risk_factors": ["factor1", "factor2"],
    "recommendations": ["action1", "action2"]
}"""
    
    tier_info = SLA_TIERS.get(customer_tier, SLA_TIERS["Bronze"])
    
    ticket_summary = f"""Ticket ID: {ticket.get('id', 'N/A')}
Description: {ticket.get('description', 'N/A')}
Priority: {ticket.get('priority', 'Medium')}
Created: {ticket.get('created_at', 'N/A')}
Hours Elapsed: {ticket.get('hours_elapsed', 0)}

Customer SLA Tier: {customer_tier}
Tier Guarantees - Response: {tier_info['response_time_hours']}h, Resolution: {tier_info['resolution_time_hours']}h"""
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": ticket_summary}
    ]
    
    response = call_llm(messages)
    
    if response is None:
        return {"at_risk": False, "breach_type": "None", "hours_until_breach": -1, 
                "risk_factors": [], "recommendations": []}
    
    try:
        if "{" in response:
            json_str = response[response.find("{"):response.rfind("}")+1]
            return json.loads(json_str)
    except:
        pass
    
    return {"at_risk": False, "breach_type": "None", "hours_until_breach": -1, 
            "risk_factors": [], "recommendations": []}


def generate_sla_report(tickets: list, customers: list) -> str:
    """Generate SLA compliance report using LLM."""
    system_prompt = """You are an SLA Report Generator. 
Analyze the provided ticket and customer data and generate a compliance report.

Include:
- Overall compliance rate
- Breach analysis by tier
- Common issues
- Recommendations for improvement

Be professional and concise."""
    
    # Build context
    context = f"Total Customers: {len(customers)}\nTotal Active Tickets: {len(tickets)}\n\n"
    
    tier_stats = {}
    for tier in SLA_TIERS:
        tier_customers = [c for c in customers if c.get('sla_tier') == tier]
        tier_tickets = [t for t in tickets if t.get('customer_tier') == tier]
        tier_stats[tier] = {
            "customers": len(tier_customers),
            "tickets": len(tier_tickets),
            "breaches": len([t for t in tier_tickets if t.get('breached')])
        }
    
    context += "Tier Statistics:\n"
    for tier, stats in tier_stats.items():
        compliance = ((stats['tickets'] - stats['breaches']) / max(stats['tickets'], 1)) * 100
        context += f"- {tier}: {stats['customers']} customers, {stats['tickets']} tickets, {compliance:.1f}% compliance\n"
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": context}
    ]
    
    return call_llm(messages)


# ============================================================================
# CUSTOMER & TICKET MANAGEMENT
# ============================================================================
class Customer:
    def __init__(self, customer_id: str, name: str, business_type: str, description: str):
        self.id = customer_id
        self.name = name
        self.business_type = business_type
        self.description = description
        self.sla_tier = None
        self.assigned_at = None
        
    def assign_sla_tier(self, tier: str):
        self.sla_tier = tier
        self.assigned_at = datetime.now()
        
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "business_type": self.business_type,
            "description": self.description,
            "sla_tier": self.sla_tier,
            "assigned_at": self.assigned_at.isoformat() if self.assigned_at else None
        }


class Ticket:
    def __init__(self, ticket_id: str, customer_id: str, description: str, category: str = "Technical"):
        self.id = ticket_id
        self.customer_id = customer_id
        self.description = description
        self.category = category
        self.priority = "Medium"
        self.response_deadline = None
        self.resolution_deadline = None
        self.created_at = datetime.now()
        self.first_response_at = None
        self.resolved_at = None
        self.status = "Open"
        self.breached = False
        self.llm_analysis = {}
        
    def calculate_deadlines(self, sla_tier: str):
        tier_info = SLA_TIERS.get(sla_tier, SLA_TIERS["Bronze"])
        self.response_deadline = self.created_at + timedelta(hours=tier_info["response_time_hours"])
        self.resolution_deadline = self.created_at + timedelta(hours=tier_info["resolution_time_hours"])
        
    def check_breach(self):
        now = datetime.now()
        if self.status != "Resolved" and self.resolution_deadline and now > self.resolution_deadline:
            self.breached = True
        return self.breached
    
    def to_dict(self):
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "description": self.description,
            "priority": self.priority,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "response_deadline": self.response_deadline.isoformat() if self.response_deadline else None,
            "resolution_deadline": self.resolution_deadline.isoformat() if self.resolution_deadline else None,
            "breached": self.breached,
            "hours_elapsed": (datetime.now() - self.created_at).total_seconds() / 3600
        }


# ============================================================================
# MAIN SLA MANAGER CLASS
# ============================================================================
class SLAManager:
    """
    Central manager for ISP SLA operations.
    Uses LLM for intelligent classification and breach detection.
    """
    
    def __init__(self):
        self.customers: dict[str, Customer] = {}
        self.tickets: dict[str, Ticket] = {}
        self.ticket_counter = 0
        
    def register_customer(self, customer_id: str, name: str, 
                        business_type: str, description: str) -> Customer:
        """Register new customer and auto-classify SLA tier using LLM."""
        customer = Customer(customer_id, name, business_type, description)
        
        # Use LLM to classify
        print(f"\n🔍 Analyzing customer for SLA tier classification...")
        classification = classify_customer_sla(description)
        
        customer.assign_sla_tier(classification["tier"])
        self.customers[customer_id] = customer
        
        print(f"   ✓ Assigned to {classification['tier']} tier (confidence: {classification['confidence']:.0%})")
        print(f"   → Reasoning: {classification['reasoning']}")
        
        return customer
    
    def create_ticket(self, customer_id: str, description: str, 
                     category: str = "Technical") -> Optional[Ticket]:
        """Create ticket and assess priority using LLM."""
        if customer_id not in self.customers:
            print(f"❌ Customer {customer_id} not found!")
            return None
            
        self.ticket_counter += 1
        ticket_id = f"TKT-{self.ticket_counter:04d}"
        
        ticket = Ticket(ticket_id, customer_id, description, category)
        customer = self.customers[customer_id]
        
        # Use LLM to assess priority
        print(f"\n🔍 Analyzing ticket for priority assessment...")
        priority_info = assess_ticket_priority(description)
        
        ticket.priority = priority_info["priority"]
        ticket.llm_analysis = priority_info
        ticket.calculate_deadlines(customer.sla_tier)
        
        self.tickets[ticket_id] = ticket
        
        tier_info = SLA_TIERS.get(customer.sla_tier)
        print(f"   ✓ Priority: {priority_info['priority']}")
        print(f"   → SLA: Response within {tier_info['response_time_hours']}h, Resolution within {tier_info['resolution_time_hours']}h")
        print(f"   → Risk Assessment: {priority_info['sla_breach_risk']} breach risk")
        
        return ticket
    
    def check_ticket_health(self, ticket_id: str) -> Optional[dict]:
        """Check if a ticket is at risk of SLA breach using LLM."""
        if ticket_id not in self.tickets:
            return None
            
        ticket = self.tickets[ticket_id]
        customer = self.customers.get(ticket.customer_id)
        
        if not customer:
            return None
            
        print(f"\n🔍 Checking SLA compliance for {ticket_id}...")
        
        health_report = check_sla_breach_risk(ticket.to_dict(), customer.sla_tier)
        
        if health_report["at_risk"]:
            print(f"   ⚠️  AT RISK - {health_report['breach_type']} breach in ~{health_report['hours_until_breach']:.1f} hours")
            print(f"   → Risk factors: {', '.join(health_report['risk_factors'])}")
            print(f"   → Recommendations: {', '.join(health_report['recommendations'])}")
        else:
            print(f"   ✅ Healthy - {health_report['hours_until_breach']:.1f}+ hours until potential breach")
            
        return health_report
    
    def escalate_ticket(self, ticket_id: str, reason: str = "") -> bool:
        """Escalate ticket priority."""
        if ticket_id not in self.tickets:
            return False
            
        ticket = self.tickets[ticket_id]
        old_priority = ticket.priority
        
        priority_order = ["Low", "Medium", "High", "Critical"]
        current_idx = priority_order.index(ticket.priority) if ticket.priority in priority_order else 1
        new_idx = min(current_idx + 1, 3)
        ticket.priority = priority_order[new_idx]
        
        print(f"\n📢 Ticket {ticket_id} escalated: {old_priority} → {ticket.priority}")
        if reason:
            print(f"   → Reason: {reason}")
            
        return True
    
    def resolve_ticket(self, ticket_id: str) -> bool:
        """Mark ticket as resolved."""
        if ticket_id not in self.tickets:
            return False
            
        ticket = self.tickets[ticket_id]
        ticket.resolved_at = datetime.now()
        ticket.status = "Resolved"
        ticket.check_breach()
        
        status = "✅ Resolved" if not ticket.breached else "❌ Resolved (SLA BREACH)"
        print(f"\n{status}: {ticket_id}")
        print(f"   → Breach occurred: {'Yes' if ticket.breached else 'No'}")
        
        return True
    
    def show_dashboard(self):
        """Display SLA dashboard summary."""
        print("\n" + "="*70)
        print("                    ISP SLA DASHBOARD")
        print("="*70)
        
        # Customer summary by tier
        print("\n📊 Customers by SLA Tier:")
        for tier in ["Bronze", "Silver", "Gold", "Platinum"]:
            count = len([c for c in self.customers.values() if c.sla_tier == tier])
            tier_info = SLA_TIERS[tier]
            print(f"   {tier:8} | {count:3} customers | Resp: {tier_info['response_time_hours']}h | Res: {tier_info['resolution_time_hours']}h")
        
        # Ticket summary
        open_tickets = [t for t in self.tickets.values() if t.status != "Resolved"]
        resolved_tickets = [t for t in self.tickets.values() if t.status == "Resolved"]
        
        print(f"\n📋 Ticket Summary:")
        print(f"   Total: {len(self.tickets)} | Open: {len(open_tickets)} | Resolved: {len(resolved_tickets)}")
        
        # Priority breakdown
        print("\n   Open Tickets by Priority:")
        for priority in ["Critical", "High", "Medium", "Low"]:
            count = len([t for t in open_tickets if t.priority == priority])
            print(f"      {priority:8}: {count}")
        
        # Breach summary
        breached = len([t for t in self.tickets.values() if t.breached])
        compliance_rate = ((len(self.tickets) - breached) / max(len(self.tickets), 1)) * 100
        
        print(f"\n📈 SLA Compliance: {compliance_rate:.1f}% ({breached} breaches)")
        
        print("\n" + "="*70)
        
    def get_compliance_report(self) -> str:
        """Generate detailed compliance report using LLM."""
        print("\n📑 Generating SLA compliance report...")
        return generate_sla_report(
            [t.to_dict() for t in self.tickets.values()],
            [c.to_dict() for c in self.customers.values()]
        )


# ============================================================================
# DEMONSTRATION
# ============================================================================
def run_demo():
    """Demonstrate the SLA Manager capabilities."""
    print("\n" + "="*70)
    print("     ISP SLA ASSISTANT - LLM-POWERED SERVICE LEVEL AGREEMENT")
    print("="*70)
    print("\nThis tool uses a small LLM to:")
    print("  • Classify customers into SLA tiers (Bronze → Platinum)")
    print("  • Assess ticket priority based on business impact")
    print("  • Detect SLA breach risks before they occur")
    print("  • Generate compliance reports")
    
    # Initialize manager
    sla = SLAManager()
    
    # Register customers with different profiles
    print("\n\n" + "-"*70)
    print("STEP 1: Register Customers & Classify SLA Tiers")
    print("-"*70)
    
    customers_data = [
        ("C001", "Tech Startup", "Technology", "Small startup, 10 employees, VoIP dependent"),
        ("C002", "Home Office", "Professional Services", "Freelancer, needs reliable internet for video calls"),
        ("C003", "Law Firm", "Legal Services", "Mid-size law firm, 50 employees, compliance critical"),
        ("C004", "School", "Education", "Educational institution, 200 students, e-learning platform"),
        ("C005", "Hospital", "Healthcare", "Healthcare facility, emergency services, 24/7 operations")
    ]
    
    for cust_id, name, business_type, desc in customers_data:
        sla.register_customer(cust_id, name, business_type, desc)
        time.sleep(0.5)  # Small delay for readability
    
    # Create tickets
    print("\n\n" + "-"*70)
    print("STEP 2: Create Support Tickets")
    print("-"*70)
    
    tickets_data = [
        ("C001", "VPN connection keeps dropping during client meetings", "Technical"),
        ("C003", "Entire floor can't access internet - potential network outage", "Network"),
        ("C004", "Slow WiFi in main building affecting online classes", "Connectivity"),
        ("C005", "Patient records system unreachable - critical issue", "Critical"),
        ("C002", "Email not sending attachments over 5MB", "Technical")
    ]
    
    for cust_id, desc, cat in tickets_data:
        sla.create_ticket(cust_id, desc, cat)
        time.sleep(0.5)
    
    # Check ticket health
    print("\n\n" + "-"*70)
    print("STEP 3: SLA Health Check")
    print("-"*70)
    
    for ticket_id in ["TKT-0001", "TKT-0003", "TKT-0004"]:
        sla.check_ticket_health(ticket_id)
        time.sleep(0.5)
    
    # Escalate a ticket
    print("\n\n" + "-"*70)
    print("STEP 4: Escalation")
    print("-"*70)
    sla.escalate_ticket("TKT-0001", "Customer threatened to cancel contract")
    
    # Resolve tickets
    print("\n\n" + "-"*70)
    print("STEP 5: Resolve Tickets")
    print("-"*70)
    sla.resolve_ticket("TKT-0001")
    sla.resolve_ticket("TKT-0002")
    sla.resolve_ticket("TKT-0005")
    
    # Show dashboard
    sla.show_dashboard()
    
    # Generate report
    print("\n\n" + "-"*70)
    print("STEP 6: Compliance Report")
    print("-"*70)
    report = sla.get_compliance_report()
    print("\n" + report)
    
    print("\n" + "="*70)
    print("Demo complete! This shows how LLM can intelligently handle SLA")
    print("classification instead of complex rule-based systems.")
    print("="*70)


# ============================================================================
# ENTRY POINT
# ============================================================================
if __name__ == "__main__":
    # Check if LM Studio is running
    import urllib.request
    import urllib.error
    
    print("\n🔗 Checking LM Studio connection...")
    
    # Try multiple endpoints to check if LM Studio is running
    endpoints_to_try = [
        "http://localhost:1234/v1/models",
        "http://localhost:1234/v1/completions"
    ]
    
    server_running = False
    for endpoint in endpoints_to_try:
        try:
            req = urllib.request.Request(endpoint)
            # Add a HEAD request method to just check connectivity
            req.get_method = lambda: 'HEAD'
            urllib.request.urlopen(req, timeout=5)
            server_running = True
            break
        except urllib.error.HTTPError:
            # HTTP error means server IS running, just returned an error
            # This is fine - it means LM Studio server is active
            server_running = True
            break
        except Exception:
            continue
    
    if server_running:
        print("   ✓ LM Studio is running")
        print("   → Running SLA Assistant demo...")
        run_demo()
    else:
        print("   ❌ Cannot connect to LM Studio at http://localhost:1234")
        print("\n   Please:")
        print("   1. Start LM Studio")
        print("   2. Load a model (e.g., Qwen 2.5 or Gemma)")
        print("   3. Enable 'API' server on port 1234")
        print("      (In LM Studio: Developer > Server > Enable Local Server)")
        print("   4. Run this script again")