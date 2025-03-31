import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, on March 17th")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
st.dataframe(df.groupby("Category").sum())
# Using as_index=False here preserves the Category as a column.  If we exclude that, Category would become the datafram index and we would need to use x=None to tell bar_chart to use the index
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")
category_selected = st.selectbox("Select a Category", df['Category'].unique())
#2
filtered_df = df[df['Category'] == category_selected]

if not filtered_df.empty and 'Sub-Category' in filtered_df.columns:
    subcategories = filtered_df['Sub-Category'].dropna().unique()
    subcategories_selected = st.multiselect("Select Sub-Category", subcategories, default=subcategories)
    
    final_selection = filtered_df[filtered_df['Sub-Category'].isin(subcategories_selected)]
else:
    st.warning("No sub-categories found for the selected category.")
    final_selection = pd.DataFrame() 



# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set is as an index to our dataframe
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
# Here the Grouper is using our newly set index to group by Month ('M')
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

st.dataframe(sales_by_month)

# Here the grouped months are the index and automatically used for the x axis
st.line_chart(sales_by_month, y="Sales")

st.write("## Your additions")
st.write("### (1) add a drop down for Category (https://docs.streamlit.io/library/api-reference/widgets/st.selectbox)")
st.write("### (2) add a multi-select for Sub_Category *in the selected Category (1)* (https://docs.streamlit.io/library/api-reference/widgets/st.multiselect)")
st.write("### (3) show a line chart of sales for the selected items in (2)")
st.write("### (4) show three metrics (https://docs.streamlit.io/library/api-reference/data/st.metric) for the selected items in (2): total sales, total profit, and overall profit margin (%)")
st.write("### (5) use the delta option in the overall profit margin metric to show the difference between the overall average profit margin (all products across all categories)")



#3
if not final_selection.empty:
    sales_by_month_selected = final_selection['Sales'].resample('M').sum()
    st.line_chart(sales_by_month_selected)
else:
    st.write("No data available for selected sub-categories.")

#4
total_sales = final_selection['Sales'].sum()
total_profit = final_selection['Profit'].sum()
profit_margin = (total_profit / total_sales * 100) if total_sales != 0 else 0

#5
overall_total_sales = df['Sales'].sum()
overall_total_profit = df['Profit'].sum()
overall_profit_margin = (overall_total_profit / overall_total_sales * 100)
profit_margin_delta = profit_margin - overall_profit_margin


col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Total Profit", f"${total_profit:,.2f}")
col3.metric("Profit Margin", f"{profit_margin:.2f}%", f"{profit_margin_delta:+.2f}%")
