import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Philippine Population Dashboard", layout="wide")

# --- Load dataset ---
@st.cache_data
def load_data():
    df = pd.read_csv("Cleaned_Philippine_Population.csv")
    return df

df = load_data()

# --- Sidebar for province selection ---
st.title("Philippine Population Dashboard")

province_list = sorted(df["Province"].unique())
selected_province = st.selectbox("Select Province:", [""] + province_list)

# --- Filter data if province selected ---
if selected_province:
    filtered_df = df[df["Province"] == selected_province]
    region = filtered_df['Region'].iloc[0]
    capital = filtered_df['Capital'].iloc[0]
    island_group = filtered_df['Island Group'].iloc[0]
    info_text = f"Region: {region} | Capital: {capital} | Island Group: {island_group}"
else:
    filtered_df = df.copy()
    info_text = ""

st.markdown(f"**{info_text}**")

# --- Prepare data for plots ---
def prepare_melted_data(df_):
    df_melted = df_.melt(
        id_vars=["Province"],
        value_vars=["2000", "2010", "2015", "2020"],
        var_name="Year",
        value_name="Population"
    )
    df_melted["Population"] = pd.to_numeric(df_melted["Population"], errors="coerce")
    return df_melted

df_melted = prepare_melted_data(filtered_df)

# --- Line chart: Population Growth Over Time ---
fig_trend = px.line(
    df_melted,
    x="Year",
    y="Population",
    color="Province",
    title="Population Growth Over Time"
)

# --- Bar chart: Population by Province and Year ---
df_bar = prepare_melted_data(filtered_df)
fig_bar = px.bar(
    df_bar,
    x="Province",
    y="Population",
    color="Year",
    barmode="group",
    title="Population by Province (2000, 2010, 2015, 2020)"
)

# --- Display charts ---
st.plotly_chart(fig_trend, use_container_width=True)
st.plotly_chart(fig_bar, use_container_width=True)