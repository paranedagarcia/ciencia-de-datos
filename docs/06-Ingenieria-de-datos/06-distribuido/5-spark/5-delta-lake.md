---
id: deltalake
title: "Delta Lake"
sidebar_label: "Delta Lake"
description: "Como capa de almacenamiento de código abierto"
---

### **¿Qué es Delta Lake?**

**Delta Lake** es una capa de almacenamiento de código abierto diseñada para implementarse sobre los lagos de datos tradicionales (*data lakes*) en la nube (como AWS S3, Azure Data Lake o Google Cloud Storage) con el objetivo de dotarlos de confiabilidad, rendimiento y gobernanza analítica. Actúa como un intermediario transaccional entre el motor de procesamiento distributed (como **Apache Spark**) y el almacenamiento de objetos físicos.

A nivel arquitectónico, Delta Lake resuelve el problema del desorden y la corrupción de datos en los lagos tradicionales (los llamados *data swamps* o pantanos de datos) combinando las capacidades de escala y bajo costo del almacenamiento de objetos con las estrictas garantías **ACID** (Atomaticidad, Consistencia, Aislamiento y Durabilidad) típicas de los almacenes de datos relacionales (*Data Warehouses*). 

Cabe destacar que **Delta Lake no es un nuevo medio o formato físico de almacenamiento**. Los datos de negocio se siguen persistiendo físicamente en archivos estructurados y comprimidos bajo el formato **Apache Parquet**. El núcleo de su innovación radica en la introducción de una capa lógica gestionada por un **registro de transacciones**.

---

### **¿Cómo opera Delta Lake bajo el capó?**

La arquitectura de operación de Delta Lake se fundamenta en la interacción entre los archivos físicos de datos y un registro transaccional centralizado:

#### **1. El Registro de Transacciones (*Delta Log*)**
Cuando se crea una tabla Delta, el sistema genera dentro del directorio físico de la tabla una carpeta especial llamada **`_delta_log`**. Este directorio es la **fuente de verdad absoluta** sobre el estado de la tabla.
* **Archivos Commit JSON:** Cada transacción exitosa (inserción, actualización, borrado) se registra de forma secuencial y atómica como un archivo JSON (por ejemplo, `00000000000000000000.json`, `00000000000000000001.json`, etc.). Este commit almacena metadatos críticos: el tipo de operación, las marcas de tiempo, el usuario que la ejecutó y, principalmente, la lista exacta de archivos Parquet físicos específicos que fueron agregados (*add*) o eliminados (*remove*) lógicamente del estado actual de la tabla.
* **Puntos de control (*Checkpoints*):** Para evitar que el motor de consulta tenga que leer miles de archivos JSON en tablas con alta actividad, Delta Lake genera automáticamente un archivo de punto de control en formato Parquet después de cada **10 commits**. Este checkpoint condensa el estado acumulativo histórico, permitiendo una reconstrucción ultra-rápida de la tabla.

#### **2. Mecanismo de Lectura Segura (Evitando Lecturas Sucias)**
Cuando un consumidor ejecuta una consulta en Spark (`SELECT * FROM table`), el motor de ejecución de Delta no escanea directamente el directorio de almacenamiento. Primero **consulta el *Delta Log*** para identificar el último archivo JSON (o checkpoint) válido. El log le indica a Spark exactamente qué archivos Parquet físicos contienen los datos válidos y cuáles deben ignorarse (por haber sido marcados para eliminación lógica).

#### **3. Mecanismo de Escritura, Actualización y Eliminación (Copy-on-Write)**
Dado que los archivos Parquet son inmutables por diseño (no se pueden modificar físicamente una vez escritos), Delta Lake utiliza una estrategia de **Copia en Escritura (*Copy-on-Write*)** para actualizar y borrar registros de manera transaccional:
* **Escritura e Inserción:** Se escriben nuevos archivos Parquet y se añade un commit JSON registrando la acción (*add*) de estos ficheros.
* **Actualización y Borrado (*UPDATE / DELETE*):** Si se modifica o borra un registro contenido en un archivo Parquet (por ejemplo, `part-1.parquet`), Delta Lake lee dicho archivo, descarta los registros eliminados o aplica los cambios sobre los actualizados, y escribe una nueva versión en un archivo diferente (por ejemplo, `part-3.parquet`). Luego, añade un commit al log que marca al archivo antiguo como removido lógicamente (*remove*) y al nuevo como agregado (*add*). 
* **Tolerancia a fallos:** Si una tarea de escritura falla a mitad del proceso (por ejemplo, por corte de energía o desbordamiento de memoria), los archivos Parquet incompletos o corruptos quedarán físicamente en el disco, pero al no haberse escrito el commit JSON en `_delta_log`, los lectores concurrentes jamás verán esa información incompleta.

