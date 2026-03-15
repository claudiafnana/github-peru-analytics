import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Languages", page_icon="💻", layout="wide")
st.title("Language Analytics")

@st.cache_data
def load_data():
    repos = pd.read_csv("data/processed/repositories.csv")
    classifications = pd.read_csv("data/processed/classifications.csv")
    return repos.merge(classifications, left_on="name", right_on="repo_name", how="left")

try:
    df = load_data()

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Top 15 Languages")
        lang_counts = df["language"].value_counts().head(15).reset_index()
        lang_counts.columns = ["language", "count"]
        fig = px.bar(lang_counts, x="language", y="count", color="count")
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Language Share")
        fig = px.pie(lang_counts, values="count", names="language")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Language by Industry Heatmap")
    top_langs = df["language"].value_counts().head(10).index.tolist()
    top_industries = df["industry_name"].value_counts().head(10).index.tolist()
    heatmap_df = df[
        df["language"].isin(top_langs) & df["industry_name"].isin(top_industries)
    ].groupby(["language", "industry_name"]).size().reset_index(name="count")
    heatmap_pivot = heatmap_df.pivot(index="language", columns="industry_name", values="count").fillna(0)
    fig = px.imshow(heatmap_pivot, color_continuous_scale="Blues")
    st.plotly_chart(fig, use_container_width=True)

except FileNotFoundError:
    st.warning("No hay datos aún. Ejecuta primero los scripts de extracción.")