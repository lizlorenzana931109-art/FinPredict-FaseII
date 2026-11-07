
# FinPredict | Fase II

### Analítica inteligente para anticipar el riesgo hipotecario

**Proyecto académico de inteligencia artificial aplicada al sector financiero.**

FinPredict es un prototipo de clasificación de riesgo
hipotecario que utiliza un modelo de regresión logística
para estimar la probabilidad de incumplimiento y apoyar
la identificación de créditos que podrían requerir
seguimiento preventivo.

La solución integra un modelo predictivo, una API REST
desarrollada con FastAPI, una interfaz web construida
con Streamlit y una arquitectura de contenedores Docker.

> **Aviso:** Los datos utilizados son sintéticos.
> FinPredict es un prototipo académico y no debe
> utilizarse para aprobar, rechazar o modificar créditos
> reales sin validaciones adicionales.

---

## 1. Objetivo

Desarrollar una solución reproducible que permita:

- Ejecutar inferencias a partir de 15 variables financieras.
- Validar la estructura y calidad básica de las entradas.
- Exponer el modelo mediante una API REST.
- Consultar predicciones desde una interfaz web.
- Ejecutar frontend y backend mediante Docker Compose.
- Documentar pruebas, limitaciones y resultados.

## 2. Arquitectura

La solución está organizada en dos servicios independientes:

```text
Usuario
  |
  v
Streamlit (frontend)
  |
  | Solicitud HTTP / JSON
  v
FastAPI (backend)
  |
  | Validación de entrada
  v
Pipeline de regresión logística
  |
  v
Probabilidad y clasificación
  |
  v
Respuesta presentada en Streamlit
```

Docker Compose permite ejecutar ambos servicios dentro
de una red interna.

| Componente | Tecnología | Puerto local |
|---|---|---|
| Frontend | Streamlit | 8502 |
| Backend | FastAPI | 8002 |
| Modelo | Scikit-learn | Integrado en backend |
| Orquestación local | Docker Compose | No aplica |

La comunicación interna utiliza:

`http://api:8000/predict`

## 3. Modelo predictivo

**Algoritmo:** Regresión logística.

**Artefacto:** `model/finpredict_modelo.joblib`

**Variables predictoras:** 15.

**Umbral operativo:** 0.75.

La API devuelve:

- Probabilidad estimada de incumplimiento.
- Clasificación binaria.
- Nivel de riesgo.
- Umbral utilizado.
- Versión del modelo.

El umbral se utiliza para clasificar el resultado del
prototipo y no constituye una política crediticia real.

## 4. Tecnologías

- Python 3.13
- Scikit-learn
- Pandas y NumPy
- FastAPI y Pydantic
- Streamlit
- Pytest y HTTPX
- Docker y Docker Compose

Las versiones de las dependencias se encuentran
especificadas en `requirements.txt`.

## 5. Estructura del proyecto

```text
FinPredict-FaseII/
|
|-- api/
|   |-- main.py
|   `-- schemas.py
|
|-- frontend/
|   `-- app.py
|
|-- model/
|   `-- finpredict_modelo.joblib
|
|-- data/
|   |-- finpredict_desarrollo_v2.parquet
|   |-- finpredict_evaluacion_v2.parquet
|   `-- predicciones_holdout_final.csv
|
|-- scripts/
|   |-- validar_modelo.py
|   |-- validar_casos_extremos.py
|   |-- validar_entradas.py
|   `-- 01_evaluacion_modelos_actividad6.ipynb
|
|-- tests/
|   `-- test_api.py
|
|-- docs/
|   |-- validacion_pruebas.md
|   `-- evidencias/
|
|-- resultados/
|
|-- .dockerignore
|-- .gitignore
|-- Dockerfile.api
|-- Dockerfile.frontend
|-- compose.yaml
|-- requirements.txt
`-- README.md
```

## 6. Requisitos previos

Para ejecutar la arquitectura contenerizada se requiere:

1. Docker Desktop o Docker Engine con Compose.
2. Docker en funcionamiento.
3. Puertos locales 8002 y 8502 disponibles.
4. Acceso a los archivos del repositorio.

No es necesario crear un entorno virtual de Python
en el equipo anfitrión para ejecutar la aplicación
mediante Docker Compose.

## 7. Ejecución con Docker Compose

Desde la raíz del proyecto:

```powershell
docker compose config --quiet
docker compose up -d --build
```

Una vez iniciados los servicios:

**Interfaz FinPredict:**

`http://127.0.0.1:8502`

**Documentación Swagger:**

`http://127.0.0.1:8002/docs`

**Verificación de disponibilidad:**

`http://127.0.0.1:8002/health`

### Verificar contenedores

```powershell
docker compose ps
```

### Consultar registros

```powershell
docker compose logs --tail=30
```

### Detener servicios

```powershell
docker compose down
```

Este último comando no elimina las imágenes Docker
ni los archivos del proyecto.

