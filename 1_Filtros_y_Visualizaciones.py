import streamlit as st
import plotly.express as px
import duckdb

def connect_to_duckdb(data):
    """
    Conecta a una base de datos DuckDB en memoria y registra el DataFrame como una tabla.
    """
    con = duckdb.connect(database=':memory:')
    con.register('data', data)
    return con

def apply_filters(con, año_seleccionado, trimestre_seleccionado, departamento_seleccionado):
    """
    Aplica filtros a los datos y devuelve un DataFrame filtrado.
    """
    query = """
        SELECT * FROM data
        WHERE AÑO = ? AND TRIMESTRE = ?
    """
    params = [año_seleccionado, trimestre_seleccionado]

    if departamento_seleccionado:
        query += " AND DEPARTAMENTO IN ({})".format(", ".join(["'{}'".format(d) for d in departamento_seleccionado]))

    return con.execute(query, params).fetchdf()

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

    st.write(con.execute("SHOW TABLES").fetchdf())  # Para verificar que la tabla `data` existe
    st.write(con.execute("DESCRIBE data").fetchdf())  # Para ver las columnas de la tabla

    # Filtro de tecnología
    tecnologias = ['COBERTURA_2G', 'COBERTURA_3G', 'COBERTURA_HSPA+', 'COBERTURA_4G', 'COBERTURA_LTE', 'COBERTURA_5G']
    tecnologia_seleccionada = st.selectbox("Selecciona la tecnología:", tecnologias)

    # Aplicar filtros
    data_filtrada = apply_filters(con, año_seleccionado, trimestre_seleccionado, departamento_seleccionado)

    # Mostrar datos filtrados
    st.write("### Datos Filtrados")
    st.dataframe(data_filtrada)

