
# ============================================================
# FINPREDICT | FASE II
# VALIDACIÓN LOCAL DEL MODELO
# 1. CARGA DEL ARTEFACTO
# ============================================================

from pathlib import Path
import joblib

# Ubicación del modelo respecto al script
RUTA_BASE = Path(__file__).resolve().parent.parent
RUTA_MODELO = RUTA_BASE / "model" / "finpredict_modelo.joblib"

# Verificar existencia del archivo
assert RUTA_MODELO.is_file(), (
    f"No se encontró el modelo: {RUTA_MODELO}"
)

# Cargar artefacto
artefacto = joblib.load(RUTA_MODELO)

modelo = artefacto["modelo"]
threshold = artefacto["threshold"]
columnas = artefacto["columnas_predictoras"]

print("FINPREDICT | VALIDACIÓN LOCAL")
print("-" * 60)
print(f"Modelo: {type(modelo).__name__}")
print(f"Threshold: {threshold}")
print(f"Variables predictoras: {len(columnas)}")
print(f"Pipeline: {list(modelo.named_steps.keys())}")
print("-" * 60)
print("Carga del artefacto exitosa.")


# ============================================================
# 2. PRUEBA DE INFERENCIA LOCAL
# ============================================================

import pandas as pd
import numpy as np

# Datos sintéticos originales de evaluación
RUTA_DATOS = (
    RUTA_BASE
    / "data"
    / "finpredict_evaluacion_v2.parquet"
)

df_evaluacion = pd.read_parquet(RUTA_DATOS)

# Seleccionar cinco registros para comprobar inferencia
X_prueba = df_evaluacion[columnas].head(5).copy()

# Generar probabilidades con el artefacto exportado
probabilidades = modelo.predict_proba(X_prueba)[:, 1]

# Aplicar threshold operativo
clasificaciones = (probabilidades >= threshold).astype(int)

# Resultados
resultados = pd.DataFrame({
    "probabilidad_incumplimiento": probabilidades,
    "clasificacion": clasificaciones
})

print("\nFINPREDICT | PRUEBA DE INFERENCIA")
print("-" * 60)
print(resultados.to_string(index=False))
print("-" * 60)

# Validaciones
assert len(probabilidades) == 5
assert np.all((probabilidades >= 0) & (probabilidades <= 1))
assert set(clasificaciones).issubset({0, 1})

print("Prueba de inferencia superada.")


# ============================================================
# 3. CONSISTENCIA CON LA ACTIVIDAD 6
# ============================================================
RUTA_PREDICCIONES_ORIGINALES = (
    RUTA_BASE
    / "data"
    / "predicciones_holdout_final.csv"
)


predicciones_originales = pd.read_csv(
    RUTA_PREDICCIONES_ORIGINALES
)

# Verificar que ambos archivos conservan el mismo universo y orden
assert len(predicciones_originales) == len(df_evaluacion)

assert (
    predicciones_originales["id_credito"].to_numpy()
    == df_evaluacion["id_credito"].to_numpy()
).all(), "El orden de los créditos no coincide."

# Inferencia sobre todo el holdout
X_holdout = df_evaluacion[columnas].copy()

probabilidades_actuales = modelo.predict_proba(
    X_holdout
)[:, 1]

probabilidades_originales = (
    predicciones_originales["probabilidad_riesgo"].to_numpy()
)

diferencia_maxima = np.max(
    np.abs(probabilidades_actuales - probabilidades_originales)
)

clasificaciones_actuales = (
    probabilidades_actuales >= threshold
).astype(int)

clasificaciones_originales = (
    predicciones_originales["prediccion_threshold_075"].to_numpy()
)

coincidencia_clasificaciones = np.array_equal(
    clasificaciones_actuales,
    clasificaciones_originales
)

print("\nFINPREDICT | CONSISTENCIA HISTÓRICA")
print("-" * 60)
print(f"Registros comparados: {len(X_holdout):,}")
print(f"Diferencia máxima: {diferencia_maxima:.12f}")
print(f"Clasificaciones idénticas: {coincidencia_clasificaciones}")

assert np.allclose(
    probabilidades_actuales,
    probabilidades_originales,
    rtol=1e-10,
    atol=1e-12
), "Las probabilidades difieren de la Actividad 6."

assert coincidencia_clasificaciones, (
    "Las clasificaciones no coinciden."
)

print("Validación histórica de consistencia superada.")
