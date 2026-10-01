import json
import re

from groq import Groq

from voice_assistant.config import (
    GROQ_API_KEY,
    DATA_LLM_MODEL,
)

from voice_assistant.agents.data_analysis.data_loader import DataLoader
from voice_assistant.agents.data_analysis.analyzer import DataAnalyzer
from voice_assistant.agents.data_analysis.python_executor import PythonExecutor
from voice_assistant.agents.data_analysis.chart_generator import ChartGenerator


class DataAnalysisAgent:

    def __init__(self):

        print("Initializing Data Analysis Agent...")

        self.client = Groq(api_key=GROQ_API_KEY)
        self.model = DATA_LLM_MODEL

        self.data_loader = DataLoader()
        self.analyzer = DataAnalyzer()
        self.executor = PythonExecutor()
        self.chart_generator = ChartGenerator()

        # Currently loaded DataFrame
        self.df = None

        # Currently loaded file
        self.file_path = None

    # ==========================================================
    # DATASET LOADING
    # ==========================================================

    def load_dataset(self, file_path: str):

        self.df = self.data_loader.load(file_path)

        self.file_path = file_path

        print(
            f"Dataset ready for analysis: "
            f"{self.df.shape[0]} rows × {self.df.shape[1]} columns"
        )

        return self.df

    # ==========================================================
    # DATASET INFORMATION
    # ==========================================================

    def get_dataset_info(self):

        if self.df is None:

            return {
                "loaded": False,
                "file_path": None,
                "rows": 0,
                "columns": 0,
                "column_names": []
            }

        return {
            "loaded": True,
            "file_path": self.file_path,
            "rows": int(self.df.shape[0]),
            "columns": int(self.df.shape[1]),
            "column_names": self.df.columns.tolist()
        }

    # ==========================================================
    # CLEAN GENERATED PYTHON CODE
    # ==========================================================

    def _clean_code(self, code: str):

        if not code:
            return ""

        code = code.strip()

        # Remove markdown code fences
        code = re.sub(r"^```python\s*", "", code)
        code = re.sub(r"^```\s*", "", code)
        code = re.sub(r"\s*```$", "", code)

        return code.strip()

    # ==========================================================
    # DETECT WHETHER A CHART IS NEEDED
    # ==========================================================

    def _should_create_chart(self, question: str):

        keywords = [
            "chart",
            "graph",
            "plot",
            "visualize",
            "visualise",
            "visualization",
            "visualisation",
            "show",
            "trend",
            "distribution",
            "compare",
            "comparison"
        ]

        question_lower = question.lower()

        return any(
            keyword in question_lower
            for keyword in keywords
        )

    # ==========================================================
    # GENERATE CHART PLAN
    # ==========================================================

    def _generate_chart_plan(self, question: str):

        columns = self.df.columns.tolist()

        prompt = f"""
You are a data visualization planner.

User question:
{question}

Available dataset columns:
{columns}

Choose the most appropriate chart.

Supported chart types:

1. bar
2. line
3. histogram

Return ONLY valid JSON:

{{
    "chart_type": "bar",
    "category_column": "product",
    "value_column": "sales",
    "filename": "sales_chart.png"
}}

Rules:

- Use only columns that exist.
- Do not invent columns.
- Use "bar" for category comparisons.
- Use "line" for ordered/time trends.
- Use "histogram" for numerical distributions.
- category_column is required for bar and line charts.
- value_column is required for bar and line charts.
- histogram requires only value_column.
"""

        try:

            response = self.client.chat.completions.create(
                model=self.model,
                temperature=0.0,
                messages=[
                    {
                        "role": "system",
                        "content": prompt
                    },
                    {
                        "role": "user",
                        "content": question
                    }
                ]
            )

            content = response.choices[0].message.content.strip()

            content = self._clean_code(content)

            return json.loads(content)

        except Exception as e:

            print(f"Chart planning error: {e}")

            return None

    # ==========================================================
    # CREATE CHART
    # ==========================================================

    def _create_chart(self, plan):

        if not plan:
            return None

        chart_type = plan.get("chart_type")

        category_column = plan.get("category_column")
        value_column = plan.get("value_column")

        filename = plan.get(
            "filename",
            "generated_chart.png"
        )

        try:

            if chart_type == "bar":

                if not category_column or not value_column:
                    return None

                return self.chart_generator.bar_chart(
                    self.df,
                    category_column,
                    value_column,
                    filename
                )

            elif chart_type == "line":

                if not category_column or not value_column:
                    return None

                return self.chart_generator.line_chart(
                    self.df,
                    category_column,
                    value_column,
                    filename
                )

            elif chart_type == "histogram":

                if not value_column:
                    return None

                return self.chart_generator.histogram(
                    self.df,
                    value_column,
                    filename
                )

            return None

        except Exception as e:

            print(f"Chart generation error: {e}")

            return None

    # ==========================================================
    # GENERATE PYTHON ANALYSIS
    # ==========================================================

    def _generate_analysis_code(self, question: str):

        columns = self.df.columns.tolist()

        prompt = f"""
You are the data analysis engine of OmniSupport AI.

You must analyze the user's question using ONLY the
provided pandas DataFrame named df.

User question:
{question}

Available columns:
{columns}

Generate executable Python code.

Rules:

1. Use only:
   - pandas through df
   - numpy through np

2. Do not import anything.

3. Do not access:
   - files
   - internet
   - operating system
   - subprocess
   - network
   - environment variables

4. Do not modify the original dataframe.

5. Store the final answer in a variable named:

result

6. Return useful calculated values.

7. For rankings such as highest/lowest:
   return both the category and numerical value.

8. For aggregations:
   calculate the actual aggregated values.

9. For comparisons:
   return all relevant comparison values when appropriate.

10. For group-by questions:
    return the grouped values.

11. For trends:
    return the relevant ordered values.

12. Do not return only the name of an item if a numerical
    value is also requested or available.

13. Convert NumPy scalar values to normal Python values
    using int(), float(), or str() when appropriate.

14. Do not use print().

15. Do not generate explanations.

Return ONLY executable Python code.

Example:

result = {{
    "product": str(
        df.groupby("product")["sales"]
        .sum()
        .idxmax()
    ),
    "total_sales": int(
        df.groupby("product")["sales"]
        .sum()
        .max()
    )
}}
"""

        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0.0,
            messages=[
                {
                    "role": "system",
                    "content": prompt
                },
                {
                    "role": "user",
                    "content": question
                }
            ]
        )

        content = response.choices[0].message.content.strip()

        return self._clean_code(content)

    # ==========================================================
    # GENERATE NATURAL LANGUAGE ANSWER
    # ==========================================================

    def _generate_answer(
        self,
        question: str,
        results
    ):

        prompt = f"""
You are the response generation component of a data analysis agent.

User question:
{question}

Calculated results:
{results}

Write a concise and accurate answer based ONLY on the
calculated results.

Rules:

- Do not invent numbers.
- Do not perform new calculations.
- Do not assume currency or units unless established
  by the dataset.
- Do not mention Python.
- Do not mention Pandas.
- Do not mention internal tools.
- Do not mention the LLM.
- Clearly answer the user's question.
- If there are multiple relevant values, include them.
- Keep the answer concise.
"""

        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0.2,
            messages=[
                {
                    "role": "system",
                    "content": prompt
                },
                {
                    "role": "user",
                    "content": str(results)
                }
            ]
        )

        return response.choices[0].message.content.strip()

    # ==========================================================
    # MAIN ANALYSIS METHOD
    # ==========================================================

    def analyze(self, question: str):

        print(f"\nData analysis question: {question}")

        # ------------------------------------------------------
        # Check dataset
        # ------------------------------------------------------

        if self.df is None:

            return {
                "answer": (
                    "No dataset is currently loaded. "
                    "Please upload a CSV or Excel dataset first."
                ),
                "results": {},
                "charts": []
            }

        # ------------------------------------------------------
        # Generate analysis code
        # ------------------------------------------------------

        try:

            code = self._generate_analysis_code(question)

            print("\nGenerated analysis:")
            print(code)

        except Exception as e:

            return {
                "answer": "I could not generate the requested analysis.",
                "results": {},
                "charts": [],
                "error": str(e)
            }

        # ------------------------------------------------------
        # Execute analysis
        # ------------------------------------------------------

        execution = self.executor.execute(
            code,
            self.df
        )

        if not execution["success"]:

            print(
                f"Analysis execution error: "
                f"{execution['error']}"
            )

            return {
                "answer": (
                    "I could not complete the requested "
                    "data analysis."
                ),
                "results": {},
                "charts": [],
                "error": execution["error"]
            }

        results = execution["result"]

        print("\nAnalysis completed.")
        print(f"Results: {results}")

        # ------------------------------------------------------
        # Generate answer
        # ------------------------------------------------------

        try:

            answer = self._generate_answer(
                question,
                results
            )

        except Exception as e:

            answer = (
                f"The analysis was completed successfully. "
                f"Results: {results}"
            )

            print(f"Answer generation error: {e}")

        # ------------------------------------------------------
        # Generate chart if requested
        # ------------------------------------------------------

        charts = []

        if self._should_create_chart(question):

            chart_plan = self._generate_chart_plan(question)

            if chart_plan:

                print(
                    f"\nChart plan: {chart_plan}"
                )

                chart_path = self._create_chart(
                    chart_plan
                )

                if chart_path:

                    charts.append(chart_path)

        # ------------------------------------------------------
        # Return complete result
        # ------------------------------------------------------

        return {
            "answer": answer,
            "results": results,
            "charts": charts
        }