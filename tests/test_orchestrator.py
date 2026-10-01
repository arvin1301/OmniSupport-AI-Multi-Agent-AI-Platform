import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from voice_assistant.orchestrator import AgentOrchestrator


def print_result(title, result):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)

    print("Agent:", result["agent"])
    print("Reason:", result["reason"])
    print("Answer:", result["answer"])

    if result.get("results"):
        print("Results:", result["results"])

    if result.get("sources"):
        print("Sources:", result["sources"])

    if result.get("charts"):
        print("Charts:", result["charts"])


def main():

    orchestrator = AgentOrchestrator()

    result = orchestrator.process(
        "How are you?"
    )
    print_result("GENERAL AGENT TEST", result)

    result = orchestrator.process(
        "According to my uploaded PDF, what are the business benefits of ChatGPT?"
    )
    print_result("RAG AGENT TEST", result)

    result = orchestrator.process(
        "What are the latest AI agent frameworks?"
    )
    print_result("RESEARCH AGENT TEST", result)

    dataset_path = PROJECT_ROOT / "data" / "datasets" / "test.csv"

    orchestrator.load_data(str(dataset_path))

    result = orchestrator.process(
        "Which product generated the highest total sales?"
    )
    print_result("DATA AGENT TEST", result)


if __name__ == "__main__":
    main()