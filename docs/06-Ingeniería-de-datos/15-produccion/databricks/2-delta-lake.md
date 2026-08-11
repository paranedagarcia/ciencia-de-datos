---
id: delatalake
title: "Delta Lake"
sidebar_label: "Delta Lake"
description: "Delta Lake"
slug: /deltalake
---


**Delta Lake** es una capa de almacenamiento de código abierto que se ejecuta sobre el almacenamiento de objetos en la nube (como Azure ADLS, Amazon S3 o Google Cloud Storage). Su función principal es **transformar un lago de datos tradicional (Data Lake) en un Data Lakehouse**, combinando la escalabilidad y bajo costo del primero con la confiabilidad, gobernanza y transaccionalidad de un almacén de datos (Data Warehouse).

A continuación se detallan, las ventajas fundamentales de utilizar Delta Lake en el ecosistema de Databricks:

---

#### 1. Transacciones ACID y Consistencia de Datos
Los lagos de datos tradicionales operan bajo el modelo **BASE** (consistencia eventual), careciendo de controles transaccionales. Esto suele provocar problemas de archivos corruptos o lecturas sucias si un proceso de carga falla a mitad de camino. 

Delta Lake introduce **garantías transaccionales ACID** (Atomicidad, Consistencia, Aislamiento y Durabilidad) mediante un **registro de transacciones en formato JSON** llamado **Delta Log** (`_delta_log`). 
* **Atomicidad:** Asegura que una operación de escritura se complete al 100% o no se aplique en absoluto. Si un *pipeline* falla, no se dejan datos parciales o huérfanos; el sistema simplemente ignora los archivos no confirmados en el registro JSON.

* **Aislamiento de Instantáneas (*Snapshot Isolation*):** Permite que los lectores sigan consultando de manera consistente la última versión estable de la tabla mientras múltiples procesos de escritura realizan modificaciones simultáneas en segundo plano.

#### 2. Unificación de Batch y Real-Time (Simplificación de Lambda)
En las arquitecturas tradicionales como **Lambda**, los ingenieros de datos deben mantener y desarrollar dos tuberías (*pipelines*) de datos completamente independientes: una capa de lotes (*batch*) y una capa de velocidad (*streaming*), lo que duplica el código y complejiza la sincronización de datos. 

Con Delta Lake, esta arquitectura se unifica drásticamente. Delta permite que **múltiples consultas de streaming e inserciones por lotes escriban y lean concurrentemente sobre la misma tabla** con garantías exactamente una vez (*exactly-once*). El motor trata la tabla como un flujo infinito (*unbounded table*) al que se le añaden registros continuamente.

#### 3. Validación y Evolución del Esquema (*Schema-on-Write*)
Los lagos de datos convencionales son *schema-on-read* (esquema en la lectura), lo que significa que permiten escribir cualquier archivo corrupto o con tipos de datos incorrectos, trasladando el fallo al analista final.
* **Schema Enforcement (Validación de Esquema):** Delta Lake es de tipo **schema-on-write**; comprueba de forma estricta que cualquier DataFrame que intente escribir en la tabla sea compatible con el esquema registrado a nivel de metadatos. Si hay un conflicto de tipos de datos, la operación se aborta inmediatamente para evitar la corrupción de la tabla.
* **Schema Evolution (Evolución de Esquema):** Si el cambio de esquema es legítimo (por ejemplo, la adición de una nueva columna en el origen), Delta permite la migración automática y segura del esquema simplemente configurando la opción `.option("mergeSchema", "true")` en la escritura. Los registros históricos que no contaban con esa columna se completarán automáticamente con valores `null`.

#### 4. Viaje en el Tiempo (*Time Travel*) y Rollbacks
Dado que los archivos físicos subyacentes de Parquet en Delta Lake son inmutables, las operaciones de actualización (`UPDATE`) o borrado (`DELETE`) no modifican los archivos existentes. En su lugar, Delta escribe nuevos archivos Parquet con los datos modificados y actualiza el **Delta Log** para marcar los archivos antiguos como lógicamente removidos en la última versión de la tabla.

