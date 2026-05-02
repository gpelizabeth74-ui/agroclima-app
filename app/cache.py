import polars as pl
import os
from dotenv import load_dotenv

load_dotenv()

MODO = os.getenv("MODO_DATOS", "ficticio")

# Variables globales que viven en memoria
df_estaciones = None
df_clima = None
df_agro = None

def cargar_datos():
    global df_estaciones, df_clima, df_agro

    if MODO == "ficticio":
        print("Cargando datos ficticios...")
        df_estaciones = pl.read_csv("data_ficticia/estaciones_ficticio.csv")
        df_clima = pl.read_parquet("data_ficticia/clima_ficticio.parquet")
        df_agro = pl.read_parquet("data_ficticia/sisagri_ficticio.parquet")

    else:
        print("Cargando datos reales desde Drive...")
        from app.proveedores.drive_estaciones import leer_estaciones
        from app.proveedores.drive_clima import leer_clima
        from app.proveedores.drive_agro import leer_agro
        df_estaciones = leer_estaciones()
        df_clima = leer_clima()
        df_agro = leer_agro()

    print(f"Estaciones cargadas: {len(df_estaciones)}")
    print(f"Registros clima cargados: {len(df_clima)}")
    print(f"Registros agro cargados: {len(df_agro)}")

def get_estaciones():
    return df_estaciones

def get_clima():
    return df_clima

def get_agro():
    return df_agro