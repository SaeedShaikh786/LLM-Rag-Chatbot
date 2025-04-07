#import google.generativeai as genai
#from src.config import GOOGLE_API_KEY
import time
#genai.configure(api_key=GOOGLE_API_KEY)

#embedding_model = genai.embed_content


'''
def get_gemini_embeddings(texts, model="models/text-embedding-004", task_type="retrieval_document"):
    start=time.time()
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
    end=time.time()
    print(f"Time taken to generate embeddings: {end-start} seconds")
    return embeddings 
'''


import google.generativeai as genai
from src.config import GOOGLE_API_KEY
from concurrent.futures import ThreadPoolExecutor

genai.configure(api_key=GOOGLE_API_KEY)

embedding_model = genai.embed_content

# Function to generate a single embedding
def get_gemini_embedding(text, model="models/text-embedding-004", task_type="retrieval_document"):
    try:
        res = embedding_model(
            model=model,
            content=text,
            task_type=task_type,
            title="chunk"
        )
        return res["embedding"]
    except Exception as e:
        print(f"Embedding failed for a chunk: {e}")
        return None

# Function to generate embeddings for a list of texts in parallel
def get_gemini_embeddings(texts, model="models/text-embedding-004", task_type="retrieval_document", max_workers=4):
    start=time.time()

    embeddings = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(get_gemini_embedding, txt, model, task_type) for txt in texts]
        for future in futures:
            embeddings.append(future.result())
    end=time.time()
    print(f"Time taken to generate embeddings: {end-start} seconds")
    return embeddings