Esto habilita el **Time Travel**: la capacidad de consultar cualquier estado histórico de la tabla haciendo referencia a su número de versión (`versionAsOf`) o a una marca de tiempo específica (`timestampAsOf`). Esto es sumamente útil para:
* Revertir cambios accidentales mediante restauraciones físicas (`RESTORE TABLE`).
* Auditar cambios y cumplir con normativas de gobernanza (p. ej., GDPR).
* Reproducir experimentos de Machine Learning de manera exacta sobre el set de datos original.

#### 5. Operaciones de Manipulación de Datos (DML: UPDATE, DELETE, MERGE)
En un lago de datos puro (por ejemplo, basado en archivos Parquet planos), realizar actualizaciones o borrados requiere reescribir directorios completos manualmente. Delta Lake proporciona soporte nativo y eficiente para comandos DML estándar: `UPDATE`, `DELETE` y `MERGE`. La sentencia `MERGE` es la pieza fundamental para implementar flujos de **Change Data Capture (CDC)** y dimensiones lentamente cambiantes (SCD), permitiendo realizar *upserts* en pocas líneas de código.

#### 6. Optimización y Rendimiento Automatizado en Databricks
Cuando se ejecuta dentro de la plataforma Databricks, Delta Lake se beneficia de optimizaciones exclusivas del motor:

* **Liquid Clustering (Agrupamiento Líquido):** Reemplaza las rígidas particiones físicas tradicionales por un algoritmo dinámico que reorganiza los datos basándose en los patrones de consulta reales. En tablas administradas, se puede configurar simplemente como `CLUSTER BY AUTO`.

* **Predictive Optimization (Optimización Predictiva):** Databricks analiza las transacciones de las tablas y ejecuta de forma automática operaciones de mantenimiento como `OPTIMIZE` (compactación de archivos pequeños para acelerar lecturas) y `VACUUM` (limpieza de archivos obsoletos físicamente no referenciados) en segundo plano.

* **Caché del Delta Log en memoria:** Unity Catalog y el runtime de Databricks pueden cachear el log de transacciones directamente en memoria para evitar latencias de red al consultar el almacenamiento de objetos de la nube.

---

### Ejemplo Práctico en PySpark
**Creación, Evolución de Esquema y Time Travel**

El siguiente script de Python ejemplifica cómo un ingeniero de datos puede interactuar con Delta Lake en un entorno de desarrollo para aprovechar estas ventajas:

```python showLineNumbers
from pyspark.sql import SparkSession
import pyspark.sql.functions as F

# 1. Inicialización de la sesión de Spark con soporte para Delta
spark = SparkSession.builder \
    .appName("DeltaLakeDemo") \
    .master("local[*]") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()

# 2. Ingesta inicial (Capa Bronze / Versión 0)
datos_v0 = [
    (1, "Laptop", 1200.0),
    (2, "Mouse", 25.0)
]
df_v0 = spark.createDataFrame(datos_v0, ["id", "producto", "precio"])

# Guardamos como tabla Delta
ruta_delta = "/workspace/scratch/demo_delta"
df_v0.write.format("delta").mode("overwrite").save(ruta_delta)

# 3. Intento de escritura con esquema incompatible (Provocará error de validación)
# Añadimos la columna 'categoria' que no existe en el esquema original
datos_incompatibles = [(3, "Teclado", 45.0, "Accesorios")]
df_incompatible = spark.createDataFrame(datos_incompatibles, ["id", "producto", "precio", "categoria"])

try:
    df_incompatible.write.format("delta").mode("append").save(ruta_delta)
except Exception as e:
    print("\n[VALIDACIÓN DE ESQUEMA DETECTADA] La escritura falló como se esperaba para proteger la integridad de los datos.\n")

# 4. Evolución de Esquema Explícita (Habilitamos mergeSchema)
# Delta asimilará de forma segura la nueva estructura
df_incompatible.write.format("delta") \
    .option("mergeSchema", "true") \
    .mode("append") \
    .save(ruta_delta)

print("=== TABLA DELTA ACTUAL (Versión 1) ===")
spark.read.format("delta").load(ruta_delta).show()

# 5. Delta Time Travel (Consultamos la Versión 0 del set de datos)
print("=== TIME TRAVEL: Recuperando el estado original (Versión 0) ===")
df_historico = spark.read.format("delta") \
    .option("versionAsOf", "0") \
    .load(ruta_delta)

df_historico.show()

# Detener la sesión de Spark de forma segura
spark.stop()
```
