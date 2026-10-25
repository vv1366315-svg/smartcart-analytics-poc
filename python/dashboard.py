from pathlib import Path
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "sample_events.csv"

st.set_page_config(page_title="SmartCart Analytics", page_icon="🛒", layout="wide")
st.title("SmartCart Analytics")
st.caption("E-commerce tracking and conversion analysis · Synthetic sample data only")

df = pd.read_csv(DATA_PATH)
event_sessions = df.groupby("event_name")["session_id"].nunique().to_dict()
views = event_sessions.get("view_item", 0)
carts = event_sessions.get("add_to_cart", 0)
checkouts = event_sessions.get("begin_checkout", 0)
purchases = event_sessions.get("purchase", 0)

def rate(a, b):
    return f"{a / b * 100:.1f}%" if b else "N/A"

col1, col2, col3, col4 = st.columns(4)
col1.metric("Unique users", f"{df['user_id'].nunique():,}")
col2.metric("Product-view sessions", f"{views:,}")
col3.metric("Add-to-cart / view", rate(carts, views))
col4.metric("Purchase / checkout", rate(purchases, checkouts))

st.info("This dashboard uses synthetic sample data for demonstration. The simple stage ratios count sessions containing each event; they do not prove ordered funnel progression.")

left, right = st.columns(2)
with left:
    st.subheader("Unique sessions by event")
    event_summary = df.groupby("event_name")["session_id"].nunique().sort_values(ascending=False)
    st.bar_chart(event_summary)
with right:
    st.subheader("Top viewed products")
    products = df[df["event_name"] == "view_item"].groupby("product_name").size().sort_values(ascending=False)
    st.bar_chart(products)

st.subheader("Traffic source summary")
source_summary = df.groupby("source").agg(
    users=("user_id", "nunique"),
    purchasers=("user_id", lambda s: s[df.loc[s.index, "event_name"].eq("purchase")].nunique())
)
source_summary["purchaser_rate_pct"] = (
    source_summary["purchasers"] / source_summary["users"] * 100
).round(2)
st.dataframe(source_summary, use_container_width=True)

st.subheader("Sample event records")
st.dataframe(df.head(30), use_container_width=True)
