import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from voice_assistant.orchestrator.agent_orchestrator import AgentOrchestrator


def main():

    print()
    print("=" * 70)
    print("OMNISUPPORT AI - FULL AGENT REGRESSION TEST")
    print("=" * 70)

    print()
    print("Initializing Agent Orchestrator...")

    orchestrator = AgentOrchestrator()

    tests = [
        {
            "name": "General Agent",
            "question": "What is Python?",
            "expected_agent": "general",
        },
        {
            "name": "RAG Agent",
            "question": "What does my uploaded PDF say about AI?",
            "expected_agent": "rag",
        },
        {
            "name": "Research Agent",
            "question": "Search the web for the latest AI developments.",
            "expected_agent": "research",
        },
        {
            "name": "Data Analysis Agent",
            "question": "Which product line has the highest total sales?",
            "expected_agent": "data",
        },
        {
            "name": "Database Agent",
            "question": (
                "Which product line has the highest "
                "total sales in the database?"
            ),
            "expected_agent": "database",
        },
    ]

    passed = 0

    print()

    for index, test in enumerate(tests, start=1):

        print("=" * 70)
        print(
            f"TEST {index}/{len(tests)} - {test['name']}"
        )
        print("=" * 70)

        print()
        print("Question:")
        print(test["question"])

        print()
        print("Expected agent:")
        print(test["expected_agent"])

        print()
        print("Processing...")

        try:

            result = orchestrator.process(
                test["question"]
            )

            actual_agent = result.get(
                "agent",
                "unknown"
            )

            print()
            print("Actual agent:")
            print(actual_agent)

            print()
            print("Answer:")
            print(result.get("answer", ""))

            if actual_agent == test["expected_agent"]:

                print()
                print("STATUS: PASS")

                passed += 1

            else:

                print()
                print("STATUS: FAIL")

                print(
                    f"Expected: {test['expected_agent']}"
                )

                print(
                    f"Actual: {actual_agent}"
                )

        except Exception as e:

            print()
            print("STATUS: FAIL")

            print("Error:")
            print(e)

    print()
    print("=" * 70)
    print("REGRESSION TEST SUMMARY")
    print("=" * 70)

    print()
    print(
        f"Passed: {passed}/{len(tests)}"
    )

    print(
        f"Failed: {len(tests) - passed}/{len(tests)}"
    )

    print()

    if passed == len(tests):

        print(
            "ALL AGENT ROUTES PASSED SUCCESSFULLY."
        )

        print()
        print(
            "General + RAG + Research + Data + Database "
            "are working through the Orchestrator."
        )

    else:

        print(
            "SOME AGENT ROUTES FAILED."
        )

    print()
    print("=" * 70)


if __name__ == "__main__":
    main()