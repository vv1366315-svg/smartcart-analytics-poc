from pathlib import Path
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "sample_events.csv"
OUTPUT_DIR = ROOT / "outputs"
DB_PATH = OUTPUT_DIR / "smartcart.db"
CHART_PATH = OUTPUT_DIR / "event_analysis.png"

REQUIRED_COLUMNS = {
    "user_id", "session_id", "event_timestamp", "event_name",
    "product_id", "product_name", "price", "quantity",
    "source", "device", "is_synthetic"
}

def pct(numerator, denominator):
    return round(numerator / denominator * 100, 2) if denominator else 0.0

def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    df = pd.read_csv(DATA_PATH)

    missing_columns = REQUIRED_COLUMNS - set(df.columns)
    if missing_columns:
        raise ValueError(f"CSV is missing required columns: {sorted(missing_columns)}")

    print("\nSMARTCART ANALYTICS — SAMPLE DATA ANALYSIS")
    print("NOTE: The bundled dataset is synthetic and results are illustrative.\n")
    print(f"Rows loaded: {len(df):,}")
    print(f"Unique users: {df['user_id'].nunique():,}")
    print(f"Unique sessions: {df['session_id'].nunique():,}")
    print("\nMissing values by column:")
    print(df.isna().sum().to_string())

    # Remove only exact duplicate rows for this demonstration.
    before = len(df)
    df = df.drop_duplicates()
    print(f"\nExact duplicate rows removed: {before - len(df)}")

    event_counts = df["event_name"].value_counts().sort_values(ascending=False)
    print("\nEvent counts:")
    print(event_counts.to_string())

    # Funnel metrics based on distinct sessions containing each event.
    session_counts = df.groupby("event_name")["session_id"].nunique().to_dict()
    product_view_sessions = session_counts.get("view_item", 0)
    cart_sessions = session_counts.get("add_to_cart", 0)
    checkout_sessions = session_counts.get("begin_checkout", 0)
    purchase_sessions = session_counts.get("purchase", 0)

    print("\nDistinct-session metrics (events may not be ordered in this simple calculation):")
    print(f"Sessions with product view: {product_view_sessions}")
    print(f"Sessions with add_to_cart: {cart_sessions}")
    print(f"Sessions with begin_checkout: {checkout_sessions}")
    print(f"Sessions with purchase: {purchase_sessions}")
    print(f"Add-to-cart / product-view sessions: {pct(cart_sessions, product_view_sessions)}%")
    print(f"Purchase / checkout sessions: {pct(purchase_sessions, checkout_sessions)}%")
    print(f"Purchase / product-view sessions: {pct(purchase_sessions, product_view_sessions)}%")

    print("\nTop viewed products:")
    top_products = (
        df[df["event_name"] == "view_item"]
        .groupby("product_name").size().sort_values(ascending=False).head(5)
    )
    print(top_products.to_string() if not top_products.empty else "No view_item events found.")

    print("\nTraffic source summary:")
    source_summary = df.groupby("source").agg(
        users=("user_id", "nunique"),
        purchasers=("user_id", lambda s: s[df.loc[s.index, "event_name"].eq("purchase")].nunique())
    )
    source_summary["purchaser_rate_pct"] = (
        source_summary["purchasers"] / source_summary["users"] * 100
    ).round(2)
    print(source_summary.to_string())

    # Chart
    plot_counts = df.groupby("event_name")["session_id"].nunique().sort_values(ascending=False)
    ax = plot_counts.plot(kind="bar", figsize=(9, 5), title="Unique sessions by event")
    ax.set_xlabel("Event")
    ax.set_ylabel("Unique sessions")
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()
    plt.savefig(CHART_PATH, dpi=150)
    plt.close()
    print(f"\nChart saved to: {CHART_PATH}")

    # Load to SQLite
    with sqlite3.connect(DB_PATH) as conn:
        df.to_sql("events", conn, if_exists="replace", index=False)
    print(f"SQLite database created at: {DB_PATH}")
    print("Done.")

if __name__ == "__main__":
    main()
