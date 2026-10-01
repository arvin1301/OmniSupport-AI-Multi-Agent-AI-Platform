import pandas as pd
import numpy as np


class PythonExecutor:

    def __init__(self):
        self.allowed_builtins = {
            "len": len,
            "min": min,
            "max": max,
            "sum": sum,
            "round": round,
            "abs": abs,
            "int": int,
            "float": float,
            "str": str,
            "bool": bool,
        }

    def execute(self, code: str, df: pd.DataFrame):
        """
        Execute controlled Python analysis code against a DataFrame.

        Available variables:
            df -> pandas DataFrame
            pd -> pandas
            np -> numpy
        """

        if not code or not code.strip():
            return {
                "success": False,
                "result": None,
                "error": "No code provided.",
            }

        namespace = {
            "__builtins__": self.allowed_builtins,
            "pd": pd,
            "np": np,
            "df": df.copy(),
        }

        try:
            exec(code, namespace)

            result = namespace.get("result")

            return {
                "success": True,
                "result": result,
                "error": None,
            }

        except Exception as e:
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }