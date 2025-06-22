import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# Load data from SQLite
@st.cache_data
def load_data():
    conn = sqlite3.connect("mlb_stats.db")
    rbi_df = pd.read_sql("SELECT * FROM rbi_leaders", conn)
    batting_df = pd.read_sql("SELECT * FROM batting_avg_leaders", conn)
    conn.close()
    return rbi_df, batting_df

# Load data
rbi_df, batting_df = load_data()

# Sidebar filter
st.sidebar.title("Filters")
year = st.sidebar.selectbox("Select a Year", sorted(rbi_df["Year"].unique(), reverse=True))

# --- Streamlit App Title ---
st.title("⚾ MLB Dashboard - RBI & Batting Stats")

# --- Top RBI Leader for Selected Year ---
st.subheader(f"Top RBI Leader in {year}")
year_df = rbi_df[rbi_df["Year"] == year].sort_values("RBI", ascending=False).head(1)

if not year_df.empty:
    fig_year = px.bar(
        year_df,
        x="Player",
        y="RBI",
        title=f"Top RBI Leader in {year}",
        labels={"Player": "Player Name", "RBI": "Runs Batted In"},
        color="RBI",
        color_continuous_scale="Reds"
    )
    fig_year.update_layout(xaxis_title="Player", yaxis_title="RBI")
    st.plotly_chart(fig_year)

# --- All-Time Top 10 RBI Leaders ---
st.subheader("Top 10 RBI Leaders of All Time")
top_all_time = rbi_df.groupby("Player")["RBI"].sum().sort_values(ascending=False).head(10)

fig_all_time = px.bar(
    top_all_time.reset_index(),
    x="Player",
    y="RBI",
    title="All-Time Top 10 RBI Leaders",
    labels={"Player": "Player Name", "RBI": "Total RBI"},
    color="RBI",
    color_continuous_scale="Blues"
)
fig_all_time.update_layout(xaxis_title="Player", yaxis_title="Total RBI")
st.plotly_chart(fig_all_time)

# --- Trend of Total RBI Per Year ---
st.subheader("RBI Trends Over the Years")
trend_df = rbi_df.groupby("Year")["RBI"].sum().reset_index()
fig_trend = px.line(
    trend_df,
    x="Year",
    y="RBI",
    title="Total RBI Per Year",
    labels={"Year": "Year", "RBI": "Total RBI"},
)
fig_trend.update_traces(mode="lines+markers", line=dict(color="green"))
fig_trend.update_layout(xaxis_title="Year", yaxis_title="Total RBI")
st.plotly_chart(fig_trend)

# --- Raw Data Viewer ---
st.subheader("Raw RBI Data")
st.dataframe(rbi_df)