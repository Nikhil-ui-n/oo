import streamlit as st
import pandas as pd
import os

# ----------------------------
# Page configuration
# ----------------------------
st.set_page_config(
    page_title="Campaign ROI Dashboard",
    layout="wide"
)

# ----------------------------
# Load dataset
# ----------------------------
@st.cache_data
def load_data():
    filename = "Untitled spreadsheet - Sheet1.csv"

    # Safety check for Streamlit Cloud
    if not os.path.exists(filename):
        st.error("CSV file not found. Please upload 'Untitled spreadsheet - Sheet1.csv'")
        st.stop()

    df = pd.read_csv(filename)

    # Engagement calculation
    df["engagement"] = df["likes"] + df["comments"] + df["shares"]

    # Assumed campaign cost (for academic project)
    df["campaign_cost"] = 5000

    # Campaign ROI calculation
    df["roi"] = ((df["engagement"] - df["campaign_cost"]) / df["campaign_cost"]) * 100

    return df

df = load_data()

# ----------------------------
# Dashboard Title
# ----------------------------
st.title("💰 Campaign ROI Analysis Dashboard")
st.write("This dashboard analyzes campaign Return on Investment (ROI) across platforms.")

# ----------------------------
# ROI Calculation
# ----------------------------
best_roi_platform = (
    df.groupby("platform")["roi"]
    .mean()
    .idxmax()
)

# ----------------------------
# KPI Display
# ----------------------------
st.subheader("🔍 Key Insight")
st.metric("💰 Best ROI Platform", best_roi_platform)

# ----------------------------
# ROI Visualization
# ----------------------------
st.subheader("📉 Average Campaign ROI by Platform")

st.bar_chart(
    df.groupby("platform")["roi"].mean()
)

# ----------------------------
# Data Table
# ----------------------------
with st.expander("📄 View Data with ROI"):
    st.dataframe(df)
