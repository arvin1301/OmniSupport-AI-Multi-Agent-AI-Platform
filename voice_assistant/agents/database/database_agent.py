from groq import Groq

from voice_assistant.config import (
    GROQ_API_KEY,
    DATA_LLM_MODEL,
)

from voice_assistant.agents.database.connection import (
    DatabaseConnection,
)

from voice_assistant.agents.database.schema_inspector import (
    SchemaInspector,
)

from voice_assistant.agents.database.sql_generator import (
    SQLGenerator,
)

from voice_assistant.agents.database.sql_executor import (
    SQLExecutor,
)


class DatabaseAgent:

    def __init__(self):

        print(
            "Initializing Database Agent..."
        )

        self.client = Groq(
            api_key=GROQ_API_KEY
        )

        self.model = DATA_LLM_MODEL

        self.connection = (
            DatabaseConnection()
        )

        self.schema_inspector = (
            SchemaInspector(
                self.connection
            )
        )

        self.sql_generator = (
            SQLGenerator()
        )

        self.sql_executor = (
            SQLExecutor(
                self.connection
            )
        )

    # ========================================================
    # CONNECTION
    # ========================================================

    def test_connection(self):

        return self.connection.test_connection()

    # ========================================================
    # DATABASE SCHEMA
    # ========================================================

    def get_schema(self):

        return self.schema_inspector.get_schema()

    def get_formatted_schema(self):

        return (
            self.schema_inspector
            .format_schema_for_llm()
        )

    # ========================================================
    # SQL GENERATION
    # ========================================================

    def generate_sql(self, question):

        schema = (
            self.get_formatted_schema()
        )

        return self.sql_generator.generate(
            question=question,
            schema=schema,
        )

    # ========================================================
    # SQL EXECUTION
    # ========================================================

    def execute_sql(self, sql):

        return self.sql_executor.execute(
            sql
        )

    # ========================================================
    # ANSWER GENERATION
    # ========================================================

    def generate_answer(
        self,
        question,
        sql,
        data
    ):

        if data is None:

            return (
                "The database query did not "
                "return any data."
            )

        if data.empty:

            return (
                "The query executed successfully, "
                "but no matching records were found."
            )

        # Limit the amount of data sent
        # back to the LLM.

        preview = data.head(50)

        records = preview.to_dict(
            orient="records"
        )

        prompt = f"""
You are the answer-generation component
of the OmniSupport Database Agent.

USER QUESTION:

{question}

SQL QUERY:

{sql}

QUERY RESULT:

{records}

Write a concise and accurate answer
based ONLY on the query result.

RULES:

1. Do not invent values.

2. Do not perform calculations that
   are not supported by the query result.

3. Do not mention SQL.

4. Do not mention PostgreSQL.

5. Do not mention Python.

6. Do not mention the LLM.

7. Clearly answer the user's question.

8. Include relevant numerical values.

9. If multiple rows are returned,
   summarize the important results.

10. Keep the answer concise.
"""

        try:

            response = (
                self.client
                .chat
                .completions
                .create(
                    model=self.model,
                    temperature=0.2,
                    messages=[
                        {
                            "role": "system",
                            "content": prompt,
                        },
                        {
                            "role": "user",
                            "content": str(
                                records
                            ),
                        },
                    ],
                )
            )

            return (
                response
                .choices[0]
                .message
                .content
                .strip()
            )

        except Exception as e:

            return (
                "The database query was "
                "successful, but I could not "
                f"generate a natural-language "
                f"response. Results: {records}"
            )

    # ========================================================
    # MAIN DATABASE QUERY
    # ========================================================

    def query(self, question):

        print(
            f"\nDatabase question: "
            f"{question}"
        )

        # ----------------------------------------------------
        # TEST DATABASE CONNECTION
        # ----------------------------------------------------

        if not self.test_connection():

            return {
                "answer": (
                    "I could not connect to "
                    "the PostgreSQL database."
                ),
                "sql": None,
                "results": None,
                "error": (
                    "Database connection failed."
                ),
            }

        # ----------------------------------------------------
        # GET SCHEMA
        # ----------------------------------------------------

        try:

            schema = (
                self.get_formatted_schema()
            )

            print(
                "\nDatabase schema:"
            )

            print(schema)

        except Exception as e:

            return {
                "answer": (
                    "I could not inspect "
                    "the database schema."
                ),
                "sql": None,
                "results": None,
                "error": str(e),
            }

        # ----------------------------------------------------
        # GENERATE SQL
        # ----------------------------------------------------

        try:

            sql = self.sql_generator.generate(
                question=question,
                schema=schema,
            )

            print(
                "\nGenerated SQL:"
            )

            print(sql)

        except Exception as e:

            return {
                "answer": (
                    "I could not generate "
                    "a database query."
                ),
                "sql": None,
                "results": None,
                "error": str(e),
            }

        # ----------------------------------------------------
        # EXECUTE SQL
        # ----------------------------------------------------

        execution = (
            self.sql_executor.execute(
                sql
            )
        )

        if not execution["success"]:

            print(
                "SQL execution error:",
                execution["error"]
            )

            return {
                "answer": (
                    "I could not execute "
                    "the database query."
                ),
                "sql": sql,
                "results": None,
                "error": execution["error"],
            }

        data = execution["data"]

        print(
            "\nDatabase query completed."
        )

        print(
            data
        )

        # ----------------------------------------------------
        # GENERATE ANSWER
        # ----------------------------------------------------

        answer = self.generate_answer(
            question=question,
            sql=sql,
            data=data,
        )

        # ----------------------------------------------------
        # RETURN RESULT
        # ----------------------------------------------------

        return {
            "answer": answer,
            "sql": sql,
            "results": data,
            "error": None,
        }