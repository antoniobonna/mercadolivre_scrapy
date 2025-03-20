"""
Mercado Livre Data Processor

This script processes product data from Mercado Livre, performs data type conversions,
and stores the processed data in an SQLite database.

Usage:
    python process_mercadolivre_data.py
"""
import pandas as pd
import sqlite3
from datetime import datetime

# File paths
DATA_FILE_PATH = "../data/data.json"
DB_FILE_PATH = "../data/data.db"
TABLE_NAME = "mercadolivre"
SOURCE_URL = "https://lista.mercadolivre.com.br/geladeira-frost-free"

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load JSON data from a file into a DataFrame.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        pd.DataFrame: Raw DataFrame loaded from the JSON file.
    """
    # Load JSON data into a DataFrame
    df = pd.read_json(file_path)
    return df

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess the DataFrame by adding metadata and converting columns to appropriate types.

    Args:
        df (pd.DataFrame): Raw DataFrame to preprocess.

    Returns:
        pd.DataFrame: Preprocessed DataFrame.
    """
    # Add metadata columns
    df["_source"] = "https://lista.mercadolivre.com.br/geladeira-frost-free"
    df["_crawled_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Convert price columns from string to float
    # Replace commas with dots for proper decimal formatting
    price_columns = ["new_price", "old_price"]
    for col in price_columns:
        df[col] = df[col].astype(str).str.replace(",", ".", regex=False)
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Convert review columns to appropriate types
    df["review_rating_number"] = pd.to_numeric(df["review_rating_number"], errors="coerce")
    df["review_amount"] = pd.to_numeric(df["review_amount"], errors="coerce").astype("Int64")

    return df

def save_to_database(df: pd.DataFrame, db_path: str, table_name: str) -> None:
    """
    Save a DataFrame to a SQLite database.

    Args:
        df (pd.DataFrame): DataFrame to save.
        db_path (str): Path to the SQLite database file.
        table_name (str): Name of the table to save the data into.
    """
    # Connect to the SQLite database
    with sqlite3.connect(db_path) as conn:
        # Save the DataFrame to the database
        df.to_sql(table_name, conn, if_exists="replace", index=False)

def main() -> None:
    """
    Main function to load, preprocess, and save data.
    """
    # Define file paths and table name
    data_file_path = "../data/data.json"
    db_file_path = "../data/data.db"
    table_name = "mercadolivre"

    # Load the data
    df = load_data(data_file_path)

    # Preprocess the data
    df = preprocess_data(df)

    # Save the preprocessed data to the database
    save_to_database(df, db_file_path, table_name)

if __name__ == "__main__":
    main()
