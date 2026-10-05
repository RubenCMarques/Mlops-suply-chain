import pandas as pd


def validate_raw_table(table: pd.DataFrame, required_columns: list[str]) -> pd.DataFrame:
    """Check that a downloaded table is usable and return it unchanged."""
    if table.empty:
        raise ValueError("Downloaded table has no rows")
    duplicated = table.columns[table.columns.duplicated()].tolist()
    if duplicated:
        raise ValueError(f"Downloaded table has duplicated columns: {duplicated}")
    missing = sorted(set(required_columns) - set(table.columns))
    if missing:
        raise ValueError(f"Downloaded table is missing required columns: {missing}")
    return table
