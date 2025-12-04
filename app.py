import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Panel de control - Vehículos", layout="wide")

css = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

:root{
  --bg:#0b0d10;
  --panel:#0f1113;
  --muted:#9aa1a6;
  --text:#e6eef3;
  --accent:#cfd6db;
  --card-shadow: 0 4px 20px rgba(0,0,0,0.6);
}

html, body, [class*="css"]  {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif;
}

.main > div {
    background: transparent !important;
}

section[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, rgba(11,13,16,1) 0%, rgba(14,16,18,1) 100%) !important;
}

.stHeader {
    color: var(--text);
}

[data-testid="stAppViewContainer"] .stReport {
    padding-top: 1rem;
}

.stButton>button {
    background-color: #1b1f23 !important;
    color: var(--text) !important;
    border: 1px solid #222528 !important;
    box-shadow: none !important;
}

.st-bq, .stMarkdown {
    color: var(--muted) !important;
}

.stDataFrame table {
    background: transparent;
    color: var(--text) !important;
}

.stProgress > div > div > div {
    background-color: #2b2f33 !important;
}

footer {
    color: var(--muted) !important;
}

/* Card look for plot containers */
.element-container {
    background: var(--panel);
    border-radius: 8px;
    padding: 12px;
    box-shadow: var(--card-shadow);
    margin-bottom: 12px;
}
"""

st.markdown(css, unsafe_allow_html=True)

@st.cache_data
def load_data(path):
    return pd.read_csv(path)

data_path = "vehicles1_us.csv"
if not Path(data_path).exists():
    st.error(f"No se encontró {data_path}. Coloca el archivo CSV en la raíz del proyecto.")
    st.stop()

df = load_data(data_path)

st.header("Panel de control — Anuncios de vehículos")
st.write("Demo interactiva: visualizaciones de anuncios de vehículos.")

df_preview = df.head(8)
st.markdown('<div class="element-container">', unsafe_allow_html=True)
st.subheader("Vista previa de datos")
st.dataframe(df_preview)
st.markdown('</div>', unsafe_allow_html=True)

col1, col2 = st.columns([1,1])

with col1:
    btn_hist = st.button("Construir histograma — Millas (mi)")
with col2:
    btn_scatter = st.button("Construir dispersión — Precio vs Millas (mi)")

x_col = "odometer"
y_col_default = "price"

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
                          font=dict(family="Inter, sans-serif", color="#e6eef3"))
        st.markdown('<div class="element-container">', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("La columna de kilometraje no existe en el dataset. Revisa los nombres de columna.")

if btn_scatter:
    if x_col in df.columns and y_col in df.columns:
        fig = px.scatter(df, x=x_col, y=y_col, hover_data=[c for c in ["year","model"] if c in df.columns],
                         template='plotly_dark', title=f"Dispersión — { 'Precio' if y_col=='price' else y_col } vs Millas (mi)")
        y_label = "Precio" if y_col == "price" else y_col
        fig.update_layout(xaxis_title="Millas (mi)", yaxis_title=y_label,
                          font=dict(family="Inter, sans-serif", color="#e6eef3"))
        st.markdown('<div class="element-container">', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("No se pueden generar la gráfica. Verifica las columnas disponibles.")

st.markdown("---")
st.write("Instrucciones: pulsa un botón para generar el gráfico. Si el conjunto de datos tiene nombres distintos para millas o precio, selecciona la columna adecuada.")
if Path("vehicles_us_clean_sample.csv").exists():
    with open("vehicles_us_clean_sample.csv","rb") as f:
        st.download_button("Descargar muestra limpia (CSV)", f, file_name="vehicles_us_clean_sample.csv", mime="text/csv")
