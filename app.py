# app.py - Dashboard de anuncios de vehículos (Sprint 7)
import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title="Dashboard de Vehículos", layout="wide")

# Encabezado y descripción
st.header("Dashboard: Anuncios de vehículos")
st.write("Aplicación demo: histograma y scatter interactivos con Plotly y Streamlit.")

# Cargar datos (cacheado para rendimiento)
@st.cache_data
def load_data(path):
    return pd.read_csv(path)

data_path = "vehicles1_us.csv"
try:
    df = load_data(data_path)
except FileNotFoundError:
    st.error(f"No se encontró {data_path}. Coloca el CSV en la raíz del proyecto.")
    st.stop()

# Mostrar vista previa
st.markdown("### Vista previa de datos")
st.dataframe(df.head(10))

# Controles: botones para generar gráficos
col1, col2 = st.columns(2)
with col1:
    hist_button = st.button("Construir histograma (odometer)")
with col2:
    scatter_button = st.button("Construir scatter (price vs odometer)")

# Columnas esperadas (ajusta si tu CSV usa otros nombres)
x_col = "odometer"
y_col = "price"

# Construir histograma
if hist_button:
    if x_col in df.columns:
        fig_hist = px.histogram(df, x=x_col, nbins=50, title="Histograma: odometer")
        fig_hist.update_layout(xaxis_title=x_col, yaxis_title="Cantidad")
        st.write("Creando histograma para:", x_col)
        st.plotly_chart(fig_hist, use_container_width=True)
    else:
        st.warning(f"No existe la columna '{x_col}'. Columnas disponibles: {df.columns.tolist()}")

# Construir scatter
if scatter_button:
    if x_col in df.columns and y_col in df.columns:
        fig_scatter = px.scatter(
            df,
            x=x_col,
            y=y_col,
            hover_data=[c for c in ["year","model"] if c in df.columns],
            title=f"{y_col} vs {x_col}"
        )
        fig_scatter.update_layout(xaxis_title=x_col, yaxis_title=y_col)
        st.write(f"Creando scatter: {y_col} vs {x_col}")
        st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.warning(f"No se pueden generar scatter. Columnas disponibles: {df.columns.tolist()}")


