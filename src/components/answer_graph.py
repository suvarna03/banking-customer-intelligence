
from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from src.components.knowledge_retrieval import retrieve_documents
from src.components.answer_generation import generate_answer
from src.utils.logger import get_logger

logger = get_logger(__name__)

SIMILARITY_THRESHOLD = 0.45


class BankingAnswerState(TypedDict):
    question: str
    documents: list
    answer: str
    sources: list
    status: str


def retrieve_node(state: BankingAnswerState):
    documents = retrieve_documents(
        state["question"],
        similarity_threshold=SIMILARITY_THRESHOLD,
    )

    logger.info("Retrieved %s documents", len(documents))

    return {"documents": documents}


def check_evidence(state: BankingAnswerState):
    documents = state["documents"]

    if not documents:
        return "fallback"

    return "answer"


def answer_node(state: BankingAnswerState):
    result = generate_answer(
        state["question"],
        documents=state["documents"],
    )

    return {
        "answer": result["answer"],
        "sources": result["sources"],
        "status": "answered",
    }


def fallback_node(state: BankingAnswerState):
    return {
        "answer": (
            "I could not find sufficient supporting information in "
            "the available knowledge base. Please check your bank's "
            "official website or contact its customer support team."
        ),
        "sources": [],
        "status": "insufficient_evidence",
    }


def build_answer_graph():
    graph = StateGraph(BankingAnswerState)

    graph.add_node("retrieve", retrieve_node)
    graph.add_node("answer", answer_node)
    graph.add_node("fallback", fallback_node)

    graph.add_edge(START, "retrieve")

    graph.add_conditional_edges(
        "retrieve",
        check_evidence,
        {
            "answer": "answer",
            "fallback": "fallback",
        },
    )

    graph.add_edge("answer", END)
    graph.add_edge("fallback", END)

    return graph.compile()


answer_graph = build_answer_graph()


def ask_banking_question(question):
    if not question or not question.strip():
        raise ValueError("Question cannot be empty.")

    result = answer_graph.invoke({
        "question": question.strip(),
        "documents": [],
        "answer": "",
        "sources": [],
        "status": "",
    })

    return result
