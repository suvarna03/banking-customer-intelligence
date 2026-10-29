
from src.components.answer_generation import generate_answer


def run_tests():
    result = generate_answer(
        "Should I share my banking OTP with another person?"
    )

    print("\nQuestion:")
    print(result["question"])

    print("\nAnswer:")
    print(result["answer"])

    print("\nStatus:")
    print(result["status"])

    print("\nSources:")
    for source in result["sources"]:
        print(f"- {source['title']} ({source['publisher']})")
        print(f"  URL: {source['url']}")

    assert result["answer"], "Answer should not be empty."
    assert result["sources"], "Expected sources for the OTP question."
    assert all(source["url"] for source in result["sources"])

    print("\nPASS: Answer generation and source metadata")


if __name__ == "__main__":
    run_tests()
