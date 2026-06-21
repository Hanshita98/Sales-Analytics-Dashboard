import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("📊 Sales Analytics Dashboard")

# Read CSV
df = pd.read_csv("sales.csv")

# -------------------------
# Sidebar Filter
# -------------------------

region = st.sidebar.selectbox(
    "Select Region",
    ["All"] + list(df["Region"].unique())
)

if region != "All":
    df = df[df["Region"] == region]

# -------------------------
# KPI Cards
# -------------------------

total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
total_orders = len(df)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("💰 Total Sales", f"₹{total_sales:,}")

with col2:
    st.metric("📈 Total Profit", f"₹{total_profit:,}")

with col3:
    st.metric("📦 Total Orders", total_orders)

# -------------------------
# Download Button
# -------------------------

st.download_button(
    label="📥 Download Report",
    data=df.to_csv(index=False),
    file_name="sales_report.csv",
    mime="text/csv"
)

st.divider()

# -------------------------
# Monthly Sales Trend
# -------------------------

monthly = df.groupby("Month")["Sales"].sum().reset_index()

fig1 = px.line(
    monthly,
    x="Month",
    y="Sales",
    title="📈 Monthly Sales Trend",
    markers=True
)

st.plotly_chart(fig1, use_container_width=True)

# -------------------------
# Sales by Region
# -------------------------

region_sales = df.groupby("Region")["Sales"].sum().reset_index()

fig2 = px.bar(
    region_sales,
    x="Region",
    y="Sales",
    title="🌍 Sales by Region"
)

st.plotly_chart(fig2, use_container_width=True)

# -------------------------
# Product Distribution
# -------------------------

product = df.groupby("Product")["Sales"].sum().reset_index()

fig3 = px.pie(
    product,
    names="Product",
    values="Sales",
    title="🥧 Product Distribution"
)

st.plotly_chart(fig3, use_container_width=True)

# -------------------------
# Top Products Table
# -------------------------

st.subheader("🏆 Top Products")

top_products = (
    df.groupby("Product")["Sales"]
    .sum()
    .reset_index()
    .sort_values(by="Sales", ascending=False)
)

st.dataframe(top_products, use_container_width=True)