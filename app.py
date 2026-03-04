import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from inventory_logic import calculate_inventory_metrics
from abc_analysis import abc_analysis
from reorder_system import reorder_calculation
from forecasting import demand_forecast

st.set_page_config(page_title="Smart Inventory Optimization Tool", layout="wide")

st.title("📦 Smart Inventory Optimization Tool")

st.write("Upload your inventory CSV file to analyze stock performance.")

# Upload file
uploaded_file = st.file_uploader("Upload Inventory File", type=["csv"])

if uploaded_file is None:
    st.warning("Please upload a CSV file to continue.")
    st.stop()

# Read dataset
df = pd.read_csv(uploaded_file)

st.subheader("Uploaded Data")
st.dataframe(df)

# Run analytics
df = calculate_inventory_metrics(df)
df = abc_analysis(df)
df = reorder_calculation(df)
df = demand_forecast(df)

# Navigation
page = st.sidebar.selectbox(
    "Select Module",
    ["Dashboard","Inventory Table","Reorder Suggestions","ABC Analysis","Demand Forecast"]
)

# DASHBOARD
if page == "Dashboard":

    st.header("Inventory Health Dashboard")

    total_products = len(df)
    inventory_value = df["Inventory_Value"].sum()
    reorder_items = len(df[df["Stock_Status"]=="Reorder"])
    overstock_items = len(df[df["Stock_Status"]=="Overstock"])

    col1,col2,col3,col4 = st.columns(4)

    col1.metric("Total Products", total_products)
    col2.metric("Inventory Value", f"₹{round(inventory_value)}")
    col3.metric("Reorder Needed", reorder_items)
    col4.metric("Overstock Items", overstock_items)

# INVENTORY TABLE
elif page == "Inventory Table":

    st.header("Inventory Details")

    st.dataframe(df)

# REORDER
elif page == "Reorder Suggestions":

    st.header("Reorder Recommendations")

    reorder_df = df[df["Reorder_Quantity"] > 0]

    st.dataframe(reorder_df[[
        "Product",
        "Current_Stock",
        "Reorder_Point",
        "Reorder_Quantity"
    ]])

# ABC ANALYSIS
elif page == "ABC Analysis":

    st.header("ABC Classification")

    st.dataframe(df[["Product","Sales_Value","ABC_Category"]])

    fig, ax = plt.subplots()

    abc_counts = df["ABC_Category"].value_counts()

    ax.pie(abc_counts, labels=abc_counts.index, autopct="%1.1f%%")

    st.pyplot(fig)

# FORECAST
elif page == "Demand Forecast":

    st.header("Next Month Demand Forecast")

    st.dataframe(df[["Product","Forecast_Next_Month"]])

    fig, ax = plt.subplots()

    ax.bar(df["Product"], df["Forecast_Next_Month"])

    ax.set_xlabel("Product")
    ax.set_ylabel("Forecast Demand")

    plt.xticks(rotation=45)

    st.pyplot(fig)
