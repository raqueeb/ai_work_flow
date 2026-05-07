#!/usr/bin/env python3
"""
Traditional vs AI-Driven Workflow Demonstration
================================================
Shows the transition from deterministic (rule-based) to probabilistic (AI-driven) 
software management for service industry scenarios.

Run with LM Studio running Qwen 2.5 1.5B on localhost:1234
"""

import json
import time
from typing import Dict, List, Tuple, Optional

# ============================================================================
# CONFIGURATION
# ============================================================================

LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"
MODEL_NAME = "qwen2.5-coder-1.5b-instruct"

# ============================================================================
# PART 1: TRADITIONAL RULE-BASED SYSTEM
# ============================================================================

class TraditionalRuleBasedSystem:
    """
    Deterministic system using if-then rules.
    Every decision is predictable and traceable.
    """
    
    def classify_complaint(self, text: str) -> Dict:
        """Rule-based classification using keyword matching."""
        text_lower = text.lower()
        
        # Rule-based classification
        if "fiber" in text_lower or "cut" in text_lower:
            code = "ISP-006"
            action = "DISPATCH_FIELD_TEAM"
            priority = "CRITICAL"
        elif "red light" in text_lower or "pon led" in text_lower:
            code = "ISP-001"
            action = "TROUBLESHOOT_ONU"
            priority = "HIGH"
        elif "slow" in text_lower or "speed" in text_lower:
            code = "ISP-047"
            action = "CHECK_BANDWIDTH"
            priority = "MEDIUM"
        elif "no internet" in text_lower or "disconnected" in text_lower:
            code = "ISP-002"
            action = "CHECK_CONNECTION"
            priority = "HIGH"
        elif "wifi" in text_lower or "wireless" in text_lower:
            code = "ISP-003"
            action = "TROUBLESHOOT_WIFI"
            priority = "LOW"
        else:
            code = "ISP-050"
            action = "GENERAL_SUPPORT"
            priority = "MEDIUM"
        
        return {
            "method": "RULE-BASED",
            "code": code,
            "action": action,
            "priority": priority,
            "confidence": "99%",  # Fixed high confidence
            "reasoning": "Keyword matched"
        }
    
    def assess_sla_tier(self, customer_data: Dict) -> Dict:
        """Rule-based SLA assignment using thresholds."""
        monthly_revenue = customer_data.get("monthly_revenue", 0)
        employee_count = customer_data.get("employee_count", 0)
        
        # Hard-coded thresholds
        if monthly_revenue >= 50000:
            tier = "PLATINUM"
            response_time = "1 hour"
        elif monthly_revenue >= 20000:
            tier = "GOLD"
            response_time = "4 hours"
        elif monthly_revenue >= 5000:
            tier = "SILVER"
            response_time = "8 hours"
        else:
            tier = "BRONZE"
            response_time = "24 hours"
        
        return {
            "method": "RULE-BASED",
            "tier": tier,
            "response_time": response_time,
            "confidence": "100%",  # Deterministic
            "reasoning": f"Revenue ${monthly_revenue} > threshold"
        }
    
    def route_ticket(self, complaint: str, customer_tier: str) -> Dict:
        """Rule-based ticket routing."""
        priority = self.classify_complaint(complaint)["priority"]
        
        # Priority escalation rules
        if customer_tier == "PLATINUM":
            queue = "PRIORITY_QUEUE"
            escalate = True
        elif priority == "CRITICAL":
            queue = "CRITICAL_QUEUE"
            escalate = True
        elif priority == "HIGH":
            queue = "STANDARD_QUEUE"
            escalate = False
        else:
            queue = "LOW_PRIORITY_QUEUE"
            escalate = False
        
        return {
            "method": "RULE-BASED",
            "queue": queue,
            "escalate": escalate,
            "confidence": "100%",
            "reasoning": f"Tier={customer_tier}, Priority={priority}"
        }
    
    def diagnose_issue(self, symptoms: List[str]) -> Dict:
        """Rule-based diagnosis using decision tree."""
        symptoms_lower = [s.lower() for s in symptoms]
        
        # Decision tree logic
        if "no_signal" in symptoms_lower and "red_light" in symptoms_lower:
            diagnosis = "ONT_POWER_FAILURE"
            solution = "Replace power adapter or ONT unit"
        elif "slow_speed" in symptoms_lower and "wifi_drop" in symptoms_lower:
            diagnosis = "INTERFERENCE_CONGESTION"
            solution = "Change WiFi channel or upgrade plan"
        elif "intermittent" in symptoms_lower:
            diagnosis = "SIGNAL_DEGRADATION"
            solution = "Check cables and splice points"
        else:
            diagnosis = "UNKNOWN"
            solution = "Escalate to L2 support"
        
        return {
            "method": "RULE-BASED",
            "diagnosis": diagnosis,
            "solution": solution,
            "confidence": "95%",
            "reasoning": "Decision tree traversal"
        }


