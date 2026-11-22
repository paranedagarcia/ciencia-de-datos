---
id: pipeline
title: "Pipeline"
sidebar_label: "📄 Pipeline"
description: "Pipeline"
hide_title: true
---

## **Pipeline completo**

A continuación se detalla cómo orquestar el flujo completo del **modelo medallón (Bronce ➔ Plata ➔ Oro)** de extremo a extremo, comparando los dos enfoques más utilizados en la industria: **Apache Airflow** (enfoque *code-first* con DAGs en Python) y **Azure Data Factory / Fabric Data Factory** (enfoque visual con canalizaciones administradas).


### Arquitectura y Estrategia

El fallos e idempotencia**:

```lujo secuencial de orquestación debe estructurarse garantizando **dependencias estrictas, tolerancia a f
[ Fuentes Externas (APIs / BD / Archivos) ]
                   │
                   ▼  (1. Ingesta cruda)
         ┌───────────────────┐
         │    Capa Bronce    │ ◄── Storage: ADLS Gen2 / S3 / OneLake
         └───────────────────┘
                   │
                   ▼  (2. Limpieza, deduplicación y MERGE)
         ┌───────────────────┐
         │    Capa Plata     │ ◄── Formato Delta Lake (transacciones ACID)
         └───────────────────┘
                   │
                   ▼  (3. Modelado en estrella, agregaciones y KPIs)
         ┌───────────────────┐
         │     Capa Oro      │ ◄── Tablas de hechos y dimensiones (BI/ML)
         └───────────────────┘
                   │
                   ▼  (4. Notificación y refresco)
       [ Refresco de Semántica en Power BI / Alertas ]
```



### Opción A: Orquestación con Apache Airflow (Enfoque Python / DAGs)

**Apache Airflow** permite definir el pipeline completo como código (*Configuration as Code*), facilitando el control de versiones, reintentos automáticos, gestión de parámetros de fecha (`data_interval_start`) y ramificaciones condicionales.

El siguiente ejemplo implementa un DAG completo que orquesta la ejecución secuencial de cuadernos Spark en **Databricks**:

```python showLineNumbers
from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.databricks.operators.databricks import DatabricksRunNowOperator
from airflow.operators.empty import EmptyOperator

# Configuración básica de resiliencia y reintentos
default_args = {
    'owner': 'data_engineering',
    'depends_on_past': False,
    'email_on_failure': True,
    'email': ['alertas-datos@empresa.com'],
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='pipeline_medallon_diario',
    default_args=default_args,
    description='Pipeline diario ETL Bronce -> Plata -> Oro',
    schedule_interval='0 2 * * *',  # Ejecución todos los días a las 02:00 UTC
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=['medallion', 'spark', 'delta_lake'],
) as dag:

    inicio = EmptyOperator(task_id='inicio_pipeline')

    # 1. Ingesta de datos crudos a Bronce
    tarea_bronce = DatabricksRunNowOperator(
        task_id='ingesta_a_bronce',
        databricks_conn_id='databricks_default',
        job_id=101,  # ID del trabajo de ingesta en Databricks
        notebook_params={
            'execution_date': '{{ ds }}',
            'target_layer': 'bronze'
        }
    )

    # 2. Refinamiento, limpieza y upsert en Plata
    tarea_plata = DatabricksRunNowOperator(
        task_id='transformacion_a_plata',
        databricks_conn_id='databricks_default',
        job_id=102,
        notebook_params={
            'execution_date': '{{ ds }}',
            'target_layer': 'silver'
        }
    )

    # 3. Modelado dimensional y agregaciones a Oro
    tarea_oro = DatabricksRunNowOperator(
        task_id='agregacion_a_oro',
        databricks_conn_id='databricks_default',
        job_id=103,
        notebook_params={
            'execution_date': '{{ ds }}',
            'target_layer': 'gold'
        }
    )

    fin = EmptyOperator(task_id='fin_pipeline')

    # Definición explícita de dependencias secuenciales
    inicio >> tarea_bronce >> tarea_plata >> tarea_oro >> fin
```



### Opción B: Orquestación con Azure Data Factory (ADF) / Fabric Data Factory

En entornos gestionados de Microsoft Azure y Fabric, las canalizaciones (*pipelines*) coordinan actividades visuales mediante enlaces de dependencia condicional (`Upon Success`, `Upon Failure`):

