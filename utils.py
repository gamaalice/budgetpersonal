# utils.py — data logic for Version 2.0
import os
import pandas as pd

CSV_PATH = "budget_data.csv"
COLUMNS = ["Date", "Category", "Subcategory", "Amount"]


def ensure_csv_exists():
    """
    Ensures the CSV file exists with the correct header.
    If it does not exist, creates an empty one with only the header.
    """
    if not os.path.exists(CSV_PATH):
        df = pd.DataFrame(columns=COLUMNS)
        df.to_csv(CSV_PATH, index=False)


def load_data():
    """
    Loads data from the CSV file.
    Returns a DataFrame with the correct columns.
    """
    ensure_csv_exists()
    df = pd.read_csv(CSV_PATH)
    if df.empty:
        return pd.DataFrame(columns=COLUMNS)
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce").fillna(0.0)
    return df


def save_data(df: pd.DataFrame):
    """
    Saves the DataFrame back to CSV.
    """
    df.to_csv(CSV_PATH, index=False)


def add_transaction(date: str, category: str, subcategory: str, amount: float):
    """
    Adds a new transaction to the CSV.
    """
    df = load_data()
    new_row = {
        "Date": date,
        "Category": category,
        "Subcategory": subcategory,
        "Amount": float(amount),
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    save_data(df)


def delete_transaction(index: int):
    """
    Deletes a transaction by its index (0-based).
    """
    df = load_data()
    if 0 <= index < len(df):
        df = df.drop(index).reset_index(drop=True)
        save_data(df)


def summary_totals():
    """
    Returns a simple total summary.
    Currently: total amount spent (sum of all Amount).
    """
    df = load_data()
    if df.empty:
        return {"total_spent": 0.0}
    total_spent = df["Amount"].sum()
    return {"total_spent": total_spent}


def summary_by_category():
    """
    Returns a DataFrame with columns: Category, TotalAmount.
    Used for charts and category summary.
    """
    df = load_data()
    if df.empty:
        return pd.DataFrame(columns=["Category", "TotalAmount"])
    agg = (
        df.groupby("Category")["Amount"]
        .sum()
        .reset_index()
        .rename(columns={"Amount": "TotalAmount"})
    )
    return agg

