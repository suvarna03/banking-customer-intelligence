
from pathlib import Path

import faiss
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

from src.utils.logger import get_logger

logger = get_logger(__name__)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DOCUMENTS_PATH = PROJECT_ROOT / "data" / "knowledge_base" / "documents.csv"
INDEX_PATH = PROJECT_ROOT / "artifacts" / "phase_5" / "knowledge_index.faiss"
METADATA_PATH = PROJECT_ROOT / "artifacts" / "phase_5" / "knowledge_metadata.csv"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
SIMILARITY_THRESHOLD = 0.35

model = SentenceTransformer(MODEL_NAME)


def build_knowledge_index():
    try:
        if not DOCUMENTS_PATH.exists():
            raise FileNotFoundError(
                f"Knowledge documents not found: {DOCUMENTS_PATH}"
            )

        documents = pd.read_csv(DOCUMENTS_PATH)

        required_columns = [
            "document_id",
            "title",
            "publisher",
            "source_url",
            "content",
            "content_type",
            "verification_status",
        ]

        missing_columns = [
            column for column in required_columns
            if column not in documents.columns
        ]

        if missing_columns:
            raise ValueError(f"Missing columns: {missing_columns}")

        # Synthetic documents must not enter the public knowledge index.
        documents = documents[
            documents["content_type"] == "official_public_guidance"
        ].copy()

        documents = documents.dropna(subset=["content"])
        documents = documents[
            documents["content"].str.strip() != ""
        ].reset_index(drop=True)

        if documents.empty:
            raise ValueError("No public guidance documents available.")

        texts = documents["content"].tolist()

        embeddings = model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=True,
        )

        embeddings = np.asarray(embeddings, dtype=np.float32)

        # Normalized vectors + inner product = cosine similarity.
        index = faiss.IndexFlatIP(embeddings.shape[1])
        index.add(embeddings)

        INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)

        faiss.write_index(index, str(INDEX_PATH))
        documents.to_csv(METADATA_PATH, index=False)

        logger.info(
            "Knowledge index built with %s public documents.",
            len(documents),
        )

        print(f"Indexed documents: {index.ntotal}")
        print(f"FAISS index saved to: {INDEX_PATH}")
        print(f"Metadata saved to: {METADATA_PATH}")

    except Exception:
        logger.exception("Failed to build knowledge index.")
        raise


def retrieve_documents(
    question,
    top_k=3,
    similarity_threshold=SIMILARITY_THRESHOLD,
    include_synthetic=False,
):
    if not isinstance(question, str) or not question.strip():
        raise ValueError("Question must be a non-empty string.")

    if top_k < 1:
        raise ValueError("top_k must be at least 1.")

    if not 0 <= similarity_threshold <= 1:
        raise ValueError("similarity_threshold must be between 0 and 1.")

    if not INDEX_PATH.exists() or not METADATA_PATH.exists():
        raise FileNotFoundError(
            "Knowledge index not found. Run build_knowledge_index() first."
        )

    index = faiss.read_index(str(INDEX_PATH))
    metadata = pd.read_csv(METADATA_PATH)

    query_embedding = model.encode(
        [question],
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    query_embedding = np.asarray(query_embedding, dtype=np.float32)

    search_k = min(top_k, index.ntotal)
    scores, indices = index.search(query_embedding, search_k)

    results = []

    for score, position in zip(scores[0], indices[0]):
        if position < 0:
            continue

        document = metadata.iloc[int(position)]

        if not include_synthetic:
            if document["content_type"] != "official_public_guidance":
                continue

        similarity = float(score)

        if similarity < similarity_threshold:
            continue

        results.append({
            "document_id": document["document_id"],
            "title": document["title"],
            "publisher": document["publisher"],
            "source_url": document["source_url"],
            "content": document["content"],
            "content_type": document["content_type"],
            "verification_status": document["verification_status"],
            "similarity": round(similarity, 4),
        })

    return results


if __name__ == "__main__":
    build_knowledge_index()

    question = "What should I do if someone asks me for my banking OTP?"

    results = retrieve_documents(question)

    print("\nQuestion:", question)

    if not results:
        print("No sufficiently similar public document found.")
    else:
        for result in results:
            print("\nTitle:", result["title"])
            print("Similarity:", result["similarity"])
            print("Source:", result["source_url"])
            print("Content:", result["content"])
