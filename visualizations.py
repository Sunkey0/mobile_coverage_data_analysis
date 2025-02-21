import plotly.express as px

def plot_cobertura(data, x_axis, y_axis, title, color_scale):
    if not data.empty:
        fig = px.bar(
            data,
            x=x_axis,
            y=y_axis,
            title=title,
            labels={'Conteo': 'Número de Centros Poblados con Cobertura'},
            color=y_axis,
            color_continuous_scale=color_scale
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning(f"No hay datos de cobertura para {title}.")
