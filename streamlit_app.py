import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, on Oct 7th")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Aggregated bar chart
st.dataframe(df.groupby("Category").sum())
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Convert Order_Date and set index
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)

# Aggregate sales by month
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()
st.dataframe(sales_by_month)
st.line_chart(sales_by_month, y="Sales")

# Section for user additions
st.write("## Your additions")
st.write("### (1) add a drop down for Category (https://docs.streamlit.io/library/api-reference/widgets/st.selectbox)")

# (1) Dropdown for Category
categories = df['Category'].unique().tolist()
selected_category = st.selectbox("Select a Category", categories)

# (2) Multiselect for Sub_Category in selected Category
st.write("### (2) Add a multi-select for Sub_Category in the selected Category")
df1 = df[df['Category'] == selected_category]
subcategories = df1['Sub_Category'].unique()
selected_subcategories = st.multiselect("Select Subcategories", subcategories)

# (3) Line chart of sales by month for selected subcategories (summed as one line)
st.write("### (3) Show a line chart of sales for the selected items in (2)")
if selected_subcategories:
    df2 = df1[df1['Sub_Category'].isin(selected_subcategories)]
    sales_by_month1 = df2.groupby(pd.Grouper(freq='M'))['Sales'].sum()
    st.line_chart(sales_by_month1)

    # (4) Metrics for selected items
    st.write("### (4) Show three metrics for the selected items in (2): total sales, total profit, and overall profit margin (%)")
    total_sales = df2['Sales'].sum()
    total_profit = df2['Profit'].sum()
    overall_sales = df['Sales'].sum()
    overall_profit = df['Profit'].sum()

    avg_margin_all = overall_profit / overall_sales if overall_sales else 0
    avg_margin_selected = total_profit / total_sales if total_sales else 0
    delta = avg_margin_selected - avg_margin_all

    st.metric("Total Sales", f"${total_sales:,.2f}")
    st.metric("Total Profit", f"${total_profit:,.2f}")
    st.metric("Average Profit Margin", f"{avg_margin_selected:.2%}", delta=f"{delta:.2%}")
else:
    st.warning("Please select at least one Sub-Category to display metrics and chart.")

# (5) Notes on what was added
st.write("## Your additions")
st.write("### (1) add a drop down for Category (https://docs.streamlit.io/library/api-reference/widgets/st.selectbox)")
st.write("### (2) add a multi-select for Sub_Category *in the selected Category (1)* (https://docs.streamlit.io/library/api-reference/widgets/st.multiselect)")
st.write("### (3) show a line chart of sales for the selected items in (2)")
st.write("### (4) show three metrics (https://docs.streamlit.io/library/api-reference/data/st.metric) for the selected items in (2): total sales, total profit, and overall profit margin (%)")
st.write("### (5) use the delta option in the overall profit margin metric to show the difference between the overall average profit margin (all products across all categories)")
