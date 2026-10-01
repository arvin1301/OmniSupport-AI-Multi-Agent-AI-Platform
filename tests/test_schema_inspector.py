import sys
from pathlib import Path


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# IMPORTS
# ============================================================

from voice_assistant.agents.database.connection import (
    DatabaseConnection,
)

from voice_assistant.agents.database.schema_inspector import (
    SchemaInspector,
)


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 60)
    print("POSTGRESQL SCHEMA INSPECTION TEST")
    print("=" * 60)

    # --------------------------------------------------------
    # DATABASE CONNECTION
    # --------------------------------------------------------

    connection = DatabaseConnection()

    print()
    print("Connecting to PostgreSQL...")

    if not connection.test_connection():

        print(
            " PostgreSQL connection failed."
        )

        return

    print(
        " PostgreSQL connection successful."
    )

    # --------------------------------------------------------
    # SCHEMA INSPECTOR
    # --------------------------------------------------------

    inspector = SchemaInspector(
        connection
    )

    # --------------------------------------------------------
    # TABLES
    # --------------------------------------------------------

    print()
    print("Database tables:")

    tables = inspector.get_tables()

    for table in tables:

        print(
            f"  - {table}"
        )

    # --------------------------------------------------------
    # WALMART TABLE
    # --------------------------------------------------------

    print()
    print("Walmart table columns:")

    columns = inspector.get_columns(
        "walmart_sales"
    )

    for column in columns:

        print(
            f"  - "
            f"{column['name']} | "
            f"{column['type']} | "
            f"nullable={column['nullable']}"
        )

    # --------------------------------------------------------
    # LLM SCHEMA FORMAT
    # --------------------------------------------------------

    print()
    print("=" * 60)
    print("SCHEMA FOR LLM")
    print("=" * 60)

    formatted_schema = (
        inspector.format_schema_for_llm()
    )

    print()
    print(formatted_schema)

    # --------------------------------------------------------
    # COMPLETE
    # --------------------------------------------------------

    print()
    print("=" * 60)
    print("SCHEMA INSPECTION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()