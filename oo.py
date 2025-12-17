import streamlit as st
import pandas as pd
import os

# ----------------------------
# Page configuration
# ----------------------------
st.set_page_config(
    page_title="Optimal Posting Time by Platform",
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

    # Date processing
    df["date"] = pd.to_datetime(df["date"])
    df["hour"] = df["date"].dt.hour

    # Engagement calculation
    df["engagement"] = df["likes"] + df["comments"] + df["shares"]

    return df

df = load_data()

# ----------------------------
# Dashboard Title
# ----------------------------
st.title("⏰ Optimal Posting Time by Platform")
st.write("Best posting hour for each social media platform based on engagement.")

# ----------------------------
# Optimal Posting Time per Platform
# ----------------------------
optimal_time_per_platform = (
    df.groupby(["platform", "hour"])["engagement"]
    .mean()
    .reset_index()
)

best_hours = (
    optimal_time_per_platform
    .loc[optimal_time_per_platform.groupby("platform")["engagement"].idxmax()]
)

# ----------------------------
# KPI DISPLAY (ONE PER PLATFORM)
# ----------------------------
st.subheader("🔍 Optimal Posting Hour (Per Platform)")

for _, row in best_hours.iterrows():
    st.metric(
        label=f"📱 {row['platform']}",
        value=f"{int(row['hour'])}:00"
    )

# ----------------------------
# BAR CHART (OPTIONAL BUT GOOD)
# ----------------------------
st.subheader("📊 Engagement by Hour (Per Platform)")

selected_platform = st.selectbox(
    "Select Platform",
    df["platform"].unique()
)

platform_df = df[df["platform"] == selected_platform]

st.bar_chart(
    platform_df.groupby("hour")["engagement"].mean()
)

# ----------------------------
# Data Table
# ----------------------------
with st.expander("📄 View Data"):
    st.dataframe(best_hours)
