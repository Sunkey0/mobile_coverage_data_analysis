import streamlit as st
import plotly.express as px
import pandas as pd

def plot_cobertura(data, x_axis, y_axis, title, color_scale):
    """
    Función para generar gráficos de barras con Plotly.
    """
    if not data.empty:
        fig = px.bar(
            data,
            x=x_axis,
            y=y_axis,
            title=title,
            labels={y_axis: 'Número de Centros Poblados con Cobertura', x_axis: x_axis},
            color=y_axis,
            color_continuous_scale=color_scale
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning(f"No hay datos disponibles para {title}.")

def page_filtros_visualizaciones(con):
    """
    Página de Filtros y Visualizaciones para la Base de Datos a Nivel Colombia.
    """
    st.header("🌎 Filtros y Visualizaciones Base de Datos Nivel Colombia")

    # Filtros en columnas
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
        st.subheader(f"📊 Visualizaciones de Cobertura de {tecnologia_seleccionada}")

        # Métricas clave (KPI)
        st.markdown("#### 📈 Métricas Clave")
        col1, col2, col3 = st.columns(3)
        with col1:
            total_centros = len(data_filtrada)
            st.metric("Total de Centros Poblados", total_centros)
        with col2:
            centros_con_cobertura = len(data_filtrada[data_filtrada[tecnologia_seleccionada] == 'S'])
            st.metric(f"Centros con {tecnologia_seleccionada}", centros_con_cobertura)
        with col3:
            porcentaje_cobertura = (centros_con_cobertura / total_centros) * 100 if total_centros > 0 else 0
            st.metric(f"% de Cobertura {tecnologia_seleccionada}", f"{porcentaje_cobertura:.1f}%")

        # Gráfico de cobertura por municipio
        st.markdown("#### 🏙️ Cobertura por Municipio")
        cobertura_municipio = data_filtrada[data_filtrada[tecnologia_seleccionada] == 'S'].groupby('MUNICIPIO').size().reset_index(name='Conteo')
        plot_cobertura(cobertura_municipio, 'MUNICIPIO', 'Conteo', f"Conteo de Cobertura {tecnologia_seleccionada} por Municipio", px.colors.sequential.Viridis)

        # Gráfico de cobertura por departamento
        st.markdown("#### 🌍 Cobertura por Departamento")
        cobertura_departamento = data_filtrada[data_filtrada[tecnologia_seleccionada] == 'S'].groupby('DEPARTAMENTO').size().reset_index(name='Conteo')
        plot_cobertura(cobertura_departamento, 'DEPARTAMENTO', 'Conteo', f"Conteo de Cobertura {tecnologia_seleccionada} por Departamento", px.colors.sequential.Plasma)

        # Evolución de la cobertura por tecnología (si se seleccionan departamentos)
        if departamento_seleccionado:
            st.markdown("#### 📅 Evolución de la Cobertura por Tecnología")
            departamentos_str = ", ".join([f"'{d}'" for d in departamento_seleccionado])
            query_avance = f"""
                SELECT AÑO, 
                    COUNT(CASE WHEN COBERTURA_2G = 'S' THEN 1 END) AS COBERTURA_2G,
                    COUNT(CASE WHEN COBERTURA_3G = 'S' THEN 1 END) AS COBERTURA_3G,
                    COUNT(CASE WHEN "COBERTURA_HSPA+" = 'S' THEN 1 END) AS COBERTURA_HSPA,
                    COUNT(CASE WHEN COBERTURA_4G = 'S' THEN 1 END) AS COBERTURA_4G,
                    COUNT(CASE WHEN COBERTURA_LTE = 'S' THEN 1 END) AS COBERTURA_LTE,
                    COUNT(CASE WHEN COBERTURA_5G = 'S' THEN 1 END) AS COBERTURA_5G
                FROM data
                WHERE DEPARTAMENTO IN ({departamentos_str})
                GROUP BY AÑO
                ORDER BY AÑO
            """
            avance_cobertura = con.execute(query_avance).fetchdf()

            if not avance_cobertura.empty:
                fig_avance = px.line(
                    avance_cobertura,
                    x='AÑO',
                    y=['COBERTURA_2G', 'COBERTURA_3G', 'COBERTURA_HSPA', 'COBERTURA_4G', 'COBERTURA_LTE', 'COBERTURA_5G'],
                    title="Evolución de la Cobertura por Tecnología (Todos los Años)",
                    labels={'value': 'Número de Centros Poblados con Cobertura', 'variable': 'Tecnología'},
                    color_discrete_sequence=px.colors.sequential.Plasma
                )
                st.plotly_chart(fig_avance, use_container_width=True)
            else:
                st.warning("No hay datos de avance de cobertura para los departamentos seleccionados.")
        else:
            st.warning("Selecciona al menos un departamento para ver el avance de cobertura por año.")

        # Mapa de cobertura (opcional, si tienes datos geográficos)
        st.markdown("#### 🗺️ Mapa de Cobertura")
        st.warning("⚠️ Esta funcionalidad requiere datos geográficos (latitud y longitud).")

    else:
        st.warning("No hay datos disponibles para los filtros seleccionados.")import streamlit as st
import plotly.express as px
import pandas as pd

def plot_cobertura(data, x_axis, y_axis, title, color_scale):
    """
    Función para generar gráficos de barras con Plotly.
    """
    if not data.empty:
        fig = px.bar(
            data,
            x=x_axis,
            y=y_axis,
            title=title,
            labels={y_axis: 'Número de Centros Poblados con Cobertura', x_axis: x_axis},
            color=y_axis,
            color_continuous_scale=color_scale
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning(f"No hay datos disponibles para {title}.")

def page_filtros_visualizaciones(con):
    """
    Página de Filtros y Visualizaciones para la Base de Datos a Nivel Colombia.
    """
    st.header("🌎 Filtros y Visualizaciones Base de Datos Nivel Colombia")

    # Filtros en columnas
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
        st.subheader(f"📊 Visualizaciones de Cobertura de {tecnologia_seleccionada}")

        # Métricas clave (KPI)
        st.markdown("#### 📈 Métricas Clave")
        col1, col2, col3 = st.columns(3)
        with col1:
            total_centros = len(data_filtrada)
            st.metric("Total de Centros Poblados", total_centros)
        with col2:
            centros_con_cobertura = len(data_filtrada[data_filtrada[tecnologia_seleccionada] == 'S'])
            st.metric(f"Centros con {tecnologia_seleccionada}", centros_con_cobertura)
        with col3:
            porcentaje_cobertura = (centros_con_cobertura / total_centros) * 100 if total_centros > 0 else 0
            st.metric(f"% de Cobertura {tecnologia_seleccionada}", f"{porcentaje_cobertura:.1f}%")

        # Gráfico de cobertura por municipio
        st.markdown("#### 🏙️ Cobertura por Municipio")
        cobertura_municipio = data_filtrada[data_filtrada[tecnologia_seleccionada] == 'S'].groupby('MUNICIPIO').size().reset_index(name='Conteo')
        plot_cobertura(cobertura_municipio, 'MUNICIPIO', 'Conteo', f"Conteo de Cobertura {tecnologia_seleccionada} por Municipio", px.colors.sequential.Viridis)

        # Gráfico de cobertura por departamento
        st.markdown("#### 🌍 Cobertura por Departamento")
        cobertura_departamento = data_filtrada[data_filtrada[tecnologia_seleccionada] == 'S'].groupby('DEPARTAMENTO').size().reset_index(name='Conteo')
        plot_cobertura(cobertura_departamento, 'DEPARTAMENTO', 'Conteo', f"Conteo de Cobertura {tecnologia_seleccionada} por Departamento", px.colors.sequential.Plasma)

        # Evolución de la cobertura por tecnología (si se seleccionan departamentos)
        if departamento_seleccionado:
            st.markdown("#### 📅 Evolución de la Cobertura por Tecnología")
            departamentos_str = ", ".join([f"'{d}'" for d in departamento_seleccionado])
            query_avance = f"""
                SELECT AÑO, 
                    COUNT(CASE WHEN COBERTURA_2G = 'S' THEN 1 END) AS COBERTURA_2G,
                    COUNT(CASE WHEN COBERTURA_3G = 'S' THEN 1 END) AS COBERTURA_3G,
                    COUNT(CASE WHEN "COBERTURA_HSPA+" = 'S' THEN 1 END) AS COBERTURA_HSPA,
                    COUNT(CASE WHEN COBERTURA_4G = 'S' THEN 1 END) AS COBERTURA_4G,
                    COUNT(CASE WHEN COBERTURA_LTE = 'S' THEN 1 END) AS COBERTURA_LTE,
                    COUNT(CASE WHEN COBERTURA_5G = 'S' THEN 1 END) AS COBERTURA_5G
                FROM data
                WHERE DEPARTAMENTO IN ({departamentos_str})
                GROUP BY AÑO
                ORDER BY AÑO
            """
            avance_cobertura = con.execute(query_avance).fetchdf()

            if not avance_cobertura.empty:
                fig_avance = px.line(
                    avance_cobertura,
                    x='AÑO',
                    y=['COBERTURA_2G', 'COBERTURA_3G', 'COBERTURA_HSPA', 'COBERTURA_4G', 'COBERTURA_LTE', 'COBERTURA_5G'],
                    title="Evolución de la Cobertura por Tecnología (Todos los Años)",
                    labels={'value': 'Número de Centros Poblados con Cobertura', 'variable': 'Tecnología'},
                    color_discrete_sequence=px.colors.sequential.Plasma
                )
                st.plotly_chart(fig_avance, use_container_width=True)
            else:
                st.warning("No hay datos de avance de cobertura para los departamentos seleccionados.")
        else:
            st.warning("Selecciona al menos un departamento para ver el avance de cobertura por año.")

        # Mapa de cobertura (opcional, si tienes datos geográficos)
        st.markdown("#### 🗺️ Mapa de Cobertura")
        st.warning("⚠️ Esta funcionalidad requiere datos geográficos (latitud y longitud).")

    else:
        st.warning("No hay datos disponibles para los filtros seleccionados.")
