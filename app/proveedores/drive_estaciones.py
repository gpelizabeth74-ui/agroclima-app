import polars as pl
import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account
import io

def leer_estaciones() -> pl.DataFrame:
    DRIVE_ID = os.getenv("DRIVE_ID_ESTACIONES")
    credenciales = service_account.Credentials.from_service_account_file(
        "credenciales_drive.json",
        scopes=["https://www.googleapis.com/auth/drive.readonly"]
    )
    servicio = build("drive", "v3", credentials=credenciales)
    request = servicio.files().get_media(fileId=DRIVE_ID)
    buffer = io.BytesIO()
    downloader = MediaIoBaseDownload(buffer, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    buffer.seek(0)
    return pl.read_csv(buffer)