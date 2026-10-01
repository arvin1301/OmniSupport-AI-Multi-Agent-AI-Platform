import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from voice_assistant.agents.database.connection import DatabaseConnection
from voice_assistant.agents.database.sql_executor import SQLExecutor


def main():
    print()
    print("=" * 60)
    print("SQL EXECUTOR TEST")
    print("=" * 60)

    connection = DatabaseConnection()

    print()
    print("Connecting to PostgreSQL...")

    if not connection.test_connection():
        print(" PostgreSQL connection failed.")
        return

    print(" PostgreSQL connection successful.")

    executor = SQLExecutor(connection)

    sql = """
    SELECT
        "Product line",
        SUM("Total") AS total_sales
    FROM walmart_sales
    GROUP BY "Product line"
    ORDER BY total_sales DESC
    LIMIT 1;
    """

    print()
    print("SQL query:")
    print("-" * 60)
    print(sql.strip())
    print("-" * 60)

    print()
    print("Validating SQL...")

    validation = executor.validate_sql(sql)

    if not validation["valid"]:
        print(" SQL validation failed.")
        print("Error:", validation["error"])
        return

    print(" SQL validation successful.")

    print()
    print("Executing SQL...")

    result = executor.execute(sql)

    if not result["success"]:
        print(" SQL execution failed.")
        print("Error:", result["error"])
        return

    print(" SQL execution successful.")

    print()
    print("Query result:")
    print("-" * 60)
    print(result["data"].to_string(index=False))
    print("-" * 60)

    print()
    print("=" * 60)
    print("SQL EXECUTION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()