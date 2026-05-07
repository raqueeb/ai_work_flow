# Qwen + RAG - Bangla

**লেখক:** রাকিবুল হাসান  
**প্রতিষ্ঠান:** লিংক3 টেকনোলজিস  
**তারিখ:** জানুয়ারি ২০২৫

---

## ওভারভিউ

Qwen + RAG হলো Qwen 2.5 1.5B local LLM এবং Retrieval-Augmented Generation এর সমন্বয়। এটা knowledge-based responses দেওয়ার জন্য enhanced।

## RAG কি?

RAG (Retrieval-Augmented Generation) LLM responses বাড়ায়:
1. Knowledge base থেকে relevant documents retrieve করে
2. Retrieved context দিয়ে prompt augment করে
3. Accurate, up-to-date information দিয়ে response generate করে

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
│   Augment   │ ─────▶ Prompt-এ context যোগ করুন
└─────────────┘
     │
     ▼
┌─────────────┐
│    LLM      │ ─────▶ Response generate করুন
└─────────────┘
     │
     ▼
  Response
```

এভাবে কাজ করে RAG।

## স্ক্রিপ্টগুলো

| স্ক্রিপ্ট | বিবরণ |
|--------|-------------|
| `qwen_rag_demo.py` | Full RAG implementation |
| `qwen_simple_rag.py` | Basic RAG example |
| `qwen_vector_storage.py` | Vector storage utilities |

## দ্রুত শুরু

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

সহজ এবং straightforward।

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

## সুবিধাগুলো

| সুবিধা | বিবরণ |
|--------|-------------|
| Accuracy | Actual documents থেকে responses |
| Freshness | Knowledge base update করা যায় |
| Attribution | Sources cite করা যায় |
| Hallucination | documents-এ ground করে reduce করা যায় |

## ব্যবহারের ক্ষেত্র

1. **Technical Support** - Relevant troubleshooting guides pull করুন
2. **Policy Q&A** - Company documentation অনুযায়ী answer দিন
3. **Training** - Context-aware learning materials provide করুন

---

## সম্পর্কিত ডকুমেন্টেশন

- [শুরু করুন](../getting-started/index.md)
- [ISP Classifier](../isp-classifier/index.md)
- [Enterprise Apps](../enterprise-apps/index.md)