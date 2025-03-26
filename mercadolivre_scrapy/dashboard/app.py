"""
Frost-Free Refrigerators Market Analysis Dashboard

This Streamlit application analyzes market data for frost-free refrigerators,
displaying key performance indicators, brand distribution, pricing analysis,
and customer satisfaction metrics.

Features:
- Key Performance Indicators (KPIs)
- Top brands distribution
- Average prices by brand
- Customer satisfaction by brand
"""

import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st

# Constants
DATABASE_PATH = Path("../../data/data.db")
QUERY = "SELECT * FROM mercadolivre"
DASHBOARD_TITLE = "Pesquisa de Mercado - Geladeiras Froost Free"
CHART_WIDTH_RATIO = [4, 2]  # Width ratio for chart vs data display columns


def load_data(database_path: Path, query: str) -> pd.DataFrame:
    """
    Load data from SQLite database into a pandas DataFrame.

    Args:
        database_path: Path to the SQLite database file
        query: SQL query to execute

    Returns:
        pandas DataFrame containing the query results
    """
    try:
        conn = sqlite3.connect(database_path)
        return pd.read_sql_query(query, conn)
    finally:
        conn.close()


def display_kpi_metrics(df: pd.DataFrame) -> None:
    """
    Display key performance indicators in a 3-column layout.

    Args:
        df: DataFrame containing the market research data
    """
    st.subheader("KPIs principais do sistema")

    col1, col2, col3 = st.columns(3)

    # Total items KPI
    col1.metric(label="Total de itens", value=df.shape[0])

    # Unique brands KPI
    col2.metric(label="Total de marcas", value=df["brand"].nunique())

    # Average price KPI
    col3.metric(label="Preço Médio Novo (R$)", value=f"{df['new_price'].mean():.2f}")


def display_top_brands(df: pd.DataFrame) -> None:
    """
    Display top 10 brands distribution with bar chart and data table.

    Args:
        df: DataFrame containing the market research data
    """
    st.subheader("Marcas mais encontradas")

    # Create column layout with larger space for chart
    col1, col2 = st.columns(CHART_WIDTH_RATIO)

    # Get top 10 brands by count, sorted in descending orde
    top_brands = df["brand"].value_counts().head(10).sort_values(ascending=False)

    # Display bar chart and data
    col1.bar_chart(top_brands)
    col2.write(top_brands)


def display_average_prices(df: pd.DataFrame) -> None:
    """
    Display average prices by brand with bar chart and data table.

    Args:
        df: DataFrame containing the market research data
    """
    st.subheader("Preços médio por marca")

    # Create column layout with larger space for chart
    col1, col2 = st.columns(CHART_WIDTH_RATIO)

    # Calculate average prices by brand
    average_prices = df.groupby("brand")["new_price"].mean().sort_values(ascending=False)

    # Display bar chart and data
    col1.bar_chart(average_prices)
    col2.write(average_prices)


def display_satisfaction_ratings(df: pd.DataFrame) -> None:
    """
    Display customer satisfaction ratings by brand with bar chart and data table.

    Args:
        df: DataFrame containing the market research data
    """
    st.subheader("Satisfação por marca")

    # Create column layout with larger space for chart
    col1, col2 = st.columns(CHART_WIDTH_RATIO)

    # Calculate average satisfaction ratings by brand
    satisfaction = df.groupby("brand")["review_rating_number"].mean().sort_values(ascending=False)

    # Display bar chart and data
    col1.bar_chart(satisfaction)
    col2.write(satisfaction)


def main():
    """
    Main function to run the Streamlit application.
    Sets up the page and orchestrates all dashboard components.
    """
    # Set page title and configuration
    st.set_page_config(page_title="Análise de Mercado - Geladeiras Frost Free", layout="wide")

    # Display application title
    st.title(DASHBOARD_TITLE)

    # Load data
    df = load_data(DATABASE_PATH, QUERY)

    # Check if data was loaded successfully
    if df.empty:
        st.warning("Não foi possível carregar os dados. Verifique o caminho do banco de dados.")
        return

    # Display all dashboard components
    display_kpi_metrics(df)
    display_top_brands(df)
    display_average_prices(df)
    display_satisfaction_ratings(df)


if __name__ == "__main__":
    main()