#### Componentes de la Canalización en Data Factory
1. **Actividad de Validación / Metadata (`Get Metadata`):** Comprueba que los archivos de origen existan en el almacenamiento antes de iniciar el cómputo.
2. **Actividad de Ingesta (Copy Data / Web Activity):** Extrae datos de APIs REST, bases de datos SQL relacionales o sistemas ERP y los vuelca en formato plano o Parquet en el contenedor `bronze/`.
3. **Actividad Notebook (Databricks / Fabric Notebook):**
   * Invoca el cuaderno de limpieza que lee de `bronze/` y escribe con `MERGE` en `silver/`.
   * En caso de éxito, desencadena el segundo cuaderno que genera las dimensiones y tablas de hechos en `gold/`.
4. **Actividad de Webhook / Power BI Refresh:** Llama a la API de Power BI para actualizar los modelos semánticos en modo *Import* o refrescar metadatos de *Direct Lake*.
5. **Manejo de Errores (Failure Handler):** Se asocia una actividad `Teams/Slack Notification` o `Send Email` ante cualquier fallo de los cuadernos.



### Consideraciones Técnicas y Buenas Prácticas de Orquestación

* **Idempotencia:** Cada tarea debe ser reejecutable de manera segura. Si la tarea de Oro falla, debe poder reintentarse sin duplicar datos en las tablas de hechos ni generar inconsistencias.

* **Procesamiento incremental (*Watermarking* / Particionamiento):** En lugar de reprocesar el lago entero a diario, el orquestador debe pasar parámetros de fecha o identificadores de lote para filtrar exclusivamente los registros generados en la última ventana temporal.

* **Control de calidad previo a la Capa Oro (*Circuit Breakers*):** Antes de ejecutar la agregación final a Oro, es aconsejable incluir una verificación de integridad (con herramientas como Great Expectations o Delta Live Tables expectations). Si se detecta un porcentaje de anomalías superior a un umbral definido, el orquestador aborta la promoción a Oro para evitar contaminar los tableros ejecutivos.

* **Optimización posterior (`VACUUM` y `OPTIMIZE`):** No es necesario compactar tablas en cada corrida de micro-lote; se recomienda programar un pipeline de mantenimiento semanal que ejecute `OPTIMIZE` y `VACUUM` de manera aislada fuera del horario comercial.


## **Implementar control de calidad**

Implementar un **marco de control de calidad de datos (*Data Quality Control Framework*)** dentro de la arquitectura medallón permite garantizar que únicamente los datos confiables, íntegros y validados se promocionen a las capas superiores (*Silver* y *Gold*), protegiendo los cuadros de mando y modelos analíticos de anomalías o registros corruptos.

A continuación se detalla la estrategia integral para implementar controles de calidad y **reglas de parada (*circuit breakers*)** en el flujo de ingeniería de datos.


### Niveles de Validación en la Arquitectura Medallón

El control de calidad no debe aplicarse como un bloque monolítico, sino distribuido en diferentes momentos de la canalización:

* **Línea de defensa 1: Integridad técnica y de esquema (Bronce ➔ Plata):**
  * Validación estructural contra esquemas publicados (tipos de datos, nulabilidad de campos obligatorios y detección de *schema drift*).
  * Formato y estandarización (fechas, códigos de moneda o país, eliminación de espacios en blanco).
  * Deduplicación por clave primaria o de negocio.
* **Línea de defensa 2: Reglas de consistencia funcional y de negocio (Plata ➔ Oro):**
  * Verificación de rangos y valores plausibles (ej. montos mayores a cero, porcentajes válidos, fechas no futuras).
  * Integridad referencial cruzada (validación de existencia de clientes o productos frente a tablas maestras o dimensiones).
  * Pruebas de volumen y completitud (comprobar que la carga diaria no caiga o aumente drásticamente respecto al histórico).


### Patrones de Acción: Reglas de Parada (*Circuit Breakers*) y Cuarentena

Cuando una prueba de calidad detecta registros anómalos, el marco de control debe responder según la criticidad de la regla:

1. **Monitoreo y Alerta (*Warn / Inform*):** El dato ingresa a la capa destino pero se registra una métrica o advertencia en los metadatos de auditoría y observabilidad.
2. **Descarte o Aislamiento en Cuarentena (*Drop / Quarantine*):**
   * Los registros válidos continúan hacia la capa Plata u Oro.
   * Los registros anómalos se desvían hacia una tabla de errores o **zona de cuarentena / Error Mart** junto con un código de error y marca de tiempo. Esto permite a los analistas e ingenieros auditar los fallos y alimentar bucles de retroalimentación hacia los sistemas de origen sin frenar el pipeline completo.
