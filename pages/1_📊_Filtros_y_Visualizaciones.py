import streamlit as st
from filters import apply_filters
from visualizations import plot_cobertura
import plotly.express as px

def page_filtros_visualizaciones(data, con):
    st.title("📊 Filtros y Visualizaciones")

    col1, col2, col3 = st.columns(3)

    with col1:
        años = con.execute("SELECT DISTINCT AÑO FROM data ORDER BY AÑO").fetchdf()['AÑO'].tolist()
        año_seleccionado = st.selectbox("Selecciona el año:", años)

    with col2:
        trimestres = con.execute("SELECT DISTINCT TRIMESTRE FROM data WHERE AÑO = ? ORDER BY TRIMESTRE", [año_seleccionado]).fetchdf()['TRIMESTRE'].tolist()
        trimestre_seleccionado = st.selectbox("Selecciona el trimestre:", trimestres)

    with col3:
        departamentos = con.execute("SELECT DISTINCT DEPARTAMENTO FROM data WHERE AÑO = ? AND TRIMESTRE = ? ORDER BY DEPARTAMENTO", [año_seleccionado, trimestre_seleccionado]).fetchdf()['DEPARTAMENTO'].tolist()
        departamento_seleccionado = st.multiselect("Selecciona los departamentos:", departamentos)

    tecnologias = ['COBERTURA_2G', 'COBERTURA_3G', 'COBERTURA_HSPA+', 'COBERTURA_4G', 'COBERTURA_LTE', 'COBERTURA_5G']
    tecnologia_seleccionada = st.selectbox("Selecciona la tecnología:", tecnologias)

    data_filtrada = apply_filters(con, año_seleccionado, trimestre_seleccionado, departamento_seleccionado)

    st.write("### Datos Filtrados")
    st.dataframe(data_filtrada)

    if not data_filtrada.empty:
        st.subheader(f"Visualizaciones de Cobertura de {tecnologia_seleccionada}")

        cobertura_municipio = data_filtrada[data_filtrada[tecnologia_seleccionada] == 'S'].groupby('MUNICIPIO').size().reset_index(name='Conteo')
        plot_cobertura(cobertura_municipio, 'MUNICIPIO', 'Conteo', f"Conteo de Cobertura {tecnologia_seleccionada} por Municipio", px.colors.sequential.Viridis)

        cobertura_departamento = data_filtrada[data_filtrada[tecnologia_seleccionada] == 'S'].groupby('DEPARTAMENTO').size().reset_index(name='Conteo')
        plot_cobertura(cobertura_departamento, 'DEPARTAMENTO', 'Conteo', f"Conteo de Cobertura {tecnologia_seleccionada} por Departamento", px.colors.sequential.Plasma)
