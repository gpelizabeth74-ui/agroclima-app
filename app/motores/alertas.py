def generar_semaforo(clima_hoy: dict, temp_max_hist: float, prec_hist: float) -> str:
    temp_max = clima_hoy["temp_max"]
    precipitacion = clima_hoy["precipitacion_mm"]
    humedad = clima_hoy["humedad_relativa"]

    # Condiciones de riesgo alto
    if precipitacion > 20 or temp_max > (temp_max_hist + 5) or humedad > 90:
        return "ROJO"

    # Condiciones de precaucion
    if precipitacion > 10 or temp_max > (temp_max_hist + 3) or humedad > 80:
        return "AMARILLO"

    # Condiciones normales
    return "VERDE"


def generar_consejo(semaforo: str, clima_hoy: dict) -> str:
    temp_max = clima_hoy["temp_max"]
    precipitacion = clima_hoy["precipitacion_mm"]
    humedad = clima_hoy["humedad_relativa"]

    if semaforo == "ROJO":
        if precipitacion > 20:
            return (
                "Lluvias fuertes previstas. "
                "Proteja sus cultivos y evite aplicar fertilizantes o pesticidas hoy. "
                "Revise los canales de drenaje para evitar inundaciones."
            )
        if temp_max > 35:
            return (
                "Temperatura muy alta. "
                "Riegue en las primeras horas de la manana o al caer la tarde. "
                "Evite labores de campo en las horas de mayor calor."
            )
        if humedad > 90:
            return (
                "Humedad muy elevada. "
                "Riesgo alto de enfermedades fungicas en sus cultivos. "
                "Revise hojas y tallos, especialmente en la parte baja de la planta."
            )

    if semaforo == "AMARILLO":
        if humedad > 80:
            return (
                "Humedad moderadamente alta. "
                "Revise sus cultivos por presencia de hongos en hojas bajas. "
                "Buen momento para aplicar fungicidas preventivos si lo tiene planificado."
            )
        if precipitacion > 10:
            r