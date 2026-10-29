
from src.components.answer_graph import ask_banking_question

questions = [
    "How many days will it take to reverse my failed UPI transaction?",
    "Can I get a refund for a failed transaction?",
    "What is the procedure for reporting an unauthorized bank transaction?",
]

for question in questions:
    result = ask_banking_question(question)

    print("\n" + "=" * 60)
    print("Question:", question)
    print("Status:", result["status"])
    print("Answer:", result["answer"])

    print("Sources:")
    for source in result["sources"]:
        print(
            f"- {source['title']} "
            f"(similarity: {source['similarity']})"
        )

    if not result["sources"]:
        print("- No sources returned")
