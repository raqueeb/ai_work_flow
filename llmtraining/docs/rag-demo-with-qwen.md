# RAG Demo with Qwen 2.5 1.5B

This demonstration shows how to build a simple Retrieval-Augmented Generation (RAG) system using the Qwen 2.5 1.5B parameter model via LM Studio. The demo uses a small text corpus about ISP operations to illustrate how enterprises can deploy local, private AI solutions without relying on cloud APIs.

## Overview

Retrieval-Augmented Generation (RAG) combines the power of large language models with external knowledge retrieval. This approach:
- Reduces hallucinations by grounding responses in retrieved documents
- Allows updating the knowledge base without retraining the model
- Keeps sensitive data entirely on-premise
- Works efficiently with smaller models like Qwen 2.5 1.5B

## Prerequisites

1. **LM Studio** running with Qwen 2.5 1.5B Instruct model loaded and API server started on `http://localhost:1234`
2. Python 3.11+
3. Required Python packages:
   ```bash
   pip install sentence-transformers faiss-cpu numpy requests
   ```

## How the Demo Works

1. **Document Loading**: Loads a sample text file containing ISP-related information
2. **Text Chunking**: Splits the document into overlapping chunks for better context retention
3. **Embedding Generation**: Uses a sentence transformer model (`all-MiniLM-L6-v2`) to create vector embeddings for each chunk
4. **Vector Storage**: Stores embeddings in a FAISS index for efficient similarity search
5. **Query Processing**: 
   - Converts user query to an embedding
   - Retrieves top-k most relevant chunks from the vector store
   - Constructs a prompt with the retrieved context and the original question
   - Sends the prompt to the local Qwen 2.5 1.5B model via LM Studio's API
   - Returns the generated response

## Enterprise Benefits

- **Data Privacy**: All processing happens locally - no data leaves your network
- **Cost Effective**: No per-token API charges; runs on existing hardware
- **Customizable**: Easy to update with domain-specific documents
- **Scalable**: Can handle growing knowledge bases by adjusting chunk size and retrieval parameters
- **Compliant**: Meets data sovereignty requirements for regulated industries

## Files in This Demo

- `rag_demo_qwen.py`: Main demonstration script
- `sample_isp_data.txt`: Sample ISP knowledge base (created automatically if missing)
- `requirements.txt`: List of required Python packages

## Running the Demo

1. Ensure LM Studio is running with Qwen 2.5 1.5B Instruct loaded and API server started
2. Install required packages: `pip install -r requirements.txt`
3. Run the script: `python rag_demo_qwen.py`
4. Follow the prompts to ask questions about the sample ISP data

## Sample Output

```
Initializing RAG system with Qwen 2.5 1.5B...
Loading sample ISP data...
Creating embeddings and building vector index...
RAG system ready! Ask questions about ISP operations (type 'quit' to exit)

> What are the common causes of fiber cuts in ISP networks?
Based on the retrieved context:
Fiber cuts in ISP networks commonly occur due to:
1. Construction activities (excavation, drilling)
2. Natural disasters (floods, earthquakes, landslides)
3. Rodent damage
4. Vandalism or theft
5. Accidental damage during maintenance

The local LLM processed this query using retrieved context from the ISP knowledge base.
```

## Customizing for Your Enterprise

1. **Replace the Sample Data**: 
   - Replace `sample_isp_data.txt` with your own documents (technical manuals, SOPs, FAQs, etc.)
   - Supported formats: plain text (extend the script for PDF, DOCX, etc.)

2. **Adjust Chunking Parameters**:
   - Modify `chunk_size` and `chunk_overlap` in the script based on your document structure
   - Smaller chunks for precise retrieval, larger chunks for more context

3. **Tune Retrieval**:
   - Change `top_k` to retrieve more or fewer relevant chunks
   - Experiment with different similarity metrics in FAISS

4. **Enhance the Prompt**:
   - Modify the prompt template in `generate_response()` to include instructions, role definitions, or formatting requirements
   - Add enterprise-specific guidelines for the LLM's behavior

## Performance Considerations

- **Embedding Model**: The `all-MiniLM-L6-v2` model is lightweight and efficient for CPU-based embedding generation
- **Vector Store**: FAISS provides fast similarity search even with thousands of documents
- **LLM Inference**: Qwen 2.5 1.5B runs efficiently on consumer GPUs or modern CPUs via LM Studio
- **Batch Processing**: For multiple queries, consider batching embedding generation for better throughput

## Security Notes

- All data processing occurs on your local machine
- No data is sent to external APIs or cloud services
- The knowledge base remains entirely within your control
- Network traffic is limited to localhost communication with LM Studio

## Troubleshooting

- **Connection Errors**: Ensure LM Studio API server is running on port 1234
- **Model Not Loaded**: Verify Qwen 2.5 1.5B Instruct is loaded in LM Studio
- **Package Issues**: Install required packages with `pip install sentence-transformers faiss-cpu numpy requests`
- **CUDA Errors**: If using GPU, ensure proper drivers and CUDA toolkit are installed

## Next Steps for Enterprise Deployment

1. **Knowledge Base Expansion**: 
   - Ingest internal documentation, ticket histories, and technical guides
   - Implement automated document processing pipelines

2. **Integration Points**:
   - Connect to CRM/ERP systems for contextual responses
   - Integrate with helpdesk platforms for automated ticket responses
   - Create API endpoints for internal applications

3. **Monitoring & Feedback**:
   - Log queries and responses for quality assessment
   - Implement human-in-the-loop feedback for continuous improvement
   - Track retrieval relevance and LLM accuracy metrics

4. **Advanced Features**:
   - Add query routing for different document types
   - Implement conversation history for contextual follow-ups
   - Add multi-language support with appropriate embedding models

---

*This demo demonstrates that enterprises can leverage powerful AI capabilities locally using modest hardware, ensuring data privacy, reducing costs, and maintaining full control over their AI infrastructure.*