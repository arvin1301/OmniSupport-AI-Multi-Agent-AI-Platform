import sys
from pathlib import Path


# ============================================================
# ADD PROJECT ROOT TO PYTHON PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# IMPORT DATABASE CONNECTION
# ============================================================

from voice_assistant.agents.database.connection import (
    DatabaseConnection,
)


# ============================================================
# TEST
# ============================================================

def main():

    print()
    print("=" * 60)
    print("POSTGRESQL CONNECTION TEST")
    print("=" * 60)

    print()
    print("Initializing database connection...")

    connection = DatabaseConnection()

    print()
    print("Testing PostgreSQL connection...")

    if connection.test_connection():

        print()
        print(" PostgreSQL connection successful!")

        print()
        print("Connection details:")
        print(f"Host: {connection.host}")
        print(f"Port: {connection.port}")
        print(f"Database: {connection.database}")
        print(f"User: {connection.username}")

    else:

        print()
        print(" PostgreSQL connection failed.")


if __name__ == "__main__":
    main()