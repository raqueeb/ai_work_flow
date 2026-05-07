# ISP Classification

This section documents the ticket classification system that maps customer complaints to specific ISP codes. The system uses local LLMs to understand and categorize incoming tickets.

## Overview

The classification system processes ISP tickets through a multi-stage pipeline:

```mermaid
flowchart TD
    A[Customer Ticket] --> B[Text Preprocessing]
    B --> C[Rule-Based Fast Match]
    C --> D{Match Found?}
    D -->|Yes| E[Return ISP Code]
    D -->|No| F[LLM Classification]
    F --> G[Confidence Score]
    G --> H[Response Template]
    H --> I[Human Review]
    I --> J[Ticket Closed]
```

## Classification Categories

```mermaid
flowchart LR
    A[ISP-001 to ISP-020] --> B[Hardware Issues]
    C[ISP-030 to ISP-050] --> D[Network Problems]
    E[ISP-060 to ISP-070] --> F[Billing Issues]
    G[ISP-080 to ISP-100] --> H[Service Outages]
```

### Hardware Issues (ISP-001 to ISP-020)

| Code | Description |
|------|-------------|
| ISP-001 | Red light / Physical fiber cut |
| ISP-002 | ONT malfunction |
| ISP-003 | Router replacement needed |

### Network Problems (ISP-030 to ISP-050)

| Code | Description |
|------|-------------|
| ISP-030 | Slow connection |
| ISP-031 | Packet loss |
| ISP-032 | DNS resolution failure |

### Billing Issues (ISP-060 to ISP-070)

| Code | Description |
|------|-------------|
| ISP-060 | Invoice dispute |
| ISP-061 | Payment failed |
| ISP-062 | Subscription change |

### Service Outages (ISP-080 to ISP-100)

| Code | Description |
|------|-------------|
| ISP-080 | Planned maintenance |
| ISP-081 | Region-wide outage |
| ISP-082 | Weather-related downtime |

## Classification Workflow

```mermaid
flowchart TD
    subgraph Input["Input Processing"]
        A[Raw Ticket Text] --> B[Clean & Normalize]
        B --> C[Extract Keywords]
    end
    
    subgraph Classification["Classification Engine"]
        C --> D{Keyword Match}
        D -->|Exact| E[ISP Code Found]
        D -->|Partial| F[LLM Query]
        D -->|None| F
        F --> G{Confidence > 80%}
        G -->|Yes| H[High Confidence]
        G -->|No| I[Low Confidence]
    end
    
    subgraph Output["Output"]
        H --> J[Auto-Respond]
        I --> K[Human Review Queue]
        E --> J
        E --> K
    end
```

## Architecture Diagram

```mermaid
flowchart TB
    subgraph Web["Web Interface"]
        A[Streamlit App]
        B[Ticket Input Form]
        C[Results Display]
    end
    
    subgraph API["API Layer"]
        D[FastAPI Server]
        E[Request Validation]
        F[Response Formatting]
    end
    
    subgraph Logic["Business Logic"]
        G[Keyword Matcher]
        H[LLM Classifier]
        I[Confidence Calculator]
    end
    
    subgraph External["External Services"]
        J[LM Studio]
        K[Qwen 2.5 1.5B]
        L[Vector DB]
    end
    
    A --> B --> D --> E --> G
    G --> H
    G --> I
    H --> J --> K
    K --> L
    F --> C
```

## Running the Classifier

### Basic Usage

```bash
cd isp-classifier
python app-classifier1.py
```

### With Reasoning

```bash
python app-reasoning1.py
```

### Streamlit Interface

```bash
streamlit run app-baseline-class.py
```

## Sample Output

```json
{
  "ticket": "My ONT is showing red light",
  "predicted_code": "ISP-002",
  "confidence": 92,
  "justification": "Red light on ONT indicates hardware malfunction",
  "field_dispatch": true
}
```

## Implementation Details

### Rule-Based Matching

```python
FIELD_ISP_CODES = {
    "red light": "ISP-001",
    "fiber cut": "ISP-001",
    "ont": "ISP-002",
    "router": "ISP-003",
}
```

### LLM Fallback

When rules don't match, the system queries the local LLM:

```mermaid
sequenceDiagram
    participant App
    participant LLM as Local LLM
    participant DB as Knowledge Base
    
    App->>DB: Search similar tickets
    DB-->>App: Relevant examples
    App->>LLM: Classification query
    App->>LLM: Include context + examples
    LLM-->>App: ISP Code + Confidence
```

## Next Steps

- [Advanced Reasoning](advanced-reasoning.md) - Chain-of-thought classification
- [RAG System](rag-qwen.md) - Enhance with knowledge retrieval
- [Gemma Version](isp-classification-gemma.md) - Using Gemma 4 E4B model