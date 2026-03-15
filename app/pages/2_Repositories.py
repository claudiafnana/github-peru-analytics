import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Repositories", page_icon="📦", layout="wide")
st.title("Repository Browser")

@st.cache_data
def load_data():
    repos = pd.read_csv("data/processed/repositories.csv")
    classifications = pd.read_csv("data/processed/classifications.csv")
    return repos.merge(classifications[["repo_name", "industry_name", "industry_code", "confidence"]], 
                      left_on="name", right_on="repo_name", how="left")

try:
    df = load_data()

    col1, col2, col3 = st.columns(3)
    with col1:
        search = st.text_input("Search by name")
    with col2:
        industries = ["All"] + sorted(df["industry_name"].dropna().unique().tolist())
        industry_filter = st.selectbox("Industry", industries)
    with col3:
        languages = ["All"] + sorted(df["language"].dropna().unique().tolist())
        lang_filter = st.selectbox("Language", languages)

    filtered = df.copy()
    if search:
        filtered = filtered[filtered["name"].str.contains(search, case=False, na=False)]
    if industry_filter != "All":
        filtered = filtered[filtered["industry_name"] == industry_filter]
    if lang_filter != "All":
        filtered = filtered[filtered["language"] == lang_filter]

    st.markdown(f"Mostrando **{len(filtered)}** repositorios")
    st.dataframe(
        filtered[["name", "owner_login", "stargazers_count", "language", 
                  "industry_name", "confidence"]].sort_values("stargazers_count", ascending=False),
        use_container_width=True
    )

except FileNotFoundError:
    st.warning("No hay datos aún. Ejecuta primero los scripts de extracción.")