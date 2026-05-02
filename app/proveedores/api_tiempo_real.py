import httpx

def obtener_clima_hoy(latitud: float, longitud: float) -> dict:
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitud,
        "longitude": longitud,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,relative_humidity_2m_max",
        "timezone": "America/Lima",
        "forecast_days": 1
    }

    try:
        respuesta = httpx.get(url, params=params, timeout=10)
        datos = respuesta.json()

        daily = datos.get("daily", {})

        return {
            "temp_max": daily.get("temperature_2m_max", [0])[0] or 0.0,
            "temp_min": daily.get("temperature_2m_min", [0])[0] or 0.0,
            "precipitacion_mm": daily.get("precipitation_sum", [0])[0] or 0.0,
            "humedad_relativa": daily.get("relative_humidity_2m_max", [0])[0] or 0.0
        }

    except Exception:
        # Si no hay conexion devuelve valores neutros
        return {
            "temp_max": 0.0,
            "temp_min": 0.0,
            "precipitacion_mm": 0.0,
            "humedad_relativa": 0.0
        }