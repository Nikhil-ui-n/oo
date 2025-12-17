import streamlit as st
import pandas as pd
import os

# ----------------------------
# Page configuration
# ----------------------------
st.set_page_config(
    page_title="Optimal Posting Time Dashboard",
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

    # Convert date column to datetime
    df["date"] = pd.to_datetime(df["date"])

    # Extract hour from date
    df["hour"] = df["date"].dt.hour

    # Engagement calculation
    df["engagement"] = df["likes"] + df["comments"] + df["shares"]

    return df

df = load_data()

# ----------------------------
# Dashboard Title
# ----------------------------
st.title("⏰ Optimal Posting Time Analysis")
st.write("Identify the best time to post based on audience engagement.")

# ----------------------------
# Optimal Posting Time Calculation
# ----------------------------
optimal_posting_hour = (
    df.groupby("hour")["engagement"]
    .mean()
    .idxmax()
)

# ----------------------------
# KPI Display
# ----------------------------
st.subheader("🔍 Key Insight")
st.metric("⏰ Optimal Posting Hour", f"{optimal_posting_hour}:00")

# ----------------------------
# Visualization
# ----------------------------
st.subheader("📊 Engagement by Posting Hour")

st.bar_chart(
    df.groupby("hour")["engagement"].mean()
)

# ----------------------------
# Data Table
# ----------------------------
with st.expander("📄 View Data"):
    st.dataframe(df)
