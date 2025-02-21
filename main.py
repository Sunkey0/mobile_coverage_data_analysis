import streamlit as st
from setup import setup_app
from data_loader import load_data
from filters import connect_to_duckdb
from pages.filtros_visualizaciones import page_filtros_visualizaciones
from pages.analisis_fijo import page_analisis_fijo
from pages.mapa_coropletico import page_mapa_coropletico
from pages.calidad_conectividad import page_calidad_conectividad
from pages.mapa_calidad_conectividad import page_mapa_calidad_conectividad

def main():
    # Configuración inicial
    st.set_page_config(
        page_title="Hacia una Antioquia Conectada",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"  # Asegura que la barra lateral esté expandida
    )

    # Título de la aplicación
    st.title("📊 Hacia una Antioquia Conectada")

    # Cargar datos
    data = load_data()
    
    # Verificar si se cargaron los datos
    if data is None:
        st.stop()  # Detener la ejecución si no se subió un archivo

    # Conectar a DuckDB
    con = connect_to_duckdb(data)

    # Menú lateral
    st.sidebar.title("Menú")
    opcion = st.sidebar.radio(
        "Selecciona una sección:",
        ["Información", "Filtros y Visualizaciones", "Diagnóstico Completo 2023-T3", 
         "Mapa Coroplético de Cobertura", "Calidad de la Conectividad", 
         "Mapa Coroplético de Calidad"]
    )

    # Redirigir a la sección seleccionada
    if opcion == "Información":
        st.header("Información del Dashboard")
        st.markdown("""
            ### Resumen del Dashboard
            Este dashboard tiene como objetivo analizar la cobertura móvil en Antioquia 
            durante el tercer trimestre de 2023. A continuación, se describen las secciones disponibles:

            - **Filtros y Visualizaciones**: Permite filtrar los datos por año, trimestre, 
              departamento y tecnología, y visualizar gráficos de cobertura.
            - **Diagnóstico Completo 2023-T3**: Muestra un análisis detallado de la cobertura 
              en Antioquia para el tercer trimestre de 2023.
            - **Mapa Coroplético de Cobertura**: Visualiza la cobertura por municipio en un mapa.
            - **Calidad de la Conectividad**: Analiza la calidad de la conectividad por municipio.
            - **Mapa Coroplético de Calidad**: Muestra la calidad de la conectividad en un mapa.

            ### Fuente de Datos
            Los datos utilizados en este dashboard provienen del archivo CSV subido.
        """)
    elif opcion == "Filtros y Visualizaciones":
        page_filtros_visualizaciones(con)
    elif opcion == "Diagnóstico Completo 2023-T3":
        page_analisis_fijo(con)
    elif opcion == "Mapa Coroplético de Cobertura":
        page_mapa_coropletico(con)
    elif opcion == "Calidad de la Conectividad":
        page_calidad_conectividad()
    elif opcion == "Mapa Coroplético de Calidad":
        page_mapa_calidad_conectividad()

if __name__ == "__main__":
    main()
