from langchain_google_genai import ChatGoogleGenerativeAI

def generate_response(question, context_chunks):
    context = "\n\n".join(context_chunks)

    prompt_template = """You are a knowledgeable AI assistant. Answer the following question in detail, providing thorough explanations, examples, and key insights.

    Context: {context}

    Question: {question}

    Provide a well-structured and comprehensive response in markdown format. Use bullet points, headings, and code blocks where appropriate.
    """

    prompt = prompt_template.format(context=context, question=question)
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.2)
    response = llm.invoke(prompt)

    return response