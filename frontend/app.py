

# ============================================================
# FINPREDICT | FASE II
# FRONTEND STREAMLIT
# Identidad visual corporativa
# ============================================================

from decimal import Decimal, InvalidOperation

import requests
import streamlit as st

import os


# ============================================================
# 1. CONFIGURACIÓN GENERAL
# ============================================================

st.set_page_config(
    page_title="FinPredict | Riesgo hipotecario",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# 2. FUNCIONES DE FORMATO Y VALIDACIÓN
# ============================================================

def formato_moneda(valor):
    """Formatea un importe con separadores de miles."""
    return f"{Decimal(str(valor)):,.2f}"


def convertir_decimal(texto, campo):
    """
    Convierte un texto numérico a Decimal.

    Acepta el formato 4,784,933.89 y rechaza
    textos no numéricos o valores no finitos.
    """
    try:
        numero = Decimal(
            str(texto).strip().replace(",", "")
        )
    except (InvalidOperation, ValueError):
        raise ValueError(
            f"El campo '{campo}' debe contener "
            "un número válido."
        )

    if not numero.is_finite():
        raise ValueError(
            f"El campo '{campo}' debe ser finito."
        )

    return numero


def campo_monetario(etiqueta, valor):
    """Campo editable con formato financiero."""
    return st.text_input(
        etiqueta,
        value=formato_moneda(valor),
        help=(
            "Formato: 1,234,567.89. "
            "Puedes escribir el importe "
            "con o sin separadores de miles."
        ),
    )


def campo_decimal(etiqueta, valor, ayuda=None):
    """Conserva la precisión de indicadores decimales."""
    return st.text_input(
        etiqueta,
        value=str(valor),
        help=ayuda,
    )


# ============================================================
# 3. IDENTIDAD VISUAL FINPREDICT
# ============================================================

st.markdown("""
<style>

    /* PALETA CORPORATIVA FINPREDICT */

    .stApp {
        background-color: #F7F9FB;
        color: #102B4E;
    }

    h1, h2, h3 {
        color: #102B4E !important;
        font-weight: 700;
    }

    /* BARRA LATERAL */

    [data-testid="stSidebar"] {
        background-color: #102B4E;
    }

    [data-testid="stSidebar"] * {
        color: #FFFFFF;
    }

    /* ENCABEZADO */

    .fp-eyebrow {
        color: #159B94;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 0.3rem;
    }

    .fp-subtitle {
        color: #64748B;
        font-size: 1.08rem;
        margin-top: -0.4rem;
        margin-bottom: 1.4rem;
    }

    .fp-accent-line {
        height: 4px;
        background-color: #20B2AA;
        border-radius: 4px;
        margin: 1.2rem 0 1.6rem 0;
    }

    /* PRESENTACIÓN */

    .fp-intro {
        background-color: #FFFFFF;
        border: 1px solid #DCE5EA;
        border-left: 5px solid #20B2AA;
        border-radius: 8px;
        padding: 1.5rem 1.7rem;
        margin-bottom: 1.5rem;
    }

    .fp-intro h3 {
        margin-top: 0;
        margin-bottom: 0.7rem;
        font-size: 1.35rem;
    }

    .fp-intro p {
        color: #52657A;
        font-size: 0.98rem;
        line-height: 1.6;
        margin-bottom: 0;
    }

    /* INDICADORES EJECUTIVOS */

    .fp-metric {
        background-color: #EEF2F5;
        border: 1px solid #E0E7ED;
        border-radius: 8px;
        padding: 1.1rem 1.3rem;
        min-height: 112px;
    }

    .fp-metric-teal {
        background-color: #E8F7F3;
        border-color: #D0ECE6;
    }

    .fp-metric-value {
        color: #102B4E;
        font-size: 1.65rem;
        font-weight: 750;
        margin-bottom: 0.25rem;
    }

    .fp-metric-label {
        color: #64748B;
        font-size: 0.83rem;
    }

    /* AVISO RESPONSABLE */

    .fp-notice {
        background-color: #E8F7F3;
        border-left: 5px solid #20B2AA;
        border-radius: 6px;
        padding: 1rem 1.2rem;
        color: #26475A;
        font-size: 0.91rem;
        line-height: 1.55;
        margin: 1.5rem 0;
    }

    /* SECCIONES */

    .fp-section {
        border-bottom: 2px solid #20B2AA;
        padding-bottom: 0.5rem;
        margin-bottom: 0.9rem;
    }

    .fp-muted {
        color: #64748B;
        font-size: 0.93rem;
        line-height: 1.6;
    }

    /* ENTRADAS */

    div[data-testid="stTextInput"] input {
        background-color: #FFFFFF;
        border-radius: 6px;
    }

    div[data-testid="stNumberInput"] input {
        background-color: #FFFFFF;
        border-radius: 6px;
    }

    /* BOTÓN CORPORATIVO */

    div[data-testid="stFormSubmitButton"] button,
    div[data-testid="stFormSubmitButton"] button[kind="primary"],
    button[data-testid="stBaseButton-primary"] {
        background: #102B4E !important;
        background-color: #102B4E !important;
        border: 1px solid #102B4E !important;
        color: #FFFFFF !important;
        border-radius: 7px !important;
        font-weight: 600 !important;
    }

    div[data-testid="stFormSubmitButton"] button:hover,
    button[data-testid="stBaseButton-primary"]:hover {
        background: #20B2AA !important;
        background-color: #20B2AA !important;
        border-color: #20B2AA !important;
        color: #FFFFFF !important;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# 4. BARRA LATERAL
# ============================================================

with st.sidebar:

    st.title("FinPredict")
    st.caption("FinComercial, S.A.")

    st.divider()

    st.markdown("**EVALUACIÓN PREVENTIVA**")
    st.write("Fase II · Integración y despliegue")

    st.divider()

    st.write("**Modelo:** Regresión logística")
    st.write("**Variables:** 15 predictores")
    st.write("**Threshold:** 75%")

    st.divider()

    st.caption(
        "Prototipo académico\n\n"
        "Datos sintéticos · No productivo"
    )


# ============================================================
# 5. ENCABEZADO PRINCIPAL
# ============================================================

st.markdown(
    '<div class="fp-eyebrow">'
    'FinComercial, S.A. / Inteligencia de riesgo'
    '</div>',
    unsafe_allow_html=True,
)

st.title("FinPredict")

st.markdown(
    '<div class="fp-subtitle">'
    'Evaluación preventiva de riesgo hipotecario'
    '</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="fp-accent-line"></div>',
    unsafe_allow_html=True,
)


# ============================================================
# 6. PRESENTACIÓN
# ============================================================

st.markdown("""
<div class="fp-intro">
    <h3>Analítica inteligente para anticipar el riesgo</h3>
    <p>
        Plataforma de apoyo a la priorización preventiva
        de cartera hipotecaria mediante inteligencia
        artificial. La solución estima la probabilidad
        de incumplimiento y facilita la identificación
        de créditos que requieren atención prioritaria.
    </p>
</div>
""", unsafe_allow_html=True)


# ============================================================
# 7. INDICADORES DEL MODELO
# ============================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="fp-metric">
        <div class="fp-metric-value">15</div>
        <div class="fp-metric-label">
            Variables predictoras
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="fp-metric fp-metric-teal">
        <div class="fp-metric-value">75%</div>
        <div class="fp-metric-label">
            Umbral operativo
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="fp-metric">
        <div class="fp-metric-value">API</div>
        <div class="fp-metric-label">
            Servicio de inferencia FastAPI
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# 8. AVISO DE USO RESPONSABLE
# ============================================================

st.markdown("""
<div class="fp-notice">
    <strong>Uso académico y experimental.</strong>
    FinPredict utiliza información sintética.
    Sus resultados están destinados a la evaluación
    metodológica y no deben utilizarse para aprobar,
    rechazar o modificar créditos reales.
</div>
""", unsafe_allow_html=True)


# ============================================================
# 9. EVALUACIÓN INDIVIDUAL
# ============================================================

st.markdown(
    '<h3 class="fp-section">Evaluación individual</h3>',
    unsafe_allow_html=True,
)

st.markdown(
    '<p class="fp-muted">'
    'Capture las condiciones del crédito, su situación '
    'de morosidad y el comportamiento reciente de pagos '
    'para consultar el modelo mediante la API de FinPredict.'
    '</p>',
    unsafe_allow_html=True,
)


# ============================================================
# 10. FORMULARIO DE EVALUACIÓN
# ============================================================

with st.form("formulario_finpredict"):

    # --------------------------------------------------------
    # 10.1 CONDICIONES DEL CRÉDITO
    # --------------------------------------------------------

    st.markdown("#### 1. Condiciones del crédito")

    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:

        monto_original = campo_monetario(
            "Monto original ($)",
            "4784933.89",
        )

        plazo_meses = st.number_input(
            "Plazo (meses)",
            min_value=0,
            value=360,
            step=1,
        )

    with col2:

        tasa_interes_anual = campo_decimal(
            "Tasa de interés anual (%)",
            "10.34",
        )

        pago_mensual = campo_monetario(
            "Pago mensual ($)",
            "43198.32",
        )

    with col3:

        ingreso_mensual = campo_monetario(
            "Ingreso mensual ($)",
            "143552.49",
        )

        antiguedad_meses = st.number_input(
            "Antigüedad del crédito (meses)",
            min_value=0,
            value=51,
            step=1,
        )

    st.divider()

    # --------------------------------------------------------
    # 10.2 SITUACIÓN DE MOROSIDAD
    # --------------------------------------------------------

    st.markdown("#### 2. Situación de morosidad")

    col4, col5 = st.columns(2, gap="medium")

    with col4:

        saldo_vencido = campo_monetario(
            "Saldo vencido ($)",
            "10551.63",
        )

        dias_atraso = st.number_input(
            "Días de atraso",
            min_value=0,
            value=18,
            step=1,
        )

    with col5:

        relacion_pago_ingreso = campo_decimal(
            "Relación pago / ingreso",
            "0.3009235158512402",
            "Indicador decimal: 0.30 equivale al 30%.",
        )

        saldo_vencido_mensualidades = campo_decimal(
            "Saldo vencido en mensualidades",
            "0.24426019345196756",
        )

    st.divider()

    # --------------------------------------------------------
    # 10.3 COMPORTAMIENTO DE PAGOS
    # --------------------------------------------------------

    st.markdown("#### 3. Comportamiento de pagos")

    col6, col7, col8 = st.columns(3, gap="medium")

    with col6:

        importe_pagado_3m = campo_monetario(
            "Importe pagado últimos 3 meses ($)",
            "122220.61",
        )

        numero_pagos_3m = st.number_input(
            "Número de pagos últimos 3 meses",
            min_value=0,
            value=4,
            step=1,
        )

    with col7:

        importe_exigible_3m = campo_monetario(
            "Importe exigible últimos 3 meses ($)",
            "129594.96",
        )

        obligaciones_3m = st.number_input(
            "Obligaciones últimos 3 meses",
            min_value=0,
            value=3,
            step=1,
        )

    with col8:

        porcentaje_pago_3m = campo_decimal(
            "Proporción pagada últimos 3 meses",
            "0.9430969383377256",
            "Indicador decimal: 0.94 equivale al 94%.",
        )

    st.divider()

    enviar = st.form_submit_button(
        "Evaluar riesgo hipotecario",
        type="primary",
        use_container_width=True,
    )



# ============================================================
# 11. VALIDACIÓN Y CONEXIÓN CON FASTAPI
# ============================================================

API_URL = os.getenv(
    "FINPREDICT_API_URL",
    "http://127.0.0.1:8000/predict"
)


if enviar:

    try:
        # Convertir importes e indicadores decimales
        valores_decimales = {
            "monto_original": monto_original,
            "tasa_interes_anual": tasa_interes_anual,
            "pago_mensual": pago_mensual,
            "ingreso_mensual": ingreso_mensual,
            "saldo_vencido": saldo_vencido,
            "relacion_pago_ingreso": relacion_pago_ingreso,
            "saldo_vencido_mensualidades":
                saldo_vencido_mensualidades,
            "importe_pagado_3m": importe_pagado_3m,
            "importe_exigible_3m": importe_exigible_3m,
            "porcentaje_pago_3m": porcentaje_pago_3m,
        }

        datos = {
            nombre: float(
                convertir_decimal(valor, nombre)
            )
            for nombre, valor in valores_decimales.items()
        }

        # Variables enteras
        datos.update({
            "plazo_meses": int(plazo_meses),
            "antiguedad_meses": int(antiguedad_meses),
            "dias_atraso": int(dias_atraso),
            "numero_pagos_3m": int(numero_pagos_3m),
            "obligaciones_3m": int(obligaciones_3m),
        })

        if len(datos) != 15:
            raise ValueError(
                "La solicitud debe contener 15 variables."
            )

        # Enviar la solicitud al backend
        with st.spinner("Consultando el modelo FinPredict..."):
            respuesta = requests.post(
                API_URL,
                json=datos,
                timeout=15,
            )

        # Manejar errores de validación de la API
        if respuesta.status_code == 422:
            detalle = respuesta.json().get(
                "detail",
                "Datos de entrada inválidos."
            )
            st.error(
                f"La API rechazó la solicitud: {detalle}"
            )

        elif respuesta.status_code != 200:
            st.error(
                "La API devolvió un error HTTP "
                f"{respuesta.status_code}."
            )

        else:
            resultado = respuesta.json()

            probabilidad = float(
                resultado["probabilidad_incumplimiento"]
            )

            clasificacion = int(
                resultado["clasificacion"]
            )

            threshold = float(
                resultado["threshold"]
            )

            nivel_riesgo = resultado["nivel_riesgo"]

            st.markdown("### Resultado de la evaluación")

            col_resultado1, col_resultado2, col_resultado3 = (
                st.columns(3)
            )

            with col_resultado1:
                st.metric(
                    "Probabilidad de incumplimiento",
                    f"{probabilidad:.4%}",
                )

            with col_resultado2:
                st.metric(
                    "Clasificación",
                    nivel_riesgo,
                )

            with col_resultado3:
                st.metric(
                    "Umbral operativo",
                    f"{threshold:.0%}",
                )

            if clasificacion == 1:
                st.warning(
                    "El crédito supera el umbral operativo "
                    "y se clasifica para revisión preventiva."
                )
            else:
                st.success(
                    "El crédito no supera el umbral "
                    "operativo de priorización."
                )

            st.caption(
                "Modelo: "
                f"{resultado.get('version_modelo', 'N/D')} "
                "| Evaluación académica con datos sintéticos"
            )

    except (ValueError, OverflowError) as error:
        st.error(
            f"Error en los datos capturados: {error}"
        )


    except requests.exceptions.RequestException:
        st.error(
        "No fue posible conectar con FastAPI. "
        "Verifica que el servicio backend esté disponible "
        f"en {API_URL}."
        )

