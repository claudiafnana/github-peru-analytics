import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Industries", page_icon="🏭", layout="wide")
st.title("Industry Analysis")

@st.cache_data
def load_data():
    repos = pd.read_csv("data/processed/repositories.csv")
    classifications = pd.read_csv("data/processed/classifications.csv")
    return repos.merge(classifications, left_on="name", right_on="repo_name", how="left")

try:
    df = load_data()

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Industry Distribution")
        counts = df["industry_name"].value_counts().reset_index()
        counts.columns = ["industry", "count"]
        fig = px.bar(counts, x="count", y="industry", orientation="h", color="count")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Industry by Confidence")
        conf_counts = df.groupby(["industry_name", "confidence"]).size().reset_index(name="count")
        fig = px.bar(conf_counts, x="industry_name", y="count", color="confidence", barmode="stack")
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Top Repositories per Industry")
    selected_industry = st.selectbox("Select Industry", df["industry_name"].dropna().unique())
    top = df[df["industry_name"] == selected_industry].nlargest(10, "stargazers_count")
    st.dataframe(top[["name", "owner_login", "stargazers_count", "language", "confidence"]], 
                use_container_width=True)

except FileNotFoundError:
    st.warning("No hay datos aún. Ejecuta primero los scripts de extracción.")