import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from voice_assistant.router.agent_router import AgentRouter


def main():

    print()
    print("=" * 60)
    print("AGENT ROUTER TEST")
    print("=" * 60)

    router = AgentRouter()

    test_queries = [
        (
            "Which product line has the highest total sales in the database?",
            "database",
        ),
        (
            "Show me the average rating by branch from the database.",
            "database",
        ),
        (
            "Run a SQL query to find the highest total sales.",
            "database",
        ),
        (
            "Which product line has the highest total sales?",
            "data",
        ),
        (
            "Analyze my CSV sales data.",
            "data",
        ),
        (
            "Create a chart of sales by region.",
            "data",
        ),
        (
            "What does my uploaded PDF say about AI?",
            "rag",
        ),
        (
            "Search the web for the latest AI developments.",
            "research",
        ),
        (
            "What is Python?",
            "general",
        ),
        (
            "Hello, how are you?",
            "general",
        ),
    ]

    passed = 0

    for question, expected in test_queries:

        result = router.classify(question)

        actual = result["agent"]

        status = "PASS" if actual == expected else "FAIL"

        print()
        print(f"[{status}]")
        print(f"Question : {question}")
        print(f"Expected : {expected}")
        print(f"Actual   : {actual}")
        print(f"Reason   : {result['reason']}")

        if actual == expected:
            passed += 1

    print()
    print("=" * 60)
    print(
        f"RESULT: {passed}/{len(test_queries)} tests passed"
    )
    print("=" * 60)


if __name__ == "__main__":
    main()