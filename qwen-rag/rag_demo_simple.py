"""
================================================================================
RAG Demo with Qwen 2.5 1.5B - Simple Retrieval-Augmented Generation
================================================================================
A simple demonstration showing how smaller LLMs can use RAG effectively.
Shows the complete RAG pipeline: Index → Retrieve → Generate

Run: python rag_demo_simple.py
================================================================================
"""

import json
import os

# ============================================================================
# STEP 1: VECTOR STORE - Simple in-memory implementation
# ============================================================================
class SimpleVectorStore:
    """
    A simple vector store that uses TF-IDF instead of embeddings.
    This makes the demo run without needing sentence-transformers.
    For production, use FAISS + sentence-transformers.
    """
    
    def __init__(self):
        self.documents = []  # List of text chunks
        self.index = {}     # Simple word -> document index
        
    def add_documents(self, docs):
        """Add documents to the store"""
        self.documents = docs
        
        # Build simple inverted index
        for i, doc in enumerate(docs):
            words = set(doc.lower().split())
            for word in words:
                if word not in self.index:
                    self.index[word] = []
                self.index[word].append(i)
        
        print(f"   ✓ Added {len(docs)} documents to vector store")
    
    def search(self, query, top_k=3):
        """Find most relevant documents using simple keyword matching"""
        query_words = set(query.lower().split())
        
        # Score each document
        scores = {}
        for word in query_words:
            if word in self.index:
                for doc_idx in self.index[word]:
                    scores[doc_idx] = scores.get(doc_idx, 0) + 1
        
        # Sort by score
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        # Return top k documents
        results = []
        for idx, score in ranked[:top_k]:
            results.append({
                "document": self.documents[idx],
                "score": score,
                "index": idx
            })
        
        return results


# ============================================================================
# STEP 2: KNOWLEDGE BASE - ISP Operations Data
# ============================================================================
KNOWLEDGE_BASE = [
    # Fiber & Network Issues
    """Fiber cuts are the most common cause of network outages. 
    Common causes include construction digging, natural disasters, 
    rodent damage, and accidental damage. MTTR (mean time to repair) 
    is typically 4-12 hours depending on location.""",
    
    """Signal degradation occurs when fiber bends exceed minimum radius, 
    connectors are contaminated, or temperature extremes affect performance. 
    Customers typically report slow speeds or intermittent connectivity.""",
    
    """For ONT (Optical Network Terminal) red light issues: check fiber 
    connection, verify power supply, check for bent fiber, and ensure 
    the signal levels are within specification. If issues persist, 
    replace the ONT unit.""",
    
    # Billing & Support
    """Billing complaints should be handled with patience. Common issues 
    include unexpected charges, proration confusion, and payment failures. 
    Always verify the customer's account and explain charges clearly.""",
    
    """L1 support handles basic connectivity: rebooting equipment, speed 
    tests, account checks. L2 handles signal analysis and configuration. 
    L3 handles fiber plant and infrastructure issues.""",
    
    # SLA Information
    """Service Level Agreements: Bronze tier offers 24h response and 72h 
    resolution. Silver tier: 12h response, 48h resolution. Gold tier: 
    4h response, 24h resolution. Platinum tier: 1h response, 8h resolution.""",
    
    # Customer Onboarding
    """New customer installation process: 1) Site survey, 2) Plan selection, 
    3) Installation appointment, 4) Equipment setup (ONT, router, WiFi), 
    5) Testing speeds, 6) Billing activation. Average time: 3-5 days.""",
    
    # Network Monitoring
    """Key metrics: Latency should be under 50ms for local, under 200ms 
    for international. Packet loss under 1%. Jitter under 30ms for VoIP. 
    Uptime target: 99.9% for business customers.""",
    
    # Troubleshooting
    """When customers report no internet: 1) Check ONT status lights, 
    2) Verify all cable connections, 3) Try rebooting the router, 
    4) Run speed test, 5) Check for outages in the area.""",
    
    """PPPoE configuration issues: ensure username is exact (often includes @isp.net), 
    password is correct, service name is empty unless required. Try cloning 
    MAC address if ISP requires it.""",
]

