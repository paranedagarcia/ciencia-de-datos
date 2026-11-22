---
id: plata
title: "Capa Plata"
sidebar_label: "📄 Capa Plata"
description: "Capa Plata"
hide_title: true
---

## **Capa Plata**

Dentro del **modelo medallón** (*Medallion Architecture*) en arquitecturas de *Lakehouse* (como Databricks o Microsoft Fabric), la **capa plata** (*Silver layer*) es la capa intermedia de **refinamiento, validación y estandarización** de los datos. 

A esta etapa se le conoce frecuentemente como la **zona limpia o validada** (*cleansed / validated data*), y su propósito es transformar los datos crudos e inmutables de la capa bronce en una fuente de información estructurada, consistente y fiable.


### Principales características y funciones de la Capa Plata

* **Limpieza y resolución de anomalías:** Se corrigen o filtran inconsistencias en los registros, gestionando valores nulos o incompletos y eliminando registros inválidos o corruptos.

* **Deduplicación:** Se aplican procesos para eliminar registros repetidos a través de claves de negocio únicas, garantizando unicidad y consistencia en los datos.

* **Estandarización y tipado de esquemas:** Los formatos heterogéneos y dispersos de la capa bronce se transforman y castean a esquemas rigurosos y estandarizados (por ejemplo, normalizando representaciones de fechas, códigos numéricos o cadenas de texto).

* **Enriquecimiento básico:** Se añaden metadatos contextuales, transformaciones iniciales y cálculos derivados (como columnas técnicas de auditoría, marcas temporales o transformaciones funcionales).

* **Formato estructurado y transaccional:** Comúnmente se almacena en formatos columnares abiertos como **Delta Lake (Delta Parquet)**. Esto aporta soporte para transacciones ACID, versionado (*time travel*) y rendimiento optimizado de lectura y consulta.



### Rol y consumidores dentro del flujo de datos

| Aspecto | Capa Plata (*Silver*) |
| :--- | :--- |
| **Origen** | Lee datos brutos directamente desde las tablas o archivos de la **capa bronce**. |
| **Destino** | Alimenta las agregaciones y modelos dimensionales de la **capa oro**, y suministra datos limpios a proyectos de analítica avanzada. |
| **Usuarios principales** | Es el entorno predilecto para **ingenieros de datos**, analistas avanzados y **científicos de datos**, quienes pueden realizar análisis exploratorios, entrenar modelos de *machine learning* o construir prototipos sobre datos ya curados sin sufrir el ruido ni los errores de la capa cruda. |


***
## **Herramientas**

Para transformar datos desde la **capa Bronce** (datos crudos, históricos e inmutables) hacia la **capa Plata** (datos filtrados, limpios, tipados y estandarizados), se utilizan diversas herramientas clasificadas según su rol operativo en la arquitectura:

### Motores de Cómputo Distribuido y Cuadernos (Code-First)

Son las herramientas predilectas para transformaciones a gran escala, complejas o sobre datos semiestructurados:
*   **Apache Spark y Azure Databricks:** Es el estándar por excelencia para procesar grandes volúmenes de datos. Permite desarrollar rutinas en **PySpark, Scala o Spark SQL** mediante *notebooks* para leer datos crudos, eliminar duplicados, descartar valores nulos, estandarizar esquemas y ejecutar operaciones `MERGE` (upsert) en el destino.

*   **Delta Live Tables (DLT):** Funcionalidad de Databricks que permite construir canalizaciones declarativas con reglas automáticas de gobernanza y validación de calidad de datos (*expectations*).

*   **Spark Pools en Azure Synapse y Microsoft Fabric:** Entornos Spark administrados y preconfigurados para limpiar y validar datasets masivos directamente sobre lagos de datos (ADLS Gen2 u OneLake) sin mover físicamente la información.


### Integración y ETL/ELT

