import pandas as pd
import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
from query import *

st.set_page_config(page_title="Dashboard", page_icon=':game_die:', layout='wide')
st.subheader("OPTIMIZACIÓN DE FILL-RATE MAYORISTA")
st.markdown("##")

# Cargar los datos
result = view_all_data()
df = pd.DataFrame(result, columns=["SKU", "SUC_NADRO", "Mes", "ABCD", "CAPA_FALTANTE", "PROVEDOR ", "GRUPO", "LABORATORIO", "WEEK"])

st.sidebar.image("Rfp.png", caption="Automatización Fill-rate Mayoristas")

# Barra de filtros
st.sidebar.header("Filtros")

Suc_nadro = st.sidebar.multiselect(
    "Selecciona el SUC_NADRO",
    options=df["SUC_NADRO"].unique(),
    default=df["SUC_NADRO"].unique()
)

abcd = st.sidebar.multiselect(
    "Selecciona el ABCD",
    options=df["ABCD"].unique(),
    default=df["ABCD"].unique()
)

Mes = st.sidebar.multiselect(
    "Selecciona el Mes que deseas filtrar",
    options=df["Mes"].unique(),
    default=df["Mes"].unique()
)

Capa_faltante = st.sidebar.multiselect(
    "Selecciona el CAPA_FALTANTE",
    options=df["CAPA_FALTANTE"].unique(),
    default=df["CAPA_FALTANTE"].unique()
)

Provedor = st.sidebar.multiselect(
    "Selecciona el Proveedor",
    options=df["PROVEDOR "].unique(),
    default=df["PROVEDOR "].unique()
)

Grupo = st.sidebar.multiselect(
    "Selecciona el Grupo",
    options=df["GRUPO"].unique(),
    default=df["GRUPO"].unique()
)

Laboratorio = st.sidebar.multiselect(
    "Selecciona el Laboratorio",
    options=df["LABORATORIO"].unique(),
    default=df["LABORATORIO"].unique()
)

Week = st.sidebar.multiselect(
    "Selecciona La semana",
    options=df["WEEK"].unique(),
    default=df["WEEK"].unique()
)


# Asegurarse de que los filtros no estén vacíos
Suc_nadro = Suc_nadro if Suc_nadro else df["SUC_NADRO"].unique()
abcd = abcd if abcd else df["ABCD"].unique()
Mes = Mes if Mes else df["Mes"].unique()
Capa_faltante = Capa_faltante if Capa_faltante else df["CAPA_FALTANTE"].unique()
Provedor = Provedor if Provedor else df["PROVEDOR "].unique()
Grupo = Grupo if Grupo else df["GRUPO"].unique()
Laboratorio = Laboratorio if Laboratorio else df["LABORATORIO"].unique()
Week = Week if Week else df["WEEK"].unique()

# Realizar la selección de datos
df_selection = df.query(
    "SUC_NADRO in @Suc_nadro and ABCD in @abcd and Mes in @Mes and CAPA_FALTANTE in @Capa_faltante and `PROVEDOR ` in @Provedor and GRUPO in @Grupo and LABORATORIO in @Laboratorio and WEEK in @Week"
)

# Mostrar DataFrame filtrado
st.write("Datos filtrados:")
st.dataframe(df_selection)

def Home():
    with st.expander("Tabular"):
        showData = st.multiselect("Filter:", df_selection.columns, default=df_selection.columns.tolist())
        st.write(df_selection[showData])

Home()

# Ejemplo de una gráfica con Plotly (opcional)
fig = px.line(df_selection, x='SKU', y='CAPA_FALTANTE')  # Reemplaza 'CAPA_FALTANTE' con la columna que desees graficar
st.plotly_chart(fig)
