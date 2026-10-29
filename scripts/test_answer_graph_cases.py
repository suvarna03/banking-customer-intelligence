
from src.components.answer_graph import ask_banking_question

test_cases = [
    {
        "name": "OTP safety",
        "question": "Should I share my banking OTP with another person?",
    },
    {
        "name": "Suspicious banking link",
        "question": "I received a suspicious banking link. What should I do?",
    },
    {
        "name": "Lost payment card",
        "question": "What should I do if my payment card is lost?",
    },
    {
        "name": "Unsupported annual fee",
        "question": "What is my bank's exact annual debit card fee?",
    },
    {
        "name": "Unrelated question",
        "question": "What is the weather forecast for tomorrow?",
    },
]


def run_tests():
    for test in test_cases:
        print("\n" + "=" * 60)
        print("TEST:", test["name"])
        print("QUESTION:", test["question"])

        result = ask_banking_question(test["question"])

        print("\nSTATUS:", result["status"])
        print("ANSWER:", result["answer"])
        print("SOURCES:")

        if result["sources"]:
            for source in result["sources"]:
                print(
                    f"- {source['title']} "
                    f"({source['publisher']})"
                )
                print("  URL:", source["url"])
                print("  Similarity:", source["similarity"])
        else:
            print("- No sources returned")


if __name__ == "__main__":
    run_tests()
