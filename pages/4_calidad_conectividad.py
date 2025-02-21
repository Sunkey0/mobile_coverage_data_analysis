import streamlit as st
import pandas as pd
import plotly.express as px

def page_calidad_conectividad():
    st.header("📈 Análisis de Calidad de la Conectividad")

    # Datos de calidad de la conectividad
    calidad_conectividad = {
        "Municipio": [
            "Medellín", "Abejorral", "Abriaquí", "Alejandría", "Amagá", "Amalfi", "Andes", "Angelópolis", "Angostura", "Anorí",
            "Santa Fé de Antioquia", "Anzá", "Apartadó", "Argelia", "Armenia", "Barbosa", "Belmira", "Bello", "Betania", "Betulia",
            "Briceño", "Buriticá", "Cáceres", "Caicedo", "Caldas", "Cañasgordas", "Caracolí", "Caramanta", "Carepa", "El Carmen de Viboral",
            "Carolina", "Caucasia", "Chigorodó", "Cisneros", "Cocorná", "Concepción", "Concordia", "Copacabana", "Dabeiba", "Donmatías",
            "Ebéjico", "El Bagre", "Entrerríos", "Envigado", "Fredonia", "Frontino", "Girardota", "Gómez Plata", "Granada", "Guadalupe",
            "Guarne", "Guatapé", "Heliconia", "Hispania", "Itagüí", "Ituango", "Jardín", "La Ceja", "La Estrella", "La Pintada", 
            "La Unión", "Liborina", "Maceo", "Marinilla", "Montebello", "Murindó", "Nariño", "Necoclí", "Nechí", "Peñol",
            "Pueblorrico", "Puerto Berrío", "Puerto Nare", "Puerto Triunfo", "Retiro", "Rionegro", "Sabanalarga", "Sabaneta", "Salgar", "San Andrés de Cuerquía",
            "San Francisco", "San Jerónimo", "San José de la Montaña", "San Juan de Urabá", "San Luis", "San Pedro de Urabá", "San Roque", "San Vicente Ferrer", "Santa Bárbara", "Santa Rosa de Osos",
            "El Santuario", "Segovia", "Sonsón", "Sopetrán", "Támesis", "Tarazá", "Tarso", "Titiribí", "Toledo", "Turbo",
            "Uramita", "Urrao", "Valdivia", "Valparaíso", "Vegachí", "Venecia", "Yalí", "Yarumal", "Yolombó", "Yondó", "Zaragoza"
        ],
        "Nivel de Desempeño de Calidad": [
            "Alto", "Medio", "Bajo", "Bajo", "Bajo", "Bajo", "Bajo", "Bajo", "Medio", "Bajo",
            "Bajo", "Bajo", "Bajo", "Medio", "Medio", "Bajo", "Bajo", "Alto", "Medio", "Medio",
            "Medio", "Medio", "Medio", "Medio", "Alto", "Bajo", "Bajo", "Bajo", "Bajo", "Bajo",
            "Bajo", "Bajo", "Bajo", "Bajo", "Bajo", "Bajo", "Medio", "Alto", "Bajo", "Bajo",
            "Medio", "Bajo", "Medio", "Alto", "Medio", "Bajo", "Alto", "Bajo", "Medio", "Medio",
            "Bajo", "Alto", "Medio", "Bajo", "Alto", "Medio", "Bajo", "Alto", "Alto", "Bajo",
            "Bajo", "Medio", "Medio", "Bajo", "Medio", "Bajo", "Medio", "Bajo", "Bajo", "Bajo",
            "Medio", "Bajo", "Bajo", "Bajo", "Alto", "Alto", "Medio", "Alto", "Medio", "Medio",
            "Medio", "Bajo", "Bajo", "Bajo", "Bajo", "Bajo", "Medio", "Bajo", "Bajo", "Bajo",
            "Bajo", "Bajo", "Bajo", "Bajo", "Bajo", "Bajo", "Bajo", "Bajo", "Medio", "Bajo",
            "Medio", "Bajo", "Medio", "Medio", "Bajo", "Alto", "Bajo", "Bajo", "Medio", "Bajo",
            "Bajo"
        ]
    }

    df_calidad = pd.DataFrame(calidad_conectividad)

    # DataFrames desplegables
    with st.expander("📋 Ver tabla completa de municipios", expanded=False):
        st.write("### Calidad de la Conectividad por Municipio")
        st.dataframe(df_calidad)

    # Filtros
    st.sidebar.header("Filtros de Calidad")
    nivel_seleccionado = st.sidebar.selectbox("Selecciona el nivel de desempeño:", ["Todos", "Alto", "Medio", "Bajo"])

    # Aplicar filtro
    if nivel_seleccionado != "Todos":
        df_filtrado = df_calidad[df_calidad["Nivel de Desempeño de Calidad"] == nivel_seleccionado]
    else:
        df_filtrado = df_calidad

    # DataFrame filtrado desplegable
    with st.expander(f"📑 Ver municipios con nivel {nivel_seleccionado}", expanded=False):
        st.write(f"### Municipios con Nivel de Desempeño: {nivel_seleccionado}")
        st.dataframe(df_filtrado)

    # Calcular estadísticos
    total_municipios = 111
    conteo_calidad = df_calidad["Nivel de Desempeño de Calidad"].value_counts()

    # Gráfico de torta con Plotly
    st.write("### Distribución de Calidad de Conectividad")
    fig = px.pie(
        df_calidad,
        names="Nivel de Desempeño de Calidad",
        title="",
        color_discrete_sequence=px.colors.sequential.Viridis
    )
    st.plotly_chart(fig)
    
    # Total de municipios en una ficha adicional
    st.markdown(f"""
    <div style='background-color:#3498db; padding:20px; border-radius:10px; text-align:center; margin-top:20px; margin-bottom:30px;'>
        <h3 style='color:white; margin:0;'>🏘️ Total Municipios</h3>
        <h1 style='color:white; margin:0;'>{total_municipios}</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Crear 3 columnas para los KPIs
    col1, col2, col3 = st.columns(3)
    
    # Ficha KPI para Calidad Alta
    with col1:
        st.markdown("""
        <div style='background-color:#2ecc71; padding:20px; border-radius:10px; text-align:center'>
            <h3 style='color:white; margin:0;'>🏅 Municipios Con Calidad Alta</h3>
            <h1 style='color:white; margin:0;'>{}</h1>
        </div>
        """.format(conteo_calidad.get('Alto', 0)), unsafe_allow_html=True)
    
    # Ficha KPI para Calidad Media
    with col2:
        st.markdown("""
        <div style='background-color:#f1c40f; padding:20px; border-radius:10px; text-align:center'>
            <h3 style='color:white; margin:0;'>🎯 Municipios Con Calidad Media</h3>
            <h1 style='color:white; margin:0;'>{}</h1>
        </div>
        """.format(conteo_calidad.get('Medio', 0)), unsafe_allow_html=True)
    
    # Ficha KPI para Calidad Baja
    with col3:
        st.markdown("""
        <div style='background-color:#e74c3c; padding:20px; border-radius:10px; text-align:center'>
            <h3 style='color:white; margin:0;'>📉 Municipios Con Calidad Baja</h3>
            <h1 style='color:white; margin:0;'>{}</h1>
        </div>
        """.format(conteo_calidad.get('Bajo', 0)), unsafe_allow_html=True)
