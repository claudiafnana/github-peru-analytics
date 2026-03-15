import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Developers", page_icon="👩‍💻", layout="wide")
st.title("👩‍💻 Developer Explorer")

@st.cache_data
def load_data():
    return pd.read_csv("data/metrics/user_metrics.csv")

try:
    df = load_data()

    col1, col2, col3 = st.columns(3)
    with col1:
        min_stars = st.slider("Minimum Stars", 0, int(df["total_stars_received"].max()), 0)
    with col2:
        languages = ["All"] + sorted(df["primary_language_1"].dropna().unique().tolist())
        lang_filter = st.selectbox("Primary Language", languages)
    with col3:
        active_only = st.checkbox("Active developers only")

    filtered = df.copy()
    if min_stars > 0:
        filtered = filtered[filtered["total_stars_received"] >= min_stars]
    if lang_filter != "All":
        filtered = filtered[filtered["primary_language_1"] == lang_filter]
    if active_only:
        filtered = filtered[filtered["is_active"] == True]

    st.markdown(f"Mostrando **{len(filtered)}** desarrolladores")

    st.dataframe(
        filtered[["login", "name", "total_repos", "total_stars_received",
                  "followers", "impact_score", "primary_language_1", "is_active"]],
        use_container_width=True
    )

    st.subheader("Impact Score Distribution")
    fig = px.histogram(filtered, x="impact_score", nbins=30)
    st.plotly_chart(fig, use_container_width=True)

except FileNotFoundError:
    st.warning("⚠️ No hay datos aún. Ejecuta primero los scripts de extracción.")