3. **Regla de Parada (*Circuit Breaker / Fail*):** Si la tasa de anomalías o el porcentaje de fallos supera un umbral de tolerancia predefinido (ej. más del 5% de filas nulas o una variación de volumen anómala), el pipeline detiene de inmediato su ejecución y aborta la promoción a Oro.



### Implementación Práctica con PySpark y Lógica de Parada

El siguiente ejemplo en **PySpark** muestra cómo procesar un lote de datos, registrar los errores en una tabla de cuarentena y activar un *circuit breaker* si se supera el umbral tolerable:

```python
from pyspark.sql.functions import col, when, current_timestamp
import sys

# 1. Lectura de datos desde la capa Bronce
df_bronze = spark.read.table("bronze.transacciones_raw")
total_filas = df_bronze.count()

# 2. Evaluación de reglas de calidad y etiquetado de anomalías
df_evaluado = df_bronze.withColumn(
    "motivo_error",
    when(col("id_transaccion").isNull(), "ID_NULO")
    .when(col("monto") <= 0, "MONTO_INVALIDO")
    .when(col("codigo_moneda").isNull(), "MONEDA_NULA")
    .otherwise(None)
)

# 3. Separación de registros válidos y anómalos
df_validos = df_evaluado.filter(col("motivo_error").isNull()).drop("motivo_error")
df_rechazados = df_evaluado.filter(col("motivo_error").isNotNull())

filas_erroneas = df_rechazados.count()
tasa_error = (filas_erroneas / total_filas) * 100 if total_filas > 0 else 0

# 4. Guardar registros fallidos en tabla de Cuarentena (Error Mart)
if filas_erroneas > 0:
    (
        df_rechazados
        .withColumn("fecha_error", current_timestamp())
        .write
        .format("delta")
        .mode("append")
        .saveAsTable("silver.cuarentena_transacciones")
    )

# 5. Regla de Parada (Circuit Breaker): abortar si el error supera el 5%
UMBRAL_MAX_ERROR_PCT = 5.0
if tasa_error > UMBRAL_MAX_ERROR_PCT:
    raise Exception(
        f"[CIRCUIT BREAKER ACTIVADO] Tasa de error ({tasa_error:.2f}%) "
        f"supera el umbral permitido ({UMBRAL_MAX_ERROR_PCT}%). "
        f"Se detiene la promoción a capas posteriores."
    )

# 6. Promoción de registros válidos a la capa Plata
(
    df_validos.write
    .format("delta")
    .mode("append")
    .saveAsTable("silver.transacciones")
)
```



### Herramientas y Marcos Especializados

En plataformas de datos a escala empresarial, el control de calidad suele integrarse mediante bibliotecas y herramientas declarativas:

* **Delta Live Tables Expectations (Databricks):** Permite declarar restricciones directamente sobre flujos de datos en Spark SQL o Python:
  * `@dlt.expect("monto_positivo", "monto > 0")`: Registra métricas de fallo sin detener la canalización.
  * `@dlt.expect_or_drop("id_valido", "id_transaccion IS NOT NULL")`: Desecha los registros que no cumplan la condición.
  * `@dlt.expect_or_fail("moneda_valida", "codigo_moneda IN ('USD', 'EUR')")`: Falla y detiene la ejecución inmediatamente si una sola fila no cumple.
* **Great Expectations y Soda:** Marcos abiertos de pruebas automáticas para perfilar, documentar y evaluar datasets antes de su consumo. Se integran en orquestadores como Airflow o Azure Data Factory para validar los datos contra un conjunto de contratos o *expectativas*.
* **dbt Test:** Ejecuta validaciones de unicidad (`unique`), obligatoriedad (`not_null`), rangos de valores (`accepted_values`) y relaciones de integridad referencial (`relationships`) durante el proceso de materialización.
* **Dataflow Gen2 y Data Profiling (Microsoft Fabric / Azure Data Factory):** Herramientas visuales de bajo código que integran inspección de métricas de calidad por columna (porcentajes de nulos, valores erróneos o duplicados) y filtrado directo.



### Integración con la Observabilidad y Orquestación

Para cerrar el ciclo del gobierno de datos:
1. **Registro en el Catálogo y Metadatos:** Los resultados de las auditorías de calidad (puntuaciones de completitud, precisión y volumen de fallos) deben registrarse como metadatos en herramientas como Microsoft Purview o AWS Glue Data Catalog.
2. **Notificaciones y Circuit Breakers en el Orquestador:** Si la actividad de calidad falla, el orquestador (Airflow o Data Factory) captura el error, cancela las tareas dependientes hacia la capa Oro y envía una alerta inmediata (vía webhook a Slack/Teams o correo electrónico) al equipo responsable del dominio.
3. **Resolución en el Origen:** Como principio de gobierno, las anomalías detectadas en cuarentena deben ser corregidas en los sistemas transaccionales de origen (*golden source*) para evitar que los errores sigan propagándose.

