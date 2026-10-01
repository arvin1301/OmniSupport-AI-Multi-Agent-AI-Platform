import re

from groq import Groq

from voice_assistant.config import (
    GROQ_API_KEY,
    DATA_LLM_MODEL,
)


class SQLGenerator:

    def __init__(self):

        self.client = Groq(
            api_key=GROQ_API_KEY
        )

        self.model = DATA_LLM_MODEL

    def _clean_sql(self, sql: str):

        if not sql:
            return ""

        sql = sql.strip()

        sql = re.sub(
            r"^```sql\s*",
            "",
            sql,
            flags=re.IGNORECASE
        )

        sql = re.sub(
            r"^```\s*",
            "",
            sql
        )

        sql = re.sub(
            r"\s*```$",
            "",
            sql
        )

        return sql.strip()

    def generate(
        self,
        question: str,
        schema: str
    ):

        prompt = f"""
You are the SQL generation engine
of OmniSupport AI.

Your job is to convert the user's
natural-language question into a
safe PostgreSQL SQL query.

DATABASE SCHEMA:

{schema}

USER QUESTION:

{question}

RULES:

1. Generate PostgreSQL SQL only.

2. Use only tables and columns
   present in the provided schema.

3. Never invent tables.

4. Never invent columns.

5. Only generate read-only queries.

6. Allowed SQL operations:

   SELECT
   FROM
   WHERE
   GROUP BY
   ORDER BY
   HAVING
   LIMIT
   OFFSET
   JOIN
   LEFT JOIN
   INNER JOIN
   RIGHT JOIN
   UNION
   CASE
   aggregate functions

7. Never generate:

   INSERT
   UPDATE
   DELETE
   DROP
   ALTER
   CREATE
   TRUNCATE
   GRANT
   REVOKE

8. Do not use multiple SQL statements.

9. Do not use comments.

10. For ranking questions, use
    ORDER BY and LIMIT when appropriate.

11. For "highest" or "lowest",
    return the relevant category
    and numerical value.

12. For aggregation questions,
    calculate the requested aggregation.

13. Use PostgreSQL-compatible syntax.

14. Return ONLY SQL.

Example:

SELECT
    product_line,
    SUM(total) AS total_sales
FROM sales
GROUP BY product_line
ORDER BY total_sales DESC
LIMIT 1;
"""

        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0.0,
            messages=[
                {
                    "role": "system",
                    "content": prompt,
                },
                {
                    "role": "user",
                    "content": question,
                },
            ],
        )

        content = (
            response
            .choices[0]
            .message
            .content
        )

        return self._clean_sql(
            content
        )