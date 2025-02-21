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
def cargar_datos(uploaded_file):
    """
    Carga los datos desde el archivo subido y los almacena en caché.
    """
    data = load_data(uploaded_file)
    return data

# Título de la página de inicio
st.title("📊 Hacia una Antioquia Conectada")

# Subir archivo CSV
uploaded_file = st.sidebar.file_uploader("⬆️ Sube tu archivo CSV", type=["csv"])

# Cargar datos si se ha subido un archivo
if uploaded_file is not None:
    # Cargar datos (almacenados en caché)
    data = cargar_datos(uploaded_file)
    
    # Crear la conexión a DuckDB (no almacenada en caché)
    con = connect_to_duckdb(data)

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
        Los datos utilizados en este dashboard provienen del archivo CSV subido.
    """)

    # Mensaje en la barra lateral
    st.sidebar.success("Selecciona una página arriba.")
else:
    st.warning("Por favor, sube un archivo CSV para continuar.")
