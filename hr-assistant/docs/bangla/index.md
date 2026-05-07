# HR Assistant - Bangla

**লেখক:** রাকিবুল হাসান  
**প্রতিষ্ঠান:** লিংক3 টেকনোলজিস  
**তারিখ:** জানুয়ারি ২০২৫

---

## ওভারভিউ

HR Assistant suite দিয়ে leave management, employee queries এবং sales funnel optimization এর জন্য AI-powered automation tools আছে।

## কম্পোনেন্টগুলো

### ১. HR Manager - Leave Approval

Leave request processing এবং approval workflow স্বয়ংক্রিয় করে।

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

এভাবে leave request প্রসেস করে। automatic approve বা flag for review করা যায়।

### ২. HR Assistant Chatbot

Employee queries হ্যান্ডেল করে policy, benefits এবং procedures নিয়ে।

### ৩. Sales Funnel AI Closer

Lead convert করার জন্য AI-powered sales automation।

```python
class SalesFunnelAICloser:
    def score_lead(self, lead_data: dict) -> float:
        """Lead-দের conversion probability অনুযায়ী score করুন"""
        
    def generate_response(self, lead: dict, context: str) -> str:
        """Personalized outreach generate করুন"""
```

## বৈশিষ্ট্যগুলো

| বৈশিষ্ট্য | বিবরণ |
|---------|-------------|
| Leave Processing | auto-approve বা review-এ flag করুন |
| Policy Q&A | HR প্রশ্নের তাৎক্ষণিক উত্তর |
| Lead Scoring | high-value lead গুলো prioritize করুন |
| Response Generation | personalized sales outreach |
| Sentiment Analysis | employee concerns detect করুন |

## স্ক্রিপ্টগুলো

| স্ক্রিপ্ট | বিবরণ |
|--------|-------------|
| `HR_manager_Approve_leave.py` | Leave approval automation |
| `HR_Assistant.py` | Employee query chatbot |
| `Link3_Sales_Funnel_AI_Closer.py` | Sales funnel automation |

## আর্কিটেকচার

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

এভাবে সব component মিলে কাজ করে।

---

## সম্পর্কিত ডকুমেন্টেশন

- [শুরু করুন](../getting-started/index.md)
- [Enterprise Apps](../enterprise-apps/index.md)
- [SLA System](../sla-system/index.md)