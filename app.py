import streamlit as st
import pandas as pd

# --- Title ---
st.title("📊 Sales Dashboard")

# --- Load Data ---
try:
    df = pd.read_csv("Cleaned_SalesData.csv")
except FileNotFoundError:
    st.error("❌ File not found! Please place Cleaned_SalesData.csv in the same folder.")
    st.stop()

# --- Data Check ---
st.write("### Data Preview", df.head())

# --- Dropdown for Region ---
regions = df["Region"].dropna().unique()
region = st.selectbox("Select Region", regions)

# --- Filtered Data ---
filtered = df[df["Region"] == region]

# --- Metrics ---
total_revenue = filtered["Revenue"].sum()
total_profit = filtered["Profit"].sum()

st.metric("💰 Total Revenue", f"₹{total_revenue:,.0f}")
st.metric("📈 Total Profit", f"₹{total_profit:,.0f}")

# --- Bar Chart ---
if not filtered.empty:
    profit_by_category = filtered.groupby("Category")["Profit"].sum()
    st.bar_chart(profit_by_category)
else:
    st.warning("No data available for this region.")


# --- Filters ---
col1, col2 = st.columns(2)

regions = df["Region"].dropna().unique()
categories = df["Category"].dropna().unique()

region = col1.selectbox("Select Region", ["All"] + list(regions))
category = col2.selectbox("Select Category", ["All"] + list(categories))

# --- Apply Filters ---
filtered = df.copy()
if region != "All":
    filtered = filtered[filtered["Region"] == region]
if category != "All":
    filtered = filtered[filtered["Category"] == category]


total_revenue = filtered["Revenue"].sum()
total_profit = filtered["Profit"].sum()
profit_margin = (total_profit / total_revenue * 100) if total_revenue else 0

kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("💰 Total Revenue", f"₹{total_revenue:,.0f}")
kpi2.metric("📈 Total Profit", f"₹{total_profit:,.0f}")
kpi3.metric("📊 Profit Margin", f"{profit_margin:.2f}%")

st.subheader("🏙 Profit by Region")
st.bar_chart(df.groupby("Region")["Profit"].sum())

st.subheader("📆 Revenue Trend Over Time")
df["Date"] = pd.to_datetime(df["Date"])
trend = df.groupby("Date")["Revenue"].sum()
st.line_chart(trend)


st.subheader("📋 Summary by Category and Region")
summary = df.groupby(["Region", "Category"]).agg(
    Revenue=("Revenue", "sum"),
    Profit=("Profit", "sum"),
    Margin=("Profit", lambda x: (x.sum()/df["Revenue"].sum())*100)
).reset_index()
st.dataframe(summary)


csv = filtered.to_csv(index=False).encode('utf-8')
st.download_button(
    label="⬇️ Download Filtered Data as CSV",
    data=csv,
    file_name='filtered_sales_data.csv',
    mime='text/csv',
)
