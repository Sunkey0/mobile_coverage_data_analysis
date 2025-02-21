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
    setup_app()
    data = load_data()
    con = connect_to_duckdb(data)

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Filtros y Visualizaciones Generales",
        "Diagnóstico Completo 2023-T3",
        "Mapa Coroplético de Cobertura",
        "Calidad de la Conectividad",
        "Mapa Coroplético de Calidad"
    ])
    
    with tab1:
        page_filtros_visualizaciones(con)

    with tab2:
        page_analisis_fijo(con)

    with tab3:
        page_mapa_coropletico(con)

    with tab4:
        page_calidad_conectividad()

    with tab5:
        page_mapa_calidad_conectividad()

if __name__ == "__main__":
    main()
