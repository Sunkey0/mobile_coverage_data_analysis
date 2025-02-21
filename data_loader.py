import pandas as pd
import streamlit as st

def load_data(uploaded_file):
    """
    Carga los datos desde un archivo CSV subido por el usuario.
    """
    if uploaded_file is not None:
        try:
            # Leer el archivo CSV
            data = pd.read_csv(uploaded_file)
            
            # Renombrar columnas
            data.columns = [
                'AÑO', 'TRIMESTRE', 'PROVEEDOR', 'COD_DEPARTAMENTO', 'DEPARTAMENTO', 'COD_MUNICIPIO',
                'MUNICIPIO', 'CABECERA_MUNICIPAL', 'COD_CENTRO_POBLADO', 'CENTRO_POBLADO',
                'COBERTURA_2G', 'COBERTURA_3G', 'COBERTURA_HSPA+', 'COBERTURA_4G', 'COBERTURA_LTE', 'COBERTURA_5G'
            ]
            
            return data
        except Exception as e:
            st.error(f"Error al cargar los datos: {e}")
            st.stop()
    else:
        st.warning("Por favor, sube un archivo CSV para continuar.")
        st.stop()
