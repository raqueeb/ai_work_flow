# HR Assistant

**Author:** Rakibul Hassan  
**Company:** Link3 Technologies  
**Date:** January 2025

---

## Overview

The HR Assistant suite provides AI-powered HR automation tools for leave management, employee queries, and sales funnel optimization.

## Components

### 1. HR Manager - Leave Approval

Automates leave request processing and approval workflow.

```python
class HRManagerApproveLeave:
    def __init__(self, llm):
        self.llm = llm
    
    def process_leave_request(self, request: dict) -> dict:
        prompt = f"""Review this leave request and decide:
        
        Employee: {request['employee']}
        Type: {request['type']}
        Duration: {request['start']} to {request['end']}
        Reason: {request['reason']}
        
        Consider:
        - Leave balance
        - Team availability
        - Urgency of work
        - Past leave patterns
        """
        
        return self.llm.decide(prompt)
```

### 2. HR Assistant Chatbot

Handles employee queries about policies, benefits, and procedures.

### 3. Sales Funnel AI Closer

AI-powered sales automation for converting leads.

```python
class SalesFunnelAICloser:
    def score_lead(self, lead_data: dict) -> float:
        """Score leads based on conversion probability"""
        
    def generate_response(self, lead: dict, context: str) -> str:
        """Generate personalized outreach"""
```

## Features

| Feature | Description |
|---------|-------------|
| Leave Processing | Auto-approve or flag for review |
| Policy Q&A | Instant answers to HR questions |
| Lead Scoring | Prioritize high-value leads |
| Response Generation | Personalized sales outreach |
| Sentiment Analysis | Detect employee concerns |

## Scripts

| Script | Description |
|--------|-------------|
| `HR_manager_Approve_leave.py` | Leave approval automation |
| `HR_Assistant.py` | Employee query chatbot |
| `Link3_Sales_Funnel_AI_Closer.py` | Sales funnel automation |

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                    HR Assistant                      │
├─────────────┬─────────────┬─────────────────────────┤
│ HR Manager  │ HR Chatbot  │ Sales Funnel AI Closer  │
├─────────────┼─────────────┼─────────────────────────┤
│ Leave API   │ Policy DB   │ CRM Integration         │
│ Calendar    │ Benefits    │ Lead Database          │
│ Team Mgmt   │ Procedures  │ Email/Telephony        │
└─────────────┴─────────────┴─────────────────────────┘
                    │
                    ▼
              ┌──────────┐
              │  LLM     │
              │ (Qwen/   │
              │ Gemma)   │
              └──────────┘
```

---

## Related Documentation

- [Getting Started](../getting-started/index.md)
- [Enterprise Apps](../enterprise-apps/index.md)
- [SLA System](../sla-system/index.md)