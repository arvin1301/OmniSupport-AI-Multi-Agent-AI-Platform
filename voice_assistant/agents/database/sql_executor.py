import re

import pandas as pd
from sqlalchemy import text


class SQLExecutor:

    FORBIDDEN_KEYWORDS = {
        "INSERT",
        "UPDATE",
        "DELETE",
        "DROP",
        "ALTER",
        "TRUNCATE",
        "CREATE",
        "GRANT",
        "REVOKE",
        "MERGE",
        "CALL",
        "EXEC",
        "EXECUTE",
    }

    def __init__(self, connection):
        self.connection = connection

    def validate_sql(self, sql: str):

        if not sql or not sql.strip():

            return {
                "valid": False,
                "error": "SQL query is empty.",
            }

        cleaned = sql.strip()

        # Remove trailing semicolon for validation
        cleaned = cleaned.rstrip(";").strip()

        # Only one statement is allowed
        if ";" in cleaned:

            return {
                "valid": False,
                "error": (
                    "Multiple SQL statements "
                    "are not allowed."
                ),
            }

        # Query must start with SELECT or WITH
        if not re.match(
            r"^(SELECT|WITH)\b",
            cleaned,
            flags=re.IGNORECASE
        ):

            return {
                "valid": False,
                "error": (
                    "Only SELECT or WITH queries "
                    "are allowed."
                ),
            }

        upper_sql = cleaned.upper()

        for keyword in self.FORBIDDEN_KEYWORDS:

            pattern = (
                rf"\b{keyword}\b"
            )

            if re.search(
                pattern,
                upper_sql
            ):

                return {
                    "valid": False,
                    "error": (
                        f"Forbidden SQL operation: "
                        f"{keyword}"
                    ),
                }

        return {
            "valid": True,
            "error": None,
        }

    def execute(self, sql: str):

        validation = self.validate_sql(
            sql
        )

        if not validation["valid"]:

            return {
                "success": False,
                "data": None,
                "error": validation["error"],
            }

        try:

            engine = self.connection.connect()

            with engine.connect() as connection:

                result = pd.read_sql(
                    text(sql),
                    connection,
                )

            return {
                "success": True,
                "data": result,
                "error": None,
            }

        except Exception as e:

            return {
                "success": False,
                "data": None,
                "error": str(e),
            }