import streamlit as st
import plotly.express as px
import pandas as pd

def page_filtros_visualizaciones(con):
    st.header("🌎 Filtros y Visualizaciones Base de Datos Nivel Colombia")

    # Cargar datos de penetración de internet fijo
    try:
        internet_fijo = pd.read_csv("Internet_Fijo_Penetraci_n_Departamentos_20250206.csv", encoding='latin1')
        
        # Renombrar columnas para evitar problemas de codificación
        internet_fijo = internet_fijo.rename(columns={
            'AÃ‘O': 'AÑO',
            'POBLACIÃ“N DANE': 'POBLACION_DANE',
            'No. ACCESOS FIJOS A INTERNET': 'ACCESOS_FIJOS_INTERNET',
            'INDICE': 'INDICE'
        })
        
        # Limpiar y formatear los datos
        internet_fijo['INDICE'] = internet_fijo['INDICE'].str.replace(',', '.').astype(float)
    except Exception as e:
        st.error(f"Error al cargar los datos de penetración de internet fijo: {e}")
        return

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

    # Aplicar filtros a la base de datos principal
    if departamento_seleccionado:
        query = "SELECT * FROM data WHERE AÑO = ? AND TRIMESTRE = ? AND DEPARTAMENTO IN ({})".format(
            ", ".join(["'{}'".format(d) for d in departamento_seleccionado])
        )
        params = [año_seleccionado, trimestre_seleccionado]
    else:
        query = "SELECT * FROM data WHERE AÑO = ? AND TRIMESTRE = ?"
        params = [año_seleccionado, trimestre_seleccionado]

    try:
        data_filtrada = con.execute(query, params).fetchdf()
    except Exception as e:
        st.error(f"Error al ejecutar la consulta SQL: {e}")
        return

    # Mostrar datos filtrados
    st.write("### Datos Filtrados")
    st.dataframe(data_filtrada)

    # Visualizaciones de cobertura
    if not data_filtrada.empty:
        st.subheader(f"📊 Visualizaciones de Cobertura de {tecnologia_seleccionada}")

        # Gráfico de cobertura por municipio
        cobertura_municipio = data_filtrada[data_filtrada[tecnologia_seleccionada] == 'S'].groupby('MUNICIPIO').size().reset_index(name='Conteo')
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

        # Gráfico de cobertura por departamento
        cobertura_departamento = data_filtrada[data_filtrada[tecnologia_seleccionada] == 'S'].groupby('DEPARTAMENTO').size().reset_index(name='Conteo')
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
        st.warning("No hay datos disponibles para los filtros seleccionados.")

    # KPIs de Penetración de Internet Fijo
    st.subheader("📈 KPIs de Penetración de Internet Fijo")

    st.write(internet_fijo.columns.tolist())
    
    # Filtrar los datos de penetración de internet fijo
    if departamento_seleccionado:
        internet_fijo_filtrado = internet_fijo[
            (internet_fijo['AÑO'] == año_seleccionado) &
            (internet_fijo['TRIMESTRE'] == trimestre_seleccionado) &
            (internet_fijo['DEPARTAMENTO'].isin(departamento_seleccionado))
        ]
    else:
        internet_fijo_filtrado = internet_fijo[
            (internet_fijo['AÑO'] == año_seleccionado) &
            (internet_fijo['TRIMESTRE'] == trimestre_seleccionado)
        ]

    # Calcular KPIs
    if not internet_fijo_filtrado.empty:
        total_accesos = internet_fijo_filtrado['ACCESOS_FIJOS_INTERNET'].sum()
        total_poblacion = internet_fijo_filtrado['POBLACION_DANE'].sum()
        indice_promedio = internet_fijo_filtrado['INDICE'].mean()

        # Mostrar KPIs
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Accesos Fijos a Internet", f"{total_accesos:,}")
        with col2:
            st.metric("Población Total Cubierta", f"{total_poblacion:,}")
        with col3:
            st.metric("Índice Promedio de Penetración", f"{indice_promedio:.2f}%")
    else:
        st.warning("No hay datos de penetración de internet fijo para los filtros seleccionados.")
