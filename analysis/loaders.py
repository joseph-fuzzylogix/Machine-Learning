"""Shared helpers for loading and profiling Excel / CSV files."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"
OUTPUTS_DIR = ROOT / "outputs"


def list_source_files() -> list[Path]:
    """Return uploaded source files in data/raw (Excel + CSV)."""
    patterns = ("*.xlsx", "*.xls", "*.xlsm", "*.csv")
    files: list[Path] = []
    for pattern in patterns:
        files.extend(sorted(RAW_DIR.glob(pattern)))
    return files


def load_table(path: Path, sheet_name: str | int | None = 0, **kwargs: Any) -> pd.DataFrame:
    """Load a single Excel sheet or CSV into a DataFrame."""
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(path, **kwargs)
    if suffix in {".xlsx", ".xls", ".xlsm"}:
        return pd.read_excel(path, sheet_name=sheet_name, **kwargs)
    raise ValueError(f"Unsupported file type: {path}")


def list_excel_sheets(path: Path) -> list[str]:
    """List sheet names for an Excel workbook."""
    if path.suffix.lower() not in {".xlsx", ".xls", ".xlsm"}:
        return []
    workbook = pd.ExcelFile(path)
    return list(workbook.sheet_names)


def profile_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Return a compact column profile for quick data understanding."""
    rows = []
    for column in df.columns:
        series = df[column]
        rows.append(
            {
                "column": column,
                "dtype": str(series.dtype),
                "non_null": int(series.notna().sum()),
                "nulls": int(series.isna().sum()),
                "null_pct": round(float(series.isna().mean() * 100), 2),
                "unique": int(series.nunique(dropna=True)),
                "sample": series.dropna().astype(str).head(3).tolist(),
            }
        )
    return pd.DataFrame(rows)


def inventory_sources() -> pd.DataFrame:
    """Summarize every uploaded file and Excel sheet."""
    records = []
    for path in list_source_files():
        rel = path.relative_to(ROOT).as_posix()
        if path.suffix.lower() == ".csv":
            df = load_table(path)
            records.append(
                {
                    "file": rel,
                    "sheet": None,
                    "rows": len(df),
                    "columns": len(df.columns),
                    "column_names": list(df.columns),
                }
            )
            continue

        for sheet in list_excel_sheets(path):
            df = load_table(path, sheet_name=sheet)
            records.append(
                {
                    "file": rel,
                    "sheet": sheet,
                    "rows": len(df),
                    "columns": len(df.columns),
                    "column_names": list(df.columns),
                }
            )
    return pd.DataFrame(records)
