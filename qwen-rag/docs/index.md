# Qwen + RAG

**Author:** Rakibul Hassan  
**Company:** Link3 Technologies  
**Date:** January 2025

---

## Overview

Qwen + RAG combines Qwen 2.5 1.5B local LLM with Retrieval-Augmented Generation for enhanced knowledge-based responses.

## What is RAG?

RAG (Retrieval-Augmented Generation) enhances LLM responses by:
1. Retrieving relevant documents from a knowledge base
2. Augmenting the prompt with retrieved context
3. Generating responses with accurate, up-to-date information

```
User Query
     │
     ▼
┌─────────────┐
│  Retriever  │ ─────▶ Vector Database
└─────────────┘
     │
     ▼
┌─────────────┐
│   Augment   │ ─────▶ Add context to prompt
└─────────────┘
     │
     ▼
┌─────────────┐
│    LLM      │ ─────▶ Generate response
└─────────────┘
     │
     ▼
  Response
```

## Scripts

| Script | Description |
|--------|-------------|
| `qwen_rag_demo.py` | Full RAG implementation |
| `qwen_simple_rag.py` | Basic RAG example |
| `qwen_vector_storage.py` | Vector storage utilities |

## Quick Start

```python
from qwen_rag import RAGPipeline

# Initialize
rag = RAGPipeline(
    model="qwen2.5-coder-1.5b-instruct",
    vector_store="./vector_store"
)

# Query
response = rag.query("What are the common ISP troubleshooting steps?")
print(response)
```

## Vector Storage

```python
from qwen_vector_storage import VectorStore

# Create store
store = VectorStore(embedding_model="nomic-embed-text")

# Add documents
store.add_documents([
    {"content": "ONT red light indicates fiber issue", "metadata": {"code": "ISP-001"}},
    {"content": "Router restart fixes most WiFi issues", "metadata": {"code": "ISP-002"}}
])

# Search
results = store.search("my internet stopped working", top_k=3)
```

## Benefits

| Benefit | Description |
|---------|-------------|
| Accuracy | Responses based on actual documents |
| Freshness | Knowledge base can be updated |
| Attribution | Sources can be cited |
| Hallucination | Reduced by grounding in documents |

## Use Cases

1. **Technical Support** - Pull relevant troubleshooting guides
2. **Policy Q&A** - Answer based on company documentation
3. **Training** - Provide context-aware learning materials

---

## Related Documentation

- [Getting Started](../getting-started/index.md)
- [ISP Classifier](../isp-classifier/index.md)
- [Enterprise Apps](../enterprise-apps/index.md)