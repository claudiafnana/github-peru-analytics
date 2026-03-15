import streamlit as st
import pandas as pd
import plotly.express as px
import json

st.set_page_config(
    page_title="GitHub Peru Analytics",
    page_icon="🇵🇪",
    layout="wide"
)

@st.cache_data
def load_data():
    users_df = pd.read_csv("data/metrics/user_metrics.csv")
    repos_df = pd.read_csv("data/processed/repositories.csv")
    classifications_df = pd.read_csv("data/processed/classifications.csv")
    with open("data/metrics/ecosystem_metrics.json") as f:
        ecosystem = json.load(f)
    return users_df, repos_df, classifications_df, ecosystem

try:
    users_df, repos_df, classifications_df, ecosystem = load_data()

    st.title("GitHub Peru Analytics")
    st.markdown("Análisis del ecosistema de desarrolladores peruanos en GitHub")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Developers", ecosystem["total_developers"])
    with col2:
        st.metric("Total Repositories", ecosystem["total_repositories"])
    with col3:
        st.metric("Total Stars", ecosystem["total_stars"])
    with col4:
        st.metric("Active Developers", f"{ecosystem['active_developer_pct']}%")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Top 10 Developers by Impact")
        top_devs = users_df.nlargest(10, "impact_score")[["login", "impact_score"]]
        fig = px.bar(top_devs, x="login", y="impact_score", color="impact_score")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Industry Distribution")
        industry_counts = classifications_df["industry_name"].value_counts().reset_index()
        industry_counts.columns = ["industry", "count"]
        fig = px.bar(industry_counts, x="count", y="industry", orientation="h",
                    color="count", color_continuous_scale="Blues")
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Top 10 Repositories by Stars")
    top_repos = repos_df.nlargest(10, "stargazers_count")[["name", "owner_login", "stargazers_count", "language"]]
    st.dataframe(top_repos, use_container_width=True)

except FileNotFoundError:
    st.warning("⚠️ No hay datos aún. Ejecuta primero los scripts de extracción.")
    st.code("python -m scripts.extract_data")