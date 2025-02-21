import streamlit as st
import pandas as pd

def load_data():
    uploaded_file = st.sidebar.file_uploader("⬆️ Sube tu archivo CSV", type=["csv"])
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        data.columns = [
            'AÑO', 'TRIMESTRE', 'PROVEEDOR', 'COD_DEPARTAMENTO', 'DEPARTAMENTO', 'COD_MUNICIPIO',
            'MUNICIPIO', 'CABECERA_MUNICIPAL', 'COD_CENTRO_POBLADO', 'CENTRO_POBLADO',
            'COBERTURA_2G', 'COBERTURA_3G', 'COBERTURA_HSPA+', 'COBERTURA_4G', 'COBERTURA_LTE', 'COBERTURA_5G'
        ]
        return data
    else:
        st.warning("Por favor, sube un archivo CSV para continuar.")
        st.stop()