*****
*****
## **Desarrollo de un pipeline**

**Apache Airflow** es la herramienta estándar de código abierto para orquestar flujos de ingeniería de datos complejos mediante grafos acíclicos dirigidos (**DAGs**) definidos como código en Python. En una arquitectura medallón, Airflow coordina la secuencia estricta entre la ingesta a **Bronce**, el refinamiento en **Plata** y el modelado analítico en **Oro**, asegurando que los datos solo avancen si se cumplen las reglas de calidad y dependencias de cada capa.


### Flujo de Trabajo

Cada etapa del modelo medallón se modela como un nodo dentro del DAG, organizándose comúnmente con **Task Groups** para dar claridad estructural y modularidad:

```text
       ┌────────────────────────┐
       │     inicio_pipeline    │
       └───────────┬────────────┘
                   │
                   ▼
       ┌────────────────────────┐
       │   Grupo Capa Bronce    │  ◄── Ingesta cruda (S3/ADLS/GCS)
       │ (Sensores + Extracción)│
       └───────────┬────────────┘
                   │
                   ▼
       ┌────────────────────────┐
       │    Grupo Capa Plata    │  ◄── Limpieza, deduplicación, tipado
       │   (Spark / Databricks) │
       └───────────┬────────────┘
                   │
                   ▼
       ┌────────────────────────┐
       │  Control de Calidad    │  ◄── Regla de parada (Circuit Breaker)
       │ (evaluar_tasa_error)   │
       └─────┬────────────┬─────┘
  [Éxito]    │            │ [Tasa de error > umbral]
             ▼            ▼
┌──────────────────┐  ┌──────────────────────┐
│  Grupo Capa Oro  │  │  alerta_cuarentena   │ (Detiene avance y notifica)
│(Hechos/Dimension)│  └──────────────────────┘
└────────────┬─────┘
             ▼
┌────────────────────────┐
│  refresco_powerbi_bi   │  ◄── Notificación de finalización / Catálogo
└────────────────────────┘
```



### DAG en Python

El siguiente DAG utiliza la **TaskFlow API** (`@dag`, `@task`, `@task_group`) junto con operadores y sensores habituales en entornos de nube (como Databricks, Spark y notificaciones):

