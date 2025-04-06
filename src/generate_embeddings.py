import google.generativeai as genai
from src.config import GOOGLE_API_KEY

genai.configure(api_key=GOOGLE_API_KEY)

embedding_model = genai.embed_content

def get_gemini_embeddings(texts, model="models/text-embedding-004", task_type="retrieval_document"):
    embeddings = []
    for txt in texts:
        try:
            res = embedding_model(
                model=model,
                content=txt,
                task_type=task_type,
                title="chunk"
            )
            embeddings.append(res["embedding"])
        except Exception as e:
            print(f"Embedding failed for a chunk: {e}")
            embeddings.append(None)
    return embeddings