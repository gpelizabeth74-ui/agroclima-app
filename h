[1mdiff --git a/app/main.py b/app/main.py[m
[1mindex b4a7568..7262f3a 100644[m
[1m--- a/app/main.py[m
[1m+++ b/app/main.py[m
[36m@@ -1,4 +1,7 @@[m
 from fastapi import FastAPI[m
[32m+[m[32mfrom fastapi.middleware.cors import CORSMiddleware[m
[32m+[m[32mfrom fastapi.staticfiles import StaticFiles[m
[32m+[m[32mfrom fastapi.responses import FileResponse[m
 from contextlib import asynccontextmanager[m
 from app.cache import cargar_datos[m
 from app.index import router as index_router[m
[36m@@ -16,5 +19,19 @@[m [mapp = FastAPI([m
     lifespan=lifespan[m
 )[m
 [m
[32m+[m[32mapp.add_middleware([m
[32m+[m[32m    CORSMiddleware,[m
[32m+[m[32m    allow_origins=["*"],[m
[32m+[m[32m    allow_credentials=True,[m
[32m+[m[32m    allow_methods=["*"],[m
[32m+[m[32m    allow_headers=["*"],[m
[32m+[m[32m)[m
[32m+[m
[32m+[m[32mapp.mount("/static", StaticFiles(directory="static"), name="static")[m
[32m+[m
[32m+[m[32m@app.get("/app")[m
[32m+[m[32mdef frontend():[m
[32m+[m[32m    return FileResponse("static/index.html")[m
[32m+[m
 app.include_router(index_router)[m
 app.include_router(localizacion_router)[m
\ No newline at end of file[m
