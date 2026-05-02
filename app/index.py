from fastapi import APIRouter
from app.cache import get_estaciones

router = APIRouter()

@router.get("/")
def bienvenida():
    return {
        "servicio": "AgroClima API",
        "version": "1.0.0",
        "descripcion": "Consulta agroclimática para agricultores del Perú",
        "estado": "activo",
        "endpoints": {
            "consulta por coordenadas": "/consulta/por-coordenadas",
            "consulta por distrito": "/consulta/por-distrito",
            "lista de estaciones": "/estaciones"
        }
    }

@router.get("/estaciones")
def listar_estaciones(departamento: str = None, provincia: str = None):
    estaciones = get_estaciones()

    if departamento:
        estaciones = estaciones.filter(
            estaciones["departamento"] == departamento.upper()
        )

    if provincia:
        estaciones = estaciones.filter(
            estaciones["provincia"] == provincia.upper()
        )

    return estaciones.to_dicts()