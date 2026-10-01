import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from voice_assistant.agents.data_analysis.data_loader import DataLoader
from voice_assistant.agents.data_analysis.python_executor import PythonExecutor


def main():

    loader = DataLoader()
    executor = PythonExecutor()

    df = loader.load("data/datasets/test.csv")

    code = """
result = {
    "total_sales": df["sales"].sum(),
    "average_sales": df["sales"].mean(),
    "total_quantity": df["quantity"].sum(),
    "highest_sale": df["sales"].max()
}
"""

    output = executor.execute(code, df)

    print("\n EXECUTION RESULT")
    print(output)


if __name__ == "__main__":
    main()