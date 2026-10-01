import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from voice_assistant.agents.data_analysis.data_loader import DataLoader
from voice_assistant.agents.data_analysis.chart_generator import ChartGenerator


def main():

    loader = DataLoader()
    chart_generator = ChartGenerator()

    df = loader.load("data/datasets/test.csv")

    print("\n Creating sales chart...")

    chart_path = chart_generator.bar_chart(
        df,
        category_column="product",
        value_column="sales",
        filename="sales_by_product.png",
    )

    print(f"\n Chart created successfully:")
    print(chart_path)


if __name__ == "__main__":
    main()