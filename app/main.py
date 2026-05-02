from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.cache import cargar_datos
from app.index import router as index_router
from app.localizacion import router as localizacion_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    cargar_datos()
    yield

app = FastAPI(
    title="AgroClima API",
    description="Microservicio de consulta agroclimática para agricultores del Perú",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(index_router)
app.include_router(localizacion_router)