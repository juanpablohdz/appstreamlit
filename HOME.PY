#instalar stramlit y ploty desde terminal
#para correr este proyecto:
#pocisionarse en la carpeta donde esta el proyecto en terminal
#correr streamlit desde cmd  codigo : streamlit run HOME.py
#instalar complementos de python para visual studio
import pandas as pd
import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
from query import *
import time

st.set_page_config(page_title="Dashboard",page_icon=':game_die:',layout='wide')
st.subheader("OPTIMIZACIÓN DE FILL-RATE MAYORISTA")
st.markdown("##")


result=view_all_data()
df=pd.DataFrame(result,columns=["SKU","SUC_NADRO","Mes","ABCD","CAPA_FALTANTE","PROVEDOR ","GRUPO","LABORATORIO","WEEK","COMPRATOTAL"])

#st.dataframe(df)

st.sidebar.image("Rfp.png", caption="Automatización Fill-rate Mayoristas")
#barra de filtros
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

# Realizar la selección de datos EN DADO CASO QUE SE REQUIERA DE QUERY GESTOR DE BD
# df_selection = df.query(
#     "SUC_NADRO == @Suc_nadro & ABCD == @abcd & Mes == @Mes & CAPA_FALTANTE == @Capa_faltante & `PROVEDOR ` == @Provedor & GRUPO == @Grupo & LABORATORIO == @Laboratorio & WEEK == @Week"
# )

# def Home():
#     with st.expander("Tabular"):
#         showData=st.multiselect("Filter:",df_selection.columns,default=[])
#         st.write(df_selection[showData])
# Home()

# Realizar la selección de datos

# Asegurarse de que los filtros no estén vacíos
Suc_nadro = Suc_nadro if Suc_nadro else df["SUC_NADRO"].unique()
abcd = abcd if abcd else df["ABCD"].unique()
Mes = Mes if Mes else df["Mes"].unique()
Capa_faltante = Capa_faltante if Capa_faltante else df["CAPA_FALTANTE"].unique()
Provedor = Provedor if Provedor else df["PROVEDOR "].unique()
Grupo = Grupo if Grupo else df["GRUPO"].unique()
Laboratorio = Laboratorio if Laboratorio else df["LABORATORIO"].unique()
Week = Week if Week else df["WEEK"].unique()

df_selection = df.query(
    "SUC_NADRO in @Suc_nadro and ABCD in @abcd and Mes in @Mes and CAPA_FALTANTE in @Capa_faltante and `PROVEDOR ` in @Provedor and GRUPO in @Grupo and LABORATORIO in @Laboratorio and WEEK in @Week"
)

# Mostrar DataFrame filtrado prueba de tabla 
#st.write("Datos filtrados:")
#st.dataframe(df_selection)
def Home():
    with st.expander("Tabular"):
        showData = st.multiselect("Filter:", df_selection.columns, default=df_selection.columns.tolist())
        st.write(df_selection[showData])
    #Las formulas  se cambian mediante se realiza los filtros
    suma_importe_factural = df['IMPORTE_FACTURA'].sum() if 'IMPORTE_FACTURA' in df.columns else 0
    suma_compra_total = df['COMPRATOTAL'].sum() if 'COMPRATOTAL' in df.columns else 0
    reultado_costo = suma_importe_factural / suma_compra_total if suma_compra_total != 0 else 0
    total1, total2, total3,total4 = st.columns(4, gap='large')
    with total1:
        st.info('total pedido costo', icon='ℹ️')
        st.metric(label='suma de costo', value=f'{reultado_costo:,.0f}')
    with total2:
        st.info('total surtido de costo', icon='ℹ️')
        
        st.metric(label='suma suma_compra_total', value=f'{suma_compra_total:,.0f}')
    with total3:
        st.info('Total fillrate (U) bruto', icon='ℹ️')
        st.metric(label='suma_importe_factural', value=f'{suma_importe_factural:,.0f}')
    with total4:
        st.info('Total fillrate ($) bruto', icon='ℹ️')
        st.metric(label='suma_importe_factural', value=f'{suma_importe_factural:,.0f}')


    st.markdown("""---""")

#Home()
def graphs():
    # Sumar y promediar las compras totales
    total_investment = int(df_selection["COMPRATOTAL"].sum())
    total_investment_mean = int(round(df_selection["COMPRATOTAL"].mean(), 2))

    # Gráfica simple de barra horizontal
    suma_compra = (
        df_selection.groupby(by="COMPRATOTAL").size().reset_index(name='counts')
    )
    fig_Compratotal_bar = px.bar(
        suma_compra,
        x='counts',
        y='COMPRATOTAL',
        orientation="h",
        title='<b>Compras Totales</b>',
        color_discrete_sequence=["#0083b8"] * len(suma_compra),
        template="plotly_white",
    )
    fig_Compratotal_bar.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False)
    )

    # Gráfica simple de líneas
    fig_Compratotal_line = px.line(
        suma_compra,
        x='COMPRATOTAL',
        y='counts',
        title='<b>Compras de Costo</b>',
        color_discrete_sequence=["#0083b8"] * len(suma_compra),
        template="plotly_white",
    )
    fig_Compratotal_line.update_layout(
        xaxis=dict(tickmode="linear"),
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(showgrid=False)
    )

    # Colocar gráficos en columnas
    left, right = st.columns(2)
    left.plotly_chart(fig_Compratotal_bar, use_container_width=True)
    right.plotly_chart(fig_Compratotal_line, use_container_width=True)


def progressbar():
    st.markdown(""" <style>.stProgress >div>div>div>div{ background-image:linear-gradient(to right, #99ff99, #FFFF00)}</style>""",unsafe_allow_html=True,)
    target=30000000
    current=df_selection["COMPRATOTAL"].sum()
    percent=round((current/target*100))
    mybar=st.progress(0)

    if percent>100:
        st.subheader("Target done")
    else:
        st.write("you have",percent,"%","of",(format(target,'d')),"TZS")
        for percent_complete in range (percent):
            time.sleep(0.1)
            mybar.progress(percent_complete+1,text="Target percentage ")

from streamlit_option_menu import option_menu

def sidebar():
    with st.sidebar:
        selected = option_menu(
            menu_title="Main Menu",
            options=["Home", "Progress"],
            icons=["house", "eye"],
            menu_icon="cast",
            default_index=0
        )
    return selected

# Llamar a la función sidebar() y asignar el valor de la opción seleccionada
selected = sidebar()

# Usar la variable selected fuera de la función sidebar()
if selected == 'Home':
    st.subheader(f"Page {selected}")
    Home()
    graphs()
elif selected == 'Progress':
    st.subheader(f"Page {selected}")
    progressbar()
    graphs()


#TEMA

hide_st_style="""
<style>
#Mainmenu{visibility:hidden;}
footer{visibility:hidden;}
header{visibility:hidden;}
</style>

"""


#PARA SUBIR A APLICACION A STREAM LIT 
#PASOS
#* pip install pipreqs -U
#* pipreqs .

# IDEA PONER LIMITE EN LA TABLA Y SOLO QUE SE MUESTREN 10 DE LO QUE NOS INTERESA  LO VEO INECESARIO
#EN ESTE FILTRO PODEMOS INCLUIR LO QUE ES LA SUMA DE UNIQUE  BRUTO ETC


## O YA QUE TENEMOS LA TABLA PODEMOS QUE  SOLO MUESTRE LOS RESULTADOS ESPERADOS COMO LO ESTA HACIENDO EN LOS KPI\

# PONER GRAFICOS INTERACIVOS QUE SE CONECTEN ENTRE TABLAS 

