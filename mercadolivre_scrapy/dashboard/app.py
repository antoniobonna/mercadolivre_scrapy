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

import locale
import sqlite3
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_card import card

# Set locale for Brazilian Portuguese formatting
locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")

# Constants
DATABASE_PATH = Path("../../data/data.db")
QUERY = "SELECT * FROM mercadolivre"
DASHBOARD_TITLE = "Pesquisa de Mercado - Geladeiras Frost-Free"
THEME_COLOR = "#3498db"  # Primary theme color
SECONDARY_COLOR = "#2ecc71"  # Secondary theme color for accents

# Custom CSS for styling
CUSTOM_CSS = """
<style>
    .main-header {
        color: #2c3e50;
        font-family: 'Helvetica Neue', sans-serif;
        padding-bottom: 20px;
        border-bottom: 2px solid #ecf0f1;
        margin-bottom: 30px;
    }

    .subheader {
        color: #34495e;
        font-family: 'Helvetica Neue', sans-serif;
        padding-top: 20px;
        padding-bottom: 10px;
        border-bottom: 1px solid #ecf0f1;
        margin-bottom: 15px;
    }

    .stMetric {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 10px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }

    .stMetric label {
        font-weight: bold;
        color: #34495e;
    }

    .stMetric .value {
        font-size: 24px;
        font-weight: bold;
        color: #3498db;
    }

    .chart-container {
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }

    .data-table {
        background-color: white;
        border-radius: 10px;
        padding: 10px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }
</style>
"""


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
        df = pd.read_sql_query(query, conn)

        # Clean and prepare data
        df["brand"] = df["brand"].str.title()  # Capitalize brand names properly

        return df
    except sqlite3.Error as e:
        st.error(f"Erro ao acessar o banco de dados: {e}")
        return pd.DataFrame()
    finally:
        if "conn" in locals():
            conn.close()


def format_currency(value) -> str:
    """
    Format currency value to Brazilian Real format (R$ _.___,__).

    Args:
        value: Numeric value to format

    Returns:
        Formatted currency string
    """
    try:
        # Format as requested: R$ _.___,__
        return f"R$ {value:_.2f}".replace(".", ",").replace("_", ".")
    except:
        return f"R$ {value:.2f}".replace(".", ",")


