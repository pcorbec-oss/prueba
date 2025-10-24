import streamlit as st
import pandas as pd
import plotly.express as px

# Datos de ejemplo
data = {
    'Mes': ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio'] * 2,
    'Producto': ['Celular'] * 6 + ['Notebook'] * 6,
    'Ventas': [120, 100, 130, 145, 160, 155, 80, 90, 95, 120, 110, 115]
}

df = pd.DataFrame(data)

st.title('Dashboard de Ventas Mensuales')
st.markdown("Aquí puedes visualizar las ventas y filtrar por producto.")

# Filtro de producto
producto = st.selectbox("Selecciona el producto:", df['Producto'].unique())

# Filtra datos según selección
df_filtrado = df[df['Producto'] == producto]

# Gráfico de líneas
fig = px.line(
    df_filtrado,
    x='Mes',
    y='Ventas',
    title=f'Evolución de ventas de {producto}',
    markers=True
)
st.plotly_chart(fig, use_container_width=True)

# Tabla de datos filtrada
st.subheader("Tabla de ventas")
st.dataframe(df_filtrado)
