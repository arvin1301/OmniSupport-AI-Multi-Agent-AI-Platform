import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from voice_assistant.agents.data_analysis.data_loader import DataLoader


def main():

    loader = DataLoader()

    df = loader.load("data/datasets/test.csv")

    print("\n Dataset Preview:")
    print(df.head())

    print("\n Dataset Overview:")
    overview = loader.get_overview(df)

    for key, value in overview.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()