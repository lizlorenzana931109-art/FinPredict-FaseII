
# ============================================================
# FINPREDICT | FASE II
# VALIDACIÓN DE CASOS EXTREMOS
# 1. SELECCIÓN DE ESCENARIOS
# ============================================================

from pathlib import Path
import joblib
import pandas as pd

RUTA_BASE = Path(__file__).resolve().parent.parent
RUTA_DATOS = RUTA_BASE / "data"


# Cargar modelo entrenado
artefacto = joblib.load(
    RUTA_BASE / "model" / "finpredict_modelo.joblib"
)

modelo = artefacto["modelo"]
threshold = artefacto["threshold"]
columnas = artefacto["columnas_predictoras"]

# Cargar datos sintéticos de evaluación
df = pd.read_parquet(
    RUTA_DATOS / "finpredict_evaluacion_v2.parquet"
)

# Cargar datos sintéticos de desarrollo
df_desarrollo = pd.read_parquet(
    RUTA_DATOS / "finpredict_desarrollo_v2.parquet"
)

# Seleccionar registros completos sin alterar sus variables
escenarios = {
    "Sin atraso": df.loc[df["dias_atraso"] == 0].head(1),
    "Atraso máximo": df.loc[df["dias_atraso"] == 60].head(1),
    "Sin pagos recientes": df_desarrollo.loc[
        df_desarrollo["importe_pagado_3m"] == 0
    ].head(1),
    "Ingreso mínimo": df.nsmallest(1, "ingreso_mensual"),
    "Saldo vencido máximo": df.nlargest(1, "saldo_vencido")
}

registros = []

for nombre, muestra in escenarios.items():
    if muestra.empty:
        print(f"Escenario sin registros: {nombre}")
        continue

    registro = muestra.iloc[0]

    registros.append({
        "Escenario": nombre,
        "Días atraso": int(registro["dias_atraso"]),
        "Ingreso mensual": registro["ingreso_mensual"],
        "Saldo vencido": registro["saldo_vencido"],
        "Pagado 3m": registro["importe_pagado_3m"]
    })

resumen = pd.DataFrame(registros)

print("FINPREDICT | ESCENARIOS SELECCIONADOS")
print("-" * 90)

print(
    resumen.to_string(
        index=False,
        formatters={
            "Ingreso mensual": "{:,.2f}".format,
            "Saldo vencido": "{:,.2f}".format,
            "Pagado 3m": "{:,.2f}".format
        }
    )
)

print("-" * 90)
print(f"Escenarios encontrados: {len(resumen)} de 5")


# ============================================================
# 2. INFERENCIA SOBRE ESCENARIOS EXTREMOS
# ============================================================

resultados = []

for nombre, muestra in escenarios.items():
    if muestra.empty:
        continue

    # Conservar las 15 variables y su orden original
    X = muestra[columnas].copy()

    # Inferencia con el modelo entrenado
    probabilidad = float(modelo.predict_proba(X)[0, 1])
    clasificacion = int(probabilidad >= threshold)

    resultados.append({
        "Escenario": nombre,
        "Probabilidad": probabilidad,
        "Clasificación": clasificacion,
        "Resultado": (
            "RIESGO ALTO" if clasificacion == 1
            else "RIESGO BAJO"
        )
    })

df_resultados = pd.DataFrame(resultados)

print("\nFINPREDICT | INFERENCIA DE CASOS EXTREMOS")
print("-" * 90)

print(
    df_resultados.to_string(
        index=False,
        formatters={
            "Probabilidad": "{:.2%}".format
        }
    )
)

print("-" * 90)
print(f"Threshold operativo: {threshold:.0%}")
print(f"Escenarios evaluados: {len(df_resultados)} de 5")


# ============================================================
# 3. VALIDACIONES AUTOMÁTICAS
# ============================================================

import numpy as np

assert len(df_resultados) == 5, (
    "No se evaluaron los cinco escenarios esperados."
)

assert np.isfinite(df_resultados["Probabilidad"]).all(), (
    "Se detectaron probabilidades no finitas."
)

assert df_resultados["Probabilidad"].between(0, 1).all(), (
    "Se detectaron probabilidades fuera del rango [0, 1]."
)

assert df_resultados["Clasificación"].isin([0, 1]).all(), (
    "Se detectaron clasificaciones inválidas."
)

assert (
    df_resultados["Clasificación"].to_numpy()
    == (
        df_resultados["Probabilidad"].to_numpy() >= threshold
    ).astype(int)
).all(), "Las clasificaciones no coinciden con el threshold."

print("\nFINPREDICT | VALIDACIONES AUTOMÁTICAS")
print("-" * 60)
print("Cantidad de escenarios: CORRECTA")
print("Probabilidades finitas: CORRECTAS")
print("Probabilidades entre 0 y 1: CORRECTAS")
print("Clasificaciones binarias: CORRECTAS")
print("Aplicación del threshold: CORRECTA")
print("-" * 60)
print("RESULTADO: 5 DE 5 VALIDACIONES SUPERADAS")