# ============================================================================
# PART 2: AI-DRIVEN PROBABILISTIC SYSTEM
# ============================================================================

def call_llm(messages: List[Dict], temperature: float = 0.3) -> str:
    """Call local LLM via LM Studio."""
    import urllib.request
    import urllib.error
    
    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": 500
    }
    
    try:
        req = urllib.request.Request(
            LM_STUDIO_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Error: {e}"


class AIDrivenProbabilisticSystem:
    """
    Probabilistic system using LLM for intelligent decisions.
    Decisions are based on context understanding and learning patterns.
    """
    
    def classify_complaint(self, text: str) -> Dict:
        """AI-powered classification with context understanding."""
        prompt = f"""Classify this customer complaint for an ISP support ticket.

Complaint: "{text}"

Consider:
- What is the root cause?
- What actions should be taken?
- What is the urgency level?

Respond in JSON format:
{{
    "code": "ISP-XXX",
    "category": "brief category",
    "action": "recommended action",
    "priority": "CRITICAL/HIGH/MEDIUM/LOW",
    "confidence": "0-100%",
    "reasoning": "brief explanation"
}}"""

        messages = [{"role": "user", "content": prompt}]
        response = call_llm(messages)
        
        try:
            # Try to parse JSON from response
            if "{" in response and "}" in response:
                json_str = response[response.index("{"):response.rindex("}")+1]
                result = json.loads(json_str)
                result["method"] = "AI-DRIVEN"
                return result
        except:
            pass
        
        return {
            "method": "AI-DRIVEN",
            "code": "UNKNOWN",
            "category": "Unclassified",
            "action": "Manual review needed",
            "priority": "MEDIUM",
            "confidence": "0%",
            "reasoning": "Parse failed"
        }
    
    def assess_sla_tier(self, customer_data: Dict) -> Dict:
        """AI-powered SLA assessment considering business context."""
        prompt = f"""Assess the appropriate SLA tier for this customer considering business value,
compliance requirements, and strategic importance.

Customer Data:
- Company: {customer_data.get('company_name', 'N/A')}
- Industry: {customer_data.get('industry', 'N/A')}
- Monthly Revenue: ${customer_data.get('monthly_revenue', 0)}
- Employee Count: {customer_data.get('employee_count', 0)}
- Criticality: {customer_data.get('criticality', 'standard')}
- SLA History: {customer_data.get('sla_history', 'good')}

Consider beyond just revenue - think about business impact, compliance needs, and strategic value.

Respond in JSON format:
{{
    "tier": "PLATINUM/GOLD/SILVER/BRONZE",
    "response_time": "expected response time",
    "confidence": "0-100%",
    "reasoning": "business context explanation",
    "recommended_features": ["feature1", "feature2"]
}}"""

        messages = [{"role": "user", "content": prompt}]
        response = call_llm(messages)
        
        try:
            if "{" in response and "}" in response:
                json_str = response[response.index("{"):response.rindex("}")+1]
                result = json.loads(json_str)
                result["method"] = "AI-DRIVEN"
                return result
        except:
            pass
        
        return {
            "method": "AI-DRIVEN",
            "tier": "SILVER",
            "response_time": "8 hours",
            "confidence": "0%",
            "reasoning": "Parse failed"
        }
    
    def route_ticket(self, complaint: str, customer_data: Dict, history: List[Dict]) -> Dict:
        """AI-powered intelligent ticket routing."""
        history_summary = "\n".join([
            f"- {h['date']}: {h['issue']} -> {h['resolution']}"
            for h in history[-3:]
        ]) if history else "No history available"
        
        prompt = f"""Analyze this support ticket and determine the best routing strategy.

Current Complaint: "{complaint}"

Customer: {customer_data.get('company_name', 'N/A')} ({customer_data.get('tier', 'STANDARD')})
History:
{history_summary}

Consider:
- Which team has relevant expertise?
- What priority based on context and history?
- Should this be escalated or handled at current level?

Respond in JSON format:
{{
    "queue": "recommended queue",
    "team": "best suited team",
    "priority": "CRITICAL/HIGH/MEDIUM/LOW",
    "escalate": true/false,
    "confidence": "0-100%",
    "reasoning": "context-aware explanation"
}}"""

        messages = [{"role": "user", "content": prompt}]
        response = call_llm(messages)
        
        try:
            if "{" in response and "}" in response:
                json_str = response[response.index("{"):response.rindex("}")+1]
                result = json.loads(json_str)
                result["method"] = "AI-DRIVEN"
                return result
        except:
            pass
        
        return {
            "method": "AI-DRIVEN",
            "queue": "STANDARD_QUEUE",
            "team": "General Support",
            "priority": "MEDIUM",
            "escalate": False,
            "confidence": "0%",
            "reasoning": "Parse failed"
        }
    
    def diagnose_issue(self, symptoms: List[str], context: str) -> Dict:
        """AI-powered diagnosis with pattern recognition."""
        prompt = f"""Diagnose this network issue by analyzing the symptoms and context.

Symptoms reported:
{chr(10).join(f'- {s}' for s in symptoms)}

Customer Context: {context}

Use pattern recognition from similar cases and provide intelligent diagnosis.
Consider multiple possible causes and rank by likelihood.

Respond in JSON format:
{{
    "diagnosis": "primary diagnosis",
    "probability": "0-100%",
    "differential_diagnoses": ["other possibility 1", "other possibility 2"],
    "solution": "recommended solution",
    "confidence": "0-100%",
    "reasoning": "pattern-based explanation"
}}"""

        messages = [{"role": "user", "content": prompt}]
        response = call_llm(messages)
        
        try:
            if "{" in response and "}" in response:
                json_str = response[response.index("{"):response.rindex("}")+1]
                result = json.loads(json_str)
                result["method"] = "AI-DRIVEN"
                return result
        except:
            pass
        
        return {
            "method": "AI-DRIVEN",
            "diagnosis": "Unknown",
            "probability": "0%",
            "differential_diagnoses": [],
            "solution": "Manual review",
            "confidence": "0%",
            "reasoning": "Parse failed"
        }


# ============================================================================
# PART 3: DEMONSTRATION SCENARIOS
# ============================================================================

SCENARIOS = [
    {
        "id": 1,
        "title": "Ambiguous Complaint Classification",
        "complaint": "My internet has been acting weird since the storm last night. Sometimes it works, sometimes it doesn't. The kids are complaining they can't watch their shows.",
        "customer": {"tier": "GOLD", "monthly_revenue": 15000}
    },
    {
        "id": 2,
        "title": "Context-Aware SLA Assessment",
        "complaint": "We're a hospital network with 200 beds. Any downtime means lives at risk. We need the best support possible.",
        "customer": {"company_name": "City General Hospital", "industry": "Healthcare", "monthly_revenue": 35000, "employee_count": 500, "criticality": "critical"}
    },
    {
        "id": 3,
        "title": "Intelligent Ticket Routing",
        "complaint": "Multiple customers in Chittagong are reporting the same issue - no signal after the rain. This feels like a larger outage.",
        "customer": {"company_name": "Chittagong Port Authority", "tier": "PLATINUM"},
        "history": [
            {"date": "2024-01-15", "issue": "Fiber cut in zone B", "resolution": "Repaired within 4 hours"},
            {"date": "2024-02-20", "issue": "Intermittent connectivity", "resolution": "Replaced ONT units"},
            {"date": "2024-03-10", "issue": "Slow speeds during peak", "resolution": "Bandwidth upgrade"}
        ]
    },
    {
        "id": 4,
        "title": "Pattern-Based Diagnosis",
        "complaint": "The network keeps dropping every 15 minutes. We've tried restarting everything but it keeps happening.",
        "customer": {"company_name": "Tech Startup Office"},
        "symptoms": ["intermittent_drop", "wifi_disconnect", "router_reboot_required", "specific_timing_pattern"]
    },
    {
        "id": 5,
        "title": "Customer Sentiment Impact",
        "complaint": "I have been calling about this issue for 3 days and nobody seems to care. This is ridiculous. I want to speak to a manager immediately.",
        "customer": {"company_name": "Small Business Owner", "tier": "SILVER", "complaints_last_month": 5}
    }
]


def print_header(title: str):
    """Print formatted header."""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")


def print_result(method: str, result: Dict):
    """Print formatted result."""
    for key, value in result.items():
        print(f"  {key.upper()}: {value}")
    print()


def run_scenario(scenario: Dict, rule_system: TraditionalRuleBasedSystem, 
                 ai_system: AIDrivenProbabilisticSystem):
    """Run a single demonstration scenario."""
    print_header(f"SCENARIO {scenario['id']}: {scenario['title']}")
    
    complaint = scenario["complaint"]
    customer = scenario.get("customer", {})
    
    print(f"CUSTOMER COMPLAINT:")
    print(f'  "{complaint}"')
    print(f"\nCUSTOMER DATA: {json.dumps(customer, indent=2)}")
    
    # Scenario 1 & 2: Classification
    if scenario["id"] in [1, 5]:
        print_header("TASK 1: COMPLAINT CLASSIFICATION")
        
        print("📋 TRADITIONAL RULE-BASED APPROACH:")
        rule_result = rule_system.classify_complaint(complaint)
        print_result("RULES", rule_result)
        
        print("🤖 AI-DRIVEN APPROACH:")
        ai_result = ai_system.classify_complaint(complaint)
        print_result("AI", ai_result)
    
    # Scenario 2: SLA Assessment
    elif scenario["id"] == 2:
        print_header("TASK: SLA TIER ASSESSMENT")
        
        print("📋 TRADITIONAL RULE-BASED APPROACH:")
        rule_result = rule_system.assess_sla_tier(customer)
        print_result("RULES", rule_result)
        
        print("🤖 AI-DRIVEN APPROACH:")
        ai_result = ai_system.assess_sla_tier(customer)
        print_result("AI", ai_result)
    
    # Scenario 3: Ticket Routing
    elif scenario["id"] == 3:
        print_header("TASK: INTELLIGENT TICKET ROUTING")
        
        history = scenario.get("history", [])
        customer_tier = customer.get("tier", "STANDARD")
        
        print("📋 TRADITIONAL RULE-BASED APPROACH:")
        rule_result = rule_system.route_ticket(complaint, customer_tier)
        print_result("RULES", rule_result)
        
        print("🤖 AI-DRIVEN APPROACH:")
        ai_result = ai_system.route_ticket(complaint, customer, history)
        print_result("AI", ai_result)
    
    # Scenario 4: Diagnosis
    elif scenario["id"] == 4:
        print_header("TASK: ISSUE DIAGNOSIS")
        
        symptoms = scenario.get("symptoms", [])
        context = customer.get("company_name", "Business Customer")
        
        print(f"SYMPTOMS: {symptoms}")
        
        print("📋 TRADITIONAL RULE-BASED APPROACH:")
        rule_result = rule_system.diagnose_issue(symptoms)
        print_result("RULES", rule_result)
        
        print("🤖 AI-DRIVEN APPROACH:")
        ai_result = ai_system.diagnose_issue(symptoms, context)
        print_result("AI", ai_result)


def print_summary():
    """Print comparison summary."""
    print_header("DETERMINISTIC vs PROBABILISTIC: KEY DIFFERENCES")
    
    comparison = """
┌────────────────────────────────────────────────────────────────────┐
│                    COMPARISON SUMMARY                               │
├──────────────────────┬─────────────────────┬────────────────────────┤
│ Aspect               │ Rule-Based          │ AI-Driven              │
├──────────────────────┼─────────────────────┼────────────────────────┤
│ Decision Logic       │ If-Then conditions  │ Pattern recognition    │
│ Confidence           │ Fixed (99-100%)     │ Variable (0-100%)      │
│ Context Understanding│ Limited to keywords │ Full context analysis  │
│ Edge Cases           │ Fails               │ Handles gracefully     │
│ Maintenance          │ High (many rules)   │ Low (model learns)     │
│ Explainability       │ Very High           │ Medium                 │
│ Scalability          │ O(rules)            │ O(model size)          │
│ Adaptability         │ Manual updates      │ Continuous learning    │
│ Cost to Maintain     │ High (developer)    │ Low (compute)          │
│ Human Judgment       │ Programmed in rules │ Emergent from data     │
└──────────────────────┴─────────────────────┴────────────────────────┘
"""
    print(comparison)


def print_architecture():
    """Print architecture diagrams."""
    print_header("ARCHITECTURE COMPARISON")
    
    rule_arch = """
┌─────────────────────────────────────────────────────────────────────┐
│              TRADITIONAL RULE-BASED SYSTEM                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   INPUT ──────▶ KEYWORD ──────▶ RULE ENGINE ──────▶ ACTION         │
│   "fiber"         MATCH        IF fiber THEN         DISPATCH      │
│   "cut"                             ISP-006                         │
│                                                                     │
│   +──────────────+                                        ▲        │
│   │  500+ Rules  │                                        │        │
│   │  Hard-coded  │                                        │        │
│   │  Maintained  │                                        │        │
│   │  by Devs     │                                        │        │
│   +──────────────+                                        │        │
│                                                             │        │
│   ⚠️  Fragile: One new pattern = New rule needed           │        │
│   ⚠️  Brittle: Missing keyword = Wrong classification       │        │
│   ⚠️  Expensive: Every update = Developer time             │        │
└─────────────────────────────────────────────────────────────────────┘
"""
    print(rule_arch)
    
    ai_arch = """
┌─────────────────────────────────────────────────────────────────────┐
│              AI-DRIVEN PROBABILISTIC SYSTEM                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   INPUT ──────▶ CONTEXT ──────▶ LLM REASONING ──────▶ ACTION       │
│   "fiber         Extracted     "This likely indicates   DISPATCH    │
│    cut..."        context       a physical issue..."      FIELD      │
│                                                                     │
│   +──────────────+                                        ▲        │
│   │  1.5B params │                                        │        │
│   │  Learned     │                                        │        │
│   │  from data   │                                        │        │
│   │  Understands │                                        │        │
│   │  nuance      │                                        │        │
│   +──────────────+                                        │        │
│                                                             │        │
│   ✅ Resilient: Handles new patterns without rules         │        │
│   ✅ Adaptive: Learns from every interaction                │        │
│   ✅ Scalable: One model handles everything                 │        │
└─────────────────────────────────────────────────────────────────────┘
"""
    print(ai_arch)


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Run the demonstration."""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║     TRANSITIONING FROM TRADITIONAL TO AI-DRIVEN WORKFLOWS            ║
║                                                                      ║
║     Deterministic Rules → Probabilistic AI Reasoning                 ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
""")
    
    # Initialize systems
    rule_system = TraditionalRuleBasedSystem()
    ai_system = AIDrivenProbabilisticSystem()
    
    # Check LM Studio connection
    print("Checking LM Studio connection...")
    test_response = call_llm([
        {"role": "user", "content": "Reply with just 'OK' if you can understand me."}
    ])
    
    if "Error" in test_response:
        print(f"""
⚠️  WARNING: Could not connect to LM Studio at {LM_STUDIO_URL}

Please ensure:
1. LM Studio is running
2. Qwen 2.5 1.5B model is loaded
3. Server is running on localhost:1234

Run the demo without AI features? (y/n): """)
        use_ai = input().lower() == 'y'
        if not use_ai:
            return
    else:
        print("✅ LM Studio connected successfully\n")
    
    # Print architecture comparison
    print_architecture()
    
    input("\n📍 Press Enter to start scenarios...")
    
    # Run scenarios
    for scenario in SCENARIOS:
        run_scenario(scenario, rule_system, ai_system)
        input("\n📍 Press Enter for next scenario...")
    
    # Print summary
    print_summary()
    
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║                         DEMONSTRATION COMPLETE                          ║
║                                                                      ║
║  KEY TAKEAWAYS:                                                      ║
║  • Rule-based systems are predictable but fragile                    ║
║  • AI-driven systems are adaptive but probabilistic                  ║
║  • Hybrid approaches often work best for production                   ║
║  • Small models (1.5B) can handle real business logic locally         ║
║                                                                      ║
║  NEXT STEPS:                                                         ║
║  1. Review the code in this file                                     ║
║  2. Modify scenarios for your use case                               ║
║  3. Build a hybrid system for production                             ║
║  4. Add RAG for domain-specific knowledge                           ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
""")


if __name__ == "__main__":
    main()
