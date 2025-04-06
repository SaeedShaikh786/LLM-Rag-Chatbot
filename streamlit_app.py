import streamlit as st
import os
from src.load_and_chunk_pdfs import load_and_chunk_pdfs
from src.generate_embeddings import get_gemini_embeddings
from src.store_embeddings import store_in_pinecone
from src.retrieve_embeddings import retrieve_from_pinecone
from src.generate_response import generate_response

def run_rag_pipeline(query, namespace="default"):
    retrieved = retrieve_from_pinecone(query, namespace=namespace,index_name="llm-chatbot")
    response = generate_response(query, retrieved)
    return response

def main():
    st.set_page_config(layout="wide")
    st.title("📄 PDF RAG Chatbot")

    # Create directory for saving PDFs if not exists
    pdf_dir = "pdfs"
    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir)

    # Initialize session state variables
    if "pdf_processed" not in st.session_state:
        st.session_state.pdf_processed = False

    # Sidebar for uploading and processing PDFs
    with st.sidebar:
        st.header("📥 Upload PDFs")
        pdf_files = st.file_uploader("Upload PDFs", type=["pdf"], accept_multiple_files=True)

        if pdf_files:
            pdf_paths = []
            for pdf_file in pdf_files:
                pdf_path = os.path.join(pdf_dir, pdf_file.name)
                pdf_paths.append(pdf_path)
                with open(pdf_path, "wb") as f:
                    f.write(pdf_file.getbuffer())
            st.success("PDFs uploaded successfully.")

            if st.button("🔄 Process PDFs"):
                with st.spinner("Processing PDFs..."):
                    chunks = load_and_chunk_pdfs(pdf_paths)
                    texts = [doc.page_content for doc in chunks]

                with st.spinner("Generating embeddings..."):
                    embeddings = get_gemini_embeddings(texts)

                with st.spinner("Storing in Pinecone..."):
                    store_in_pinecone(chunks, embeddings, namespace="RAGchatbot-2",index_name="llm-chatbot")

                st.success("All steps completed.")
                st.session_state.pdf_processed = True  # Update flag

    # Main area for asking questions
    st.header("💬 Ask a Question")
    if st.session_state.pdf_processed:
        query = st.text_input("Ask something about the PDFs:")
        if query:
            with st.spinner("Generating answer..."):
                answer = run_rag_pipeline(query, namespace="RAGchatbot-2")
            st.success("Here’s the response:")
            st.markdown(answer)
    else:
        st.info("Please upload and process PDFs using the sidebar.")

if __name__ == "__main__":
    main()
