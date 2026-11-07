
# ============================================================
# FINPREDICT | FASE II
# ESQUEMAS DE ENTRADA DE LA API
# ============================================================

from pydantic import BaseModel, ConfigDict, StrictFloat, StrictInt


class SolicitudPrediccion(BaseModel):
    """Variables requeridas para evaluar un crédito."""

    model_config = ConfigDict(extra="forbid")

    monto_original: StrictFloat
    plazo_meses: StrictInt
    tasa_interes_anual: StrictFloat
    pago_mensual: StrictFloat
    ingreso_mensual: StrictFloat
    antiguedad_meses: StrictInt
    saldo_vencido: StrictFloat
    dias_atraso: StrictInt
    relacion_pago_ingreso: StrictFloat
    saldo_vencido_mensualidades: StrictFloat
    importe_pagado_3m: StrictFloat
    numero_pagos_3m: StrictInt
    importe_exigible_3m: StrictFloat
    obligaciones_3m: StrictInt
    porcentaje_pago_3m: StrictFloat
