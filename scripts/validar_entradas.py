

# ============================================================
# FINPREDICT | FASE II
# VALIDACIÓN DE ENTRADAS
# ============================================================

from pathlib import Path
from numbers import Real
import math
import joblib


# ============================================================
# 1. CONFIGURACIÓN DEL MODELO
# ============================================================

RUTA_BASE = Path(__file__).resolve().parent.parent
RUTA_MODELO = RUTA_BASE / "model" / "finpredict_modelo.joblib"

# Recuperar las variables requeridas por el modelo
artefacto = joblib.load(RUTA_MODELO)
columnas_requeridas = artefacto["columnas_predictoras"]


# ============================================================
# 2. VALIDACIÓN DE CAMPOS OBLIGATORIOS
# ============================================================

def validar_campos_obligatorios(datos):
    """Comprueba que estén presentes las 15 variables."""

    if not isinstance(datos, dict):
        raise ValueError(
            "La entrada debe ser un diccionario de variables."
        )

    faltantes = [
        columna
        for columna in columnas_requeridas
        if columna not in datos
    ]

    if faltantes:
        raise ValueError(
            "Faltan variables obligatorias: "
            + ", ".join(faltantes)
        )

    return True


# ============================================================
# 3. VALIDACIÓN DE TIPOS Y VALORES NUMÉRICOS
# ============================================================

def validar_valores_numericos(datos):
    """Exige números reales finitos en las 15 variables."""

    validar_campos_obligatorios(datos)

    for columna in columnas_requeridas:
        valor = datos[columna]

        if (
            isinstance(valor, bool)
            or not isinstance(valor, Real)
            or not math.isfinite(valor)
        ):
            raise ValueError(
                f"Valor numérico inválido en: {columna}"
            )

    return True


# ============================================================
# 4. VALIDACIÓN DE RESTRICCIONES FINANCIERAS
# ============================================================

def validar_restricciones_financieras(datos):
    """Comprueba restricciones básicas de las variables."""

    validar_valores_numericos(datos)

    # Variables que no pueden tomar valores negativos
    variables_no_negativas = [
        "saldo_vencido",
        "dias_atraso",
        "saldo_vencido_mensualidades",
        "importe_pagado_3m",
        "numero_pagos_3m",
        "importe_exigible_3m",
        "relacion_pago_ingreso",
        "porcentaje_pago_3m",
    ]

    for columna in variables_no_negativas:
        if datos[columna] < 0:
            raise ValueError(
                f"Valor negativo no permitido: {columna}"
            )

    # Variables que deben ser estrictamente positivas
    variables_positivas = [
        "monto_original",
        "plazo_meses",
        "tasa_interes_anual",
        "pago_mensual",
        "ingreso_mensual",
        "antiguedad_meses",
        "obligaciones_3m",
    ]

    for columna in variables_positivas:
        if datos[columna] <= 0:
            raise ValueError(
                f"Valor no positivo: {columna}"
            )

    return True


# ============================================================
# 5. PRUEBAS AUTOMÁTICAS
# ============================================================

def ejecutar_pruebas():
    """Ejecuta las 15 pruebas locales de validación."""

    # Entrada completa para probar reglas individuales.
    # No representa un crédito financieramente real.
    entrada_completa = {
        columna: 1.0 for columna in columnas_requeridas
    }

    # --------------------------------------------------------
    # 5.1 CAMPOS OBLIGATORIOS
    # --------------------------------------------------------

    assert validar_campos_obligatorios(entrada_completa)

    entrada_incompleta = entrada_completa.copy()
    entrada_incompleta.pop("dias_atraso")

    try:
        validar_campos_obligatorios(entrada_incompleta)
    except ValueError as error:
        assert "dias_atraso" in str(error)
        print("Campo faltante detectado correctamente.")
    else:
        raise AssertionError(
            "No se rechazó una entrada incompleta."
        )

    try:
        validar_campos_obligatorios([1, 2, 3])
    except ValueError:
        print("Estructura de entrada inválida detectada.")
    else:
        raise AssertionError(
            "No se rechazó una estructura inválida."
        )

    print("\nFINPREDICT | VALIDACIÓN DE CAMPOS")
    print("-" * 60)
    print(f"Variables obligatorias: {len(columnas_requeridas)}")
    print("Entrada completa: CORRECTA")
    print("Campo faltante: RECHAZADO")
    print("Estructura inválida: RECHAZADA")
    print("-" * 60)
    print("RESULTADO: 3 DE 3 PRUEBAS SUPERADAS")

    # --------------------------------------------------------
    # 5.2 TIPOS Y VALORES NUMÉRICOS
    # --------------------------------------------------------

    casos_invalidos = {
        "Texto": {"dias_atraso": "treinta"},
        "Nulo": {"ingreso_mensual": None},
        "NaN": {"saldo_vencido": float("nan")},
        "Infinito": {"monto_original": float("inf")},
        "Booleano": {"dias_atraso": True},
    }

    print("\nFINPREDICT | VALIDACIÓN NUMÉRICA")
    print("-" * 60)

    assert validar_valores_numericos(entrada_completa)
    print("Entrada numérica completa: ACEPTADA")

    for nombre, cambio in casos_invalidos.items():
        entrada_prueba = entrada_completa.copy()
        entrada_prueba.update(cambio)

        try:
            validar_valores_numericos(entrada_prueba)
        except ValueError:
            print(f"{nombre}: RECHAZADO CORRECTAMENTE")
        else:
            raise AssertionError(
                f"El caso {nombre} no fue rechazado."
            )

    print("-" * 60)
    print(
        "RESULTADO: 6 DE 6 PRUEBAS NUMÉRICAS SUPERADAS"
    )

    # --------------------------------------------------------
    # 5.3 RESTRICCIONES FINANCIERAS
    # --------------------------------------------------------

    casos_financieros_invalidos = {
        "Saldo vencido negativo": {"saldo_vencido": -100.0},
        "Días de atraso negativos": {"dias_atraso": -5},
        "Monto original cero": {"monto_original": 0.0},
        "Ingreso mensual negativo": {
            "ingreso_mensual": -1000.0
        },
        "Plazo cero": {"plazo_meses": 0},
    }

    print("\nFINPREDICT | RESTRICCIONES FINANCIERAS")
    print("-" * 60)

    assert validar_restricciones_financieras(entrada_completa)
    print("Estructura financiera de prueba: ACEPTADA")

    for nombre, cambio in casos_financieros_invalidos.items():
        entrada_prueba = entrada_completa.copy()
        entrada_prueba.update(cambio)

        try:
            validar_restricciones_financieras(entrada_prueba)
        except ValueError:
            print(f"{nombre}: RECHAZADO CORRECTAMENTE")
        else:
            raise AssertionError(
                f"El caso {nombre} no fue rechazado."
            )

    print("-" * 60)
    print(
        "RESULTADO: 6 DE 6 PRUEBAS FINANCIERAS SUPERADAS"
    )


# ============================================================
# 6. PUNTO DE EJECUCIÓN
# ============================================================

if __name__ == "__main__":
    ejecutar_pruebas()
