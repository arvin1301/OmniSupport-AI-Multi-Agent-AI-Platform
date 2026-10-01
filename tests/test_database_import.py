import sys
from pathlib import Path

import pandas as pd
from sqlalchemy import text


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# IMPORT
# ============================================================

from voice_assistant.agents.database.connection import (
    DatabaseConnection,
)


# ============================================================
# DATASET
# ============================================================

DATASET_PATH = (
    PROJECT_ROOT
    / "data"
    / "uploads"
    / "Walmart Sales Data.csv.csv"
)


TABLE_NAME = "walmart_sales"


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 60)
    print("WALMART DATASET → POSTGRESQL")
    print("=" * 60)

    # --------------------------------------------------------
    # CHECK FILE
    # --------------------------------------------------------

    print()
    print("Checking dataset...")

    if not DATASET_PATH.exists():

        print(
            f"❌ Dataset not found:\n"
            f"{DATASET_PATH}"
        )

        return

    print(
        f"Dataset found: "
        f"{DATASET_PATH.name}"
    )

    # --------------------------------------------------------
    # LOAD CSV
    # --------------------------------------------------------

    print()
    print("Loading CSV...")

    df = pd.read_csv(
        DATASET_PATH
    )

    print(
        f"Loaded: "
        f"{df.shape[0]} rows × "
        f"{df.shape[1]} columns"
    )

    # --------------------------------------------------------
    # DATABASE CONNECTION
    # --------------------------------------------------------

    print()
    print("Connecting to PostgreSQL...")

    database = DatabaseConnection()

    engine = database.connect()

    # --------------------------------------------------------
    # IMPORT DATA
    # --------------------------------------------------------

    print()
    print(
        f"Importing data into table: "
        f"{TABLE_NAME}"
    )

    df.to_sql(
        TABLE_NAME,
        engine,
        if_exists="replace",
        index=False,
    )

    print(
        " Dataset imported successfully."
    )

    # --------------------------------------------------------
    # VERIFY ROW COUNT
    # --------------------------------------------------------

    print()
    print("Verifying imported data...")

    with engine.connect() as connection:

        result = connection.execute(
            text(
                f'SELECT COUNT(*) FROM "{TABLE_NAME}"'
            )
        )

        row_count = result.scalar()

    print(
        f"PostgreSQL row count: "
        f"{row_count}"
    )

    # --------------------------------------------------------
    # PREVIEW
    # --------------------------------------------------------

    print()
    print("Preview:")

    with engine.connect() as connection:

        result = connection.execute(
            text(
                f'''
                SELECT *
                FROM "{TABLE_NAME}"
                LIMIT 5
                '''
            )
        )

        rows = result.fetchall()

        for row in rows:
            print(row)

    # --------------------------------------------------------
    # RESULT
    # --------------------------------------------------------

    print()
    print("=" * 60)
    print("IMPORT COMPLETE")
    print("=" * 60)

    print()
    print(
        f"Table: {TABLE_NAME}"
    )

    print(
        f"Rows: {row_count}"
    )

    print(
        f"Columns: {len(df.columns)}"
    )

    print()
    print(
        " Walmart dataset is now "
        "available in PostgreSQL."
    )


if __name__ == "__main__":
    main()