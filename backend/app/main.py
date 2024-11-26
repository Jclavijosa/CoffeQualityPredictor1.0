from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.api import api_router
from app.core.config import settings
from app.db.database import engine
from app.db.base_class import Base
from app.db import models

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Predicción de Calidad del Café",
    description="API para predecir los puntos totales de una taza de café basándose en características sensoriales.",
    version="1.0.0",
)

# Configuración de CORS
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # O usa ["*"] para permitir todas las conexiones (no recomendado en producción)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir las rutas de la API
app.include_router(api_router, prefix=settings.API_V1_STR)
