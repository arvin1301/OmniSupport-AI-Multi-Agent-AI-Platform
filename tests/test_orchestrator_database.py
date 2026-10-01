import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from voice_assistant.orchestrator.agent_orchestrator import AgentOrchestrator


def main():

    print()
    print("=" * 60)
    print("ORCHESTRATOR DATABASE INTEGRATION TEST")
    print("=" * 60)

    print()
    print("Initializing Agent Orchestrator...")

    orchestrator = AgentOrchestrator()

    question = (
        "Which product line has the highest "
        "total sales in the database?"
    )

    print()
    print("User question:")
    print(question)

    print()
    print("Processing request...")

    result = orchestrator.process(
        question
    )

    print()
    print("=" * 60)
    print("ORCHESTRATOR RESULT")
    print("=" * 60)

    print()
    print("Agent:")
    print(result.get("agent"))

    print()
    print("Reason:")
    print(result.get("reason"))

    print()
    print("Answer:")
    print(result.get("answer"))

    print()
    print("SQL:")
    print("-" * 60)
    print(result.get("sql"))
    print("-" * 60)

    print()
    print("Error:")
    print(result.get("error"))

    print()
    print("=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()