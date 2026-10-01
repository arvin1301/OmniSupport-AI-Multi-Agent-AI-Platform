from pathlib import Path
import pandas as pd


class DataLoader:

    SUPPORTED_EXTENSIONS = {".csv", ".xlsx", ".xls"}

    def load(self, file_path: str) -> pd.DataFrame:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported file type: {path.suffix}. "
                f"Supported types: {', '.join(self.SUPPORTED_EXTENSIONS)}"
            )

        print(f"📂 Loading dataset: {path.name}")

        if path.suffix.lower() == ".csv":
            df = pd.read_csv(path)

        elif path.suffix.lower() in {".xlsx", ".xls"}:
            df = pd.read_excel(path)

        else:
            raise ValueError("Unsupported file format.")

        print(f"✅ Dataset loaded: {df.shape[0]} rows × {df.shape[1]} columns")

        return df

    def get_overview(self, df: pd.DataFrame) -> dict:
        return {
            "rows": int(df.shape[0]),
            "columns": int(df.shape[1]),
            "column_names": df.columns.tolist(),
            "data_types": {
                column: str(dtype)
                for column, dtype in df.dtypes.items()
            },
            "missing_values": {
                column: int(value)
                for column, value in df.isna().sum().items()
                if value > 0
            },
            "duplicate_rows": int(df.duplicated().sum()),
        }