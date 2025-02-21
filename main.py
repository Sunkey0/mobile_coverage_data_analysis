import streamlit as st
from setup import setup_app
from data_loader import load_data
from filters import connect_to_duckdb
from pages.filtros_visualizaciones import page_filtros_visualizaciones
from pages.analisis_fijo import page_analisis_fijo
from pages.mapa_coropletico import page_mapa_coropletico
from pages.calidad_conectividad import page_calidad_conectividad
from pages.mapa_calidad_conectividad import page_mapa_calidad_conectividad

# Configuración de la página
st.set_page_config(
    page_title="Hacia una Antioquia Conectada",
    page_icon="📊",
    layout="wide"
)

# Función para cargar los datos (almacenados en caché)
@st.cache_data
def cargar_datos():
    # Cargar datos desde el repositorio de GitHub
    data = load_data()
    # Conectar a DuckDB
    con = connect_to_duckdb(data)
    return data, con

# Cargar datos una sola vez
data, con = cargar_datos()

# Título de la página de inicio
st.title("📊 Hacia una Antioquia Conectada")

# Resumen del dashboard
st.markdown("""
    ### Resumen del Dashboard
    Este dashboard tiene como objetivo analizar la cobertura móvil en Antioquia 
    durante el tercer trimestre de 2023. A continuación, se describen las secciones disponibles:

    - **📊 Filtros y Visualizaciones**: Permite filtrar los datos por año, trimestre, 
      departamento y tecnología, y visualizar gráficos de cobertura.
    - **📈 Diagnóstico Completo 2023-T3**: Muestra un análisis detallado de la cobertura 
      en Antioquia para el tercer trimestre de 2023.
    - **🌍 Mapa Coroplético de Cobertura**: Visualiza la cobertura por municipio en un mapa.
    - **📶 Calidad de la Conectividad**: Analiza la calidad de la conectividad por municipio.
    - **🗺️ Mapa Coroplético de Calidad**: Muestra la calidad de la conectividad en un mapa.

    ### Fuente de Datos
    Los datos utilizados en este dashboard provienen de [nombre de la fuente].
""")

# Mensaje en la barra lateral
st.sidebar.success("Selecciona una página arriba.")