Facilitan la preparación visual de datos y la orquestación automatizada de los pipelines:
*   **Azure Data Factory / Fabric Data Factory:**
    *   **Data Pipelines:** Orquestan y programan dependencias de ejecución secuencial (como desencadenar primero la carga a Bronce y luego ejecutar cuadernos o scripts hacia Plata).
    *   **Dataflow Gen2 / Mapping Data Flows:** Ofrecen una interfaz visual y de bajo código (*low-code/no-code*) basada en Power Query para filtrar registros, tipar columnas y unir datos a escala ejecutándose sobre infraestructura Spark.

*   **AWS Glue:** Servicio ETL *serverless* que ejecuta trabajos sobre clústeres Spark automatizados. Permite generar y ejecutar scripts en Python/Scala, convertir datos brutos a formatos columnares optimizados (como Delta Lake o Parquet) y aplicar transformaciones de deduplicación mediante algoritmos integrados (como *FindMatches*).

*   **Google Cloud Dataprep y Cloud Dataflow:** Dataprep permite explorar y limpiar datos de forma interactiva sugiriendo patrones de transformación, ejecutando las cargas subyacentes a través de pipelines de Cloud Dataflow (Apache Beam).


### Herramientas

**dbt (data build tool)** 

Muy adoptada para complementar a motores como Spark y Databricks. Permite escribir transformaciones y selecciones modulares mediante plantillas SQL y archivos de configuración YAML, aplicando pruebas de integridad y facilitando el diseño de tablas con historización (como dimensiones de cambio lento / SCD Tipo 2) al alimentar la capa Plata.

**Delta Lake** 

Más que una herramienta de cálculo, es el **formato y motor de almacenamiento abierto** sobre el que se materializa la capa Plata. Construido sobre archivos Parquet con un log de transacciones (`_delta_log`), garantiza **cumplimiento ACID**, imposición de esquemas (*schema enforcement*), versionado (*time travel*) y soporte nativo para comandos de actualización y combinación (`UPDATE`, `DELETE`, `MERGE`) esenciales para consolidar los datos limpios.


### Resumen de selección

| Escenario / Perfil | Herramienta Recomendada | Beneficio Clave |
| :--- | :--- | :--- |
| **Ingeniería de datos avanzada / Big Data masivo** | Apache Spark / Databricks (PySpark, Scala) | Máximo control, escalado distribuido y optimización de consultas complejas. |
| **Enfoque analítico declarativo / SQL** | dbt + Delta Lake | Modularidad, control de versiones, pruebas de calidad y linaje automático. |
| **Desarrollo sin código (*Low-code / No-code*)** | Dataflow Gen2 / AWS Glue Studio / Dataprep | Interfaz visual interactiva para limpieza y tipado sin escribir código complejo. |
| **Orquestación del flujo end-to-end** | Azure Data Factory / AWS Step Functions / Airflow | Coordinación de dependencias, reintentos y programación automatizada de tareas. |


***
## **Diferencias con bronce**

Las diferencias fundamentales entre la **capa Bronce** y la **capa Plata** dentro del modelo medallón radican en el nivel de refinamiento, la estructura técnica, la mutabilidad y los casos de uso a los que sirven:


#### Estado y Calidad del Dato
* **Capa Bronce (Crudo / *Raw*):** Almacena los datos en su estado original y sin procesar tal como provienen de los sistemas fuente (*as-is*). No se aplican filtros de validación de negocio, por lo que puede contener registros duplicados, valores nulos, registros corruptos o inconsistencias.

* **Capa Plata (Limpio y Enriquecido):** Los datos han sido sometidos a procesos rigurosos de limpieza, filtrado, manejo de valores ausentes y validación de calidad. Las inconsistencias numéricas y de formato se corrigen o descartan antes de persistirlos.

#### Formato y Esquema
* **Capa Bronce:** Puede alojar una amplia variedad de formatos y estructuras dispares (archivos planos CSV, JSON semiestructurados, datos no estructurados o volcados de bases de datos relacionales) con un nivel mínimo de organización y metadatos básicos de ingesta.

