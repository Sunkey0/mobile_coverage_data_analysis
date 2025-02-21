import streamlit as st
import folium
from streamlit_folium import folium_static
import json
import pandas as pd

def page_mapa_calidad_conectividad():   
    st.header("🌍 Mapa Coroplético de Calidad de Conectividad por Municipio")

    # Subir el archivo GeoJSON
    uploaded_file = st.file_uploader(
        "Sube un archivo GeoJSON con los límites de los municipios de Antioquia", 
        type=["geojson"],
        key="file_uploader_mapa_calidad"
    )

    if uploaded_file is not None:
        # Leer y filtrar GeoJSON
        geojson_data = json.load(uploaded_file)

        # Filtrar solo los municipios de Antioquia
        antioquia_geojson = {
            "type": "FeatureCollection",
            "features": [feature for feature in geojson_data["features"] if feature["properties"]["DEPTO"] == "ANTIOQUIA"]
        }

        # Asignar un ID a cada municipio en el GeoJSON
        for loc in antioquia_geojson["features"]:
            loc["id"] = loc["properties"]["MPIO_CNMBR"]  # Asegurar que coincide con el DataFrame
        
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
        
        # Generar la columna "Codigo_Calidad"
        calidad_conectividad["Codigo_Calidad"] = [
            2 if x == "Alto" else 1 if x == "Medio" else 0 
            for x in calidad_conectividad["Nivel de Desempeño de Calidad"]
        ]
        
        # Convertir a DataFrame
        df_calidad = pd.DataFrame(calidad_conectividad)
    
        with st.expander("📋 Ver tabla completa de calidad", expanded=False):
            st.write("### Tabla de calidad de conectividad por municipio")
            st.dataframe(df_calidad)
        
        # Normalizar nombres en el DataFrame
        df_calidad["Municipio"] = (
            df_calidad["Municipio"]
            .str.upper()
            .str.normalize("NFKD")
            .str.encode("ascii", errors="ignore")
            .str.decode("utf-8")
        )

        # Aplicar correcciones
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
            "SAN VICENTE FERRER": "SAN VICENTE",
            "SANTA FE DE ANTIOQUIA": "SANTAFE DE ANTIOQUIA"
        }
        df_calidad["Municipio"] = df_calidad["Municipio"].replace(correcciones)

        def style_function(feature):
            # Obtener el nombre o código del municipio (ajustar según la estructura del GeoJSON)
            municipio = feature['properties']['MPIO_CNMBR']
            
            # Verificar si el municipio existe en el DataFrame
            if municipio in df_calidad['Municipio'].values:
                # Buscar el nivel de calidad en el DataFrame
                nivel_calidad = df_calidad.loc[df_calidad['Municipio'] == municipio, 'Codigo_Calidad'].values[0]
                
                # Asignar colores según el nivel de calidad
                if nivel_calidad == 0:
                    color = '#FF0000'  # Rojo para Bajo
                elif nivel_calidad == 1:
                    color = '#FFFF00'  # Amarillo para Medio
                else:
                    color = '#00FF00'  # Verde para Alto
            else:
                # Si el municipio no está en el DataFrame, asignar un color por defecto
                color = '#FF9999'  # rosa para municipios no encontrados
            
            # Retornar el estilo
            return {
                'fillColor': color,
                'color': 'black',  # Contorno negro
                'weight': 0.5,  # Grosor del contorno
                'fillOpacity': 0.7  # Opacidad del relleno
            }
        
        # Crear el mapa
        m = folium.Map(location=[6.230833, -75.590553], zoom_start=8, tiles="CartoDB PositronNoLabels")
        
        # Agregar el GeoJSON con la función de estilo personalizada
        folium.GeoJson(
            antioquia_geojson,
            style_function=style_function,  # Aplicar el estilo personalizado
            tooltip=folium.GeoJsonTooltip(fields=["MPIO_CNMBR"], aliases=["Municipio: "])  # Agregar tooltip si es necesario
        ).add_to(m)
        
        # Mostrar el mapa
        folium_static(m)

        municipios_df = set(df_calidad["Municipio"])
        
        # Municipios en el GeoJSON (corregidos)
        municipios_geojson = set(loc["properties"]["MPIO_CNMBR"] for loc in antioquia_geojson["features"])
        
        # Municipios en el GeoJSON que no están en el DataFrame
        with st.expander("⚠ Municipios faltantes en la base de datos", expanded=False):
            st.write("### Municipios que no están en el DataFrame:")
            st.write(municipios_geojson - municipios_df)
        
    else:
        st.warning("Por favor, sube un archivo GeoJSON para continuar.")

# Ejecutar la función principal
page_mapa_calidad_conectividad()
