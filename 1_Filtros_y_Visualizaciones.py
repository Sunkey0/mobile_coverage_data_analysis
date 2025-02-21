import streamlit as st
import plotly.express as px
from filters import apply_filters
from visualizations import plot_cobertura

def page_filtros_visualizaciones(con):
    """
    Página de Filtros y Visualizaciones.
    Permite al usuario filtrar los datos y visualizar gráficos de cobertura.
    """
    st.header("Filtros y Visualizaciones")

    # Crear columnas para los filtros
    col1, col2, col3 = st.columns(3)

    with col1:
        # Filtro de año
        años = con.execute("SELECT DISTINCT AÑO FROM data ORDER BY AÑO").fetchdf()['AÑO'].tolist()
        año_seleccionado = st.selectbox("Selecciona el año:", años)

    with col2:
        # Filtro de trimestre
        trimestres = con.execute(
            "SELECT DISTINCT TRIMESTRE FROM data WHERE AÑO = ? ORDER BY TRIMESTRE", 
            [año_seleccionado]
        ).fetchdf()['TRIMESTRE'].tolist()
        trimestre_seleccionado = st.selectbox("Selecciona el trimestre:", trimestres)

    with col3:
        # Filtro de departamento
        departamentos = con.execute(
            "SELECT DISTINCT DEPARTAMENTO FROM data WHERE AÑO = ? AND TRIMESTRE = ? ORDER BY DEPARTAMENTO", 
            [año_seleccionado, trimestre_seleccionado]
        ).fetchdf()['DEPARTAMENTO'].tolist()
        departamento_seleccionado = st.multiselect("Selecciona los departamentos:", departamentos)

    # Filtro de tecnología
    tecnologias = ['COBERTURA_2G', 'COBERTURA_3G', 'COBERTURA_HSPA+', 'COBERTURA_4G', 'COBERTURA_LTE', 'COBERTURA_5G']
    tecnologia_seleccionada = st.selectbox("Selecciona la tecnología:", tecnologias)

    # Aplicar filtros
    data_filtrada = apply_filters(con, año_seleccionado, trimestre_seleccionado, departamento_seleccionado)

    # Mostrar datos filtrados
    st.write("### Datos Filtrados")
    st.dataframe(data_filtrada)

    # Visualizaciones de cobertura
    if not data_filtrada.empty:
        st.subheader(f"Visualizaciones de Cobertura de {tecnologia_seleccionada}")

        # Conteo de cobertura por municipio
        cobertura_municipio = data_filtrada[data_filtrada[tecnologia_seleccionada] == 'S'].groupby('MUNICIPIO').size().reset_index(name='Conteo')
        plot_cobertura(
            cobertura_municipio, 
            'MUNICIPIO', 
            'Conteo', 
            f"Conteo de Cobertura {tecnologia_seleccionada} por Municipio", 
            px.colors.sequential.Viridis
        )

        # Conteo de cobertura por departamento
        cobertura_departamento = data_filtrada[data_filtrada[tecnologia_seleccionada] == 'S'].groupby('DEPARTAMENTO').size().reset_index(name='Conteo')
        plot_cobertura(
            cobertura_departamento, 
            'DEPARTAMENTO', 
            'Conteo', 
            f"Conteo de Cobertura {tecnologia_seleccionada} por Departamento", 
            px.colors.sequential.Plasma
        )
    else:
        st.warning("No hay datos disponibles para los filtros seleccionados.")
