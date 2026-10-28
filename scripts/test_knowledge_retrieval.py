
from src.components.knowledge_retrieval import (
    build_knowledge_index,
    retrieve_documents,
)


def run_tests():
    build_knowledge_index()
    
    results = retrieve_documents(
        "Should I share my banking OTP with another person?",
        similarity_threshold=0.20,
    )

    assert results, "Expected a relevant public document."
    assert all(
        result["content_type"] == "official_public_guidance"
        for result in results
    )

    print("PASS: Public-source retrieval")
    print("Top result:", results[0]["title"])

    assert all(result["source_url"] for result in results)
    print("PASS: Source metadata is available")

    try:
        retrieve_documents("   ")
        raise AssertionError("Empty question should have failed.")
    except ValueError:
        print("PASS: Empty question validation")

    results = retrieve_documents(
        "What is my bank's exact annual debit card fee?",
        similarity_threshold=0.99,
    )

    assert results == [], "Expected no result at this strict threshold."
    print("PASS: Strict-threshold fallback test")


if __name__ == "__main__":
    run_tests()