* **Capa Plata:** El esquema es estricto, estandarizado y tipado. Los datos se unifican y almacenan en un formato columnar optimizado y abierto, preferentemente **Delta Lake (Delta Parquet)**, lo que garantiza cumplimiento ACID, alto rendimiento y protección contra la corrupción.

#### Operatoria de Escritura: *Append-Only* vs. *Upsert (Merge)*
* **Capa Bronce:** Es generalmente **inmutable y de solo anexado (*append-only*)**. Actúa como un registro histórico permanente y auditable del origen, lo que permite reconstruir o reprocesar cualquier capa posterior en caso de errores en los pipelines analíticos.

* **Capa Plata:** Soporta mutabilidad controlada mediante operaciones de **`MERGE` (upsert)**, eliminando duplicados mediante claves de negocio y actualizando registros ya existentes con sus versiones más recientes (o gestionando tablas de dimensiones de cambio lento / SCD Tipo 2).

#### Audiencia y Consumidores
* **Capa Bronce:** Su acceso suele estar reservado de forma automatizada para ingenieros de datos y procesos de ETL/ELT; no está concebida para el consumo directo del usuario final ni para herramientas de visualización.

* **Capa Plata:** Diseñada para **ingenieros de datos, analistas y científicos de datos**. Sirve de base para analítica fundacional, entrenamiento de modelos de Machine Learning y como punto de partida para construir las tablas de hechos y dimensiones de la **capa Oro**.


#### Resumen comparativo

| Dimensión | Capa Bronce (*Bronze*) | Capa Plata (*Silver*) |
| :--- | :--- | :--- |
| **Nivel de refinamiento** | Datos crudos y sin procesar (*raw / as-is*). | Datos limpios, filtrados y enriquecidos. |
| **Integridad de datos** | Admite registros incompletos, nulos o duplicados. | Deduplicada y validada según reglas de integridad. |
| **Estructura y formato** | Múltiples formatos heterogéneos (CSV, JSON, texto). | Formato columnar estandarizado (Delta Parquet). |
| **Patrón de carga** | Inmutable, anexado continuo (*append-only*). | Incremental con `MERGE` / upsert y control de versiones. |
| **Propósito clave** | Registro histórico fidedigno y trazabilidad. | Base confiable para analítica avanzada y capa Oro. |
| **Consumidores directos** | Pipelines de ingesta y orquestación técnica. | Ingenieros de datos, analistas y científicos de datos. |


***
## 🖥️ **Ejemplo**

Se presentan dos enfoques principales para aplicar transformaciones desde la capa Bronce hacia la capa Plata: mediante **PySpark con `MERGE` en Delta Lake** y mediante **dbt (data build tool)** con materialización incremental y control de calidad.


### Pyspark pipeline
**Pipeline en PySpark con UPSERT (`MERGE`) en Delta Lake**

Este enfoque es el más utilizado en motores de procesamiento distribuido como **Azure Databricks**, **Spark Pools de Synapse** o **Microsoft Fabric**. Permite leer los datos crudos, aplicar limpieza y tipado estricto, y consolidar los cambios en la tabla Delta evitando duplicados.

