import streamlit as st
from src.load_and_chunk_pdfs import load_and_chunk_pdfs
from src.generate_embeddings import get_gemini_embeddings
from src.store_embeddings import store_in_pinecone
from src.retrieve_embeddings import retrieve_from_pinecone
from src.generate_response import generate_response

def run_rag_pipeline(query, namespace="default"):
    retrieved = retrieve_from_pinecone(query, namespace=namespace)
    response = generate_response(query, retrieved)
    return response

def main():
    st.title("PDF RAG Chatbot")
    st.write("Upload PDF files and ask questions to get answers based on the content of the PDFs.")

    # File uploader
    pdf_files = st.file_uploader("Upload PDFs", type=["pdf"], accept_multiple_files=True)

    if pdf_files:
        pdf_paths = []
        for pdf_file in pdf_files:
            pdf_path = pdf_file.name
            pdf_paths.append(pdf_path)
            with open(pdf_path, "wb") as f:
                f.write(pdf_file.getbuffer())

        # Load and chunk the PDFs
        chunks = load_and_chunk_pdfs(pdf_paths)
        
        # Get embeddings
        texts = [doc.page_content for doc in chunks]
        embeddings = get_gemini_embeddings(texts)
        
        # Store embeddings in Pinecone
        store_in_pinecone(chunks, embeddings, namespace="RAGchatbot-2",index_name='llm-chatbot')

        st.success("PDFs processed and embeddings stored successfully.")

        # Query input
        query = st.text_input("Ask a question about the PDF content:")

        if query:
            # Run the RAG pipeline
            answer = run_rag_pipeline(query, namespace="RAGchatbot-2")
            st.markdown(answer)

if __name__ == "__main__":
    main()