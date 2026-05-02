from pydantic import BaseModel
from typing import Optional, List

# Entradas

class ConsultaPorCoordenadas(BaseModel):
    latitud: float
    longitud: float

class ConsultaPorDistrito(BaseModel):
    departamento: str
    provincia: str
    distrito: str

# Salidas

class ClimaHoy(BaseModel):
    temp_max: float
    temp_min: float
    precipitacion_mm: float
    humedad_relativa: float

class ContextoHistorico(BaseModel):
    temp_max_promedio_historico: float
    precipitacion_promedio_historico: float
    comparacion: str

class RealidadAgricola(BaseModel):
    cultivo: str
    produccion_t: float
    cosecha_ha: float
    precio_soles_kg: float

class RespuestaConsulta(BaseModel):
    distrito: str
    estacion_referencia: str
    fecha_consulta: str
    semaforo: str
    clima_hoy: ClimaHoy
    contexto_historico: ContextoHistorico
    realidad_agricola: List[RealidadAgricola]
    consejo: str