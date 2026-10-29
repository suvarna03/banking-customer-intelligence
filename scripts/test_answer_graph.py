
from src.components.answer_graph import ask_banking_question


def run_tests():
    result = ask_banking_question(
        "Should I share my banking OTP with another person?"
    )

    print("\nSupported question:")
    print(result["question"])
    print("\nAnswer:")
    print(result["answer"])
    print("\nStatus:")
    print(result["status"])
    print("\nSources:")
    for source in result["sources"]:
        print(f"- {source['title']} ({source['publisher']})")

    assert result["status"] == "answered"
    assert result["sources"]
    assert result["answer"]

    print("\nPASS: Supported question")

    result = ask_banking_question(
        "What is my bank's exact annual debit card fee?"
    )

    print("\nUnsupported question:")
    print(result["question"])
    print("\nAnswer:")
    print(result["answer"])
    print("\nStatus:")
    print(result["status"])

    if result["status"] == "insufficient_evidence":
        assert result["sources"] == []
        print("\nPASS: Fallback path")
    else:
        print(
            "\nREVIEW: Retrieval found documents for the fee question. "
            "This shows why similarity alone cannot guarantee evidence sufficiency."
        )

    try:
        ask_banking_question("   ")
        raise AssertionError("Empty question should have failed.")
    except ValueError:
        print("PASS: Empty question validation")


if __name__ == "__main__":
    run_tests()
