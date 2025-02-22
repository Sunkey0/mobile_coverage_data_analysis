import streamlit as st
import plotly.express as px
import pandas as pd

def page_analisis_fijo(con):
    st.header("Análisis Fijo y Avanzado (2023, Trimestre 3, Antioquia)")

    query_fijo = """
        SELECT * FROM data
        WHERE AÑO = '2023' AND TRIMESTRE = '3' AND DEPARTAMENTO = 'ANTIOQUIA'
    """
    data_fijo = con.execute(query_fijo).fetchdf()

    tecnologias = ['COBERTURA_2G', 'COBERTURA_3G', 'COBERTURA_HSPA+', 'COBERTURA_4G', 'COBERTURA_LTE', 'COBERTURA_5G']
    tecnologia_seleccionada_fijo = st.selectbox("Selecciona la tecnología para el análisis:", tecnologias)

    query_porcentaje = f"""
        SELECT 
            MUNICIPIO,
            COUNT(CASE WHEN {tecnologia_seleccionada_fijo} = 'S' THEN 1 END) * 1.0 / COUNT(*) * 100 AS porcentaje_cobertura
        FROM data_fijo
        GROUP BY MUNICIPIO
    """
    porcentaje_cobertura = con.execute(query_porcentaje).fetchdf()

    st.subheader(f"Porcentaje de Centros Poblados con Cobertura {tecnologia_seleccionada_fijo} en Cabeceras Municipales")
    with st.expander("Ver DataFrame de Porcentajes"):
        st.dataframe(porcentaje_cobertura)

    if not porcentaje_cobertura.empty:
        fig_porcentaje = px.bar(
            porcentaje_cobertura,
            x='MUNICIPIO',
            y='porcentaje_cobertura',
            title=f"Porcentaje de Cobertura {tecnologia_seleccionada_fijo} por Municipio",
            labels={'porcentaje_cobertura': 'Porcentaje de Cobertura (%)'},
            color='porcentaje_cobertura',
            color_continuous_scale=px.colors.sequential.Plasma
        )
        st.plotly_chart(fig_porcentaje, use_container_width=True)
    else:
        st.warning("No hay datos disponibles para el análisis fijo.")

    if not porcentaje_cobertura.empty:
        porcentaje_cobertura['Categoria'] = porcentaje_cobertura['porcentaje_cobertura'].apply(lambda x: '≥60%' if x >= 60 else '<60%')
        fig_torta = px.pie(
            porcentaje_cobertura,
            names='Categoria',
            title="Distribución de Municipios por Nivel de Conectividad",
            color_discrete_sequence=px.colors.sequential.Plasma
        )
        st.plotly_chart(fig_torta, use_container_width=True)
    else:
        st.warning("No hay datos disponibles para el gráfico de torta.")

    st.subheader("Porcentaje de Cobertura en Cabeceras y No Cabeceras Municipales")
    query_cobertura_acumulada = f"""
        SELECT 
            CABECERA_MUNICIPAL,
            COUNT(CASE WHEN {tecnologia_seleccionada_fijo} = 'S' THEN 1 END) * 1.0 / COUNT(*) * 100 AS porcentaje_cobertura
        FROM data_fijo
        GROUP BY CABECERA_MUNICIPAL
    """
    cobertura_acumulada = con.execute(query_cobertura_acumulada).fetchdf()
    cobertura_acumulada['CABECERA_MUNICIPAL'] = cobertura_acumulada['CABECERA_MUNICIPAL'].map({'S': 'Cabecera Municipal', 'N': 'No Cabecera Municipal'})

    if not cobertura_acumulada.empty:
        fig_barras_acumuladas = px.bar(
            cobertura_acumulada,
            x='CABECERA_MUNICIPAL',
            y='porcentaje_cobertura',
            title=f"Porcentaje de Cobertura {tecnologia_seleccionada_fijo} en Cabeceras y No Cabeceras Municipales",
            labels={'porcentaje_cobertura': 'Porcentaje de Cobertura (%)', 'CABECERA_MUNICIPAL': 'Tipo de Centro Poblado'},
            color='CABECERA_MUNICIPAL',
            color_discrete_sequence=px.colors.sequential.Plasma
        )
        st.plotly_chart(fig_barras_acumuladas, use_container_width=True)
    else:
        st.warning("No hay datos disponibles para el gráfico de barras acumuladas.")

    st.subheader("Porcentaje de Cobertura por Municipio (Cabeceras y No Cabeceras Municipales - Apiladas)")
    query_porcentaje_municipio = f"""
        SELECT 
            MUNICIPIO,
            CABECERA_MUNICIPAL,
            COUNT(CASE WHEN {tecnologia_seleccionada_fijo} = 'S' THEN 1 END) * 1.0 / COUNT(*) * 100 AS porcentaje_cobertura
        FROM data_fijo
        GROUP BY MUNICIPIO, CABECERA_MUNICIPAL
    """
    porcentaje_municipio = con.execute(query_porcentaje_municipio).fetchdf()
    porcentaje_municipio['CABECERA_MUNICIPAL'] = porcentaje_municipio['CABECERA_MUNICIPAL'].map({'S': 'Cabecera Municipal', 'N': 'No Cabecera Municipal'})

    if not porcentaje_municipio.empty:
        fig_barras_apiladas = px.bar(
            porcentaje_municipio,
            x='MUNICIPIO',
            y='porcentaje_cobertura',
            color='CABECERA_MUNICIPAL',
            barmode='stack',
            title=f"Porcentaje de Cobertura {tecnologia_seleccionada_fijo} por Municipio (Cabeceras y No Cabeceras Municipales - Apiladas)",
            labels={'porcentaje_cobertura': 'Porcentaje de Cobertura (%)', 'MUNICIPIO': 'Municipio', 'CABECERA_MUNICIPAL': 'Tipo de Centro Poblado'},
            color_discrete_sequence=px.colors.sequential.Plasma
        )
        st.plotly_chart(fig_barras_apiladas, use_container_width=True)
    else:
        st.warning("No hay datos disponibles para el gráfico de barras apiladas.")

    # Análisis Avanzado
    st.header("📈 Análisis Avanzado de Conectividad Móvil en Antioquia")

    tecnologia_seleccionada_p3 = st.selectbox(
        "Selecciona la tecnología para el análisis avanzado:",
        tecnologias,
        key="tecnologia_p3"
    )

    st.subheader("📊 Comparación de Proveedores (2023, Trimestre 3)")
    col1, col2 = st.columns(2)

    with col1:
        query_proveedores = f"""
            SELECT 
                PROVEEDOR,
                COUNT(CASE WHEN {tecnologia_seleccionada_p3} = 'S' THEN 1 END) * 1.0 / SUM(COUNT(CASE WHEN {tecnologia_seleccionada_p3} = 'S' THEN 1 END)) OVER () * 100 AS porcentaje_cobertura
            FROM data
            WHERE DEPARTAMENTO = 'ANTIOQUIA' AND AÑO = '2023' AND TRIMESTRE = '3'
            GROUP BY PROVEEDOR
            ORDER BY porcentaje_cobertura DESC
        """
        datos_proveedores = con.execute(query_proveedores).fetchdf()

        if not datos_proveedores.empty:
            fig_torta_proveedores = px.pie(
                datos_proveedores,
                names='PROVEEDOR',
                values='porcentaje_cobertura',
                title=f"Distribución de Cobertura {tecnologia_seleccionada_p3} por Proveedor (2023, Trimestre 3)",
                color_discrete_sequence=px.colors.sequential.Plasma
            )
            st.plotly_chart(fig_torta_proveedores, use_container_width=True)
            proveedor_mayor_cobertura = datos_proveedores.iloc[0]['PROVEEDOR']
        else:
            st.warning("No hay datos disponibles para la comparación de proveedores en 2023, Trimestre 3.")

    with col2:
        if not datos_proveedores.empty:
            query_top5_municipios = f"""
                SELECT 
                    MUNICIPIO,
                    COUNT(CASE WHEN {tecnologia_seleccionada_p3} = 'S' THEN 1 END) AS cobertura
                FROM data
                WHERE DEPARTAMENTO = 'ANTIOQUIA' AND AÑO = '2023' AND TRIMESTRE = '3' AND PROVEEDOR = '{proveedor_mayor_cobertura}'
                GROUP BY MUNICIPIO
                ORDER BY cobertura DESC
                LIMIT 5
            """
            top5_municipios = con.execute(query_top5_municipios).fetchdf()

            if not top5_municipios.empty:
                st.write(f"#### Top 5 Municipios con Mayor Presencia de {proveedor_mayor_cobertura}")
                st.dataframe(top5_municipios)
            else:
                st.warning(f"No hay datos disponibles para el Top 5 de municipios de {proveedor_mayor_cobertura}.")

    st.subheader("📅 Evolución Temporal de la Cobertura (Trimestre 3)")
    query_evolucion = """
        SELECT 
            AÑO,
            TRIMESTRE,
            COUNT(CASE WHEN COBERTURA_2G = 'S' THEN 1 END) * 1.0 / COUNT(*) * 100 AS COBERTURA_2G,
            COUNT(CASE WHEN COBERTURA_3G = 'S' THEN 1 END) * 1.0 / COUNT(*) * 100 AS COBERTURA_3G,
            COUNT(CASE WHEN "COBERTURA_HSPA+" = 'S' THEN 1 END) * 1.0 / COUNT(*) * 100 AS COBERTURA_HSPA,
            COUNT(CASE WHEN COBERTURA_4G = 'S' THEN 1 END) * 1.0 / COUNT(*) * 100 AS COBERTURA_4G,
            COUNT(CASE WHEN COBERTURA_5G = 'S' THEN 1 END) * 1.0 / COUNT(*) * 100 AS COBERTURA_5G
        FROM data
        WHERE DEPARTAMENTO = 'ANTIOQUIA' AND TRIMESTRE = '3'
        GROUP BY AÑO, TRIMESTRE
        ORDER BY AÑO
    """
    datos_evolucion = con.execute(query_evolucion).fetchdf()

    if not datos_evolucion.empty:
        fig_evolucion = px.line(
            datos_evolucion,
            x='AÑO',
            y=['COBERTURA_2G', 'COBERTURA_3G', 'COBERTURA_HSPA', 'COBERTURA_4G', 'COBERTURA_5G'],
            title="📈 Evolución Histórica de la Cobertura por Tecnología (Todos los años - Trimestre 3)",
            labels={'value': 'Porcentaje de Cobertura (%)', 'variable': 'Tecnología'},
            markers=True,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_evolucion.update_layout(hovermode="x unified")
        st.plotly_chart(fig_evolucion, use_container_width=True)
    else:
        st.warning("No hay datos disponibles para la evolución temporal.")

    st.subheader("⚠️ Brechas de Cobertura por Tecnología (2023, Trimestre 3)")
    with st.expander("Configuración de Análisis de Brechas"):
        tecnologia_brechas = st.selectbox(
            "Selecciona la tecnología para analizar brechas:",
            tecnologias,
            key="tecnologia_brechas"
        )

        query_brechas = f"""
            SELECT 
                MUNICIPIO,
                COUNT(CASE WHEN {tecnologia_brechas} = 'S' THEN 1 END) * 1.0 / COUNT(*) * 100 AS porcentaje_cobertura
            FROM data
            WHERE DEPARTAMENTO = 'ANTIOQUIA' AND AÑO = '2023' AND TRIMESTRE = '3'
            GROUP BY MUNICIPIO
            HAVING porcentaje_cobertura < 60
            ORDER BY porcentaje_cobertura ASC
        """
        datos_brechas = con.execute(query_brechas).fetchdf()

        query_centros_sin_cobertura = f"""
            SELECT 
                d.MUNICIPIO,
                d.CENTRO_POBLADO,
                d.CABECERA_MUNICIPAL,
                d.COBERTURA_4G AS cobertura
            FROM data d
            JOIN (
                SELECT MUNICIPIO
                FROM data
                WHERE DEPARTAMENTO = 'ANTIOQUIA' AND AÑO = '2023' AND TRIMESTRE = '3'
                GROUP BY MUNICIPIO
                HAVING COUNT(CASE WHEN {tecnologia_brechas} = 'S' THEN 1 END) * 1.0 / COUNT(*) * 100 < 60
            ) AS filtro
            ON d.MUNICIPIO = filtro.MUNICIPIO
            WHERE d.DEPARTAMENTO = 'ANTIOQUIA' AND d.AÑO = '2023' AND d.TRIMESTRE = '3' AND d.COBERTURA_4G = 'N'
            ORDER BY d.MUNICIPIO, d.CENTRO_POBLADO
        """
        datos_centros_sin_cobertura = con.execute(query_centros_sin_cobertura).fetchdf()
        datos_centros_sin_cobertura['CABECERA_MUNICIPAL'] = datos_centros_sin_cobertura['CABECERA_MUNICIPAL'].map({'S': 'Cabecera Municipal', 'N': 'No Cabecera Municipal'})

    col1, col2 = st.columns(2)
    with col1:
        if not datos_brechas.empty:
            st.markdown(f"#### Municipios con Cobertura {tecnologia_brechas} < 60%")
            st.dataframe(datos_brechas.style.format({'porcentaje_cobertura': '{:.2f}%'}))
        else:
            st.warning("No hay municipios con cobertura menor al 60% para la tecnología seleccionada")

    with col2:
        if not datos_centros_sin_cobertura.empty:
            st.markdown("#### Centros Poblados sin Cobertura seleccionada en Zonas Vulnerables")
            st.dataframe(datos_centros_sin_cobertura)
        else:
            st.info("✅ Todos los centros poblados tienen Cobertura seleccionada en áreas vulnerables")

    st.subheader("📶 Penetración Tecnológica por Municipio")
    query_tecnologias = """
        SELECT 
            MUNICIPIO,
            COUNT(CASE WHEN COBERTURA_2G = 'S' THEN 1 END) * 1.0 / COUNT(*) * 100 AS COBERTURA_2G,
            COUNT(CASE WHEN COBERTURA_3G = 'S' THEN 1 END) * 1.0 / COUNT(*) * 100 AS COBERTURA_3G,
            COUNT(CASE WHEN "COBERTURA_HSPA+" = 'S' THEN 1 END) * 1.0 / COUNT(*) * 100 AS COBERTURA_HSPA,
            COUNT(CASE WHEN COBERTURA_4G = 'S' THEN 1 END) * 1.0 / COUNT(*) * 100 AS COBERTURA_4G,
            COUNT(CASE WHEN COBERTURA_5G = 'S' THEN 1 END) * 1.0 / COUNT(*) * 100 AS COBERTURA_5G
        FROM data
        WHERE DEPARTAMENTO = 'ANTIOQUIA' AND AÑO = '2023' AND TRIMESTRE = '3'
        GROUP BY MUNICIPIO
    """
    datos_tecnologias = con.execute(query_tecnologias).fetchdf()

    if not datos_tecnologias.empty:
        fig_tecnologias = px.bar(
            datos_tecnologias,
            x='MUNICIPIO',
            y=['COBERTURA_2G', 'COBERTURA_3G', 'COBERTURA_HSPA', 'COBERTURA_4G', 'COBERTURA_5G'],
            title="🌐 Penetración Tecnológica por Municipio (Cobertura Acumulada)",
            labels={'value': 'Porcentaje de Cobertura (%)', 'variable': 'Tecnología'},
            barmode='stack',
            color_discrete_sequence=px.colors.sequential.Plasma
        )
        st.plotly_chart(fig_tecnologias, use_container_width=True)
    else:
        st.warning("No hay datos disponibles para el análisis de tecnologías.")

    st.subheader("📊 Resumen Estadístico")
    with st.container():
        cols = st.columns(3)
        with cols[0]:
            st.markdown("""
            <div style='background-color:#2ecc71; padding:20px; border-radius:10px; text-align:center'>
                <h3 style='color:white; margin:0;'>📶 Cobertura Promedio por Tecnología</h3>
            </div>
            """, unsafe_allow_html=True)
            
            tecnologia_promedio = st.selectbox(
                "Seleccionar tecnología:",
                tecnologias,
                key="tecnologia_promedio"
            )
            query_promedio = f"""
                SELECT 
                    AVG(CASE WHEN {tecnologia_promedio} = 'S' THEN 1 ELSE 0 END) * 100 AS promedio
                FROM data
                WHERE DEPARTAMENTO = 'ANTIOQUIA' AND AÑO = '2023' AND TRIMESTRE = '3'
            """
            promedio = con.execute(query_promedio).fetchdf()
            if not promedio.empty:
                st.markdown(f"""
                <div style='background-color:#2ecc71; padding:20px; border-radius:10px; text-align:center'>
                    <h1 style='color:white; margin:0;'>{promedio['promedio'].iloc[0]:.1f}%</h1>
                </div>
                """, unsafe_allow_html=True)
    
        with cols[1]:
            st.markdown("""
            <div style='background-color:#f1c40f; padding:20px; border-radius:10px; text-align:center'>
                <h3 style='color:white; margin:0;'>🌍 Cobertura Total Integrada</h3>
            </div>
            """, unsafe_allow_html=True)
    
            query_total = """
                SELECT 
                    AVG(
                        (CASE WHEN COBERTURA_2G = 'S' THEN 1 ELSE 0 END) +
                        (CASE WHEN COBERTURA_3G = 'S' THEN 1 ELSE 0 END) +
                        (CASE WHEN "COBERTURA_HSPA+" = 'S' THEN 1 ELSE 0 END) +
                        (CASE WHEN COBERTURA_4G = 'S' THEN 1 ELSE 0 END) +
                        (CASE WHEN COBERTURA_5G = 'S' THEN 1 ELSE 0 END)
                    ) * 100 / 5 AS total
                FROM data
                WHERE DEPARTAMENTO = 'ANTIOQUIA' AND AÑO = '2023' AND TRIMESTRE = '3'
            """
            total = con.execute(query_total).fetchdf()
            if not total.empty:
                st.markdown(f"""
                <div style='background-color:#f1c40f; padding:20px; border-radius:10px; text-align:center'>
                    <h1 style='color:white; margin:0;'>{total['total'].iloc[0]:.1f}%</h1>
                </div>
                """, unsafe_allow_html=True)
    
        with cols[2]:
            st.markdown("""
            <div style='background-color:#e74c3c; padding:20px; border-radius:10px; text-align:center'>
                <h3 style='color:white; margin:0;'>🌐 Cobertura Geográfica</h3>
            </div>
            """, unsafe_allow_html=True)
    
            query_municipios = """
                SELECT 
                    COUNT(DISTINCT MUNICIPIO) AS total
                FROM data
                WHERE DEPARTAMENTO = 'ANTIOQUIA' AND AÑO = '2023' AND TRIMESTRE = '3'
            """
            total_municipios = con.execute(query_municipios).fetchdf()
            if not total_municipios.empty:
                st.markdown(f"""
                <div style='background-color:#e74c3c; padding:20px; border-radius:10px; text-align:center'>
                    <h1 style='color:white; margin:0;'>{total_municipios['total'].iloc[0]}</h1>
                </div>
                """, unsafe_allow_html=True)

    st.subheader("🏆 Ranking de Municipios por tecnologia selecionada ")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Top 5 Municipios con Mayor Cobertura")
        query_top_mayor = f"""
            SELECT 
                MUNICIPIO,
                COUNT(CASE WHEN {tecnologia_seleccionada_p3} = 'S' THEN 1 END) * 1.0 / COUNT(*) * 100 AS cobertura
            FROM data
            WHERE DEPARTAMENTO = 'ANTIOQUIA' AND AÑO = '2023' AND TRIMESTRE = '3'
            GROUP BY MUNICIPIO
            ORDER BY cobertura DESC
            LIMIT 5
        """
        top_mayor = con.execute(query_top_mayor).fetchdf()
        if not top_mayor.empty:
            st.dataframe(top_mayor.style.format({'cobertura': '{:.1f}%'}))
        else:
            st.warning("No hay datos para el ranking")

    with col2:
        st.markdown("### Top 5 Municipios con Menor Cobertura")
        query_top_menor = f"""
            SELECT 
                MUNICIPIO,
                COUNT(CASE WHEN {tecnologia_seleccionada_p3} = 'S' THEN 1 END) * 1.0 / COUNT(*) * 100 AS cobertura
            FROM data
            WHERE DEPARTAMENTO = 'ANTIOQUIA' AND AÑO = '2023' AND TRIMESTRE = '3'
            GROUP BY MUNICIPIO
            ORDER BY cobertura ASC
            LIMIT 5
        """
        top_menor = con.execute(query_top_menor).fetchdf()
        if not top_menor.empty:
            st.dataframe(top_menor.style.format({'cobertura': '{:.1f}%'}))
        else:
            st.warning("No hay datos para el ranking")
    st.subheader("🏆 Top 5 Municipios con Mayor Presencia de COMCEL (Porcentaje de Cobertura)")

    # Calcular el total de centros poblados por municipio
    query_total_centros = """
        SELECT 
            MUNICIPIO,
            COUNT(*) AS total_centros_poblados
        FROM data
        WHERE DEPARTAMENTO = 'ANTIOQUIA' AND AÑO = '2023' AND TRIMESTRE = '3'
        GROUP BY MUNICIPIO
    """
    total_centros_municipio = con.execute(query_total_centros).fetchdf()
    
    # Filtrar los datos para COMCEL
    query_comcel = """
        SELECT 
            MUNICIPIO,
            COUNT(*) AS centros_cubiertos
        FROM data
        WHERE DEPARTAMENTO = 'ANTIOQUIA' AND AÑO = '2023' AND TRIMESTRE = '3' AND PROVEEDOR = 'COMUNICACION CELULAR S A COMCEL S A'
        GROUP BY MUNICIPIO
    """
    comcel_cobertura = con.execute(query_comcel).fetchdf()
    
    # Combinar los datos de cobertura de COMCEL con el total de centros poblados
    comcel_porcentaje = pd.merge(comcel_cobertura, total_centros_municipio, on='MUNICIPIO', how='left')
    
    # Calcular el porcentaje de cobertura
    comcel_porcentaje['porcentaje_cobertura'] = (comcel_porcentaje['centros_cubiertos'] / comcel_porcentaje['total_centros_poblados']) * 100
    
    # Ordenar por porcentaje de cobertura y obtener el Top 5
    top_5_comcel = comcel_porcentaje.sort_values(by='porcentaje_cobertura', ascending=False).head(5)
    
    # Mostrar el Top 5 en un DataFrame
    st.dataframe(top_5_comcel[['MUNICIPIO', 'porcentaje_cobertura']].style.format({'porcentaje_cobertura': '{:.1f}%'}))
    
    # Gráfico de barras para el Top 5
    if not top_5_comcel.empty:
        fig_top_5_comcel = px.bar(
            top_5_comcel,
            x='MUNICIPIO',
            y='porcentaje_cobertura',
            title="Top 5 Municipios con Mayor Presencia de COMCEL (Porcentaje de Cobertura)",
            labels={'porcentaje_cobertura': 'Porcentaje de Cobertura (%)', 'MUNICIPIO': 'Municipio'},
            color='porcentaje_cobertura',
            color_continuous_scale=px.colors.sequential.Viridis
        )
        st.plotly_chart(fig_top_5_comcel, use_container_width=True)
    else:
        st.warning("No hay datos disponibles para el Top 5 de municipios con presencia de COMCEL.")
