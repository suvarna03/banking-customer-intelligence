
from langchain_ollama import ChatOllama
from src.components.knowledge_retrieval import retrieve_documents
from src.utils.logger import get_logger

logger = get_logger(__name__)

llm = ChatOllama(
    model="llama3.2",
    temperature=0,
    num_ctx=2048,
    num_gpu=0,
)

def generate_answer(question, documents=None):
    if not question or not question.strip():
        raise ValueError("Question cannot be empty.")

    if documents is None:
        documents = retrieve_documents(question)

    if not documents:
        return {
            "question": question,
            "answer": (
                "I could not find sufficient supporting information "
                "in the available knowledge base. Please check the "
                "relevant bank's official website or contact its support team."
            ),
            "sources": [],
            "status": "insufficient_evidence",
        }

    context = "\n\n".join(
        f"Source: {doc['title']}\n"
        f"Publisher: {doc['publisher']}\n"
        f"Content: {doc['content']}"
        for doc in documents
    )

    prompt = f"""
You are a banking customer-support assistant.

Answer the customer's question using only the evidence provided below.

Rules:
- Do not invent banking policies, fees, deadlines, or guarantees.
- If the evidence does not answer the question, say that the
  available information is insufficient.
- Give a clear, concise answer.
- Do not claim that you performed any banking transaction.

Evidence:
{context}

Customer question:
{question}

Answer:
"""

    response = llm.invoke(prompt)
    answer = response.content.strip()

    sources = [
        {
            "title": doc["title"],
            "publisher": doc["publisher"],
            "url": doc["source_url"],
            "similarity": round(float(doc["similarity"]), 4),
        }
        for doc in documents
    ]

    logger.info("Generated answer using %s retrieved documents", len(documents))

    return {
        "question": question,
        "answer": answer,
        "sources": sources,
        "status": "answered",
    }
