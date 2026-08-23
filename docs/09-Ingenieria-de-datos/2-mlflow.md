---
id: mlflow
title: "MLflow"
sidebar_label: "💻 MLflow"
description: "Plataforma de código abierto para gestionar el ciclo de vida completo del aprendizaje automático y de aplicaciones de inteligencia artificial"
slug: /mlflow
---

<center>
<figure>
![](img/mlflow.png)
<figcaption></figcaption>
</figure>
</center>

**MLflow** es una plataforma de código abierto diseñada para gestionar el ciclo de vida completo de los modelos de Machine Learning (ML). Fue creada para resolver uno de los mayores problemas en la transición de la analítica experimental a la producción: la falta de estandarización, la dificultad para reproducir experimentos y la complejidad de desplegar y monitorear modelos en infraestructuras heterogéneas.

Dentro de la **Ingeniería de Datos**, MLflow no se limita a ser una herramienta exclusiva de los Científicos de Datos. Actúa como el **puente de comunicación, gobernanza y operacionalización** entre las canalizaciones de datos (*data pipelines*) y los activos de Inteligencia Artificial.

---

### Los 4 Pilares de MLflow

Para entender cómo opera, debemos analizar sus cuatro componentes principales:

1.  **MLflow Tracking:** Un motor de base de datos de metadatos y una interfaz gráfica que registra y compara ejecuciones (*runs*). Permite almacenar de forma estructurada parámetros de configuración, métricas de evaluación, código fuente y, principalmente, **artefactos** (archivos físicos como pesos de modelos, conjuntos de datos de prueba o gráficos de diagnóstico).

2.  **MLflow Projects:** Un formato de empaquetado estandarizado para organizar el código de manera reproducible. Define las dependencias de software exactas (mediante entornos Conda, archivos `requirements.txt` o contenedores Docker) necesarias para que un proceso de preparación de datos o entrenamiento se ejecute de forma idéntica en cualquier servidor de la red.

3.  **MLflow Models:** Una convención para empaquetar modelos de aprendizaje automático en múltiples "sabores" (*flavors*). Un modelo guardado bajo este formato contiene un archivo de metadatos `MLmodel` que describe cómo el modelo puede ser interpretado por diferentes motores de ejecución (por ejemplo, como una función nativa de Python, un pipeline de Scikit-Learn o una función distribuida de Apache Spark).

4.  **MLflow Model Registry:** Un almacén de datos centralizado y gobernado para la gestión colaborativa del ciclo de vida del modelo. Permite registrar modelos con versiones incrementales, auditar el linaje de quién entrenó el modelo y transicionar su estado lógico a través de etapas de desarrollo controladas (**Staging, Production, Archived**).



### Función de MLflow

El Ingeniero de Datos utiliza MLflow como una pieza de infraestructura clave para resolver desafíos de automatización, escalabilidad y robustez:

#### 1. Implementación de Inferencia en Lote Distribuidora (*Batch Inference*)
Una de las tareas más comunes de un Ingeniero de Datos es tomar un modelo de ML validado y aplicarlo sobre tablas de escala de petabytes. MLflow permite cargar un modelo registrado y transformarlo automáticamente en una **Función Definida por el Usuario de Spark (Spark UDF)**. Esto permite que el modelo se ejecute en paralelo en todos los nodos del clúster de cómputo, procesando millones de filas de manera distribuida directamente sobre una tabla Delta.

#### 2. Asegurar el Linaje de Datos y Modelos (*Data & Model Lineage*)
Bajo las mejores prácticas de **DataOps**, el Ingeniero de Datos debe saber exactamente qué conjunto de datos y qué versión de la base de datos (por ejemplo, el número de commit de una tabla Delta Lake) se utilizó para entrenar cada versión del modelo. MLflow permite registrar en el *Tracking* la firma del esquema de entrada y salida, así como los punteros o URIs de los datos físicos utilizados, garantizando una auditoría completa del flujo.

#### 3. Reducción del *Training-Serving Skew*
El Ingeniero de Datos debe asegurar que las transformaciones matemáticas pesadas aplicadas a los datos de entrenamiento (escalamiento de variables, imputación de nulos) sean exactamente idénticas al procesar los datos de inferencia. MLflow permite empaquetar todo el pipeline de transformación junto con el modelo. El Ingeniero de Datos simplemente despliega el paquete unificado de MLflow, eliminando la necesidad de reescribir la lógica de preprocesamiento en el entorno de producción.

---

### Ejemplo Práctico en PySpark 
**Inferencia Distribuida con MLflow**

El siguiente script en Python es un ejemplo típico de cómo operacionalizar un modelo utilizando **MLflow** y **Apache Spark** para procesar una tabla Delta Lake de gran escala de forma distribuida:

```python showLineNumbers
"""
Carga de un modelo desde el Model Registry de MLflow
y ejecución de inferencia masiva y distribuida en un clúster de Spark.
"""

from pyspark.sql import SparkSession
import mlflow

# 1. Inicialización de la sesión de Spark configurada para Delta Lake
spark = SparkSession.builder \
    .appName("Inferencia_Distribuida_MLflow") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .getOrCreate()

# Enlace al servidor centralizado de MLOps de la organización
mlflow.set_tracking_uri("http://servidor-mlflow-central:8080")

# 2. El Ingeniero de Datos carga la tabla Delta Lake (Capa Silver de producción)
ruta_tabla_delta = "s3://silver-zone/ventas_limpias"
df_ventas = spark.read.format("delta").load(ruta_tabla_delta)

# 3. Transformación del modelo de MLflow a una UDF distribuida de Spark
# Apuntamos al modelo campeón promovido a la etapa de "Production"
model_name = "modelo_retencion_clientes"
model_stage = "Production"
model_uri = f"models:/{model_name}/{model_stage}"

# mlflow.pyfunc.spark_udf genera dinámicamente una función distribuida optimizada
# para ejecutarse en paralelo usando todos los núcleos del clúster de Spark.
predecir_abandono_udf = mlflow.pyfunc.spark_udf(
    spark, 
    model_uri=model_uri, 
    result_type="double"  # Definimos el tipo de dato de salida de la predicción
)

# 4. Ejecución del scoring en paralelo sobre la tabla Delta
# Aplicamos la UDF sobre las columnas de características de la tabla de ventas
df_predicciones = df_ventas.withColumn(
    "probabilidad_abandono",
    predecir_abandono_udf("Quantity", "UnitPrice", "TotalAmount")
)

# 5. Persistencia de los resultados en la Capa Gold para análisis analítico posterior
# Guardamos de forma transaccional y particionada
(df_predicciones.write
 .format("delta")
 .mode("overwrite")
 .option("mergeSchema", "true")
 .save("s3://gold-zone/score_abandono_clientes"))

print("Inferencia en lote distribuida completada con éxito sobre Delta Lake.")
spark.stop()
```

## Machine Learning

## LLM

## Referencias
- https://mlflow.org/
- https://learn.microsoft.com/es-es/azure/databricks/mlflow/
