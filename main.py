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
            Los datos utilizados en este dashboard provienen de Datos Abiertos de Colombia.
        """)

        # Resumen Ejecutivo
        st.markdown("""
            ### Resumen Ejecutivo

            Este proyecto tiene como objetivo analizar el estado actual de la cobertura móvil en Antioquia, con un enfoque en la diferencia entre zonas urbanas y rurales. Para ello, se utilizarán datos de la base de datos **"Cobertura_movil_por_tecnologia__departamento_y_municipio_por_proveedor"**, obtenidos de Datos Abiertos de Colombia, los cuales serán complementados con información sobre la calidad de la conectividad por municipio, de acuerdo con la **Resolución CRC 5050 de 2016**.

            A través del uso de técnicas avanzadas de análisis de datos y visualización, el estudio busca identificar patrones, factores determinantes de la cobertura y posibles brechas en el acceso a la conectividad móvil en los municipios de Antioquia. Con ello, se espera generar insumos valiosos para la toma de decisiones en materia de infraestructura digital y políticas públicas de conectividad.

            El proyecto busca evaluar la cobertura móvil en Antioquia a nivel municipal, identificando qué zonas presentan mayores deficiencias en el acceso a internet móvil y en la calidad del servicio. Además, pretende analizar la relación entre la cobertura móvil y la calidad de la conectividad, considerando variables socioeconómicas y geográficas que puedan influir en estas condiciones.

            Otro de los objetivos es proporcionar información basada en datos que sirva como insumo para la toma de decisiones en políticas públicas y estrategias de inversión en infraestructura digital. A partir de este análisis, se busca desarrollar visualizaciones interactivas y reportes detallados que faciliten la interpretación del estado de la conectividad en el departamento, tanto para entidades gubernamentales como para la sociedad en general.

            Como resultado de este estudio, se espera identificar los municipios con mayores deficiencias en cobertura móvil y calidad de conectividad, proporcionando una visión clara de las zonas que requieren mayor atención en términos de infraestructura tecnológica. Asimismo, se generarán mapas y gráficos interactivos que permitan visualizar el estado actual de la conectividad en Antioquia, facilitando la interpretación de los datos y promoviendo la transparencia en la información.

            Además, el proyecto dará lugar a un informe detallado con hallazgos clave y recomendaciones estratégicas para mejorar la infraestructura digital en el departamento. Con estos resultados, se pretende contribuir al desarrollo de iniciativas de alfabetización digital e inclusión tecnológica en comunidades con menor acceso, impulsando así una Antioquia más conectada, equitativa y competitiva en un entorno cada vez más digitalizado.
        """)
    elif opcion == "Filtros globales de la Base de datos":
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
