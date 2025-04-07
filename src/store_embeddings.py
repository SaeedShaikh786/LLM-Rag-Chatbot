import os
import uuid
from pinecone import Pinecone, ServerlessSpec

# Initialize Pinecone client
#pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
from src.config import PINECONE_API_KEY
# Initialize Pinecone client
pc = Pinecone(api_key=PINECONE_API_KEY)

def store_in_pinecone(chunks, embeddings, namespace="default", index_name="rag-chatbot", dimension=768, batch_size=100):
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

            # If batch size is reached, upsert the batch and clear the list
            if len(to_upsert) >= batch_size:
                index.upsert(vectors=to_upsert, namespace=namespace)
                print(f"✅ Stored {len(to_upsert)} vectors in index '{index_name}' under namespace '{namespace}'")
                to_upsert = []

    # Upsert any remaining vectors
    if to_upsert:
        index.upsert(vectors=to_upsert, namespace=namespace)
        print(f"✅ Stored {len(to_upsert)} vectors in index '{index_name}' under namespace '{namespace}'")
