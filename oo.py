import streamlit as st
import pandas as pd
import os

# ----------------------------
# Page configuration
# ----------------------------
st.set_page_config(
    page_title="Optimal Posting Time (Per Platform)",
    layout="wide"
)

# ----------------------------
# Load dataset
# ----------------------------
@st.cache_data
def load_data():
    filename = "Untitled spreadsheet - Sheet1.csv"

    if not os.path.exists(filename):
        st.error("CSV file not found")
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
# Title
# ----------------------------
st.title("⏰ Optimal Posting Time – Platform Wise")
st.write("Each bar chart shows engagement across hours for one platform.")

# ----------------------------
# Separate Bar Charts for Each Platform
# ----------------------------
platforms = df["platform"].unique()

for platform in platforms:
    st.subheader(f"📱 {platform} – Engagement by Hour")

    platform_df = df[df["platform"] == platform]

    st.bar_chart(
        platform_df.groupby("hour")["engagement"].mean()
    )

# ----------------------------
# Best Hour Table (Optional but Good)
# ----------------------------
best_hours = (
    df.groupby(["platform", "hour"])["engagement"]
    .mean()
    .reset_index()
    .loc[lambda x: x.groupby("platform")["engagement"].idxmax()]
)

st.subheader("✅ Best Posting Hour per Platform")
st.dataframe(best_hours[["platform", "hour"]])
