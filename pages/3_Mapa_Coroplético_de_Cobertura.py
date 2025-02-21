import streamlit as st
import folium
from streamlit_folium import folium_static
import json
import pandas as pd
import duckdb

def page_mapa_coropletico(con):
    st.header("🌍 Mapa Coroplético de Cobertura por Municipio")

    # Subir el archivo GeoJSON
    uploaded_file = st.file_uploader("Sube un archivo GeoJSON con los límites de los municipios de Antioquia", type=["geojson"])

    if uploaded_file is not None:
        # Leer el archivo GeoJSON
        geojson_data = json.load(uploaded_file)

        # Filtrar solo los municipios de Antioquia
        antioquia_geojson = {
            "type": "FeatureCollection",
            "features": [feature for feature in geojson_data["features"] if feature["properties"]["DEPTO"] == "ANTIOQUIA"]
        }

        # Asignar un ID a cada municipio en el GeoJSON
        for loc in antioquia_geojson["features"]:
            loc["id"] = loc["properties"]["MPIO_CNMBR"]  # Asegurar que coincide con el DataFrame

        # Seleccionar la tecnología para el mapa coroplético
        tecnologias = ['COBERTURA_2G', 'COBERTURA_3G', 'COBERTURA_HSPA+', 'COBERTURA_4G', 'COBERTURA_LTE', 'COBERTURA_5G']
        tecnologia_seleccionada = st.selectbox("Selecciona la tecnología para el mapa coroplético:", tecnologias)

        # Obtener los porcentajes de cobertura por municipio
        query_porcentaje = f"""
            SELECT 
                MUNICIPIO,
                COUNT(CASE WHEN {tecnologia_seleccionada} = 'S' THEN 1 END) * 1.0 / COUNT(*) * 100 AS porcentaje_cobertura
            FROM data
            WHERE DEPARTAMENTO = 'ANTIOQUIA' AND AÑO = '2023' AND TRIMESTRE = '3'
            GROUP BY MUNICIPIO
        """
        porcentaje_cobertura = con.execute(query_porcentaje).fetchdf()

        # Normalizar nombres en el DataFrame (eliminando "Ñ" y "ñ")
        porcentaje_cobertura["MUNICIPIO"] = (
            porcentaje_cobertura["MUNICIPIO"]
            .str.upper()  # Convertir a mayúsculas
            .str.normalize("NFKD")  # Normalizar caracteres (quitar acentos)
            .str.encode("ascii", errors="ignore")  # Eliminar caracteres no ASCII
            .str.decode("utf-8")  # Volver a cadena de texto
            .str.replace("Ñ", "N")  # Reemplazar "Ñ" por "N"
            .str.replace("ñ", "n")  # Reemplazar "ñ" por "n" (por si acaso)
        )

        # Diccionario de correcciones
        correcciones = {
            "SAN PEDRO DE LOS MILAGROS": "SAN PEDRO",
            "EL SANTUARIO": "SANTUARIO",
            "NARINO": "NARIÑO",
            "BRICENO": "BRICEÑO",
            "CANASGORDAS": "CAÑASGORDAS",
            "PENOL": "PEÑOL",
            "EL CARMEN DE VIBORAL": "CARMEN DE VIBORAL",
            "DONMATIAS": "DON MATIAS",
            "SANTA ROSA DE OSOS": "SANTA.ROSA DE OSOS",
            "SAN ANDRES DE CUERQUIA": "SAN ANDRES",
            "SAN JOSE DE LA MONTANA": "SAN JOSE DE LA MONTAÑA",
            "SAN VICENTE FERRER": "SAN VICENTE"
        }

        # Aplicar las correcciones al DataFrame
        porcentaje_cobertura["MUNICIPIO"] = porcentaje_cobertura["MUNICIPIO"].replace(correcciones)

        # Crear el mapa base con Folium (usando un estilo sin etiquetas)
        mapa = folium.Map(location=[6.230833, -75.590553], zoom_start=8, tiles="CartoDB PositronNoLabels")  # Estilo sin etiquetas

        # Añadir el mapa coroplético
        choropleth = folium.Choropleth(
            geo_data=antioquia_geojson,  # Datos GeoJSON filtrados
            name="Cobertura",
            data=porcentaje_cobertura,  # Datos de porcentaje de cobertura
            columns=["MUNICIPIO", "porcentaje_cobertura"],  # Columna de municipio y valor
            key_on="feature.id",  # Usar el ID asignado en el GeoJSON
            fill_color="viridis",  # Escala de colores 
            fill_opacity=0.7,  # Opacidad del relleno
            line_opacity=0.2,  # Opacidad de las líneas de los límites
            legend_name="Porcentaje de Cobertura (%)",  # Leyenda del mapa
        ).add_to(mapa)

        # Añadir tooltips con el nombre del municipio y el porcentaje de cobertura
        folium.GeoJsonTooltip(
            fields=["MPIO_CNMBR"],  # Nombre del municipio en el GeoJSON
            aliases=["Municipio: "],  # Etiqueta para el tooltip
            localize=True,
            sticky=False,
            labels=True,
            style="""
                background-color: white;
                border: 1px solid black;
                border-radius: 3px;
                box-shadow: 3px 3px rgba(0, 0, 0, 0.2);
                padding: 2px;
                font-size: 12px;
            """
        ).add_to(choropleth.geojson)

        # Añadir un control de capas
        folium.LayerControl().add_to(mapa)

        # Mostrar el mapa en Streamlit
        folium_static(mapa)
    else:
        st.warning("Por favor, sube un archivo GeoJSON para continuar.")
