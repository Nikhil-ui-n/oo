import streamlit as st
import pandas as pd
import os

# ----------------------------
# Page configuration
# ----------------------------
st.set_page_config(
    page_title="Optimal Posting Time - Line Plot",
    layout="wide"
)

# ----------------------------
# Load dataset
# ----------------------------
@st.cache_data
def load_data():
    filename = "Untitled spreadsheet - Sheet1.csv"

    if not os.path.exists(filename):
        st.error("CSV file not found. Please upload 'Untitled spreadsheet - Sheet1.csv'")
        st.stop()

    df = pd.read_csv(filename)

    # Date & time processing
    df["date"] = pd.to_datetime(df["date"])
    df["hour"] = df["date"].dt.hour

    # Engagement calculation
    df["engagement"] = df["likes"] + df["comments"] + df["shares"]

    return df

df = load_data()

# ----------------------------
# Dashboard title
# ----------------------------
st.title("⏰ Optimal Posting Time Analysis (Line Plot)")
st.write(
    "Line plots show engagement trends across posting hours for each platform."
)

# ----------------------------
# Platform-wise Line Plots
# ----------------------------
platforms = df["platform"].unique()

for platform in platforms:
    st.subheader(f"📱 {platform} – Engagement Trend by Hour")

    platform_df = df[df["platform"] == platform]

    # Line plot
    st.line_chart(
        platform_df.groupby("hour")["engagement"].mean()
    )

# ----------------------------
# Best Posting Hour per Platform
# ----------------------------
best_hours = (
    df.groupby(["platform", "hour"])["engagement"]
    .mean()
    .reset_index()
    .loc[lambda x: x.groupby("platform")["engagement"].idxmax()]
)

st.subheader("✅ Optimal Posting Hour (Per Platform)")
st.dataframe(best_hours[["platform", "hour"]])

# ----------------------------
# Data table
# ----------------------------
with st.expander("📄 View Full Data"):
    st.dataframe(df)
