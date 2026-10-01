import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from voice_assistant.agents.data_analysis.data_loader import DataLoader
from voice_assistant.agents.data_analysis.analyzer import DataAnalyzer


def main():

    loader = DataLoader()
    analyzer = DataAnalyzer()

    df = loader.load("data/datasets/test.csv")

    results = analyzer.analyze(df)

    print("\n BASIC STATISTICS")
    for column, values in results["basic_statistics"].items():
        print(f"\n{column}:")
        for metric, value in values.items():
            print(f"  {metric}: {value}")

    print("\n COLUMN SUMMARY")
    for column in results["column_summary"]:
        print(column)

    print("\n CORRELATIONS")
    print(results["correlations"])

    print("\n CATEGORICAL SUMMARY")
    for column, values in results["categorical_summary"].items():
        print(f"{column}: {values}")


if __name__ == "__main__":
    main()