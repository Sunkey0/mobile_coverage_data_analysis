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

    # Verificar que la tabla `data` existe
    try:
        tables = con.execute("SHOW TABLES").fetchdf()
        if 'data' not in tables['name'].values:
            st.error("La tabla 'data' no existe en la base de datos.")
            return
    except Exception as e:
        st.error(f"Error al verificar las tablas: {e}")
        return

    # Verificar las columnas de la tabla `data`
    try:
        columns = con.execute("DESCRIBE data").fetchdf()
        st.write("### Columnas de la tabla `data`")
        st.dataframe(columns)
    except Exception as e:
        st.error(f"Error al describir la tabla 'data': {e}")
        return

    # Crear columnas para los filtros
    col1, col2, col3 = st.columns(3)

    with col1:
        # Filtro de año
        try:
            años = con.execute("SELECT DISTINCT AÑO FROM data ORDER BY AÑO").fetchdf()['AÑO'].tolist()
            año_seleccionado = st.selectbox("Selecciona el año:", años)
        except Exception as e:
            st.error(f"Error al obtener los años: {e}")
            return

    with col2:
        # Filtro de trimestre
        try:
            trimestres = con.execute(
                "SELECT DISTINCT TRIMESTRE FROM data WHERE AÑO = ? ORDER BY TRIMESTRE", 
                [año_seleccionado]
            ).fetchdf()['TRIMESTRE'].tolist()
            trimestre_seleccionado = st.selectbox("Selecciona el trimestre:", trimestres)
        except Exception as e:
            st.error(f"Error al obtener los trimestres: {e}")
            return

    with col3:
        # Filtro de departamento
        try:
            departamentos = con.execute(
                "SELECT DISTINCT DEPARTAMENTO FROM data WHERE AÑO = ? AND TRIMESTRE = ? ORDER BY DEPARTAMENTO", 
                [año_seleccionado, trimestre_seleccionado]
            ).fetchdf()['DEPARTAMENTO'].tolist()
            departamento_seleccionado = st.multiselect("Selecciona los departamentos:", departamentos)
        except Exception as e:
            st.error(f"Error al obtener los departamentos: {e}")
            return

    # Filtro de tecnología
    tecnologias = ['COBERTURA_2G', 'COBERTURA_3G', 'COBERTURA_HSPA+', 'COBERTURA_4G', 'COBERTURA_LTE', 'COBERTURA_5G']
    tecnologia_seleccionada = st.selectbox("Selecciona la tecnología:", tecnologias)

    # Aplicar filtros
    try:
        data_filtrada = apply_filters(con, año_seleccionado, trimestre_seleccionado, departamento_seleccionado)
    except Exception as e:
        st.error(f"Error al aplicar los filtros: {e}")
        return

    # Mostrar datos filtrados
    st.write("### Datos Filtrados")
    st.dataframe(data_filtrada)

    # Visualizaciones de cobertura
    if not data_filtrada.empty:
        st.subheader(f"Visualizaciones de Cobertura de {tecnologia_seleccionada}")

        # Conteo de cobertura por municipio
        try:
            cobertura_municipio = data_filtrada[data_filtrada[tecnologia_seleccionada] == 'S'].groupby('MUNICIPIO').size().reset_index(name='Conteo')
            if not cobertura_municipio.empty:
                fig_municipio = px.bar(
                    cobertura_municipio,
                    x='MUNICIPIO',
                    y='Conteo',
                    title=f"Conteo de Cobertura {tecnologia_seleccionada} por Municipio",
                    labels={'Conteo': 'Número de Centros Poblados con Cobertura', 'MUNICIPIO': 'Municipio'},
                    color='Conteo',
                    color_continuous_scale=px.colors.sequential.Viridis
                )
                st.plotly_chart(fig_municipio, use_container_width=True)
            else:
                st.warning("No hay datos de cobertura por municipio para los filtros seleccionados.")
        except Exception as e:
            st.error(f"Error al generar la gráfica por municipio: {e}")

        # Conteo de cobertura por departamento
        try:
            cobertura_departamento = data_filtrada[data_filtrada[tecnologia_seleccionada] == 'S'].groupby('DEPARTAMENTO').size().reset_index(name='Conteo')
            if not cobertura_departamento.empty:
                fig_departamento = px.bar(
                    cobertura_departamento,
                    x='DEPARTAMENTO',
                    y='Conteo',
                    title=f"Conteo de Cobertura {tecnologia_seleccionada} por Departamento",
                    labels={'Conteo': 'Número de Centros Poblados con Cobertura', 'DEPARTAMENTO': 'Departamento'},
                    color='Conteo',
                    color_continuous_scale=px.colors.sequential.Plasma
                )
                st.plotly_chart(fig_departamento, use_container_width=True)
            else:
                st.warning("No hay datos de cobertura por departamento para los filtros seleccionados.")
        except Exception as e:
            st.error(f"Error al generar la gráfica por departamento: {e}")
    else:
        st.warning("No hay datos disponibles para los filtros seleccionados.")
