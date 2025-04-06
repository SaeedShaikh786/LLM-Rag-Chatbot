# PDF RAG Chatbot

This project is a Retrieval-Augmented Generation (RAG) chatbot that processes PDFs, generates embeddings for their content, stores the embeddings in Pinecone, and retrieves relevant information to answer user queries. The chatbot is built using Streamlit for the user interface and integrates with Pinecone and Google's generative AI for embedding and response generation.

## Features

- **Upload PDF Files**: Upload multiple PDF files to the chatbot.
- **Generate Embeddings**: Generate embeddings for the content of the PDFs.
- **Store Embeddings**: Store the embeddings in Pinecone.
- **Retrieve Information**: Retrieve relevant information from the stored embeddings to answer user queries.
- **Responsive Answers**: Generate well-structured and comprehensive responses in markdown format.

## File Structure

```plaintext
rag_chatbot/
├── .env
├── requirements.txt
├── Dockerfile
├── README.md
├── main.py
└── src/
    ├── config.py
    ├── load_and_chunk_pdfs.py
    ├── generate_embeddings.py
    ├── store_embeddings.py
    ├── retrieve_embeddings.py
    └── generate_response.py
```

## Setup

### Prerequisites

- Python 3.12
- [Streamlit](https://streamlit.io/)
- [Pinecone](https://www.pinecone.io/)
- [Google Generative AI](https://cloud.google.com/ai-platform)

### Installation

1. **Clone the repository**:
   ```sh
   git clone https://github.com/SaeedShaikh786/rag_chatbot.git
   cd rag_chatbot
   ```

2. **Set up virtual environment**:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   - Create a `.env` file in the root directory and add your Pinecone API key and Google API key.
   ```plaintext
   PINECONE_API_KEY=your_pinecone_api_key
   GOOGLE_API_KEY=your_google_api_key
   ```

### Running the App

1. **Run the Streamlit app**:
   ```sh
   streamlit run main.py
   ```

2. **Open the app**:
   - The app will be available at `http://localhost:8501`.

## Docker Setup

1. **Build the Docker image**:
   ```sh
   docker build -t rag_chatbot:latest .
   ```

2. **Run the Docker container**:
   ```sh
   docker run -p 8501:8501 rag_chatbot:latest
   ```

3. **Access the app**:
   - The app will be available at `http://localhost:8501`.

## Usage

1. **Upload PDFs**:
   - Use the file uploader in the Streamlit interface to upload one or more PDF files.

2. **Ask Questions**:
   - After the PDFs are processed, use the text input to ask questions about the content of the PDFs. The app will generate responses based on the content.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or inquiries, please contact [Saeed Shaikh](https://github.com/SaeedShaikh786).