#### **4. Validación y Evolución del Esquema (*Schema Enforcement & Evolution*)**
Delta Lake es una arquitectura de **esquema en escritura** (*schema-on-write*). Al momento de escribir registros, valida que el DataFrame de entrada se ajuste estrictamente a la estructura de la tabla (tipos de datos y nombres de columna) en el log. Si detecta inconsistencias, interrumpe la operación para prevenir la corrupción de los datos analíticos. No obstante, permite habilitar la evolución dinámica de esquemas a través de la directiva `mergeSchema` si se requiere incorporar nuevos atributos de negocio de forma incremental.

#### **5. Viaje en el Tiempo (*Time Travel*) y Compactación (*VACUUM*)**
Debido a que Delta Lake no borra físicamente los archivos marcados como eliminados (*remove*) en el log, conserva un histórico inmutable de todos los estados previos de la tabla. Esto permite realizar consultas analíticas retrospectivas (*Time Travel*) para auditar datos, reproducir experimentos de Machine Learning o revertir desastres mediante la sintaxis `VERSION AS OF` o `TIMESTAMP AS OF`. Para eliminar permanentemente los archivos obsoletos y reducir costos de almacenamiento en la nube, se ejecuta el comando físico **`VACUUM`**.



### *Ejemplo Práctico en PySpark

<br />
<Tabs>
<TabItem value="mnp" label="Ejemplo" default>
<div class="alert alert--primary">
**Implementación y Operación**

Se presenta un código estructurado en Python que ejemplifica cómo interactuar con Delta Lake utilizando su API nativa para simular un proceso de actualización, auditoría histórica y viaje en el tiempo:
</div>
</TabItem>
<TabItem value="mnp-python" label="💻 Código">

```python showLineNumbers
# Implementación en Python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit

# 1. Inicialización de la sesión de Spark configurada para Delta Lake
spark = SparkSession.builder \
    .appName("ClaseMaestraDeltaLake") \
    .master("local[*]") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()

# Ruta física del almacenamiento de la tabla Delta (Data Lake simulado localmente)
ruta_tabla_delta = "/tmp/delta_lending_club"

# 2. Ingesta inicial: Datos de solicitantes de préstamos (Capa Bronze)
datos_prestamos = [
    (1001, "Jules Damji", 15000.0, "CA"),
    (1002, "Brooke Wenig", 24000.0, "TX"),
    (1003, "Denny Lee", 18500.0, "WA")
]
schema_columnas = ["loan_id", "cliente", "monto_financiado", "addr_state"]

df_inicial = spark.createDataFrame(datos_prestamos, schema_columnas)

# Escritura en formato Delta (Esto creará los Parquet y la carpeta _delta_log)
df_inicial.write.format("delta").mode("overwrite").save(ruta_tabla_delta)

# 3. Modificación Transaccional: Actualización lógica (UPDATE)
# Para realizar operaciones DML eficientes, importamos el modulo nativo de DeltaTable
from delta.tables import DeltaTable

delta_table = DeltaTable.forPath(spark, ruta_tabla_delta)

# Modificamos el monto financiado de Denny Lee (ID 1003) por ajuste de riesgo
print(">>> Aplicando actualización transaccional en Delta Lake...")
delta_table.update(
    condition=col("loan_id") == 1003,
    set={"monto_financiado": lit(20000.0)}
)

# 4. Auditoría de Linaje e Historia de la Tabla
# Consultamos de forma granular el log de transacciones para comprobar el versionado
print("=== HISTORIAL DE OPERACIONES (AUDIT LOG) ===")
delta_table.history() \
    .select("version", "timestamp", "operation", "operationParameters") \
    .show(truncate=False)

# 5. Delta Time Travel (Viaje en el Tiempo)
# Comparamos la versión actual (Versión 1) con la versión inicial del lago (Versión 0)
print("=== ESTADO ACTUAL EN PRODUCCIÓN (Versión 1) ===")
spark.read.format("delta").load(ruta_tabla_delta).show()

print("=== ESTADO DE LA TABLA ANTES DE LA ACTUALIZACIÓN (Versión 0) ===")
# Cargamos el snapshot exacto de la tabla de forma determinista usando el log histórico
spark.read.format("delta") \
    .option("versionAsOf", 0) \
    .load(ruta_tabla_delta) \
    .show()

# Apagamos la sesión de Spark de forma limpia
spark.stop()
```
</TabItem>
</Tabs><br />



🧩 La integración de Delta Lake con Apache Spark permite a los ingenieros de datos procesar canalizaciones masivas unificando flujos por lotes (*batch*) y en tiempo real (*streaming*) en una sola arquitectura. ¿Te gustaría que cree una guía interactiva detallada (Tailored Report) en tu panel de **Studio** que profundice en la optimización física de tablas Delta mediante la indexación con curvas multidimensionales **Z-Order** y operaciones de compactación de archivos pequeños?