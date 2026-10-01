import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from voice_assistant.orchestrator import AgentOrchestrator


def main():

    print("=" * 70)
    print("DATASET STATE TEST")
    print("=" * 70)

    # Initialize orchestrator
    orchestrator = AgentOrchestrator()

    # ------------------------------------------------------
    # Check state before loading dataset
    # ------------------------------------------------------

    print("\nBefore loading dataset:")

    info = orchestrator.get_dataset_info()

    print(info)

    # ------------------------------------------------------
    # Dataset path
    # ------------------------------------------------------

    dataset_path = (
        PROJECT_ROOT
        / "data"
        / "datasets"
        / "test.csv"
    )

    print("\nDataset path:")
    print(dataset_path)

    # ------------------------------------------------------
    # Check dataset exists
    # ------------------------------------------------------

    if not dataset_path.exists():

        print("\nERROR: Dataset not found.")

        return

    # ------------------------------------------------------
    # Load dataset
    # ------------------------------------------------------

    print("\nLoading dataset...")

    orchestrator.load_data(
        str(dataset_path)
    )

    # ------------------------------------------------------
    # Check state after loading
    # ------------------------------------------------------

    print("\nAfter loading dataset:")

    info = orchestrator.get_dataset_info()

    print(info)

    # ------------------------------------------------------
    # Display individual values
    # ------------------------------------------------------

    print("\nDataset status:")
    print("Loaded:", info["loaded"])
    print("File:", info["file_path"])
    print("Rows:", info["rows"])
    print("Columns:", info["columns"])
    print("Column names:", info["column_names"])

    print("\n" + "=" * 70)
    print("DATASET STATE TEST COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()