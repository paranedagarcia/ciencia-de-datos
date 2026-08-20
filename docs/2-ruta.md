---
id: bd-intro
title: "Ruta de Aprendizaje"
sidebar_label: "💻 Ruta de Aprendizaje"
sidebar_position: 2
description: "Propuesta de ruta de aprendizaje para Ciencia e Ingenieria de datos"
---


## **Ruta de Ciencia e Ingeniería**

Para unificar con éxito la **Ciencia de Datos** y la **Ingeniería de Datos**, es crucial aplicar principios de **andragogía constructivista**. El aprendizaje óptimo sigue una progresión lógica que va de **lo concreto a lo abstracto**, y de **lo local a lo distribuido**. 

No se puede esperar que un profesional diseñe un pipeline de Machine Learning automatizado en la nube (MLOps) sin comprender antes cómo orquestar tareas de forma idempotente, procesar terabytes de datos de manera distribuida o estructurar un análisis exploratorio riguroso.

Se detalla a continuacion la **ruta de aprendizaje secuencial**, estructurada en **5 módulos progresivos**.

---


```
  ┌──────────────────────────────────────────────────────────┐
  │              MÓDULO 1: Cimientos de Datos                │
  │     (Python, SQL ANSI, Git, Análisis Exploratorio/EDA)   │
  └────────────────────────────┬─────────────────────────────┘
                               │ (Avanza a escala masiva)
                               ▼
  ┌──────────────────────────────────────────────────────────┐
  │         MÓDULO 2: Cómputo Distribuido y Lakehouse        │
  │           (Apache Spark, Delta Lake, Parquet)            │
  └────────────────────────────┬─────────────────────────────┘
                               │ (Añade automatización)
                               ▼
  ┌──────────────────────────────────────────────────────────┐
  │      MÓDULO 3: Orquestación, DataOps y Gobernanza        │
  │     (Apache Airflow 3, Task SDK, Unity Catalog, DAGs)    │
  └────────────────────────────┬─────────────────────────────┘
                               │ (Implementa modelado)
                               ▼
  ┌──────────────────────────────────────────────────────────┐
  │             MÓDULO 4: Ciencia de Datos Aplicada          │
  │          (Scikit-Learn, PyTorch, Model Tuning, ML)       │
  └────────────────────────────┬─────────────────────────────┘
                               │ (Operacionaliza y escala)
                               ▼
  ┌──────────────────────────────────────────────────────────┐
  │        MÓDULO 5: MLOps y Ciclo de Vida del Modelo        │
  │    (MLflow, Model Registry, Inferencia, Drift, CI/CD)    │
  └──────────────────────────────────────────────────────────┘
```
---

### Módulo 1: Cimientos de Datos
**Programación, Consulta y Análisis Local**

*   **Justificación:** Antes de enfrentarse a entornos de Big Data distribuidos, los estudiantes deben dominar las herramientas locales de manipulación de datos. Este módulo sienta las bases de la estructuración del código, el control de cambios (vital para la reproducibilidad) y el concepto de calidad de datos.
*   **Temas Teóricos:** 
    *   Datos estructurados frente a datos no estructurados.
    *   Principios de la percepción visual y storytelling con datos.
    *   Metodología de Análisis Exploratorio de Datos (EDA).
