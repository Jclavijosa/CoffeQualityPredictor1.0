# app/core/config.py

from pydantic import BaseSettings

class Settings(BaseSettings):
    # Configuraciones de la aplicación
    APP_NAME: str = "Wine Quality Predictor API"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "Zimoi2024*"  # Cambia esto por una clave secreta segura
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Configuraciones de la base de datos
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///./sql_app.db"

    # Configuraciones del modelo
    MODEL_PATH: str = "models/wine_quality_model.pkl"
    SCALER_PATH: str = "models/scaler.pkl"

    class Config:
        case_sensitive = True

settings = Settings()
