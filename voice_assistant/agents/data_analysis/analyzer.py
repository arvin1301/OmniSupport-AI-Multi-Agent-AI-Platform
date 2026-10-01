import pandas as pd


class DataAnalyzer:

    def basic_statistics(self, df: pd.DataFrame) -> dict:
        numeric_df = df.select_dtypes(include="number")

        if numeric_df.empty:
            return {}

        return numeric_df.describe().to_dict()

    def column_summary(self, df: pd.DataFrame) -> list:
        summary = []

        for column in df.columns:
            summary.append({
                "column": column,
                "dtype": str(df[column].dtype),
                "unique_values": int(df[column].nunique()),
                "missing_values": int(df[column].isna().sum()),
            })

        return summary

    def numeric_correlations(self, df: pd.DataFrame) -> dict:
        numeric_df = df.select_dtypes(include="number")

        if numeric_df.shape[1] < 2:
            return {}

        return numeric_df.corr().round(3).to_dict()

    def categorical_summary(self, df: pd.DataFrame) -> dict:
        result = {}

        categorical_df = df.select_dtypes(include=["object", "category"])

        for column in categorical_df.columns:
            result[column] = (
                df[column]
                .value_counts()
                .to_dict()
            )

        return result

    def analyze(self, df: pd.DataFrame) -> dict:
        return {
            "basic_statistics": self.basic_statistics(df),
            "column_summary": self.column_summary(df),
            "correlations": self.numeric_correlations(df),
            "categorical_summary": self.categorical_summary(df),
        }