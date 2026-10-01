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

from voice_assistant.agents.database.sql_generator import (
    SQLGenerator,
)


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 60)
    print("SQL GENERATOR TEST")
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
    # SCHEMA
    # --------------------------------------------------------

    inspector = SchemaInspector(
        connection
    )

    schema = (
        inspector.format_schema_for_llm()
    )

    print()
    print("Schema loaded successfully.")

    # --------------------------------------------------------
    # SQL GENERATOR
    # --------------------------------------------------------

    generator = SQLGenerator()

    question = (
        "Which product line has the "
        "highest total sales?"
    )

    print()
    print("User question:")
    print(question)

    # --------------------------------------------------------
    # GENERATE SQL
    # --------------------------------------------------------

    print()
    print("Generating SQL...")

    sql = generator.generate(
        question=question,
        schema=schema,
    )

    print()
    print("Generated SQL:")
    print("-" * 60)
    print(sql)
    print("-" * 60)

    # --------------------------------------------------------
    # COMPLETE
    # --------------------------------------------------------

    print()
    print("=" * 60)
    print("SQL GENERATION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()