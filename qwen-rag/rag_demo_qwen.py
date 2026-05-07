"""
RAG Demo with Qwen 2.5 1.5B - Local Retrieval-Augmented Generation
Demonstrates how enterprises can use RAG with smaller local LLMs
"""

import os
import re
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import requests
import json

# Configuration
LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"
MODEL_NAME = "qwen2.5-coder-1.5b-instruct"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
CHUNK_SIZE = 200
CHUNK_OVERLAP = 50
TOP_K = 3

# Sample ISP data - created if file doesn't exist
SAMPLE_DATA = """# ISP Operations Knowledge Base

## Fiber Cuts
Fiber cuts are the most common cause of network outages in ISP operations. Common causes include:
1. Construction activities - excavation, drilling, and road work often damage underground cables
2. Natural disasters - floods, earthquakes, and landslides can sever fiber links
3. Rodent damage - rats and other rodents frequently chew through cable insulation
4. Vandalism - intentional cable cutting or theft of copper components
5. Accidental damage - maintenance work or agricultural activities can accidentally damage cables

MTTR for fiber cuts averages 4-12 hours depending on location and severity.

## Signal Degradation
Signal degradation occurs when:
- Fiber bends exceed minimum radius specifications
- Connector contamination or damage
- Splice losses accumulate beyond thresholds
- Temperature extremes affect transceiver performance

Customers typically report slow speeds or intermittent connectivity.

## Billing Issues
Common billing complaints:
1. Unexpected charges - customers disputing items they don't recognize
2. Proration confusion - misunderstanding how partial month billing works
3. Payment processing failures - expired cards, insufficient funds
4. Plan renewal surprises - promotional rates ending

Billing tickets should be routed to billing department with high priority.

## Technical Support
L1 support handles:
- Basic connectivity issues (rebooting ONT/router)
- Speed test guidance
- Account status checks
- Simple troubleshooting steps

L2 support handles:
- Signal level analysis
- Configuration issues
- Equipment replacements
- Escalated connectivity problems

L3 support handles:
- Fiber plant issues
- Network infrastructure problems
- Complex technical escalations

## Service Level Agreements (SLA)
Different tiers have different response times:
- Bronze: 24 hour response, 72 hour resolution
- Silver: 12 hour response, 48 hour resolution
- Gold: 4 hour response, 24 hour resolution
- Platinum: 1 hour response, 8 hour resolution

SLA breach risks should be flagged immediately to management.

## Network Monitoring
Key metrics to monitor:
1. Latency - should be <50ms for local, <200ms for international
2. Packet loss - should be <1% during peak hours
3. Jitter - should be <30ms for voice services
4. Uptime - 99.9% for business, 99.5% for residential

Automated alerts should trigger when thresholds are exceeded.

## Customer Onboarding
New customer installation process:
1. Site survey - check signal availability and installation feasibility
2. Plan selection - help customer choose appropriate speed tier
3. Installation appointment - schedule technician visit
4. Equipment setup - install ONT, router, and configure WiFi
5. Testing - verify speeds and connectivity
6. Billing setup - activate recurring billing

Average onboarding time is 3-5 business days.
"""

def create_sample_data(filename="sample_isp_data.txt"):
    """Create sample ISP data file if it doesn't exist"""
    if not os.path.exists(filename):
        print(f"Creating sample data file: {filename}")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(SAMPLE_DATA)
        return True
    return False

def load_and_chunk_text(filename="sample_isp_data.txt", chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """Load text file and split into overlapping chunks"""
    print(f"Loading text from {filename}...")
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Split into chunks with overlap
    chunks = []
    start = 0
    text_len = len(text)
    
    while start < text_len:
        end = min(start + chunk_size, text_len)
        chunk = text[start:end]
        chunks.append(chunk)
        if end >= text_len:
            break
        start = end - overlap
    
    print(f"Created {len(chunks)} text chunks")
    return chunks

def create_vector_store(chunks, model_name=EMBEDDING_MODEL):
    """Create embeddings and FAISS index from text chunks"""
    print(f"Loading embedding model: {model_name}")
    model = SentenceTransformer(model_name)
    
    print("Generating embeddings...")
    embeddings = model.encode(chunks)
    
    # Create FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings.astype(np.float32))
    
    print(f"Created vector store with {index.ntotal} vectors of dimension {dimension}")
    return index, embeddings, model

def retrieve_relevant_chunks(query, model, index, chunks, top_k=TOP_K):
    """Retrieve top-k most relevant chunks for a query"""
    query_embedding = model.encode([query])[0]
    distances, indices = index.search(np.array([query_embedding]).astype(np.float32), top_k)
    
    retrieved = [chunks[idx] for idx in indices[0]]
    return retrieved, distances[0]

def generate_response(query, context_chunks, model=MODEL_NAME, url=LM_STUDIO_URL):
    """Generate response using Qwen 2.5 via LM Studio API"""
    # Construct context from retrieved chunks
    context = "\n\n---\n\n".join(context_chunks)
    
    # Build prompt with RAG context
    prompt = f"""You are a helpful ISP operations assistant. Use the following context to answer the user's question. If the answer is not in the context, say so.

Context:
{context}

Question: {query}

Answer:"""
    
    # Call LM Studio API
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a helpful ISP operations assistant that answers based on provided context."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 500
    }
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error calling LLM: {str(e)}"

def main():
    """Main RAG demonstration"""
    print("=" * 60)
    print("RAG Demo with Qwen 2.5 1.5B via LM Studio")
    print("=" * 60)
    print("\nInitializing RAG system...")
    
    # Step 1: Create sample data if needed
    create_sample_data()
    
    # Step 2: Load and chunk text
    chunks = load_and_chunk_text()
    
    # Step 3: Create vector store
    index, embeddings, embedding_model = create_vector_store(chunks)
    
    print("\n" + "=" * 60)
    print("RAG system ready! Ask questions about ISP operations")
    print("Type 'quit' to exit, 'reload' to reload data")
    print("=" * 60 + "\n")
    
    while True:
        try:
            query = input("> ").strip()
            
            if not query:
                continue
            if query.lower() == 'quit':
                print("Goodbye!")
                break
            if query.lower() == 'reload':
                print("Reloading data...")
                chunks = load_and_chunk_text()
                index, embeddings, embedding_model = create_vector_store(chunks)
                print("Data reloaded!")
                continue
            
            # Retrieve relevant chunks
            retrieved_chunks, distances = retrieve_relevant_chunks(
                query, embedding_model, index, chunks
            )
            
            print(f"\n[Retrieved {len(retrieved_chunks)} relevant chunks]")
            for i, (chunk, dist) in enumerate(zip(retrieved_chunks, distances)):
                print(f"  Chunk {i+1} (distance: {dist:.4f}):")
                print(f"  {chunk[:100]}...")
            
            # Generate response
            print("\nGenerating response with Qwen 2.5 1.5B...")
            response = generate_response(query, retrieved_chunks)
            
            print(f"\nAnswer:\n{response}\n")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {str(e)}\n")

if __name__ == "__main__":
    main()