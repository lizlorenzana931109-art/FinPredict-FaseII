
# ============================================================
# FINPREDICT | FASE II
# API DE INFERENCIA
# ============================================================

from fastapi import FastAPI

from pathlib import Path
import joblib
import pandas as pd
from api.schemas import SolicitudPrediccion
from fastapi import HTTPException
from scripts.validar_entradas import validar_restricciones_financieras

# Ubicación del artefacto entrenado
RUTA_BASE = Path(__file__).resolve().parent.parent
RUTA_MODELO = RUTA_BASE / "model" / "finpredict_modelo.joblib"

# Recuperar modelo y configuración
artefacto = joblib.load(RUTA_MODELO)

modelo = artefacto["modelo"]
threshold = artefacto["threshold"]
columnas_predictoras = artefacto["columnas_predictoras"]

# Inicialización de la aplicación
app = FastAPI(
    title="FinPredict API",
    description=(
        "Servicio de inferencia para la predicción "
        "preventiva de incumplimiento hipotecario."
    ),
    version="1.0.0"
)


# ============================================================
# 1. ENDPOINT DE SALUD
# ============================================================

@app.get("/health", tags=["Monitoreo"])
def verificar_salud():
    """Verifica que el servicio HTTP esté disponible."""

    return {
        "servicio": "FinPredict API",
        "estado": "operativo",
        "version": "1.0.0"
    }


# ============================================================
# 2. ENDPOINT DE PREDICCIÓN
# ============================================================

@app.post("/predict", tags=["Predicción"])
def predecir_incumplimiento(
    solicitud: SolicitudPrediccion
):
    """
    Genera una probabilidad de incumplimiento
    utilizando el modelo previamente entrenado.
    """

    # Recuperar los datos recibidos
    datos = solicitud.model_dump()
    
    # Validar restricciones financieras antes de predecir
    try:
        validar_restricciones_financieras(datos)
    except ValueError as error:
        raise HTTPException(
        status_code=422,
        detail=str(error)
    ) from error

    # Construir el registro con el orden original
    # de las 15 variables predictoras
    X = pd.DataFrame(
        [datos],
        columns=columnas_predictoras
    )

    # Realizar inferencia
    probabilidad = float(
        modelo.predict_proba(X)[0, 1]
    )

    # Aplicar el umbral operativo
    clasificacion = int(
        probabilidad >= threshold
    )

    return {
        "probabilidad_incumplimiento": round(
            probabilidad, 6
        ),
        "clasificacion": clasificacion,
        "nivel_riesgo": (
            "ALTO" if clasificacion == 1
            else "BAJO"
        ),
        "threshold": threshold,
        "version_modelo": artefacto["version"]
    }
