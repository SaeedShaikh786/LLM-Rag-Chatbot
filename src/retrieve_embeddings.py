'''
from src.generate_embeddings import get_gemini_embeddings
from src.store_embeddings import index

def retrieve_from_pinecone(query, top_k=5, namespace="default"):
    query_embedding = get_gemini_embeddings([query])[0]

    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True,
        namespace=namespace
    )

    retrieved_chunks = [match['metadata']['text'] for match in results['matches']]
    return retrieved_chunks
'''
import os
from pinecone import Pinecone
from src.generate_embeddings import get_gemini_embeddings
from src.config import PINECONE_API_KEY

# Initialize Pinecone client
pc = Pinecone(api_key=PINECONE_API_KEY)

# Initialize Pinecone client
#pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

#index_name = "llm-chatbot"

def retrieve_from_pinecone(query, top_k=6, namespace="default",index_name="llm-chatbot"):
    index = pc.Index(index_name)
    query_embedding = get_gemini_embeddings([query])[0]

    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True,
        namespace=namespace
    )

    retrieved_chunks = [match['metadata']['text'] for match in results['matches']]
    return retrieved_chunks