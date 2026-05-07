# Customer SLA Management - Service Level Agreement Tool

> Intelligent SLA classification and compliance monitoring using local LLM

## Overview

The **SLA LLM Assistant** (`sla_llm_assistant.py`) replaces rigid rule-based SLA classification with natural language understanding. Instead of hundreds of if-else statements to handle every business scenario, a small LLM analyzes customer profiles and ticket descriptions to intelligently classify service tiers and predict compliance risks.

---

## Features

### 1. Customer SLA Tier Classification
- **Bronze** — Standard support, 24h response, 72h resolution, 99.0% uptime
- **Silver** — Priority support, 12h response, 48h resolution, 99.5% uptime
- **Gold** — VIP support, 4h response, 24h resolution, 99.9% uptime
- **Platinum** — Critical support, 1h response, 8h resolution, 99.99% uptime

### 2. Ticket Priority Assessment
The LLM analyzes ticket descriptions to determine:
- Priority level (Critical, High, Medium, Low)
- Response and resolution deadlines
- SLA breach risk assessment

### 3. Breach Risk Detection
- Monitors open tickets against SLA guarantees
- Predicts breach timing based on ticket age and complexity
- Provides risk factors and recommended actions

### 4. Compliance Reporting
- Generates natural language compliance summaries
- Analyzes breach patterns by customer tier
- Provides actionable recommendations

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     SLA LLM ASSISTANT                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Customer Registration                                           │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Business Description → LLM → SLA Tier Classification    │   │
│  │  "Mid-size hospital, emergency services, 24/7 ops"        │   │
│  │                                    ↓                       │   │
│  │                              PLATINUM (99.99%)             │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  Ticket Processing                                               │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Ticket Description → LLM → Priority + Deadlines         │   │
│  │  "Patient records system unreachable"                    │   │
│  │                                    ↓                       │   │
│  │                       CRITICAL (1h response, 4h resolve) │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  Compliance Monitoring                                           │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Ticket Age + Tier Guarantees → LLM → Breach Risk Report │   │
│  │  12 hours elapsed, 24h resolution, Gold tier              │   │
│  │                                    ↓                       │   │
│  │                   AT RISK - 12 hours until potential     │   │
│  │                   breach. Recommend immediate escalation   │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Running the SLA Assistant

### Prerequisites
1. **LM Studio** running with a model loaded (Qwen 2.5 or Gemma)
2. **Local server** active on `http://localhost:1234`

### Quick Start
```bash
cd c:\Downloads\classifier-app
python sla_llm_assistant.py
```

### What You'll See
1. **Customer Registration** — LLM classifies 5 sample businesses into SLA tiers
2. **Ticket Creation** — Creates tickets and assigns priorities using AI
3. **SLA Health Check** — Monitors breach risks on open tickets
4. **Escalation** — Demonstrates priority escalation workflow
5. **Resolution** — Marks tickets resolved and checks for breaches
6. **Compliance Report** — LLM generates natural language summary

---

## LLM-Powered Decisions

### Customer Classification (Rule-Based vs LLM)

**Rule-Based Approach (Brittle):**
```python
if "hospital" in description or "medical" in description:
    tier = "Platinum"
elif "small" in description or "home" in description:
    tier = "Bronze"
else:
    tier = "Silver"
```

**LLM Approach (Flexible):**
```
Input: "We run a small dental clinic with 5 staff, mostly need 
        email and basic browsing"

LLM Output:
{
  "tier": "Silver",
  "confidence": 0.82,
  "reasoning": "Small team with basic needs. No compliance 
                requirements mentioned. Dental services often 
                benefit from priority support but small scale 
                justifies Silver over Gold.",
  "recommended_features": ["email support", "business hours coverage"]
}
```

### Ticket Priority (Rule-Based vs LLM)

**Rule-Based (Limited):**
```python
if "critical" in text or "emergency" in text:
    priority = "Critical"
```

**LLM (Contextual):**
```
Input: "VPN keeps disconnecting during important client calls"

LLM Output:
{
  "priority": "High",
  "response_deadline_hours": 4,
  "resolution_deadline_hours": 12,
  "sla_breach_risk": "Medium",
  "justification": "Revenue-impacting issue affecting client 
                   relationships. VPN reliability is critical 
                   for business operations."
}
```

---

## SLA Tier Details

| Tier | Response Time | Resolution Time | Uptime | Support Hours | Monthly Cost |
|------|---------------|-----------------|--------|---------------|--------------|
| Bronze | 24 hours | 72 hours | 99.0% | Business Hours | $29.99 |
| Silver | 12 hours | 48 hours | 99.5% | Business + Email | $79.99 |
| Gold | 4 hours | 24 hours | 99.9% | 24/7 Phone + Email | $199.99 |
| Platinum | 1 hour | 8 hours | 99.99% | 24/7 Dedicated | $499.99 |

---

## Integration Points

### With ISP Ticket Classifier
```python
# After classifying an ISP ticket
ticket_classified = classify_ticket(ticket_text)

# Check customer SLA based on customer ID
customer_tier = get_customer_tier(customer_id)
deadline = calculate_deadline(ticket_classified.priority, customer_tier)
```

### With ERP Approval System
```python
# SLA tier can affect approval thresholds
sla_tier = customer.sla_tier
if sla_tier == "Platinum":
    auto_approve_threshold = 50000  # Higher for VIP
else:
    auto_approve_threshold = 10000
```

---

## Customization

### Modify SLA Tiers
Edit the `SLA_TIERS` dictionary:
```python
SLA_TIERS = {
    "Bronze": {
        "response_time_hours": 24,
        "resolution_time_hours": 72,
        "uptime_percent": 99.0,
        # ... add custom fields
    }
}
```

### Adjust LLM Behavior
Change the system prompts in these functions:
- `classify_customer_sla()` — Customer classification
- `assess_ticket_priority()` — Priority assessment
- `check_sla_breach_risk()` — Breach detection
- `generate_sla_report()` — Report generation

### Switch Models
```python
# In sla_llm_assistant.py
MODEL_NAME = "qwen2.5-coder-1.5b-instruct"  # Use Qwen
# or
MODEL_NAME = "gemma-4-2b-it"  # Use Gemma for better reasoning
```

---

## Benefits Over Rule-Based Systems

| Aspect | Rule-Based | LLM-Powered |
|--------|------------|-------------|
| **Flexibility** | Must add rules for every scenario | Handles unseen patterns |
| **Maintenance** | Hundreds of rules to update | Prompt tuning only |
| **Context Understanding** | Keyword matching only | Full business context |
| **Edge Cases** | Often misclassified | Intelligently handled |
| **Consistency** | Can contradict across rules | Coherent decision-making |

---

## Example Output

```
🔍 Analyzing customer for SLA tier classification...
   ✓ Assigned to Platinum tier (confidence: 91%)
   → Reasoning: Healthcare facility with emergency services
                 requires critical-level SLA. 24/7 operations
                 and patient safety considerations demand
                 immediate response capabilities.

🔍 Analyzing ticket for priority assessment...
   ✓ Priority: Critical
   → SLA: Response within 1h, Resolution within 8h
   → Risk Assessment: High breach risk

⚠️  AT RISK - Resolution breach in ~4.2 hours
   → Risk factors: High priority, customer has VIP tier
   → Recommendations: Escalate to senior engineer,
                      notify customer of ETA
```

---

*Part of the Link3 Enterprise AI Automations suite — local LLM-powered workflows for ISP operations.*