```python showLineNumbers
from pyspark.sql.functions import col, to_date, trim, current_timestamp
from delta.tables import DeltaTable

# 1. Leer los datos crudos desde la capa Bronce
bronze_df = spark.read.table("bronze.transacciones_raw")

# 2. Limpieza, validación de reglas básicas y tipado de columnas
silver_updates_df = (
    bronze_df
    # Descartar registros nulos o inconsistentes
    .filter(col("id_transaccion").isNotNull() & (col("monto") > 0))
    # Estandarización de texto
    .withColumn("codigo_moneda", trim(col("codigo_moneda")))
    # Tipado explícito de campos
    .withColumn("id_transaccion", col("id_transaccion").cast("long"))
    .withColumn("id_cliente", col("id_cliente").cast("long"))
    .withColumn("fecha_transaccion", to_date(col("fecha_raw"), "yyyy-MM-dd"))
    .withColumn("monto", col("monto").cast("double"))
    # Metadatos de auditoría
    .withColumn("fecha_actualizacion_silver", current_timestamp())
    # Deduplicación de la carga actual por clave primaria/negocio
    .dropDuplicates(["id_transaccion"])
)

# 3. Aplicar MERGE (Upsert) en la tabla Delta de la Capa Plata
silver_table_name = "silver.transacciones"

if spark.catalog.tableExists(silver_table_name):
    silver_delta_table = DeltaTable.forName(spark, silver_table_name)

    (
        silver_delta_table.alias("target")
        .merge(
            source=silver_updates_df.alias("source"),
            condition="target.id_transaccion = source.id_transaccion"
        )
        # Si ya existe la transacción, actualiza con la versión más reciente
        .whenMatchedUpdateAll()
        # Si es nueva, la inserta
        .whenNotMatchedInsertAll()
        .execute()
    )
else:
    # Primera carga: crear y particionar la tabla Silver
    (
        silver_updates_df.write
        .format("delta")
        .mode("overwrite")
        .partitionBy("fecha_transaccion")
        .saveAsTable(silver_table_name)
    )
```


### Data Build Tool
**Pipeline declarativo con dbt (data build tool)**

En arquitecturas donde se prefiere el modelado modular en SQL con control de versiones y pruebas de integridad automáticas, se combinan un modelo SQL incremental y un archivo de configuración de pruebas (YAML).

#### 1. Definición del modelo SQL (`models/silver/stg_transacciones.sql`)
```sql showLineNumbers
{{ config(
    materialized='incremental',
    unique_key='id_transaccion',
    file_format='delta'
) }}

WITH raw_bronze AS (
    SELECT *
    FROM {{ source('bronze', 'transacciones_raw') }}
    WHERE id_transaccion IS NOT NULL
      AND monto > 0
),

cleaned AS (
    SELECT
        CAST(id_transaccion AS BIGINT)       AS id_transaccion,
        CAST(id_cliente AS BIGINT)           AS id_cliente,
        CAST(fecha_raw AS DATE)              AS fecha_transaccion,
        TRIM(codigo_moneda)                  AS codigo_moneda,
        CAST(monto AS DOUBLE)                AS monto,
        CURRENT_TIMESTAMP()                  AS fecha_actualizacion_silver
    FROM raw_bronze
)

SELECT *
FROM cleaned

{% if is_incremental() %}
    -- En ejecuciones incrementales, filtrar únicamente registros nuevos o modificados
    WHERE fecha_transaccion >= (SELECT MAX(fecha_transaccion) FROM {{ this }})
{% endif %}
```

#### 2. Pruebas automáticas de calidad (`models/silver/schema.yml`)
dbt evalúa la integridad de los datos durante la compilación y ejecución antes de promoverlos a la capa Plata:

```yaml showLineNumbers
version: 2

models:
  - name: stg_transacciones
    description: "Tabla de transacciones limpia y estandarizada en capa Plata"
    columns:
      - name: id_transaccion
        description: "Clave primaria de la transacción"
        tests:
          - unique
          - not_null
      - name: monto
        tests:
          - not_null
      - name: codigo_moneda
        tests:
          - accepted_values:
              values: ['USD', 'EUR', 'CLP', 'MXN']
```



### Consideraciones técnicas
1. **Idempotencia:** La lógica de `MERGE` o `unique_key` asegura que reejecutar el pipeline varias veces no cree registros duplicados ni altere los totales.

2. **Control de versiones (*Time Travel*):** Al emplear Delta Lake, cada operación de `MERGE` crea una nueva entrada en el log de transacciones (`_delta_log`), permitiendo consultar el estado exacto de la tabla en momentos anteriores o revertir cambios si una carga resulta anómala.

3. **Mantenimiento:** Tras cargas masivas de datos en la capa Plata, se recomienda ejecutar `OPTIMIZE silver.transacciones ZORDER BY (id_cliente)` para compactar los archivos y acelerar las futuras lecturas.