def display_kpi_metrics(df: pd.DataFrame) -> None:
    """
    Display key performance indicators in a 3-column layout with styled cards.

    Args:
        df: DataFrame containing the market research data
    """
    st.markdown('<div class="subheader">KPIs Principais do Sistema</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    # Total items KPI with icon
    with col1:
        card(
            title="Total de Itens",
            text=f"{df.shape[0]}",
            image="https://cdn-icons-png.flaticon.com/512/3500/3500833.png",
            key="items_card",
        )

    # Unique brands KPI with icon
    with col2:
        card(
            title="Total de Marcas",
            text=f"{df['brand'].nunique()}",
            image="https://cdn-icons-png.flaticon.com/512/1170/1170678.png",
            key="brands_card",
        )

    # Average price KPI with formatted currency and icon
    avg_price = df["new_price"].mean()
    with col3:
        card(
            title="Preço Médio",
            text=format_currency(avg_price),
            image="https://cdn-icons-png.flaticon.com/512/639/639365.png",
            key="price_card",
        )


def display_top_brands(df: pd.DataFrame) -> None:
    """
    Display top 10 brands distribution with interactive bar chart and data table.

    Args:
        df: DataFrame containing the market research data
    """
    st.markdown('<div class="subheader">Marcas mais Encontradas</div>', unsafe_allow_html=True)

    # Create column layout with larger space for chart
    col1, col2 = st.columns([3, 1])

    # Get top 10 brands by count, sorted in descending order
    top_brands_data = df["brand"].value_counts().reset_index()
    top_brands_data.columns = ["Marca", "Quantidade"]
    top_brands_data = top_brands_data.head(10).sort_values("Quantidade", ascending=True)

    # Create interactive bar chart with Plotly
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig = px.bar(
            top_brands_data,
            y="Marca",
            x="Quantidade",
            orientation="h",
            color="Quantidade",
            color_continuous_scale=["#BDE0FE", "#3498db", "#1A5276"],
            title="Top 10 Marcas por Quantidade de Produtos",
            text="Quantidade",
        )
        fig.update_layout(
            height=400,
            xaxis_title="Quantidade de Produtos",
            yaxis_title="",
            coloraxis_showscale=False,
            hoverlabel=dict(bgcolor="white", font_size=12),
            margin=dict(l=0, r=0, t=40, b=0),
        )
        fig.update_traces(
            texttemplate="%{x}",
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>Quantidade: %{x}<extra></extra>",
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Display data table with styling
    with col2:
        st.markdown('<div class="data-table">', unsafe_allow_html=True)
        st.dataframe(
            top_brands_data.sort_values("Quantidade", ascending=False),
            column_config={"Quantidade": st.column_config.NumberColumn(format="%d")},
            hide_index=True,
            use_container_width=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)


def display_average_prices(df: pd.DataFrame) -> None:
    """
    Display average prices by brand with interactive bar chart and data table.

    Args:
        df: DataFrame containing the market research data
    """
    st.markdown('<div class="subheader">Preços Médios por Marca</div>', unsafe_allow_html=True)

    # Create column layout with larger space for chart
    col1, col2 = st.columns([3, 1])

    # Calculate average prices by brand
    avg_prices = df.groupby("brand")["new_price"].mean().reset_index()
    avg_prices.columns = ["Marca", "Preço Médio"]
    avg_prices = avg_prices.sort_values("Preço Médio", ascending=True).tail(10)

    # Create interactive bar chart with Plotly
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig = px.bar(
            avg_prices,
            y="Marca",
            x="Preço Médio",
            orientation="h",
            color="Preço Médio",
            color_continuous_scale=["#ABEBC6", "#2ecc71", "#196F3D"],
            title="Top 10 Marcas por Preço Médio",
            text_auto=".2f",
        )
        fig.update_layout(
            height=400,
            xaxis_title="Preço Médio (R$)",
            yaxis_title="",
            coloraxis_showscale=False,
            hoverlabel=dict(bgcolor="white", font_size=12),
            margin=dict(l=0, r=0, t=40, b=0),
        )
        fig.update_traces(
            texttemplate="R$ %{x:.2f}",
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>Preço Médio: R$ %{x:.2f}<extra></extra>",
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Display data table with styled currency values
    with col2:
        st.markdown('<div class="data-table">', unsafe_allow_html=True)
        st.dataframe(
            avg_prices.sort_values("Preço Médio", ascending=False),
            column_config={
                "Preço Médio": st.column_config.NumberColumn(
                    "Preço Médio",
                    format="R$ %.2f",
                ),
            },
            hide_index=True,
            use_container_width=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)


def display_satisfaction_ratings(df: pd.DataFrame) -> None:
    """
    Display customer satisfaction ratings by brand with interactive bar chart and data table.

    Args:
        df: DataFrame containing the market research data
    """
    st.markdown('<div class="subheader">Satisfação por Marca</div>', unsafe_allow_html=True)

    # Create column layout with larger space for chart
    col1, col2 = st.columns([3, 1])

    # Calculate average satisfaction ratings by brand
    satisfaction = df.groupby("brand")["review_rating_number"].mean().reset_index()
    satisfaction.columns = ["Marca", "Avaliação Média"]
    satisfaction = satisfaction.sort_values("Avaliação Média", ascending=True).tail(10)

    # Create interactive bar chart with Plotly
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig = px.bar(
            satisfaction,
            y="Marca",
            x="Avaliação Média",
            orientation="h",
            color="Avaliação Média",
            color_continuous_scale=["#F9E79F", "#f39c12", "#9A7D0A"],
            range_color=[3.5, 5],
            title="Top 10 Marcas por Avaliação dos Clientes",
            text_auto=".1f",
        )
        fig.update_layout(
            height=400,
            xaxis_title="Avaliação Média (0-5)",
            xaxis=dict(range=[3, 5]),  # Focus on the range that matters
            yaxis_title="",
            coloraxis_showscale=False,
            hoverlabel=dict(bgcolor="white", font_size=12),
            margin=dict(l=0, r=0, t=40, b=0),
        )
        fig.update_traces(
            texttemplate="%{x:.1f} ★",
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>Avaliação: %{x:.1f} ★<extra></extra>",
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Display data table with styled ratings
    with col2:
        st.markdown('<div class="data-table">', unsafe_allow_html=True)
        st.dataframe(
            satisfaction.sort_values("Avaliação Média", ascending=False),
            column_config={
                "Avaliação Média": st.column_config.NumberColumn(
                    "Avaliação Média",
                    format="%.1f ★",
                ),
            },
            hide_index=True,
            use_container_width=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)


def display_data_filters(df: pd.DataFrame) -> pd.DataFrame:
    """
    Display filters for the dashboard data.

    Args:
        df: Original DataFrame containing the market research data

    Returns:
        Filtered DataFrame based on user selections
    """
    st.sidebar.markdown("## Filtros")

    # Brand filter
    selected_brands = st.sidebar.multiselect(
        "Filtrar por Marca:", options=sorted(df["brand"].unique()), default=[]
    )

    # Price range filter
    min_price = float(df["new_price"].min())
    max_price = float(df["new_price"].max())
    price_range = st.sidebar.slider(
        "Faixa de Preço (R$):",
        min_value=min_price,
        max_value=max_price,
        value=(min_price, max_price),
        format="R$ %.2f",
    )

    # Rating filter
    rating_range = st.sidebar.slider(
        "Avaliação Mínima:", min_value=0.0, max_value=5.0, value=0.0, step=0.5, format="%.1f ★"
    )

    # Apply filters
    filtered_df = df.copy()

    if selected_brands:
        filtered_df = filtered_df[filtered_df["brand"].isin(selected_brands)]

    filtered_df = filtered_df[
        (filtered_df["new_price"] >= price_range[0])
        & (filtered_df["new_price"] <= price_range[1])
        & (filtered_df["review_rating_number"] >= rating_range)
    ]

    # Display number of filtered items
    st.sidebar.markdown(f"**{len(filtered_df)} produtos** correspondem aos filtros.")

    return filtered_df


def main():
    """
    Main function to run the Streamlit application.
    Sets up the page and orchestrates all dashboard components.
    """
    # Set page title and configuration
    st.set_page_config(
        page_title="Análise de Mercado - Geladeiras Frost-Free",
        page_icon="❄️",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Apply custom CSS
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    # Display application title with styled header
    st.markdown(
        f'<div class="main-header"><h1>{DASHBOARD_TITLE}</h1></div>', unsafe_allow_html=True
    )

    # Add dashboard description
    with st.expander("ℹ️ Sobre este Dashboard", expanded=False):
        st.markdown("""
        Este dashboard apresenta uma análise detalhada do mercado de geladeiras frost-free,
        baseada em dados coletados do Mercado Livre. Você pode visualizar estatísticas importantes
        como preços médios, distribuição de marcas e avaliações de clientes.

        **Funcionalidades:**
        - Indicadores de desempenho (KPIs)
        - Distribuição das principais marcas
        - Análise de preços por marca
        - Métricas de satisfação do cliente

        Use os filtros no menu lateral para refinar sua análise.
        """)

    try:
        # Load data
        df = load_data(DATABASE_PATH, QUERY)

        # Check if data was loaded successfully
        if df.empty:
            st.warning(
                "⚠️ Não foi possível carregar os dados. Verifique o caminho do banco de dados."
            )
            return

        # Apply data filters
        filtered_df = display_data_filters(df)

        # Add filter indicator
        if len(filtered_df) < len(df):
            st.info(
                f"📊 Exibindo {len(filtered_df)} de {len(df)} produtos. Use os filtros à esquerda."
            )

        # Display all dashboard components with filtered data
        display_kpi_metrics(filtered_df)
        display_top_brands(filtered_df)
        display_average_prices(filtered_df)
        display_satisfaction_ratings(filtered_df)

        # Add footer
        st.markdown("---")
        st.markdown(
            "<div style='text-align: center; color: #7f8c8d; padding: 10px;'>"
            "© 2025 Análise de Mercado - Geladeiras Frost-Free"
            "</div>",
            unsafe_allow_html=True,
        )

    except Exception as e:
        st.error(f"❌ Ocorreu um erro: {e}")
        st.exception(e)


if __name__ == "__main__":
    main()
