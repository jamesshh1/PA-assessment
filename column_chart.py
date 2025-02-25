import pandas as pd
import plotly.express as px
import streamlit as st

# Load the dataset
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_transactions.csv")
    return df

df = load_data()

# Define the function to generate the column chart
def generate_column_chart(x_axis: str):
    """Generates a stacked column chart based on the selected x-axis category."""
    # Aggregate data
    agg_df = df.groupby([x_axis, "Payment Method"], as_index=False).agg(
        {
            "Amount (£)": ["sum", "median"],
            "Transaction ID": "count"
        }
    )

    # Rename columns for clarity
    agg_df.columns = [x_axis, "Payment Method", "Total Amount (£)", "Median Transaction Value (£)", "Number of Transactions"]

    # Create stacked column chart
    fig = px.bar(
        agg_df, x=x_axis, y="Total Amount (£)", color="Payment Method",
        title=f"Total Transaction Amount by {x_axis}",
        labels={"Total Amount (£)": "Total Amount (£)"},
        barmode="stack",
        hover_data={
            "Number of Transactions": True,
            "Median Transaction Value (£)": True,
            "Total Amount (£)": True
        }
    )

    return fig
