import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from voice_assistant.agents.database.database_agent import DatabaseAgent


def main():
    print()
    print("=" * 60)
    print("DATABASE AGENT TEST")
    print("=" * 60)

    print()
    print("Initializing Database Agent...")

    agent = DatabaseAgent()

    print()
    print("Testing PostgreSQL connection...")

    if not agent.test_connection():
        print(" PostgreSQL connection failed.")
        return

    print(" PostgreSQL connection successful.")

    question = "Which product line has the highest total sales?"

    print()
    print("User question:")
    print(question)

    print()
    print("Running Database Agent...")

    result = agent.query(question)

    print()
    print("=" * 60)
    print("DATABASE AGENT RESULT")
    print("=" * 60)

    print()
    print("Answer:")
    print(result["answer"])

    print()
    print("Generated SQL:")
    print("-" * 60)
    print(result["sql"])
    print("-" * 60)

    if result["error"]:
        print()
        print("Error:")
        print(result["error"])

    print()
    print("=" * 60)
    print("DATABASE AGENT TEST COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()