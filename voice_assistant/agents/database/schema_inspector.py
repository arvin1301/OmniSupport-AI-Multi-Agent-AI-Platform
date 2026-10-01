from sqlalchemy import inspect


class SchemaInspector:

    def __init__(self, connection):
        self.connection = connection

    def get_tables(self):

        engine = self.connection.connect()

        inspector = inspect(engine)

        return inspector.get_table_names()

    def get_columns(self, table_name):

        engine = self.connection.connect()

        inspector = inspect(engine)

        columns = inspector.get_columns(
            table_name
        )

        return [
            {
                "name": column["name"],
                "type": str(column["type"]),
                "nullable": column.get(
                    "nullable",
                    True
                ),
            }
            for column in columns
        ]

    def get_schema(self):

        tables = self.get_tables()

        schema = {}

        for table in tables:

            schema[table] = self.get_columns(
                table
            )

        return schema

    def format_schema_for_llm(self):

        schema = self.get_schema()

        if not schema:

            return "No database tables are available."

        lines = []

        for table_name, columns in schema.items():

            lines.append(
                f"Table: {table_name}"
            )

            for column in columns:

                nullable = (
                    "NULL"
                    if column["nullable"]
                    else "NOT NULL"
                )

                lines.append(
                    f"  - "
                    f"{column['name']} "
                    f"({column['type']}) "
                    f"{nullable}"
                )

            lines.append("")

        return "\n".join(lines)