import pdfplumber
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

def load_and_chunk_pdfs(pdf_paths, chunk_size=1000, chunk_overlap=100):
    documents = []

    for pdf_path in pdf_paths:
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                if page_text:
                    metadata = {"page": i + 1, "source": pdf_path}
                    documents.append(Document(page_content=page_text, metadata=metadata))

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""]
    )

    chunks = splitter.split_documents(documents)
    return chunks