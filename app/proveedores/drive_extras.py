# Reservado para capas futuras: Suelos, Ecosistemas, Precios de mercado
# Seguir el mismo patron de drive_clima.py y drive_agro.py
# Al agregar una nueva capa:
# 1. Copiar este archivo con el nombre de la nueva capa
# 2. Cambiar DRIVE_ID y el metodo de lectura segun el formato
# 3. Registrar la carga en cache.py

import polars as pl

def leer_extras() -> pl.DataFrame:
    pass