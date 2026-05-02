from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/app")
def frontend():
    return FileResponse("static/index.html")

app.include_router(index_router)
app.include_router(localizacion_router)