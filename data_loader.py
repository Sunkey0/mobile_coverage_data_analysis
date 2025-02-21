import pandas as pd
import streamlit as st

def load_data():
    # URL del archivo CSV en el repositorio de GitHub
    url = "https://raw.githubusercontent.com/tu_usuario/tu_repositorio/main/ruta/al/archivo.csv"
    
    # Cargar datos desde la URL
    data = pd.read_csv(url)
    
    # Renombrar columnas
    data.columns = [
        'AÑO', 'TRIMESTRE', 'PROVEEDOR', 'COD_DEPARTAMENTO', 'DEPARTAMENTO', 'COD_MUNICIPIO',
        'MUNICIPIO', 'CABECERA_MUNICIPAL', 'COD_CENTRO_POBLADO', 'CENTRO_POBLADO',
        'COBERTURA_2G', 'COBERTURA_3G', 'COBERTURA_HSPA+', 'COBERTURA_4G', 'COBERTURA_LTE', 'COBERTURA_5G'
    ]
    
    return data
