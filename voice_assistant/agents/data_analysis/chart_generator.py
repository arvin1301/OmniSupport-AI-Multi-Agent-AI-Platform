import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path


class ChartGenerator:

    def __init__(self, output_dir="data/charts"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def bar_chart(
        self,
        df: pd.DataFrame,
        category_column: str,
        value_column: str,
        filename: str = "bar_chart.png",
    ):

        if category_column not in df.columns:
            raise ValueError(f"Column not found: {category_column}")

        if value_column not in df.columns:
            raise ValueError(f"Column not found: {value_column}")

        grouped = (
            df.groupby(category_column)[value_column]
            .sum()
            .sort_values(ascending=False)
        )

        output_path = self.output_dir / filename

        plt.figure(figsize=(10, 6))
        grouped.plot(kind="bar")
        plt.title(f"{value_column} by {category_column}")
        plt.xlabel(category_column)
        plt.ylabel(value_column)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()

        print(f" Chart saved: {output_path}")

        return str(output_path)

    def line_chart(
        self,
        df: pd.DataFrame,
        x_column: str,
        y_column: str,
        filename: str = "line_chart.png",
    ):

        if x_column not in df.columns:
            raise ValueError(f"Column not found: {x_column}")

        if y_column not in df.columns:
            raise ValueError(f"Column not found: {y_column}")

        output_path = self.output_dir / filename

        plt.figure(figsize=(10, 6))
        plt.plot(df[x_column], df[y_column], marker="o")
        plt.title(f"{y_column} over {x_column}")
        plt.xlabel(x_column)
        plt.ylabel(y_column)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()

        print(f" Chart saved: {output_path}")

        return str(output_path)

    def histogram(
        self,
        df: pd.DataFrame,
        column: str,
        filename: str = "histogram.png",
    ):

        if column not in df.columns:
            raise ValueError(f"Column not found: {column}")

        output_path = self.output_dir / filename

        plt.figure(figsize=(10, 6))
        plt.hist(df[column].dropna(), bins=10)
        plt.title(f"Distribution of {column}")
        plt.xlabel(column)
        plt.ylabel("Frequency")
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()

        print(f" Histogram saved: {output_path}")

        return str(output_path)