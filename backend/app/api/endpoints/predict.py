from fastapi import APIRouter, HTTPException
from app.schemas.predict import PredictionInput, PredictionOutput
import joblib
import os
import numpy as np
import pandas as pd

router = APIRouter()

# Obtener la ruta absoluta del directorio base del proyecto
current_dir = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(current_dir, "../../.."))

# Rutas a los archivos necesarios
model_path = os.path.join(BASE_DIR, 'models', 'cafe_quality_model.pkl')
scaler_path = os.path.join(BASE_DIR, 'models', 'scaler.pkl')
feature_order_path = os.path.join(BASE_DIR, 'models', 'feature_order.pkl')
label_encoder_path = os.path.join(BASE_DIR, 'models', 'label_encoder.pkl')

# Cargar el modelo, el escalador, el orden de las características y el codificador de etiquetas al iniciar
try:
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    feature_order = joblib.load(feature_order_path)
    label_encoder = joblib.load(label_encoder_path)
except Exception as e:
    model = None
    scaler = None
    feature_order = None
    label_encoder = None
    print(f"Error al cargar los archivos necesarios: {e}")

@router.post("/", response_model=PredictionOutput)
def predict(input_data: PredictionInput):
    if None in (model, scaler, feature_order, label_encoder):
        raise HTTPException(status_code=500, detail="No se pudieron cargar los archivos necesarios para la predicción.")

    # Construir el vector de características en el orden correcto
    try:
        input_features_dict = input_data.dict()

        # Ordenar las características según 'feature_order'
        input_features = [input_features_dict[feature] for feature in feature_order]
        input_features_df = pd.DataFrame([input_features], columns=feature_order)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al construir las características de entrada: {e}")

    # Escalar las características de entrada
    try:
        input_features_scaled = scaler.transform(input_features_df)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al escalar las características: {e}")

    # Realizar la predicción
    try:
        prediction_encoded = model.predict(input_features_scaled)[0]
        calidad = label_encoder.inverse_transform([prediction_encoded])[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al realizar la predicción: {e}")

    # Devolver la predicción
    return PredictionOutput(calidad=calidad)
