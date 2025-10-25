import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# Configuracion de la pagina
st.set_page_config(
    page_title="Dashboard de Ventas",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Titulo principal
st.title("📊 Dashboard de Ventas")
st.markdown("---")

# Datos de ejemplo
@st.cache_data
def cargar_datos():
    datos = pd.DataFrame({
        'Fecha': pd.date_range(start='2024-01-01', periods=100),
        'Ventas': np.random.randint(1000, 5000, 100),
        'Clientes': np.random.randint(5, 50, 100),
        'Producto': np.random.choice(['Producto A', 'Producto B', 'Producto C'], 100)
    })
    return datos

datos = cargar_datos()

# Filtros en la barra lateral
st.sidebar.header("Filtros")
fecha_inicio = st.sidebar.date_input(
    "Fecha de inicio",
    value=datos['Fecha'].min(),
    min_value=datos['Fecha'].min(),
    max_value=datos['Fecha'].max()
)
fecha_fin = st.sidebar.date_input(
    "Fecha de fin",
    value=datos['Fecha'].max(),
    min_value=datos['Fecha'].min(),
    max_value=datos['Fecha'].max()
)

producto_seleccionado = st.sidebar.multiselect(
    "Selecciona productos",
    options=datos['Producto'].unique(),
    default=datos['Producto'].unique()
)

# Filtrar datos
datos_filtrados = datos[
    (datos['Fecha'].dt.date >= fecha_inicio) &
    (datos['Fecha'].dt.date <= fecha_fin) &
    (datos['Producto'].isin(producto_seleccionado))
]

# Métricas principales en columnas
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="💰 Ventas Totales",
        value=f"${datos_filtrados['Ventas'].sum():,.0f}",
        delta=f"+{(datos_filtrados['Ventas'].sum() / datos['Ventas'].sum() * 100):.1f}%"
    )

with col2:
    st.metric(
        label="👥 Total de Clientes",
        value=f"{datos_filtrados['Clientes'].sum()}",
        delta=f"+{(datos_filtrados['Clientes'].sum() / datos['Clientes'].sum() * 100):.1f}%"
    )

with col3:
    st.metric(
        label="📈 Venta Promedio",
        value=f"${datos_filtrados['Ventas'].mean():,.0f}"
    )

with col4:
    st.metric(
        label="📊 Dias con datos",
        value=f"{len(datos_filtrados)}"
    )

st.markdown("---")

# Gráficos
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Ventas en el Tiempo")
    fig_linea = px.line(
        datos_filtrados,
        x='Fecha',
        y='Ventas',
        markers=True,
        title="Tendencia de ventas"
    )
    fig_linea.update_layout(hovermode='x unified')
    st.plotly_chart(fig_linea, use_container_width=True)

with col2:
    st.subheader("🎯 Ventas por Producto")
    ventas_producto = datos_filtrados.groupby('Producto')['Ventas'].sum()
    fig_pie = px.pie(
        values=ventas_producto.values,
        names=ventas_producto.index,
        title="Distribucion de ventas"
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# Grafico de barras
st.subheader("📊 Clientes por Producto")
fig_barras = px.bar(
    datos_filtrados.groupby('Producto')['Clientes'].sum().reset_index(),
    x='Producto',
    y='Clientes',
    title="Cantidad de clientes por producto",
    color='Clientes',
    color_continuous_scale='Blues'
)
st.plotly_chart(fig_barras, use_container_width=True)

# Tabla de datos
st.subheader("📋 Datos Detallados")
st.dataframe(
    datos_filtrados.sort_values('Fecha', ascending=False),
    use_container_width=True,
    height=400
)

# Estadisticas adicionales
st.subheader("📉 Estadísticas")
stats_col1, stats_col2, stats_col3 = st.columns(3)

with stats_col1:
    st.write(f"**Venta Máxima:** ${datos_filtrados['Ventas'].max():,.0f}")
    st.write(f"**Venta Mínima:** ${datos_filtrados['Ventas'].min():,.0f}")

with stats_col2:
    st.write(f"**Desviación Estándar:** ${datos_filtrados['Ventas'].std():,.0f}")
    st.write(f"**Mediana:** ${datos_filtrados['Ventas'].median():,.0f}")

with stats_col3:
    st.write(f"**Periodo:** {fecha_inicio} a {fecha_fin}")
    st.write(f"**Dias analizados:** {len(datos_filtrados)}")

st.markdown("---")
st.markdown("<p style='text-align: center;'>Dashboard creado con Streamlit | 2025</p>", unsafe_allow_html=True)
