# ISP SLA Assistant - Service Level Agreement Tool with LLM

## Overview

The ISP SLA Assistant is a comprehensive tool that uses a small LLM to classify customer SLA tiers, track compliance, and detect potential breaches before they occur. This tool replaces complex rule-based systems with intelligent natural language processing for better accuracy and flexibility.

## Features

- **Customer Classification**: Automatically classify customers into appropriate SLA tiers (Bronze → Platinum) based on business needs
- **Ticket Priority Assessment**: Intelligently assess ticket priority based on business impact using LLM analysis
- **SLA Breach Detection**: Proactively detect tickets at risk of SLA breach before they occur
- **Compliance Reporting**: Generate detailed SLA compliance reports using LLM analysis
- **Dashboard Visualization**: Real-time dashboard showing SLA metrics and ticket status

## Architecture

### Core Components

1. **SLAManager**: Central class managing all SLA operations
2. **Customer**: Customer data model with SLA tier assignment
3. **Ticket**: Ticket data model with priority and deadline tracking
4. **LLM Integration**: Functions for calling local LLM via LM Studio

### SLA Tiers

The system defines four SLA tiers with specific guarantees:

| Tier | Response Time | Resolution Time | Uptime | Support Hours | Monthly Price |
|------|---------------|-----------------|--------|--------------|---------------|
| Bronze | 24 hours | 72 hours | 99.0% | Business Hours | Tk29.99 |
| Silver | 12 hours | 48 hours | 99.5% | Business Hours + Email | Tk79.99 |
| Gold | 4 hours | 24 hours | 99.9% | 24/7 Phone + Email | Tk199.99 |
| Platinum | 1 hour | 8 hours | 99.99% | 24/7 Dedicated Line | Tk499.99 |

### Priority Levels

Ticket priorities are mapped to SLA requirements:

- **Critical**: 1 hour response, 4 hours resolution
- **High**: 4 hours response, 12 hours resolution
- **Medium**: 8 hours response, 24 hours resolution
- **Low**: 24 hours response, 48 hours resolution

## Setup Requirements

### Prerequisites

1. **LM Studio**: Must be running on localhost:1234
2. **Model**: Load one of these models in LM Studio:
   - Qwen 2.5 Coder 1.5B Instruct (recommended)
   - Gemma 4B Instruct
3. **API Server**: Enable the API server in LM Studio on port 1234

### Configuration

Update these variables in the script:

```python
BASE_URL = "http://localhost:1234/v1/chat/completions"
MODEL_NAME = "qwen2.5-coder-1.5b-instruct"  # or "gemma-4-2b-it"
```

## Usage

### Basic Usage

```python
from sla_llm_assistant import SLAManager

# Initialize manager
sla = SLAManager()

# Register customer
customer = sla.register_customer(
    customer_id="C001",
    name="Tech Startup",
    business_type="Small startup, 10 employees, VoIP dependent",
    description="Technology company with remote workforce"
)

# Create ticket
ticket = sla.create_ticket(
    customer_id="C001",
    description="VPN connection keeps dropping during client meetings",
    category="Technical"
)

# Check SLA health
health = sla.check_ticket_health("TKT-0001")

# Resolve ticket
sla.resolve_ticket("TKT-0001")

# Generate compliance report
report = sla.get_compliance_report()
```

### Running the Demo

Execute the built-in demonstration:

```bash
python sla_llm_assistant.py
```

The demo will:
1. Register 5 different customers with varying business profiles
2. Create support tickets for each customer
3. Perform SLA health checks
4. Demonstrate ticket escalation
5. Resolve tickets and show dashboard
6. Generate a compliance report

## Key Functions

### Customer Management

- `register_customer(customer_id, name, business_type, description)`: Register new customer and auto-classify SLA tier
- `assign_sla_tier(tier)`: Manually assign SLA tier to customer

### Ticket Management

- `create_ticket(customer_id, description, category)`: Create ticket with LLM priority assessment
- `check_ticket_health(ticket_id)`: Check if ticket is at risk of SLA breach
- `escalate_ticket(ticket_id, reason)`: Escalate ticket priority
- `resolve_ticket(ticket_id)`: Mark ticket as resolved

### Reporting

- `show_dashboard()`: Display SLA dashboard summary
- `get_compliance_report()`: Generate detailed compliance report using LLM

## LLM Integration

The tool uses LM Studio's API to call local LLMs for:

1. **Customer Classification**: Analyzes business description to determine appropriate SLA tier
2. **Ticket Priority**: Assesses business impact and assigns priority based on multiple factors
3. **Breach Detection**: Analyzes ticket age, priority, and customer tier to detect breach risks
4. **Report Generation**: Creates professional compliance reports from ticket data

### Prompt Engineering

The system uses carefully crafted prompts for each LLM interaction:

- **System Role Definition**: Clear role assignment for each analysis type
- **Structured Output**: JSON format for consistent parsing
- **Context Enhancement**: Rich context including SLA guarantees and ticket history
- **Fallback Mechanisms**: Graceful handling of LLM errors

## Benefits

### Traditional vs LLM-Based Approach

| Aspect | Traditional Rule-Based | LLM-Based |
|--------|----------------------|----------|
| Classification | Hardcoded business rules | Natural language understanding |
| Flexibility | Rigid, requires code changes | Adapts to new scenarios |
| Accuracy | Limited by rule complexity | Context-aware analysis |
| Maintenance | Constant rule updates | Self-improving with better models |
| Scalability | Complex rule management | Handles diverse use cases |

### Advantages

1. **Intelligent Classification**: Understands business context beyond simple rules
2. **Proactive Breach Detection**: Identifies risks before they become actual breaches
3. **Adaptive Learning**: Improves with better LLM models
4. **Reduced Complexity**: Eliminates complex rule maintenance
5. **Better Customer Experience**: More accurate SLA assignments

## Limitations

1. **LLM Dependency**: Requires LM Studio running with appropriate model
2. **Response Time**: LLM calls add latency compared to rule-based systems
3. **Cost**: Local inference requires hardware resources
4. **Accuracy Variance**: Performance depends on model quality and prompt engineering

## Future Enhancements

1. **Multiple Model Support**: Support for various local LLM models
2. **Historical Analysis**: Track trends and patterns over time
3. **Automated Escalation**: Automatic escalation based on risk assessment
4. **Integration**: API endpoints for external systems
5. **Advanced Analytics**: Predictive analytics for SLA compliance

## Troubleshooting

### Common Issues

1. **LM Studio Connection Error**
   - Ensure LM Studio is running
   - Verify port 1234 is accessible
   - Check model is loaded and API server enabled

2. **LLM Response Errors**
   - Verify model is appropriate for the task
   - Check prompt formatting
   - Review temperature and max_tokens settings

3. **JSON Parsing Errors**
   - Verify LLM returns valid JSON
   - Check fallback mechanisms are working
   - Review response parsing logic

## License

This tool is provided as-is for educational and demonstration purposes.

## Author

Rakibul Hassan
Date: May 2026