import streamlit as st
import pandas as pd
import os
import plotly.express as px

# Set page config
st.set_page_config(page_title="Payments Intelligence interactive table", layout="wide")

# Centered title using markdown and HTML
st.markdown(
    "<h1 style='text-align: center;'>Payments Intelligence</h1>", 
    unsafe_allow_html=True
)

st.markdown(
    "<h4 style='text-align: center; font-weight: normal;'>Select a category to drill down into the payments data</h4>", 
    unsafe_allow_html=True
)

# Interactive table

# Load transaction data
@st.cache_data
def load_data():
    return pd.read_csv("cleaned_transactions.csv")

df = load_data()

# Define selectable categories
category_options = [
    "Merchant Category",
    "Location",
    "Customer Segment",
    "Sales Channel",
    "Customer Device Type"
]


# Dropdown menu for category selection
selected_category = st.selectbox("Select a category to see the most common payment method, number of transactions and median transaction value for each market segment:", category_options)

if selected_category:
    # Compute the most common payment method, transaction count, and median transaction value
    summary_df = (
        df.groupby(selected_category)
        .agg(
            most_common_payment_method=("Payment Method", lambda x: x.mode()[0] if not x.mode().empty else "No Data"),
            number_of_transactions=("Payment Method", "count"),
            median_transaction_value=("Amount (£)", "median"),
        )
        .reset_index()
    )

    # Rank the table so that the highest count is '1'
    summary_df["rank"] = summary_df["number_of_transactions"].rank(method="dense", ascending=False).astype(int)
    summary_df = summary_df.sort_values(by="rank")

    # Reorder columns to display rank first
    summary_df = summary_df[["rank", selected_category, "most_common_payment_method", "number_of_transactions", "median_transaction_value"]]

    # Reset index to remove the default index column
    summary_df = summary_df.reset_index(drop=True)

    # Rename columns with spaces and lowercase except first letter
    summary_df.columns = [col.replace("_", " ").capitalize() for col in summary_df.columns]

    # Format median transaction value with '£' symbol
    summary_df["Median transaction value"] = summary_df["Median transaction value"].apply(lambda x: f"£{x:,.2f}")

    # Use Markdown for smaller font size
    st.markdown(f"<h4 style='font-size:18px;'>Most common payment method by: {selected_category}</h4>", unsafe_allow_html=True)

    # Display table without the far-left index column
    st.dataframe(summary_df, hide_index=True)