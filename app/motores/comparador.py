from app.cache import get_clima, get_agro
from app.proveedores.api_tiempo_real import obtener_clima_hoy
from app.motores.alertas import generar_semaforo, generar_consejo
from datetime import date

def generar_informe(estacion: dict) -> dict:

    cod_estacion = estacion["cod_estacion"]
    distrito = estacion["distrito"]
    latitud = estacion["latitud"]
    longitud = estacion["longitud"]

    df_clima = get_clima()
    historico = df_clima.filter(df_clima["cod_estacion"] == cod_estacion)

    temp_max_hist = 0.0
    prec_hist = 0.0

    if not historico.is_empty():
        temp_max_hist = round(historico["temp_max_C"].mean(), 1)
        prec_hist = round(historico["pc_precipitacion_mm"].mean(), 1)

    clima_hoy = obtener_clima_hoy(latitud, longitud)

    diff_temp = round(clima_hoy["temp_max"] - temp_max_hist, 1)
    if diff_temp > 3:
        comparacion = "Temperatura por encima de lo normal para la epoca."
    elif diff_temp < -3:
        comparacion = "Temperatura por debajo de lo normal para la epoca."
    else:
        comparacion = "Temperatura dentro del rango normal para la epoca."

    df_agro = get_agro()
    agro_distrito = df_agro.filter(df_agro["Dist"] == distrito.upper())

    realidad_agricola = []
    if not agro_distrito.is_empty():
        for fila in agro_distrito.iter_rows(named=True):
            realidad_agricola.append({
                "cultivo": fila["dsc_Cultivo"],
                "produccion_t": fila["PRODUCCION_t"],
                "cosecha_ha": fila["COSECHA_ha"],
                "precio_soles_kg": fila["MTO_PRECCHAC_soles_kg"]
            })

    semaforo = generar_semaforo(clima_hoy, temp_max_hist, prec_hist)
    consejo = generar_consejo(semaforo, clima_hoy)

    return {
        "distrito": distrito,
        "estacion_referencia": estacion["nombre_estacion"],
        "fecha_consulta": str(date.today()),
        "semaforo": semaforo,
        "clima_hoy": clima_hoy,
        "contexto_historico": {
            "temp_max_promedio_historico": temp_max_hist,
            "precipitacion_promedio_historico": prec_hist,
            "comparacion": comparacion
        },
        "realidad_agricola": realidad_agricola,
        "consejo": consejo
    }