## 8. Pruebas y validación

Se realizaron pruebas de:

- Consistencia histórica sobre 33,603 registros.
- Inferencia sobre cinco escenarios financieros extremos.
- Quince validaciones automatizadas de entradas.
- Cinco pruebas HTTP automatizadas de la API.
- Integración local entre Streamlit y FastAPI.
- Manejo de desconexión y recuperación del backend.
- Construcción de imágenes Docker.
- Integración end-to-end mediante Docker Compose.
- Validación de datos inválidos en contenedores.
- Reconstrucción de imágenes y prueba de regresión.

El caso sintético de referencia produjo:

| Indicador | Resultado |
|---|---|
| Probabilidad estimada | 5.4075% |
| Clasificación | Riesgo bajo |
| Umbral operativo | 75% |

Estos resultados fueron reproducidos en la ejecución
local y en la arquitectura Docker evaluada.

**Informe detallado:**

[Validación y pruebas](docs/validacion_pruebas.md)


### Reproducibilidad de las pruebas históricas

El repositorio incluye los conjuntos de datos sintéticos
necesarios para reproducir las validaciones del modelo:

| Archivo | Propósito |
|---|---|
| `data/finpredict_desarrollo_v2.parquet` | Selección del escenario sin pagos recientes |
| `data/finpredict_evaluacion_v2.parquet` | Validación histórica y selección de escenarios |
| `data/predicciones_holdout_final.csv` | Comparación con las predicciones originales |

Los scripts utilizan rutas relativas a la raíz de
FinPredict – Fase II y no requieren la carpeta de la
Actividad 6.

Para ejecutar las validaciones desde un entorno Python
con las dependencias instaladas:

```powershell
python .\scripts\validar_modelo.py
python .\scripts\validar_casos_extremos.py
```

**Resultados verificados:**

- Consistencia histórica: 33,603 registros.
- Diferencia máxima reportada: 0.000000000000.
- Coincidencia de clasificaciones: 100%.
- Casos extremos: 5 de 5 escenarios evaluados.
- Validaciones automáticas de casos extremos: 5 de 5.

Estas pruebas se ejecutan mediante Python en el
entorno de desarrollo. No forman parte del arranque
automático de los contenedores de inferencia.

## 9. Limitaciones

- El conjunto de datos es sintético.
- El modelo no ha sido validado con datos reales.
- No se realizaron pruebas de carga o concurrencia.
- No se implementó autenticación ni autorización.
- No se configuró infraestructura productiva en la nube.
- No se evaluó alta disponibilidad o escalamiento horizontal.
- Las reglas financieras requieren aprobación de negocio.
- La reconstrucción fue validada utilizando caché Docker;
  no se ha comprobado una instalación completamente limpia.

Por estas razones, la solución se considera un
**prototipo académico funcional**, no un sistema
productivo de decisión crediticia.

## 10. Documentación técnica

FinPredict – Fase II cuenta con documentación técnica
que permite comprender su arquitectura, reproducir
su despliegue y verificar los resultados obtenidos.

| Documento | Descripción | Acceso |
|---|---|---|
| Manual de despliegue y operación | Arquitectura, requisitos, instalación con Docker Compose, pruebas funcionales, mantenimiento, solución de problemas y propuesta de despliegue AWS. | [Consultar manual](docs/manual_despliegue.md) |
| Informe técnico de validación y pruebas | Consistencia histórica, casos extremos, validaciones HTTP, integración frontend/backend y pruebas Docker. | [Consultar informe](docs/validacion_pruebas.md) |
| Evidencias técnicas | Capturas de las pruebas ejecutadas durante el desarrollo y validación del prototipo. | [Ver evidencias](docs/evidencias/) |

### Evidencia documental

El proyecto dispone de **24 evidencias técnicas**
que respaldan los resultados de construcción,
integración, ejecución y validación.

El inventario completo y la descripción de cada
evidencia se encuentran en el informe técnico.

### Ruta recomendada de revisión

Para evaluar FinPredict se recomienda:

1. Consultar este README para conocer el propósito
   y la arquitectura general.
2. Revisar el informe técnico para verificar
   los resultados y las evidencias.
3. Consultar el manual para reproducir el despliegue
   y las pruebas funcionales.

La aplicación puede ejecutarse mediante Docker Compose
siguiendo las instrucciones descritas en el manual.


## 11. Uso de inteligencia artificial generativa

Durante el desarrollo se utilizó ChatGPT como
herramienta de asistencia técnica para explorar
alternativas de implementación, estructurar código,
comprender herramientas, revisar errores y apoyar
la documentación.

Las decisiones de implementación, la ejecución
de las pruebas y la revisión de los resultados
forman parte del trabajo desarrollado para el proyecto.

---

**FinPredict | Fase II**

*Inteligencia artificial aplicada a la gestión
preventiva del riesgo hipotecario.*
