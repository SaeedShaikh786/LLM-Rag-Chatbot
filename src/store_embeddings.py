import os
import uuid
from pinecone import Pinecone, ServerlessSpec

# Initialize Pinecone client
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

def store_in_pinecone(chunks, embeddings, namespace="default", index_name="rag-chatbot", dimension=768):
    # Create the index if it doesn't exist
    if index_name not in pc.list_indexes().names():
        print(f"Index '{index_name}' not found. Creating new index...")
        pc.create_index(
            name=index_name,
            dimension=dimension,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )
        print(f"✅ Index '{index_name}' created successfully!")

    # Connect to the index
    index = pc.Index(index_name)

    # Prepare vectors
    to_upsert = []
    for doc, embed in zip(chunks, embeddings):
        if embed is not None:
            vector = {
                "id": str(uuid.uuid4()),
                "values": embed,
                "metadata": {
                    "text": doc.page_content,
                    "page": doc.metadata.get("page", 0)
                }
            }
            to_upsert.append(vector)

    # Upsert into Pinecone
    index.upsert(vectors=to_upsert, namespace=namespace)
    print(f"✅ Stored {len(to_upsert)} vectors in index '{index_name}' under namespace '{namespace}'")



'''
import uuid
from pinecone import Pinecone
from src.config import PINECONE_API_KEY

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index("rag-chatbot")

def store_in_pinecone(chunks, embeddings, namespace="default"):
    to_upsert = []

    for doc, embed in zip(chunks, embeddings):
        if embed is not None:
            vector = {
                "id": str(uuid.uuid4()),
                "values": embed,
                "metadata": {
                    "text": doc.page_content,
                    "page": doc.metadata.get("page", 0)
                }
            }
            to_upsert.append(vector)

    index.upsert(vectors=to_upsert, namespace=namespace) '''