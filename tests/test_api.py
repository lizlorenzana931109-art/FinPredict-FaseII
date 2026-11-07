
# ============================================================
# FINPREDICT | FASE II
# PRUEBAS AUTOMATIZADAS DE LA API
# ============================================================

from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


# ============================================================
# 1. REGISTRO SINTÉTICO DE REFERENCIA
# ============================================================

# Primer registro del holdout utilizado en Swagger.
# No contiene información de clientes reales.

CREDITO_VALIDO = {
    "monto_original": 4784933.89,
    "plazo_meses": 360,
    "tasa_interes_anual": 10.34,
    "pago_mensual": 43198.32,
    "ingreso_mensual": 143552.49,
    "antiguedad_meses": 51,
    "saldo_vencido": 10551.63,
    "dias_atraso": 18,
    "relacion_pago_ingreso": 0.3009235158512402,
    "saldo_vencido_mensualidades": 0.24426019345196756,
    "importe_pagado_3m": 122220.61,
    "numero_pagos_3m": 4,
    "importe_exigible_3m": 129594.95999999999,
    "obligaciones_3m": 3,
    "porcentaje_pago_3m": 0.9430969383377256,
}


# ============================================================
# 2. DISPONIBILIDAD DE LA API
# ============================================================

def test_health():
    respuesta = client.get("/health")

    assert respuesta.status_code == 200
    assert respuesta.json()["estado"] == "operativo"


# ============================================================
# 3. PREDICCIÓN VÁLIDA
# ============================================================

def test_prediccion_valida():
    respuesta = client.post("/predict", json=CREDITO_VALIDO)

    assert respuesta.status_code == 200

    resultado = respuesta.json()

    assert abs(
        resultado["probabilidad_incumplimiento"] - 0.054075
    ) < 0.000001

    assert resultado["clasificacion"] == 0
    assert resultado["nivel_riesgo"] == "BAJO"
    assert resultado["threshold"] == 0.75


# ============================================================
# 4. INGRESO MENSUAL NEGATIVO
# ============================================================

def test_ingreso_negativo():
    datos = CREDITO_VALIDO.copy()
    datos["ingreso_mensual"] = -1000.0

    respuesta = client.post("/predict", json=datos)

    assert respuesta.status_code == 422
    assert respuesta.json()["detail"] == (
        "Valor no positivo: ingreso_mensual"
    )


# ============================================================
# 5. CAMPO OBLIGATORIO FALTANTE
# ============================================================

def test_campo_faltante():
    datos = CREDITO_VALIDO.copy()
    datos.pop("dias_atraso")

    respuesta = client.post("/predict", json=datos)

    assert respuesta.status_code == 422

    errores = respuesta.json()["detail"]

    assert any(
        error["loc"][-1] == "dias_atraso"
        and error["type"] == "missing"
        for error in errores
    )


# ============================================================
# 6. TIPO DE DATO INCORRECTO
# ============================================================

def test_tipo_incorrecto():
    datos = CREDITO_VALIDO.copy()
    datos["dias_atraso"] = "dieciocho"

    respuesta = client.post("/predict", json=datos)

    assert respuesta.status_code == 422

    errores = respuesta.json()["detail"]

    assert any(
        error["loc"][-1] == "dias_atraso"
        and error["type"] == "int_type"
        for error in errores
    )