```python
from datetime import datetime, timedelta
from airflow.decorators import dag, task, task_group
from airflow.operators.empty import EmptyOperator
from airflow.providers.databricks.operators.databricks import DatabricksRunNowOperator
from airflow.exceptions import AirflowException

# ---------------------------------------------------------------------------
# Argumentos predeterminados y políticas de resiliencia
# ---------------------------------------------------------------------------
def notificar_fallo_slack(context):
    """Callback invocado automáticamente si falla alguna tarea crítica."""
    task_id = context['task_instance'].task_id
    run_id = context['run_id']
    error = context.get('exception')
    print(f"🚨 [ALERTA] La tarea '{task_id}' falló en la corrida '{run_id}'. Detalle: {error}")

default_args = {
    'owner': 'data_engineering',
    'depends_on_past': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'on_failure_callback': notificar_fallo_slack,
}

@dag(
    dag_id='pipeline_medallon_airflow',
    default_args=default_args,
    description='Orquestación de principio a fin: Bronce -> Plata -> Oro con Control de Calidad',
    schedule='@daily',
    start_date=datetime(2026, 1, 1),
    catchup=False,
    max_active_runs=1,
    tags=['medallion', 'delta_lake', 'spark'],
)
def pipeline_medallon():

    inicio = EmptyOperator(task_id='inicio_proceso')

    # =========================================================================
    # 1. CAPA BRONCE: Ingesta cruda y verificación de disponibilidad
    # =========================================================================
    @task_group(group_id='capa_bronce')
    def grupo_bronce():
        # Ejecutar job de ingesta que copia datos desde el origen a archivos crudos
        ingesta_cruda = DatabricksRunNowOperator(
            task_id='ejecutar_ingesta_bronce',
            databricks_conn_id='databricks_default',
            job_id=201,
            notebook_params={'capa': 'bronze'}
        )
        return ingesta_cruda

    # =========================================================================
    # 2. CAPA PLATA: Limpieza, normalización y MERGE en Delta Lake
    # =========================================================================
    @task_group(group_id='capa_plata')
    def grupo_plata():
        # Ejecuta notebook Spark de deduplicación, filtrado y upsert
        transformar_plata = DatabricksRunNowOperator(
            task_id='ejecutar_transformacion_plata',
            databricks_conn_id='databricks_default',
            job_id=202,
            notebook_params={'capa': 'silver'}
        )
        return transformar_plata

    # =========================================================================
    # 3. CONTROL DE CALIDAD Y CIRCUITO DE PARADA (Circuit Breaker)
    # =========================================================================
    @task.branch(task_id='evaluar_calidad_plata')
    def evaluar_calidad():
        """
        Consulta la tasa de error generada en la tabla de cuarentena.
        Si supera el umbral, desvía el flujo para abortar la promoción a Oro.
        """
        # Simulación de lectura de métricas generadas por el job de Plata
        total_procesados = 1000000
        total_en_cuarentena = 8000
        tasa_error = (total_en_cuarentena / total_procesados) * 100

        UMBRAL_MAX_ERROR_PCT = 2.0  # Máximo 2% de registros corruptos tolerados

        if tasa_error > UMBRAL_MAX_ERROR_PCT:
            print(f"Calidad insuficiente ({tasa_error:.2f}%). Activando parada...")
            return 'notificar_parada_calidad'
        
        print(f"Calidad aceptable ({tasa_error:.2f}%). Continuando a capa Oro...")
        return 'capa_oro.ejecutar_modelo_oro'

    @task(task_id='notificar_parada_calidad')
    def notificar_parada():
        raise AirflowException(
            "CIRCUIT BREAKER: Tasa de error en capa Plata excedida. Promoción a Oro cancelada."
        )

    # =========================================================================
    # 4. CAPA ORO: Agregaciones, hechos y dimensiones
    # =========================================================================
    @task_group(group_id='capa_oro')
    def grupo_oro():
        generar_oro = DatabricksRunNowOperator(
            task_id='ejecutar_modelo_oro',
            databricks_conn_id='databricks_default',
            job_id=203,
            notebook_params={'capa': 'gold'}
        )
        return generar_oro

    # =========================================================================
    # 5. POST-PROCESAMIENTO: Refresco semántico en Power BI y Cierre
    # =========================================================================
    refresco_bi = EmptyOperator(
        task_id='refrescar_modelo_powerbi',
        trigger_rule='all_success'
    )

    fin = EmptyOperator(task_id='fin_proceso')

    # -------------------------------------------------------------------------
    # Definición explícita de dependencias del pipeline
    # -------------------------------------------------------------------------
    nodo_bronce = grupo_bronce()
    nodo_plata = grupo_plata()
    check_calidad = evaluar_calidad()
    nodo_oro = grupo_oro()
    abortar_calidad = notificar_parada()

    inicio >> nodo_bronce >> nodo_plata >> check_calidad
    check_calidad >> nodo_oro >> refresco_bi >> fin
    check_calidad >> abortar_calidad

pipeline_medallon()
```



### Buenas Prácticas

1. **Evitar código pesado en el nivel superior (*Top-Level Code*):**  
   Airflow reanaliza los archivos de la carpeta `dags` continuamente (por defecto cada 30 segundos). Consultas SQL directas, conexiones externas o llamadas a APIs pesadas no deben ubicarse fuera de las funciones `@task` para no saturar el programador (*Scheduler*).

2. **Idempotencia mediante particiones de fecha:**  
   Es fundamental parametrizar los notebooks pasando variables de contexto de Airflow (como `{{ ds }}` para la fecha de ejecución) en lugar de usar marcas de tiempo del sistema (`datetime.now()`), permitiendo reejecutar cualquier día histórico (*backfill*) sin generar inconsistencias ni duplicados.

3. **Uso de Operadores Deferrables (*Deferrable Operators*):**  
   Cuando un trabajo de Spark o Databricks tarda minutos o una hora en completarse, utilizar la versión *deferrable* del operador libera el hilo del worker mientras espera la finalización externa, evitando bloquear la capacidad de ejecución de Airflow.
   
4. **Desacoplamiento mediante Airflow Datasets (Data-Aware Scheduling):**  
   En organizaciones grandes, en lugar de un único DAG gigante, se pueden separar en tres DAGs independientes enlazados por eventos de conjuntos de datos: el DAG de Plata se programa con `schedule=[Dataset('lakehouse/bronze')]`, disparándose en cuanto el DAG de Bronce termina exitosamente.

