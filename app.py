import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Panel de control - Vehículos", layout="wide")

css = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

:root{
  --bg: #021a2b;
  --panel: #0b3b52;
  --panel-alt: #153f59;
  --muted: #9fb3c2;
  --text: #f2f6f8;
  --accent: #74a0be;
  --gold: #d4af37;
  --card-shadow: 0 8px 30px rgba(2,18,30,0.55);
}

html, body, [class*="css"]  {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif;
    -webkit-font-smoothing:antialiased;
    -moz-osx-font-smoothing:grayscale;
}

section[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, rgba(2,26,43,1) 0%, rgba(8,34,48,1) 100%) !important;
    padding-top: 1.6rem;
    padding-bottom: 2rem;
}

.stHeader, h1 {
    text-align: center !important;
    font-weight: 600 !important;
    margin-top: 0.2rem;
    margin-bottom: 0.1rem;
    color: var(--text) !important;
}
.title-wrap {
    display: block;
    max-width: 980px;
    margin: 0 auto 0.6rem auto;
    padding: 8px 12px;
}

.stMarkdown, .st-bq {
    color: var(--muted) !important;
    text-align: center;
    max-width: 920px;
    margin: 0 auto 1.2rem auto;
}

.element-container {
    background: linear-gradient(180deg, var(--panel) 0%, var(--panel-alt) 100%);
    border-radius: 12px;
    padding: 14px;
    box-shadow: var(--card-shadow);
    border: 1px solid rgba(116,144,176,0.08);
    margin: 12px auto;
    display: block;
    max-width: 1100px;
    width: calc(100% - 48px);
    box-sizing: border-box;
}

.element-inline {
    display: inline-block;
    width: auto;
    max-width: 90%;
    padding: 10px 14px;
    margin: 0 8px 12px 0;
    vertical-align: top;
    background: transparent;
    border: none;
    box-shadow: none;
}

.full-width-container {
    display: block;
    width: 100%;
    margin: 8px 0;
    padding: 6px 12px;
    box-sizing: border-box;
    background: transparent;
}

.full-width-container .stDataFrame {
    width: 100% !important;
}
.full-width-container .stDataFrame table {
    width: 100% !important;
}

.stButton>button {
    background-color: transparent !important;
    color: var(--text) !important;
    border: 1px solid rgba(116,144,176,0.14) !important;
    padding: 8px 12px;
    border-radius: 8px;
    transition: all 0.18s ease;
}
.stButton>button:hover {
    background-color: var(--gold) !important;
    color: #071218 !important;
    transform: translateY(-1px);
    border-color: rgba(0,0,0,0.0) !important;
}

.stDataFrame {
    overflow-x: auto;
    padding: 4px;
}
.stDataFrame table {
    background: transparent !important;
    color: var(--text) !important;
    border-collapse: collapse;
}
.stDataFrame thead th {
    color: var(--accent) !important;
    font-weight: 600;
    border-bottom: 1px solid rgba(116,144,176,0.06);
}

.small-muted {
    color: var(--muted) !important;
    font-size: 0.92em;
}

footer {
    color: var(--muted) !important;
    opacity: 0.95;
}

@media (max-width: 900px) {
    .element-container { width: calc(100% - 24px); padding: 10px; max-width: 92%; }
    .stHeader, h1 { font-size: 1.4rem; }
    .stDataFrame table { font-size: 0.9rem; }
}
"""

st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

@st.cache_data
def load_data(path):
    return pd.read_csv(path)

data_path = "vehicles1_us.csv"
if not Path(data_path).exists():
    st.error(f"No se encontró {data_path}. Coloca el archivo CSV en la raíz del proyecto.")
    st.stop()

df = load_data(data_path)

df = df.rename(columns={
    "odometer": "millas_mi",
    "price": "precio"
})

st.markdown('<div class="title-wrap"><h1>Panel de control — Anuncios de vehículos</h1></div>', unsafe_allow_html=True)
st.markdown('<div class="small-muted">Demo interactiva: visualizaciones de anuncios de vehículos.</div>', unsafe_allow_html=True)

df_preview = df.head(8)
st.markdown('<div class="element-inline">', unsafe_allow_html=True)
st.subheader("Vista previa de datos")
st.dataframe(df_preview)
st.markdown('</div>', unsafe_allow_html=True)

col1, col2 = st.columns([1,1])
with col1:
    btn_hist = st.button("Construir histograma — Millas (mi)")
with col2:
    btn_scatter = st.button("Construir dispersión — Precio vs Millas (mi)")

st.markdown('<div class="full-width-container">', unsafe_allow_html=True)
st.dataframe(df)
st.markdown('</div>', unsafe_allow_html=True)

x_col = "millas_mi"
y_col_default = "precio"
available_columns = df.columns.tolist()
if y_col_default not in available_columns:
    y_col = st.selectbox("Selecciona columna para eje Y", options=available_columns, index=0)
else:
    y_col = y_col_default

if btn_hist:
    if x_col in df.columns:
        fig = px.histogram(df, x=x_col, nbins=50, template='plotly_dark',
                           title="Histograma — Millas recorridas por vehículo (mi)")
        fig.update_layout(xaxis_title="Millas (mi)", yaxis_title="Cantidad",
                          font=dict(family="Inter, sans-serif", color="#f2f6f8"))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("La columna de millas no existe en el dataset. Verifica los nombres de columna.")

if btn_scatter:
    if x_col in df.columns and y_col in df.columns:
        fig = px.scatter(df, x=x_col, y=y_col, hover_data=[c for c in ["year","model"] if c in df.columns],
                         template='plotly_dark', title=f"Dispersión — {'Precio' if y_col=='precio' else y_col} vs Millas (mi)")
        y_label = "Precio" if y_col == "precio" else y_col
        fig.update_layout(xaxis_title="Millas (mi)", yaxis_title=y_label,
                          font=dict(family="Inter, sans-serif", color="#f2f6f8"))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No se pueden generar la gráfica. Verifica las columnas disponibles.")

st.markdown("---")
st.write("Pulsa un botón para generar el gráfico. Si el conjunto de datos usa otros nombres para millas o precio, selecciona la columna adecuada.")
if Path("vehicles_us_clean_sample.csv").exists():
    with open("vehicles_us_clean_sample.csv","rb") as f:
        st.download_button("Descargar muestra limpia (CSV)", f, file_name="vehicles_us_clean_sample.csv", mime="text/csv")
