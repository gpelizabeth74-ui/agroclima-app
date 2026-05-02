from fastapi import APIRouter, HTTPException
from app.esquemas import ConsultaPorCoordenadas, ConsultaPorDistrito, RespuestaConsulta
from app.cache import get_estaciones
from app.motores.comparador import generar_informe
import math

router = APIRouter()

def calcular_distancia(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return R * 2 * math.asin(math.sqrt(a))

def estacion_mas_cercana(latitud, longitud):
    estaciones = get_estaciones()
    menor_distancia = float("inf")
    estacion_elegida = None

    for fila in estaciones.iter_rows(named=True):
        distancia = calcular_distancia(
            latitud, longitud,
            fila["latitud"], fila["longitud"]
        )
        if distancia < menor_distancia:
            menor_distancia = distancia
            estacion_elegida = fila

    return estacion_elegida

@router.post("/consulta/por-coordenadas", response_model=RespuestaConsulta)
def consulta_por_coordenadas(datos: ConsultaPorCoordenadas):
    estacion = estacion_mas_cercana(datos.latitud, datos.longitud)
    if not estacion:
        raise HTTPException(status_code=404, detail="No se encontro ninguna estacion cercana")
    return generar_informe(estacion)

@router.post("/consulta/por-distrito", response_model=RespuestaConsulta)
def consulta_por_distrito(datos: ConsultaPorDistrito):
    estaciones = get_estaciones()
    resultado = estaciones.filter(
        (estaciones["departamento"] == datos.departamento.upper()) &
        (estaciones["provincia"] == datos.provincia.upper()) &
        (estaciones["distrito"] == datos.distrito.upper())
    )
    if resultado.is_empty():
        raise HTTPException(status_code=404, detail="Distrito no encontrado en el indice de estaciones")
    estacion = resultado.row(0, named=True)
    return generar_informe(estacion)