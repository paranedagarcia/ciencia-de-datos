---
id: bronce
title: "Capa Bronce"
sidebar_label: "📄 Capa Bronce"
description: "Capa Bronce"
hide_title: true
---

## **Capa Bronce**

Dentro del **modelo medallón** (*Medallion Architecture*), la **capa bronce** (*Bronze layer*) es la capa inicial de ingesta y almacenamiento de datos brutos (*raw data*). 

Esta capa funciona como la puerta de entrada al *data lakehouse*, preservando la información en su estado más puro tal como proviene de los sistemas de origen.


### Características

1. **Datos en estado crudo (*Raw Data / As-is*):**
   * Los datos se ingieren y almacenan en su formato nativo o en un estado *"tal cual"* (*as-is*) sin alterar su contenido ni aplicar reglas de negocio o transformaciones complejas.
   * Se admite una amplia variedad de fuentes y formatos: datos estructurados (tablas relacionales, CSV), semiestructurados (JSON, XML) o no estructurados (registros de log, telemetría IoT, eventos).

2. **Registro histórico inmutable y auditable (*Single Source of Truth* de origen):**
   * Actúa como un archivo o histórico inmutable (*append-only*), donde habitualmente se van anexando los registros y archivos nuevos.
   * Al conservar los datos en su estado original, ofrece trazabilidad y permite reprocesar o reconstruir las etapas posteriores (*Silver* y *Gold*) en caso de errores en los pipelines o cambios en las reglas analíticas.

3. **Particionamiento y metadatos básicos:**
   * Aunque los datos no se depuran en esta etapa, comúnmente se les añaden metadatos técnicos mínimos para su gestión, tales como etiquetas del sistema fuente, identificadores de lote o esquemas de partición por fecha/hora (por ejemplo, `YYYYMMDD`) para facilitar lecturas incrementales y depuraciones.

4. **Formato de almacenamiento:**
   * En plataformas modernas como Databricks o Microsoft Fabric, los datos en la capa bronce suelen almacenarse en el almacenamiento de objetos (como Azure Data Lake Storage Gen2 o Amazon S3). 
   * A menudo se almacenan como archivos planos o se estructuran directamente en formato abierto optimizado como **Delta Lake (Delta Parquet)** para habilitar transacciones ACID y capacidades de *time travel* desde el primer nivel.



### El rol

| Capa | Estado del Dato | Propósito principal |
| :--- | :--- | :--- |
| **Bronce (*Bronze*)** | **Bruto / Crudo (*Raw*)** | Ingesta de fuentes heterogéneas, persistencia histórica y registro auditable sin transformaciones. |
| **Plata (*Silver*)** | **Limpio y estandarizado** | Filtrado, deduplicación, resolución de valores nulos, tipado de datos y enriquecimiento. |
| **Oro (*Gold*)** | **Consumo de negocio** | Agregaciones, modelos dimensionales (estrella/copo de nieve) y tablas listas para analítica, reportes BI y toma de decisiones. |


## **Pipeline**

El pipeline de transición entre la **capa Bronce** y la **capa Plata** es el núcleo de la ingeniería de datos en una arquitectura Medallón: transforma datos crudos, dispares e inmutables en una **fuente limpia, tipada, validada y estructurada** en formato Delta Lake.

A continuación se detalla su arquitectura, etapas operativas y un ejemplo práctico de implementación en **PySpark**.

---

### Responsabilidades clave de la Capa Plata
A diferencia de la capa Bronce (que conserva los datos tal como llegan del origen), el procesamiento hacia la capa Plata debe resolver:
* **Aplicación de esquemas y tipado estricto:** Castear columnas desde tipos genéricos (como cadenas de texto) a enteros, dobles, booleanos o fechas formales.
* **Limpieza de calidad de datos:** Tratar o descartar registros con valores nulos críticos, eliminar espacios en blanco y filtrar inconsistencias numéricas.
* **Deduplicación:** Eliminar duplicados mediante funciones nativas (`dropDuplicates`) basadas en identificadores de negocio.
* **Enriquecimiento y derivación:** Añadir columnas calculadas (como partes de fechas o códigos de estado).
* **Persistencia ACID y Merge incremental:** Guardar en formato Delta Lake y aplicar operaciones `MERGE` (upsert) para actualizar registros existentes e insertar los nuevos manteniendo el historial de transacciones.

