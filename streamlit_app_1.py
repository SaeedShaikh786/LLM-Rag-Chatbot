import streamlit as st
import os
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
    st.set_page_config(layout="wide")
    st.title("PDF RAG Chatbot")
    st.write("Upload PDF files and ask questions to get answers based on the content of the PDFs.")

    # Create columns for layout
    col1, col2 = st.columns([1, 3])

    with col1:
        st.header("Upload PDFs")
        # Create the directory for storing PDFs if it doesn't exist
        pdf_dir = "pdfs"
        if not os.path.exists(pdf_dir):
            os.makedirs(pdf_dir)

        # File uploader
        pdf_files = st.file_uploader("Upload PDFs", type=["pdf"], accept_multiple_files=True)

        if pdf_files:
            pdf_paths = []
            for pdf_file in pdf_files:
                # Save the uploaded PDFs to the 'pdfs' directory
                pdf_path = os.path.join(pdf_dir, pdf_file.name)
                pdf_paths.append(pdf_path)
                with open(pdf_path, "wb") as f:
                    f.write(pdf_file.getbuffer())
            st.success("PDFs uploaded and saved successfully.")

            # Show a spinner during processing
            with st.spinner("Processing PDFs..."):
                # Load and chunk the PDFs
                chunks = load_and_chunk_pdfs(pdf_paths)
                st.success("PDFs processed and chunked successfully.")

                # Get embeddings
                st.info("Generating embeddings for PDF content...")
                texts = [doc.page_content for doc in chunks]
                embeddings = get_gemini_embeddings(texts)
                st.success("Embeddings generated successfully.")

                # Store embeddings in Pinecone
                st.info("Storing embeddings in Pinecone...")
                store_in_pinecone(chunks, embeddings, namespace="RAGchatbot-2")
                st.success("Embeddings stored in Pinecone successfully.")

    with col2:
        st.header("Ask Questions")
        # Query input
        query = st.text_input("Ask a question about the PDF content:")

        if query:
            # Show a spinner during response generation
            with st.spinner("Retrieving relevant information and generating response..."):
                # Run the RAG pipeline
                answer = run_rag_pipeline(query, namespace="RAGchatbot-2")
                st.success("Response generated successfully.")
                st.markdown(answer)

if __name__ == "__main__":
    main()