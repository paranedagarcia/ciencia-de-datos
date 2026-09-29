---
id: orquestacion-intro
title: "Procesos de orquestación"
sidebar_label: "📄 Presentación"
description: "Automatizar, coordinar y gestionar de manera centralizada el flujo de trabajo de múltiples tareas interdependientes que componen un pipeline o canalización de datos."
---

La **orquestación de datos** es el proceso de automatizar, coordinar y gestionar de manera centralizada el flujo de trabajo de múltiples tareas interdependientes que componen un pipeline o canalización de datos. 

En este ámbito, los datos raramente se procesan en un único paso monolítico. El flujo típico abarca desde la ingesta de fuentes heterogéneas, la validación y limpieza, hasta el enriquecimiento analítico, el entrenamiento de modelos de Machine Learning y la carga en un repositorio analítico. **El orquestador actúa como el director de escena (o conductor de orquesta)**, asegurando que cada tarea se ejecute en el orden correcto, bajo los recursos adecuados y respondiendo con resiliencia ante cualquier fallo en la infraestructura.



### DAG como concepto clave

Para representar y coordinar estas dependencias, los orquestadores modelan los pipelines como **DAGs** (por sus siglas en inglés, *Directed Acyclic Graph*):
*   **Grafo:** Una estructura compuesta por **nodos** (que representan las tareas individuales o unidades atómicas de trabajo) y **bordes o aristas** (que definen las relaciones de dependencia entre ellos).
*   **Dirigido:** Las aristas tienen una dirección unívoca (flechas) que indica el orden estricto de ejecución (por ejemplo, la Tarea B no puede iniciar hasta que la Tarea A termine con éxito).
*   **Acíclico:** El grafo no contiene bucles o ciclos cerrados. Esta propiedad es matemáticamente indispensable para evitar dependencias circulares infinitas, donde la Tarea A esperase a la Tarea B y viceversa, bloqueando indefinidamente la ejecución del pipeline.



### ¿Por qué un Orquestador? 
**(Frente a Scripts Secuenciales y Cron)**

Históricamente, los pipelines de datos se ejecutaban mediante scripts secuenciales encadenados y planificados a través de tareas programadas del sistema operativo (**cron jobs**). Sin embargo, este enfoque monolítico presenta serias limitaciones operativas que los orquestadores resuelven de forma nativa:

*   **Tolerancia a fallos granular (Atomicidad):** Si una secuencia de scripts cron de 10 pasos falla en el paso 8, es extremadamente difícil reiniciar el proceso de forma segura desde ese punto exacto. Un orquestador aísla cada paso en una tarea atómica; si una de ellas falla, el sistema detiene el flujo descendente (*downstream*), permite corregir el problema y **reejecutar únicamente la tarea fallida** sin necesidad de volver a calcular los pasos previos que tuvieron éxito.

*   **Idempotencia y Backfilling:** La idempotencia garantiza que ejecutar la misma tarea varias veces con la misma entrada produzca siempre idéntico resultado sin duplicar o corromper datos. Esto es vital al realizar un **backfill** (reejecutar de manera automatizada flujos de fechas pasadas para corregir estadísticas o poblar datos históricos con una lógica nueva).

*   **Ejecución paralela y eficiente:** Un orquestador detecta dinámicamente qué ramas del DAG son independientes entre sí y las ejecuta en paralelo aprovechando al máximo la infraestructura distribuida de cómputo.

*   **Observabilidad centralizada:** Provee interfaces de usuario (UIs) ricas para monitorizar en tiempo real el estado de cada tarea (`success`, `failed`, `skipped`), auditar tiempos de ejecución e inspeccionar trazas de logs de error detalladas sin navegar por los servidores físicos.



### Herramientas Clave

Existen diversas herramientas en el mercado diseñadas para cubrir distintos requerimientos arquitectónicos, de red y de volumen de datos:

#### A. Apache Airflow (El Estándar de la Industria)
Iniciado en Airbnb en 2014, **Airflow** es el orquestador más extendido y maduro. Destaca por su principio de **"Configuración como Código"**, lo que significa que los DAGs se definen completamente utilizando código de Python. Esto permite aplicar las mejores prácticas de la ingeniería de software (control de versiones con Git, pruebas unitarias e integración continua CI/CD) a los pipelines de datos.

*   **Componentes Clave:** El **Scheduler** (planificador que decide qué tareas encolar), el **DAG Processor** (que analiza y serializa el código), el **API Server** (interfaz de comunicación y portal de la UI) y los **Workers** (los agentes físicos que ejecutan las tareas).
*   **La Revolución de Airflow 3:** Introducido para consolidar la seguridad y escalabilidad distribuidas, Airflow 3 desacopla la ejecución de tareas del acceso directo a la base de datos de metadatos utilizando el nuevo **Task SDK** y el **API Server**. Habilita la **ejecución remota** segura (*run anywhere*) mediante el `EdgeExecutor` y soporta de forma nativa entornos multiejecutor concurrentes.

