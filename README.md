# AgroClima - Microservicio de Consulta Agroclimática

Sistema de consulta agroclimática para agricultores del Perú. Cruza datos históricos de clima (PISCOP, SENAMHI), datos de producción agrícola (SISAGRI) y clima en tiempo real (Open-Meteo) para generar consejos prácticos por distrito.

---

## Tabla de Contenidos

1. [Principios del Proyecto](#1-principios-del-proyecto)
2. [Estructura del Repositorio](#2-estructura-del-repositorio)
3. [Arquitectura General](#3-arquitectura-general)
4. [Fuentes de Datos](#4-fuentes-de-datos)
5. [Estructura de los Archivos Maestros](#5-estructura-de-los-archivos-maestros)
6. [Instalación y Configuración](#6-instalación-y-configuración)
7. [Variables de Entorno](#7-variables-de-entorno)
8. [Cómo Correr el Servicio](#8-cómo-correr-el-servicio)
9. [Endpoints Disponibles](#9-endpoints-disponibles)
10. [Flujo de una Consulta](#10-flujo-de-una-consulta)
11. [Escalabilidad](#11-escalabilidad)
12. [Equipo y Responsabilidades](#12-equipo-y-responsabilidades)
13. [Roadmap](#13-roadmap)

---

## 1. Principios del Proyecto

**Lenguaje directo**: La interfaz no usa tecnicismos. Los datos numéricos se traducen en consejos prácticos para el agricultor.

**Sin emojis ni animaciones**: La interfaz de consulta es texto limpio y estructurado.

**Privacidad de la data**: Los archivos maestros procesados (Parquet) viven en Google Drive privado y no se suben al repositorio. El repositorio solo contiene código y datos ficticios de ejemplo para desarrollo.

**Escalabilidad modular**: Añadir un nuevo dominio de datos (Suelos, Precios, Telemetría) solo requiere subir un nuevo Parquet al Drive y registrar su lector en `proveedores/`. No se reescribe el núcleo del sistema.

**100% gratuito y Open Source**: FastAPI, Polars, xarray, Open-Meteo. Sin costos de infraestructura ni licencias.

---

## 2. Estructura del Repositorio

```
agroclima-app/
│
├── app/
│   ├── main.py                  # Punto de entrada FastAPI, arranque y cache
│   ├── index.py                 # Rutas de bienvenida y documentación de la API
│   ├── cache.py                 # Carga única de Parquet al iniciar el servicio
│   ├── localizacion.py          # Motor de búsqueda: GPS, nombre de lugar, mapa
│   ├── esquemas.py              # Modelos Pydantic de entrada y salida
│   │
│   ├── motores/
│   │   ├── alertas.py           # Generador de semáforo y consejos en lenguaje simple
│   │   └── comparador.py        # Cruce de dato histórico vs. dato actual
│   │
│   └── proveedores/
│       ├── drive_estaciones.py  # Lector del Índice de Estaciones desde Drive
│       ├── drive_clima.py       # Lector del Maestro Clima (PISCOP + SENAMHI)
│       ├── drive_agro.py        # Lector del Maestro Agro (SISAGRI)
│       ├── drive_extras.py      # Lector de capas futuras: Suelos, Ecosistemas
│       └── api_tiempo_real.py   # Conexión a Open-Meteo (clima de hoy)
│
├── notebooks/
│   ├── 01_validar_estaciones.ipynb   # Revisión del índice de estaciones
│   ├── 02_procesar_piscop.ipynb      # Conversión NC a Parquet por estación
│   ├── 03_validar_sisagri.ipynb      # Limpieza y validación del maestro agro
│   └── 04_generar_datos_ficticios.ipynb  # Generación de data de prueba
│
├── data_ficticia/
│   ├── estaciones_ficticio.csv       # Índice de estaciones de prueba
│   ├── clima_ficticio.parquet        # Clima histórico ficticio
│   └── sisagri_ficticio.parquet      # Producción agrícola ficticia
│
├── static/
│   └── peru_distritos.geojson        # GeoJSON de distritos del Perú para el mapa
│
├── frontend/
│   └── index.html                    # Interfaz básica de consulta (GitHub Pages)
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 3. Arquitectura General

```
AGRICULTOR
    |
    | (GPS / nombre de lugar / clic en mapa)
    v
[Frontend - GitHub Pages]
    |
    | HTTP request
    v
[FastAPI - GitHub Codespaces]
    |
    |-- cache.py (datos ya en memoria RAM)
    |       |-- Maestro Clima (Parquet, Drive)
    |       |-- Maestro Agro  (Parquet, Drive)
    |       |-- Índice Estaciones (Parquet, Drive)
    |
    |-- api_tiempo_real.py
    |       |-- Open-Meteo (clima de hoy, sin API key)
    |
    |-- motores/comparador.py
    |       |-- Cruza histórico vs. actual
    |
    |-- motores/alertas.py
            |-- Genera semáforo y consejo
    |
    v
RESPUESTA AL AGRICULTOR
    - Semáforo de situación actual
    - Contexto histórico del distrito
    - Realidad agrícola (cultivos, rendimiento)
    - Consejo técnico en lenguaje simple
```

**Principio clave de rendimiento**: Los archivos Parquet se cargan desde Drive una sola vez al arrancar el servicio, no en cada consulta. Todas las consultas leen desde memoria RAM.

---

## 4. Fuentes de Datos

| Fuente | Tipo | Periodo | Variables | Estado |
|--------|------|---------|-----------|--------|
| PISCOP | NetCDF (.nc) | 1981 - 2016 | PET, Prec, Tmax, Tmin | En procesamiento |
| SENAMHI | CSV / Excel | 2017 - 2025 | Temp, Humedad, Precipitación | En procesamiento |
| SISAGRI | Excel / CSV | 2016 - 2025 | Cultivo, Producción, Cosecha, Precio | Listo |
| Open-Meteo | API REST | Tiempo real | Temp, Humedad, Precipitación, Viento | Sin clave, gratuito |
| Índice Estaciones | CSV | Estático | Cod, Nombre, Dpto, Prov, Dist, Altitud, Lat, Lon | Listo |

### Pipeline de procesamiento (fuera del repositorio)

Los archivos PISCOP en formato NetCDF (.nc) se procesan localmente con xarray y Polars:

```
NC por variable (pet, prec, tmax, tmin)
    |
    | xarray: extracción por punto lat/lon del índice de estaciones
    v
DataFrame con columnas: cod_estacion, fecha, pet, prec, tmax, tmin
    |
    | Polars: merge con SENAMHI 2017-2025
    v
Maestro Clima consolidado (1981-2025)
    |
    | Exportar a Parquet
    v
Google Drive privado (no en GitHub)
```

---

## 5. Estructura de los Archivos Maestros

### Índice de Estaciones

```
cod_estacion | categoria | nombre_estacion | departamento | provincia | distrito | altitud_msnm | latitud | longitud
```

### Maestro Clima (Parquet en Drive)

```
cod_estacion | nombre | departamento | provincia | distrito | altitud_msnm | fecha | temp_max_C | temp_min_C | hum_relativa | pc_precipitacion_mm
```

### Maestro Agro SISAGRI (Parquet en Drive)

```
anho | mes | COD_UBIGEO | Dpto | Prov | Dist | dsc_Cultivo | PRODUCCION_t | COSECHA_ha | MTO_PRECCHAC_soles_kg
```

---

## 6. Instalación y Configuración

### Requisitos

- Python 3.11 o superior
- Cuenta de Google con acceso al Drive donde viven los Parquet

### Instalación

```bash
git clone https://github.com/tu-usuario/agroclima-app.git
cd agroclima-app
pip install -r requirements.txt
```

### requirements.txt

```
fastapi==0.111.0
uvicorn==0.29.0
polars==0.20.31
xarray==2024.3.0
netCDF4==1.7.1
geopandas==0.14.4
httpx==0.27.0
google-auth==2.29.0
google-api-python-client==2.128.0
python-dotenv==1.0.1
pydantic==2.7.1
```

---

## 7. Variables de Entorno

Crear un archivo `.env` en la raíz del proyecto. Este archivo está bloqueado en `.gitignore` y nunca se sube al repositorio.

```env
# ID de los archivos en Google Drive (se obtiene de la URL del archivo)
DRIVE_ID_ESTACIONES=1ABC...xyz
DRIVE_ID_CLIMA=1DEF...xyz
DRIVE_ID_AGRO=1GHI...xyz

# Modo de datos: "real" usa Drive, "ficticio" usa data_ficticia/
MODO_DATOS=ficticio
```

Cuando `MODO_DATOS=ficticio`, el sistema carga los archivos de la carpeta `data_ficticia/` en lugar de conectarse a Drive. Ideal para desarrollo y pruebas del equipo.

---

## 8. Cómo Correr el Servicio

### Modo local

```bash
uvicorn app.main:app --reload --port 8000
```

La API queda disponible en `http://localhost:8000`  
La documentación automática en `http://localhost:8000/docs`

### Modo Codespaces (para demo o entrega)

1. Abrir el repositorio en GitHub Codespaces.
2. Configurar el archivo `.env` con las credenciales de Drive.
3. Correr el comando de uvicorn.
4. GitHub genera una URL pública automáticamente.
5. Actualizar esa URL en el frontend antes de la demo.

---

## 9. Endpoints Disponibles

### GET /
Bienvenida y estado del servicio.

### GET /estaciones
Lista de estaciones disponibles. Útil para poblar el selector del frontend.

**Parámetros opcionales:**
- `departamento`: filtra por departamento
- `provincia`: filtra por provincia

### POST /consulta/por-coordenadas
Recibe latitud y longitud, identifica la estación más cercana y devuelve el informe completo.

**Body:**
```json
{
  "latitud": -6.7714,
  "longitud": -79.8409
}
```

### POST /consulta/por-distrito
Recibe nombre de distrito y devuelve el informe completo.

**Body:**
```json
{
  "departamento": "LAMBAYEQUE",
  "provincia": "CHICLAYO",
  "distrito": "CHICLAYO"
}
```

### Respuesta estándar de consulta

```json
{
  "distrito": "CHICLAYO",
  "estacion_referencia": "CHICLAYO",
  "fecha_consulta": "2025-07-15",
  "semaforo": "AMARILLO",
  "clima_hoy": {
    "temp_max": 28.4,
    "temp_min": 19.1,
    "precipitacion_mm": 0.0,
    "humedad_relativa": 72
  },
  "contexto_historico": {
    "temp_max_promedio_historico": 27.8,
    "precipitacion_promedio_historico": 1.2,
    "comparacion": "Temperatura dentro del rango normal. Sin lluvias previstas."
  },
  "realidad_agricola": [
    {
      "cultivo": "ARROZ",
      "produccion_t": 4520.5,
      "cosecha_ha": 980.0,
      "precio_soles_kg": 1.45
    }
  ],
  "consejo": "Las temperaturas son normales para la época. La humedad está elevada. Revise sus cultivos por presencia de hongos en hojas bajas."
}
```

---

## 10. Flujo de una Consulta

```
1. El agricultor ingresa su ubicación (GPS, nombre o mapa)
2. El frontend envía las coordenadas o el nombre de distrito a la API
3. localizacion.py identifica la estación más cercana usando el índice (Haversine)
4. cache.py entrega el histórico de esa estación desde memoria (Polars)
5. api_tiempo_real.py consulta Open-Meteo con las coordenadas de la estación
6. comparador.py cruza histórico vs. dato de hoy
7. alertas.py genera el semáforo y el consejo en lenguaje simple
8. La API responde con el JSON estructurado
9. El frontend muestra el informe al agricultor
```

---

## 11. Escalabilidad

El sistema está diseñado para crecer sin reescribir el núcleo:

**Añadir un nuevo dominio de datos** (Suelos, Precios de mercado, Fenología):
1. Procesar la data localmente y exportar a Parquet.
2. Subir el Parquet al Drive.
3. Crear un nuevo lector en `proveedores/drive_nuevo.py`.
4. Registrar la carga en `cache.py`.
5. Añadir el nuevo campo en `esquemas.py` y en `alertas.py`.

**El resto del sistema no se toca.**

**Añadir modo offline** (futuro):
- Los datos históricos ya están en memoria.
- Solo el clima de tiempo real (Open-Meteo) requiere conexión.
- Si no hay conexión, el sistema responde con histórico y lo indica al agricultor.

---

## 12. Equipo y Responsabilidades

| Rol | Archivos principales | Acceso a data real |
|-----|---------------------|-------------------|
| Arquitectura e Integración | main.py, cache.py, esquemas.py | Si |
| Calidad de Datos | notebooks/ | Solo datos ficticios |
| Motor de Alertas | motores/alertas.py, motores/comparador.py | Solo datos ficticios |
| Frontend y Testing | frontend/index.html, endpoints GET | Solo datos ficticios |

El equipo de desarrollo trabaja siempre con `MODO_DATOS=ficticio`. Solo el responsable de integración activa `MODO_DATOS=real` para validaciones finales.

---

## 13. Roadmap

**Version 1.0 - Actual**
- Consulta por GPS, nombre de distrito y mapa
- Histórico PISCOP 1981-2016 + SENAMHI 2017-2025
- Datos agrícolas SISAGRI 2016-2025
- Clima en tiempo real Open-Meteo
- Interfaz básica GitHub Pages
- Semáforo y consejo en lenguaje simple

**Version 1.1 - Siguiente**
- Capa de suelos por distrito
- Precios de mercado por cultivo
- Historial de consultas del agricultor

**Version 2.0 - Futuro**
- Modo offline: respuesta con histórico sin conexión a internet
- Consejo generado por modelo de lenguaje (Groq/Llama gratuito)
- Soporte para múltiples idiomas (quechua)
- Alertas automáticas por SMS o WhatsApp

---

## Notas Técnicas

**Por qué Polars y no Pandas**: Los archivos históricos de 40 años tienen peso considerable. Polars es entre 5 y 20 veces más rápido que Pandas para lectura y filtrado de Parquet, especialmente con columnas de fecha.

**Por qué Parquet y no CSV**: Parquet comprime los datos entre 5 y 10 veces más que CSV y permite leer solo las columnas necesarias sin cargar el archivo completo. Para 40 años de datos por estación, la diferencia es significativa.

**Por qué Open-Meteo y no otras APIs**: Es completamente gratuito, sin API key, sin límite de requests razonable, y tiene cobertura completa para Perú con datos horarios.

**Por qué carga en memoria al arrancar**: Leer un Parquet desde Google Drive en cada consulta introduce una latencia de 2 a 5 segundos por request. Cargando al arrancar, la latencia baja a milisegundos para todas las consultas posteriores.

---

*Proyecto desarrollado durante prácticas profesionales. Data histórica propietaria no incluida en el repositorio.*