*   **Herramientas y Metodologías**:
    1. - **[Python](https://patricioaraneda.cl/python)** (Pandas, Numpy), 
    2. - **[SQL ANSI-2003](https://patricioaraneda.cl/sql)**, 
    3. - **Git** (para control de versiones), 
    4. - **Visualización de datos** con Matplotlib o Seaborn.
*   **Competencia Técnica Adquirida:** El estudiante es capaz de conectarse a una fuente local, depurar inconsistencias (Data Scrubbing), realizar un análisis básico de calidad y versionar su progreso con Git.

```python showLineNumbers
# Módulo 1: Depuración de datos y EDA local con Pandas
import pandas as pd

# Lectura de datos estructurados de ventas locales
df_raw = pd.read_csv("transacciones_tienda.csv")

# Data Scrubbing: Limpieza de nulos en columnas clave para el negocio
df_cleaned = df_raw.dropna(subset=["CustomerID", "Quantity"])

# Cálculo de columnas enriquecidas
df_cleaned["TotalAmount"] = df_cleaned["Quantity"] * df_cleaned["UnitPrice"]

# Agregación analítica descriptiva
reporte_ventas = df_cleaned.groupby("Country")["TotalAmount"].sum().reset_index()
print(reporte_ventas)
```

---

### Módulo 2: Cómputo Distribuido 
**e Infraestructura Lakehouse**

*   **Justificación:** Una vez que el alumno entiende cómo manipular datos a nivel local, se introduce la limitación física de hardware de una sola máquina. Aquí aprenden el cambio de paradigma hacia la computación elástica, tolerante a fallos y en memoria sobre un clúster distribuido, sentando las bases físicas del Data Lakehouse.
*   **Temas Teóricos:**
    *   Arquitectura distribuida clásica: **Driver y Executors** (Worker Nodes).
    *   Particionamiento físico de datos, data locality y el costo de red en operaciones de barajado (*shuffle*).
    *   Evolución del almacenamiento: de sistemas de archivos planos (Parquet) a tablas transaccionales ACID con **Delta Lake**.
*   **Herramientas y Metodologías:** 
    1. **Apache Spark (PySpark)** y  
    2. **Delta Lake** (formato transaccional).
*   **Competencia Técnica Adquirida:** Ingesta distribuida escalable de datos masivos y persistencia en un Data Lakehouse con soporte transaccional e indexación física.

```python showLineNUmbers
# Módulo 2: Procesamiento de datos distribuido en clúster con PySpark y Delta Lake
from pyspark.sql import SparkSession
import pyspark.sql.functions as F

spark = SparkSession.builder \
    .appName("Modulo2_Lakehouse_ETL") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .getOrCreate()

# Ingesta elástica de gran volumen de datos (Capa Bronze)
df_bronze = spark.read.parquet("s3://raw-lakehouse/ventas_diarias/")

# Transformación masiva paralela (Capa Silver)
df_silver = df_bronze.dropna(subset=["CustomerID"]) \
                     .withColumn("UnitPrice", F.col("UnitPrice").cast("double")) \
                     .withColumn("Revenue", F.col("Quantity") * F.col("UnitPrice"))

# Persistencia transaccional ACID en formato Delta con re-particionamiento inteligente
(df_silver.repartition(10, "Country")
 .write.format("delta")
 .mode("overwrite")
 .save("s3://silver-lakehouse/ventas_validadas"))
```

---

### Módulo 3: Orquestación de Tareas
**DataOps y Gobernanza**

*   **Justificación:** Con los datos ya procesados en el clúster, los alumnos deben aprender a automatizar estas tareas periódicamente, garantizando la reproducibilidad y el manejo robusto de excepciones (DataOps). Asimismo, se aborda la gobernanza de datos para asegurar el control de accesos y linaje.
*   **Temas Teóricos:**
    *   Orquestación lógica mediante **Grafos Acíclicos Dirigidos (DAGs)**.
    *   El nuevo estándar de **Airflow 3**: Desacoplamiento absoluto de la ejecución de tareas de la base de datos de metadatos mediante el **API Server** y el **Task SDK**.
    *   Gobernanza corporativa, seguridad de confianza cero (*zero-trust*) y linaje automatizado (*data lineage*) con **Unity Catalog**.
*   **Herramientas y Metodologías:** 
    1. **Apache Airflow 3** (TaskFlow API, Multi-Executor, callbacks síncronos) 
    2. **Unity Catalog** en entornos Databricks/Cloud.
*   **Competencia Técnica Adquirida:** El estudiante implementa un pipeline de orquestación en Airflow 3 utilizando el Task SDK que monitoriza dinámicamente dependencias de datos.

```python showLineNumbers
# Módulo 3: DAG robusto en Airflow 3 utilizando el nuevo Task SDK
from airflow.sdk import dag, task
from pendulum import datetime

@dag(
    dag_id="dataops_pipeline_gobernado",
    start_date=datetime(2026, 8, 1),
    schedule="@daily",       # Planificación automática e incremental gestionada por el Scheduler
    catchup=False
)
def pipeline_dataops():

    @task
    def extraer_particion_diaria(logical_date=None) -> str:
        """
        Garantiza la idempotencia utilizando la fecha lógica del planificador
        """
        fecha_particion = logical_date.strftime("%Y-%m-%d")
        print(f"Extrayendo datos de forma idempotente para la partición: {fecha_particion}")
        return fecha_particion

    @task
    def ejecutar_etl_distribuido(fecha_particion: str):
        print(f"Iniciando cálculo distribuido en Spark para el lote {fecha_particion}")
        # Aquí se invocaría el job Spark o dbt correspondiente de forma gobernada

    # Dependencias explícitas declaradas de forma nativa por la TaskFlow API
    particion = extraer_particion_diaria()
    ejecutar_etl_distribuido(particion)

pipeline_dataops()
```

---

### Módulo 4: Ciencia de Datos 
**Aplicada y Modelado Predictivo**

*   **Justificación:** Una vez garantizado que la infraestructura de datos es confiable, orquestada e idempotente, la ruta gira hacia el modelado matemático. El estudiante asume el rol del Científico de Datos, consumiendo datos limpios del Lakehouse para entrenar modelos predictivos.
*   **Temas Teóricos:**
    *   Clasificación, regresión, clustering y detección de anomalías.
    *   El ciclo de modelado estadístico: preparación del set de entrenamiento y prueba (*train/test split*), validación cruzada y métricas de desempeño (F1-Score, RMSE, ROC).
    *   Ingeniería de Características (*Feature Engineering*) en series temporales y datos tabulares.
*   **Herramientas y Metodologías:** 
    1. **Scikit-Learn**, 
    2. **TensorFlow** 
    3. **PyTorch**.
*   **Competencia Técnica Adquirida (Código de Muestra):** Entrenamiento y ajuste de hiperparámetros de un estimador predictivo sobre conjuntos de datos tabulares consolidados.

```python showLineNumbers
# Módulo 4: Entrenamiento de un modelo predictivo con Scikit-Learn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

# Carga de características de entrenamiento limpias generadas por Ingeniería de Datos
df_features = pd.read_parquet("features_consolidadas.parquet")

X = df_features[["Quantity", "UnitPrice", "TotalAmount"]]
y = df_features["IsReturned"]  # Variable objetivo

# División determinista del conjunto de datos para evitar sobreajuste (Overfitting)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

# Ajuste del algoritmo de Random Forest
clf = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
clf.fit(X_train, y_train)

precision = clf.score(X_test, y_test)
print(f"Modelo analítico entrenado. Precisión obtenida: {precision:.4f}")
```

---

### Módulo 5: MLOps 
**Operacionalización de la Inteligencia Artificial (El Cierre del Ciclo)**

*   **Justificación:** Este último módulo integra las disciplinas de los dos mundos en un ciclo de vida cerrado. Los estudiantes aprenden a operacionalizar los prototipos matemáticos del Módulo 4 en la infraestructura robusta y escalable del Módulo 2 y 3, aplicando ingeniería de software industrial (MLOps).
*   **Temas Teóricos:**
    *   El ciclo de vida de un modelo de aprendizaje automático: **experimentación, registro, transición de fases y serving**.
    *   Sistemas de inferencia elástica: predicción en lotes (*batch*) frente a inferencia en tiempo real de baja latencia mediante microservicios API.
    *   Observabilidad en MLOps: monitoreo activo de desvíos en la distribución de datos (**Data Drift** e **Inference Logging**).
*   **Herramientas y Metodologías:**
    1. **MLflow** (Tracking, Projects, Models y Model Registry), 
    2. **Docker** y Kubernetes, 
    3. Servidores de inferencia (FastAPI, Triton, Mosaic AI Model Serving) 
    4. Integración continua de modelos (CD4ML).
*   **Competencia Técnica Adquirida:** Registro centralizado y gobernado de un experimento de Machine Learning con tracking de métricas, empaquetado portátil de dependencias y promoción automatizada del modelo al plano de producción.

```python showLineNumbers
# Módulo 5: Operacionalización MLOps con MLflow (Registro y Transición de Estados)
import mlflow
from mlflow.tracking.client import MlflowClient

# Enlace seguro al servidor centralizado de MLOps de la organización
mlflow.set_tracking_uri("http://mlflow-tracking-server:8080")
client = MlflowClient()

run_id = "0f939613782844d9897d319433df5781"
nombre_modelo = "clasificador_abandono_clientes"
model_uri = f"runs:/{run_id}/best-model"

# Registrar el modelo para garantizar linaje y trazabilidad inmutable de la IA
metadata_version = mlflow.register_model(model_uri, nombre_modelo)

# Transicionar el estado del modelo al entorno de producción de forma segura
client.transition_model_version_stage(
    name=nombre_modelo,
    version=metadata_version.version,
    stage="Production",               # Promoción directa al API Gateway de Serving
    archive_existing_versions=True     # Archiva el modelo campeón anterior de forma transparente
)

print(f"Versión {metadata_version.version} promovida con éxito a PRODUCCIÓN para inferencia en tiempo real.")
```

## **Seguimiento de ruta**



- Programación en Python