#### B. Alternativas Modernas de Datos (Prefect y Dagster)
Creados como respuestas a algunas limitaciones del diseño de las primeras versiones de Airflow (como la rigidez en el intercambio de datos entre tareas y los flujos altamente dinámicos).
*   **Prefect:** Enfatiza la programación parametrizada y dinámica basada en código nativo de Python con un fuerte enfoque en flujos asíncronos y parametrización en tiempo de ejecución.
*   **Dagster:** Introduce el paradigma de los "activos de datos" (*software-defined assets*), donde el foco no es solo la tarea en sí, sino el estado, calidad e integridad de los datos resultantes de cada paso del pipeline.

#### C. Orquestación Especializada para Machine Learning (Kubeflow Pipelines y TFX)
Cuando el pipeline tiene como objetivo principal la operacionalización de modelos predictivos (MLOps), las herramientas clásicas de ETL se complementan o reemplazan por orquestadores especializados.
*   **Kubeflow Pipelines:** Construido sobre Kubernetes y Argo Workflows, está diseñado específicamente para coordinar experimentos y despliegues de Machine Learning, facilitando el escalado dinámico de contenedores (*pods*) y recursos pesados (como GPUs/TPUs).
*   **TFX (TensorFlow Extended):** Un ecosistema unificado de componentes diseñado por Google para estandarizar e industrializar pipelines de IA, compatible con motores de orquestación subyacentes como Airflow o Kubeflow.

#### D. Soluciones en la Nube y Plataformas Administradas
*   **Servicios Nativos:** Como **Azure Data Factory** o **AWS Glue**, optimizados para integraciones drag-and-drop de bajo código.
*   **Entornos de Airflow Administrados:** Para evitar la fatiga de mantenimiento de infraestructura compleja, las empresas adoptan **Astronomer (Astro)**, **Google Cloud Composer** o **Amazon MWAA**, que automatizan el aprovisionamiento de clústeres elásticos sobre Kubernetes.



### Ejemplo Práctico
**Un DAG de ETL Moderno en Airflow 3**

El siguiente ejemplo escrito en Python implementa un pipeline de ETL utilizando el estándar moderno de la **TaskFlow API** de Airflow 3, ilustrando cómo el paso de datos entre tareas se maneja de forma implícita (vía XCom serializado) y limpia:

```python showLineNumbers
"""
Pipeline de ETL - Estándar Apache Airflow 3
Demuestra la declaración de dependencias, tipado y TaskFlow API.
"""

from pendulum import datetime
from airflow.sdk import dag, task

# Definición del DAG utilizando el decorador nativo
@dag(
    dag_id="etl_orquestacion_universitario",
    start_date=datetime(2026, 8, 20),
    schedule="@daily",       # Planificación determinista diaria
    catchup=False,           # Evita ejecuciones masivas históricas accidentales
    default_args={
        "retries": 2,        # Tolerancia a fallos: reintenta hasta 2 veces
    }
)
def pipeline_etl():

    # Tarea 1: Extracción (Bronze)
    @task
    def extraer_datos_origen() -> dict:
        """Simula la descarga de datos desde una API externa."""
        print("Iniciando extracción segura de transacciones...")
        # Retornamos un diccionario serializable (XCom nativo de Airflow)
        return {
            "estado": "success",
            "registros": [
                {"transaccion_id": "TX_901", "monto": 1250.0},
                {"transaccion_id": "TX_902", "monto": -50.0},  # Registro anómalo
                {"transaccion_id": "TX_903", "monto": 340.5}
            ]
        }

    # Tarea 2: Transformación (Silver)
    @task
    def transformar_y_limpiar(datos_brutos: dict) -> list:
        """Valida que los montos sean positivos aplicando reglas de negocio."""
        print("Procesando transformaciones y limpieza en la capa Silver...")
        registros_filtrados = []
        for reg in datos_brutos["registros"]:
            if reg["monto"] > 0:
                registros_filtrados.append(reg)
            else:
                print(f"Alerta: Registro descartado por monto negativo: {reg['transaccion_id']}")
        return registros_filtrados

    # Tarea 3: Carga (Gold)
    @task
    def cargar_data_warehouse(datos_limpios: list):
        """Simula la escritura final en el almacén de datos analítico."""
        total_cargado = len(datos_limpios)
        print(f"Carga completada de forma idempotente. {total_cargado} registros escritos.")

    # Declaración e inferencia automática de dependencias físicas y de datos
    # Airflow infiere el grafo (DAG) leyendo el paso secuencial de argumentos.
    datos_crudos = extraer_datos_origen()
    datos_procesados = transformar_y_limpiar(datos_crudos)
    cargar_data_warehouse(datos_procesados)

# Instanciación lógica del pipeline
pipeline_etl()
```

Este DAG es procesado y registrado de manera asíncrona en el API Server para su posterior secuenciación cronológica.