---

### Implementación del Pipeline en PySpark (Notebook)

El siguiente flujo ilustra el procesamiento incremental desde archivos o tablas en la capa Bronce hacia una tabla Delta en la capa Plata:

```python
from pyspark.sql.functions import col, to_date, trim, when, current_timestamp
from delta.tables import DeltaTable

# -------------------------------------------------------------
# 1. Lectura de los datos crudos desde la Capa Bronce
# -------------------------------------------------------------
bronze_df = spark.read.format("delta").load("abfss://datalake@account.dfs.core.windows.net/bronze/ventas")

# -------------------------------------------------------------
# 2. Limpieza, Tipado y Estandarización
# -------------------------------------------------------------
silver_cleaned_df = (
    bronze_df
    # Filtro de registros corruptos o incompletos
    .filter(col("id_transaccion").isNotNull() & (col("monto_venta") > 0))
    # Estandarización de textos y eliminación de espacios
    .withColumn("codigo_pais", trim(col("codigo_pais")))
    # Tipado explícito de columnas
    .withColumn("id_transaccion", col("id_transaccion").cast("long"))
    .withColumn("id_cliente", col("id_cliente").cast("long"))
    .withColumn("fecha_venta", to_date(col("fecha_raw"), "yyyy-MM-dd"))
    .withColumn("monto_venta", col("monto_venta").cast("double"))
    # Enriquecimiento técnico
    .withColumn("fecha_procesamiento", current_timestamp())
)

# -------------------------------------------------------------
# 3. Deduplicación por Clave de Negocio
# -------------------------------------------------------------
silver_dedup_df = silver_cleaned_df.dropDuplicates(["id_transaccion"])

# -------------------------------------------------------------
# 4. Carga Incremental vía UPSERT (MERGE) en Delta Lake
# -------------------------------------------------------------
silver_target_path = "abfss://datalake@account.dfs.core.windows.net/silver/ventas"

# Si la tabla ya existe, realizamos un MERGE; si no, la inicializamos
if DeltaTable.isDeltaTable(spark, silver_target_path):
    silver_table = DeltaTable.forPath(spark, silver_target_path)
    
    (
        silver_table.alias("target")
        .merge(
            source=silver_dedup_df.alias("source"),
            condition="target.id_transaccion = source.id_transaccion"
        )
        .whenMatchedUpdateAll()
        .whenNotMatchedInsertAll()
        .execute()
    )
else:
    (
        silver_dedup_df.write
        .format("delta")
        .mode("overwrite")
        .partitionBy("fecha_venta")
        .save(silver_target_path)
    )
```

---

### 3. Operación con Delta Live Tables (DLT)
En entornos como **Databricks**, este pipeline puede implementarse de forma declarativa con **Delta Live Tables**, donde se gestionan dependencias y expectativas de calidad mediante decoradores:

```python
import dlt
from pyspark.sql.functions import col

@dlt.table(
    name="ventas_silver",
    comment="Ventas limpias y validadas procedentes de Bronce"
)
@dlt.expect_or_drop("id_valido", "id_transaccion IS NOT NULL")
@dlt.expect_or_drop("monto_positivo", "monto_venta > 0")
def ventas_silver():
    return (
        dlt.read_stream("ventas_bronze")
        .dropDuplicates(["id_transaccion"])
        .select(
            col("id_transaccion").cast("long"),
            col("id_cliente").cast("long"),
            col("fecha_venta").cast("date"),
            col("monto_venta").cast("double")
        )
    )
```

---

### 4. Mantenimiento y Optimización de la Capa Plata
Para mantener un rendimiento óptimo de consulta en tablas Delta de alta concurrencia o volumen masivo:
* **Compactación de archivos (`OPTIMIZE`):** Reorganiza y compacta múltiples archivos pequeños en bloques de mayor tamaño para agilizar la lectura de Spark.
* **Ordenamiento Z-Order:** Agrupa físicamente los datos según las columnas de búsqueda o combinación más frecuentes (por ejemplo, `ZORDER BY (id_cliente)`), acelerando la omisión de datos (*data skipping*).
* **Limpieza de versiones antiguas (`VACUUM`):** Purga archivos Parquet obsoletos fuera del período de retención del log de transacciones (por defecto 30 días o 720 horas) para recuperar espacio en el almacenamiento de objetos.

