


# #en dado caso que se requiera conexion de bases de datos 
# import streamlit as st
# import  mysql.connector

# #coneccion
# conn-mysql.connector.connect(
#     host="localhost",#host
#     port="3306",#puerto
#     user="root" #usuario
#     passwd="", #contraseña
#     db="myDb"#nombre de la base de datos
# )
# c=conn.cursor()


# #busqueda llamada fetch
# def view_all_data():
#     c.execute('select * from insurance order by id asc')
#     data=c.fetchall()
#     return data


#en dado caso que fuera de excel o de csv 
# query.py
import pandas as pd

def load_data(file_path):
    df = pd.read_csv(file_path)
    return df

def view_all_data():
    file_path = r"C:\Users\polla\Desktop\solucion nadro\AUTOMATIZACION\Datos_limpios.csv"
    df = load_data(file_path)
    
    # Verifica si 'SKU' está en las columnas del DataFrame
    if 'SKU' in df.columns:
        data = df.sort_values(by='SKU', ascending=True)
    else:
        raise KeyError("La columna 'SKU' no se encuentra en el archivo CSV.")
    return data

# Para probar el código directamente en query.py
if __name__ == "__main__":
    try:
        data = view_all_data()
        print(data.head())
    except KeyError as e:
        print(e)
