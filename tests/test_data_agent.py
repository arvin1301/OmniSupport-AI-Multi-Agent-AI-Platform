import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from voice_assistant.agents.data_analysis.data_agent import DataAnalysisAgent


def main():

    agent = DataAnalysisAgent()

    print("\n Loading dataset...")

    overview = agent.load_dataset(
        "data/datasets/test.csv"
    )

    print("\n Dataset Overview:")
    print(overview)

    question = "Show sales by product"

    print(f"\n User: {question}")

    result = agent.analyze(question)

    print("\n Data Analysis Agent:")
    print(result["answer"])

    print("\n Calculated Results:")
    print(result["results"])


if __name__ == "__main__":
    main()