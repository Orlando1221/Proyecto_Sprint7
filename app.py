import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Panel de control - Vehículos", layout="wide")


css = """
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;700&family=Inter:wght@300;400;600;700&display=swap');

:root{
  --bg: #0b2430;
  --panel: #0f3a4a;
  --muted: #9fb3c2;
  --text: #f7fbfc;
  --accent: #6fa8c8;
  --gold: #d3a94a;
  --card-shadow: 2 20px 60px rgba(2,12,18,0.55);
}

html, body, [class*="css"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif;
}

/* Título: MÁS GRANDE */
.hero {
    text-align: center;
    padding: 64px 16px 22px 16px;
}
.hero .title {
    font-family: 'Playfair Display', serif;
    font-size: 64px; /* <-- AUMENTADO */
    font-weight: 600;
}
.hero .subtitle {
    color: var(--muted);
    font-size: 35px;
    text-transform: uppercase;
}

/* Contenedor general */
.element-container {
    background: rgba(15,58,74,0.12);
    border-radius: 23px;
    padding: 23px;
    box-shadow: var(--card-shadow);
    border: 1.4px solid rgba(255,255,255,0.02);
    margin-bottom: 14px;
}

/* TABLA FULL WIDTH + LETRA MÁS GRANDE */
.full-width-container .stDataFrame table {
    width: 100% !important;
    font-size: 1.4rem !important; /* <-- AUMENTADO */
}

/* BOTONES PEQUEÑOS Y BONITOS */
.stButton>button {
    background-color: transparent !important;
    color: var(--text) !important;
    border: 1px solid rgba(111,154,178,0.12) !important;
    padding: 22px 51px;
    border-radius: 14px;
    width: auto !important;
    font-weight: 730;
}
.stButton>button:hover {
    background-color: var(--gold) !important;
    color: #061219 !important;
}

/* Nota del usuario */
.small-note {
    margin-top: 13px;
    margin-bottom: 26px;
    color: var(--muted);
    font-size: 1rem;
}
"""

st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)



@st.cache_data
def load_data(path):
    return pd.read_csv(path)

data_path = "vehicles1_us.csv"
df = load_data(data_path)

df = df.rename(columns={
    "odometer": "millas_mi",
    "price": "precio"
})


st.markdown(
    '<div class="hero">'
    '<div class="title">Panel de control — Anuncios de vehículos</div>'
    '<div class="subtitle">Vista interactiva y análisis rápido</div>'
    '</div>',
    unsafe_allow_html=True
)



st.markdown('<div class="element-container full-width-container">', unsafe_allow_html=True)
st.dataframe(df, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)



st.markdown(
    '<div class="small-note">Pulsa un botón para generar el gráfico; la visualización aparecerá debajo de la tabla.</div>',
    unsafe_allow_html=True
)

colA, colB = st.columns([1,1])

with colA:
    btn_hist = st.button("Construir histograma — Millas (mi)")

with colB:
    btn_scatter = st.button("Construir dispersión — Precio vs Millas (mi)")



x_col = "millas_mi"
y_col = "precio"

if btn_hist:
    fig = px.histogram(df, x=x_col, nbins=45, template='plotly_dark',
                       title="Histograma — Millas recorridas (mi)")
    fig.update_layout(font=dict(size=14))
    st.plotly_chart(fig, use_container_width=True)

if btn_scatter:
    fig = px.scatter(df, x=x_col, y=y_col, template='plotly_dark',
                     title="Dispersión — Precio vs Millas (mi)")
    fig.update_layout(font=dict(size=14))
    st.plotly_chart(fig, use_container_width=True)



if Path("vehicles_us_clean_sample.csv").exists():
    with open("vehicles_us_clean_sample.csv","rb") as f:
        st.download_button("Descargar muestra limpia (CSV)", f,
            file_name="vehicles_us_clean_sample.csv", mime="text/csv")
