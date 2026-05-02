import polars as pl
from datetime import date, timedelta
import random
import os

random.seed(42)

# Estaciones ficticias
estaciones = pl.DataFrame({
    "cod_estacion": ["LAM001", "LAM002", "LAM003", "PIU001", "CAJ001"],
    "categoria": ["CO", "CO", "CP", "CO", "CP"],
    "nombre_estacion": ["CHICLAYO", "FERRENAFE", "INCAHUASI", "PIURA", "CAJAMARCA"],
    "departamento": ["LAMBAYEQUE", "LAMBAYEQUE", "LAMBAYEQUE", "PIURA", "CAJAMARCA"],
    "provincia": ["CHICLAYO", "FERRENAFE", "FERRENAFE", "PIURA", "CAJAMARCA"],
    "distrito": ["CHICLAYO", "FERRENAFE", "INCAHUASI", "PIURA", "CAJAMARCA"],
    "altitud_msnm": [27.0, 50.0, 2980.0, 29.0, 2720.0],
    "latitud": [-6.7714, -6.6394, -6.2317, -5.1945, -7.1631],
    "longitud": [-79.8409, -79.7936, -79.3667, -80.6328, -78.5001]
})

# Clima ficticio historico
registros_clima = []
for estacion in estaciones.iter_rows(named=True):
    fecha_inicio = date(2010, 1, 1)
    for i in range(365 * 5):
        fecha = fecha_inicio + timedelta(days=i)
        registros_clima.append({
            "cod_estacion": estacion["cod_estacion"],
            "nombre": estacion["nombre_estacion"],
            "departamento": estacion["departamento"],
            "provincia": estacion["provincia"],
            "distrito": estacion["distrito"],
            "altitud_msnm": estacion["altitud_msnm"],
            "fecha": str(fecha),
            "temp_max_C": round(random.uniform(20.0, 32.0), 1),
            "temp_min_C": round(random.uniform(14.0, 20.0), 1),
            "hum_relativa": round(random.uniform(55.0, 85.0), 1),
            "pc_precipitacion_mm": round(random.uniform(0.0, 15.0), 1)
        })

df_clima = pl.DataFrame(registros_clima)

# Agro ficticio SISAGRI
cultivos = ["ARROZ", "MAIZ AMARILLO DURO", "CAÑA DE AZUCAR", "LIMON", "MANGO"]
registros_agro = []
for estacion in estaciones.iter_rows(named=True):
    for cultivo in cultivos:
        registros_agro.append({
            "anho": 2024,
            "mes": 7,
            "COD_UBIGEO": "140101",
            "Dpto": estacion["departamento"],
            "Prov": estacion["provincia"],
            "Dist": estacion["distrito"],
            "dsc_Cultivo": cultivo,
            "PRODUCCION_t": round(random.uniform(100.0, 5000.0), 1),
            "COSECHA_ha": round(random.uniform(10.0, 500.0), 1),
            "MTO_PRECCHAC_soles_kg": round(random.uniform(0.5, 3.5), 2)
        })

df_agro = pl.DataFrame(registros_agro)

# Guardar archivos
os.makedirs("data_ficticia", exist_ok=True)
estaciones.write_csv("data_ficticia/estaciones_ficticio.csv")
df_clima.write_parquet("data_ficticia/clima_ficticio.parquet")
df_agro.write_parquet("data_ficticia/sisagri_ficticio.parquet")

print("Archivos generados correctamente:")
print(f"  Estaciones: {len(estaciones)} registros")
print(f"  Clima: {len(df_clima)} registros")
print(f"  Agro: {len(df_agro)} registros")