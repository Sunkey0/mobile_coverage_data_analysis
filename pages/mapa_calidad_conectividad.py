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
                "San Francisco", "San Jerónimo", "San José de la Montaña",