# ============================================================================
# STEP 3: RAG PIPELINE FUNCTIONS
# ============================================================================
def initialize_rag():
    """Initialize the RAG system - Index the knowledge base"""
    print("\n" + "="*60)
    print("STEP 1: Initializing RAG System")
    print("="*60)
    
    vector_store = SimpleVectorStore()
    vector_store.add_documents(KNOWLEDGE_BASE)
    
    print(f"\n✓ Vector store ready with {len(KNOWLEDGE_BASE)} documents")
    return vector_store


def retrieve(query, vector_store, top_k=3):
    """Retrieve relevant documents from the knowledge base"""
    print("\n" + "="*60)
    print("STEP 2: Retrieving Relevant Documents")
    print("="*60)
    print(f"Query: {query}")
    
    results = vector_store.search(query, top_k)
    
    print(f"\nFound {len(results)} relevant documents:")
    for i, result in enumerate(results, 1):
        print(f"\n  Document {i} (relevance score: {result['score']}):")
        # Show first 150 chars
        text = result['document'].replace('\n', ' ')[:150]
        print(f"  → {text}...")
    
    return [r['document'] for r in results]


def generate(query, context_docs, model_name="qwen2.5-coder-1.5b-instruct"):
    """Generate answer using Qwen with retrieved context"""
    print("\n" + "="*60)
    print("STEP 3: Generating Response with Qwen 2.5 1.5B")
    print("="*60)
    
    # Combine retrieved documents as context
    context = "\n\n".join([f"- {doc}" for doc in context_docs])
    
    # Build prompt
    prompt = f"""Based on the following information, answer the question.

Information:
{context}

Question: {query}

Answer concisely and only use the information provided above."""
    
    # Call LM Studio
    try:
        import urllib.request
        
        payload = {
            "model": model_name,
            "messages": [
                {"role": "system", "content": "You are a helpful ISP support assistant."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 400
        }
        
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            "http://localhost:1234/v1/chat/completions",
            data=data,
            headers={"Content-Type": "application/json"}
        )
        
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode("utf-8"))
            answer = result["choices"][0]["message"]["content"]
            
        print(f"\n🤖 Answer from Qwen 2.5:\n")
        print(answer)
        
        return answer
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("   Make sure LM Studio is running with a model loaded.")
        return None


# ============================================================================
# STEP 4: DEMONSTRATION QUERIES
# ============================================================================
DEMO_QUERIES = [
    "What causes fiber cuts and how long does repair take?",
    "How do I troubleshoot a customer with no internet?",
    "What's the response time for Gold tier SLA?",
    "What is the customer onboarding process?",
]


def run_demo(vector_store):
    """Run demonstration with sample queries"""
    print("\n" + "="*60)
    print("       RAG DEMONSTRATION WITH QWEN 2.5 1.5B")
    print("="*60)
    print("""
This demo shows how RAG helps smaller LLMs answer questions 
by retrieving relevant information from a knowledge base.

Instead of relying on the model's limited training data,
RAG retrieves up-to-date information and provides it as context.

The result: Smaller, faster models can answer specialized 
questions accurately!
""")
    
    for i, query in enumerate(DEMO_QUERIES, 1):
        print("\n" + "="*60)
        print(f"DEMO QUERY {i}/4: {query}")
        print("="*60)
        
        # RAG Pipeline: Retrieve → Generate
        docs = retrieve(query, vector_store)
        generate(query, docs)
        
        print("\n" + "-"*60)


# ============================================================================
# STEP 5: INTERACTIVE MODE
# ============================================================================
def interactive_mode(vector_store):
    """Allow user to ask their own questions"""
    print("\n" + "="*60)
    print("INTERACTIVE MODE")
    print("="*60)
    print("Type your questions about ISP operations.")
    print("Type 'quit' to exit.\n")
    
    while True:
        try:
            query = input("\n❓ Your question: ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("\nGoodbye! Thanks for using RAG Demo.")
                break
            
            if not query:
                continue
            
            docs = retrieve(query, vector_store)
            generate(query, docs)
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================
if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════╗
║           RAG Demo with Qwen 2.5 1.5B                         ║
║        Retrieval-Augmented Generation Demo                     ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Initialize RAG
    vector_store = initialize_rag()
    
    # Run demo
    run_demo(vector_store)
    
    # Ask for interactive mode
    print("\n" + "="*60)
    response = input("Run demo again? (y/n): ").strip().lower()
    
    if response == 'y':
        interactive_mode(vector_store)
    else:
        print("\nThanks for using RAG Demo! 🚀")