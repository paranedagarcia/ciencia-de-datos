---
id: parquet
title: "​📦 Apache Parquet"
sidebar_label: "​📦 ​Apache Parquet"
description: "Apache Parquet"
slug: /parquet
---


https://parquet.apache.org/

## **¿Qué es Apache Parquet?**

Apache Parquet es un formato de archivo de código abierto, gratuito y orientado a columnas, diseñado específicamente para ofrecer un alto rendimiento en consultas analíticas rápidas. Se ha consolidado como un estándar en ecosistemas de Big Data y es la opción de almacenamiento por defecto para motores de procesamiento distribuido como Apache Spark.

Debido a sus capacidades técnicas, Parquet juega un rol fundamental en la construcción de arquitecturas modernas de *Data Lakes*.

---

### Características Técnicas

* **Almacenamiento Columnar:** A diferencia de formatos tradicionales basados en filas (como CSV o Avro), Parquet almacena de forma contigua los valores pertenecientes a una misma columna. Esto permite que, al realizar una consulta, el sistema solo lea las columnas estrictamente necesarias para el análisis, reduciendo drásticamente las operaciones de lectura/escritura (I/O) en disco.

* **Diseño Autodescriptivo:** Los archivos Parquet combinan los datos en sí mismos con su esquema y estructura. Se organizan internamente en grupos de filas y fragmentos de columnas, complementados con metadatos que almacenan estadísticas descriptivas (como valores mínimos, máximos y recuentos). Esto facilita herramientas de optimización como el *data skipping*, permitiendo saltar datos irrelevantes sin procesarlos.

* **Codificación Binaria:** Al ser un formato binario, su contenido no es legible a simple vista por humanos. Sin embargo, esta codificación permite que las máquinas interpreten la información directamente sin perder tiempo en costosos procesos de transformación o parseo de texto.

* **Compresión Altamente Optimizada:** La compresión en Parquet se aplica de manera independiente columna por columna. Esto habilita el uso de esquemas de codificación flexibles que se adaptan al tipo de dato subyacente (por ejemplo, enteros, cadenas o fechas), lo que mejora significativamente el ratio de compresión.

* **Optimización *Predicate Pushdown*:** Parquet soporta la evaluación de filtros lógicos en la propia capa de almacenamiento. Los lectores del formato pueden verificar una condición de filtrado sin necesidad de materializar ni deserializar el registro completo, minimizando así el uso de CPU y memoria.



### Ejemplo de Uso en Python

Apache Spark posee integración nativa con Parquet; de hecho, su motor en memoria (Tungsten) está diseñado para aprovechar directamente la estructura de este formato. A continuación, se ilustra cómo interactuar con estos archivos utilizando PySpark:

```python
# Asumiendo que 'spark' es la sesión activa de SparkSession y 'df' un DataFrame existente

# 1. Escritura de un DataFrame a formato Parquet
# Por defecto, Spark guardará el archivo particionado y utilizará el códec de compresión Snappy[cite: 1]
df.write.parquet("/datalake/zona_silver/datos_usuarios.parquet")

# 2. Lectura de un archivo Parquet
# Spark leerá automáticamente el esquema embebido en los metadatos[cite: 1]
df_parquet = spark.read.parquet("/datalake/zona_silver/datos_usuarios.parquet")

# 3. Mostrar los resultados
df_parquet.show(5)

```

### Usos recomendables

El formato Apache Parquet es altamente recomendable en proyectos de ingeniería, específicamente cuando se trabaja con cargas analíticas y grandes volúmenes de información. Al ser un formato binario y orientado a columnas, su diseño está pensado para superar las limitaciones operativas y de rendimiento de los formatos tradicionales basados en filas, como los archivos CSV o JSON.

A continuación, se detallan los escenarios principales donde su uso es altamente recomendado:

### Cargas de Trabajo Analíticas (OLAP)

* **Consultas de exploración y modelado:** Es ideal para escenarios de "escribir una vez y leer muchas veces" (*write once, read many times*), típicos en el análisis de datos.

* **Extracción de características:** Se recomienda cuando las consultas analíticas necesitan acceder solo a columnas específicas (como en el entrenamiento de modelos), ya que su formato columnar evita cargar la tabla entera en memoria.

* **Filtrado avanzado en almacenamiento:** Es la opción indicada si se busca aprovechar técnicas como el *predicate pushdown* o el *data skipping*, donde el motor de consulta filtra los datos irrelevantes leyendo únicamente los metadatos integrados en el archivo.


### Optimización de Costos y Almacenamiento en la Nube

* **Reducción del tamaño físico:** Resulta fundamental cuando se necesita almacenar datos históricos masivos de forma rentable.

* **Compresión eficiente:** Se aconseja su uso para maximizar la compresión, dado que Parquet aplica esquemas de codificación de manera independiente para cada tipo de dato columnar.

* **Eficiencia comprobada:** Es la recomendación estándar en la nube; por ejemplo, AWS señala que Parquet puede consumir hasta 6 veces menos almacenamiento en Amazon S3 y ser el doble de rápido de procesar en comparación con formatos de texto.


### Integración en Arquitecturas Modernas

* **Procesamiento nativo con Apache Spark:** Se recomienda como el estándar por defecto al utilizar Spark, ya que su motor de ejecución en memoria (Tungsten) está diseñado explícitamente para extraer el máximo rendimiento de este formato.

* **Bases para el Data Lakehouse:** Es indispensable si se planea construir un entorno transaccional moderno (Lakehouse), pues formatos de código abierto como Delta Lake y Apache Iceberg utilizan archivos Parquet como su capa de almacenamiento físico subyacente.

* **Manejo de datos no estructurados y NLP:** Se sugiere transformar corpus de texto grandes, que superen unos cientos de megabytes y estén destinados a Procesamiento de Lenguaje Natural (NLP), hacia archivos Parquet para permitir su carga eficiente e incremental.



## **Particionamiento**

El particionamiento es una técnica estructural y arquitectónica clave en la ingeniería de datos que consiste en dividir físicamente la información a través de múltiples carpetas o directorios en el almacenamiento subyacente. Cuando se guarda información en formato Parquet, diseñar un particionamiento eficiente puede mejorar el rendimiento de las aplicaciones en órdenes de magnitud al optimizar drásticamente las lecturas.


### El Mecanismo: *Partition Pruning*

* Al guardar un DataFrame de forma particionada, Spark crea una jerarquía de carpetas basada en los valores de la columna elegida (por ejemplo, estructurando las rutas como `anio=2023/mes=10`).

* Durante el proceso de lectura, si la consulta contiene un filtro sobre la columna de partición, el motor analítico aplica una técnica llamada *partition pruning* (poda de particiones).

* Esto significa que el sistema ignora por completo los directorios que no cumplen con la condición de búsqueda, cargando en memoria de forma exclusiva los archivos relevantes para responder la consulta.


### Elegir la Clave de Partición

Reglas para elegir de mejor manera la clave de partición.

* **Baja Cardinalidad:** La columna designada para particionar debe tener una cardinalidad baja, es decir, pocos valores únicos. Ejemplos comunes y efectivos son atributos de fecha (año, mes) o categorías amplias del negocio.

* **Evitar la Alta Cardinalidad:** Nunca se debe particionar por atributos de gran variabilidad, como identificadores únicos de usuario (User ID) o marcas de tiempo exactas (*timestamps*).

* **El Problema de los Archivos Pequeños:** Utilizar una columna de alta cardinalidad o sobre-particionar los datos genera miles o millones de carpetas diminutas. Este escenario, conocido como el *small files problem*, destruye el rendimiento debido a la sobrecarga de operaciones I/O requeridas para listar y abrir cada archivo.

* **Volumen Objetivo:** Como directriz general, los ingenieros de datos deben aspirar a que cada partición contenga un volumen de datos de al menos 1 GB.



### Implementación y Control de Archivos

Debido a la naturaleza distribuida de Spark, cada tarea (*task*) en paralelo intentará escribir su propio archivo dentro de la partición correspondiente. Para evitar la proliferación indeseada de archivos diminutos, es una práctica recomendada agrupar y consolidar los datos en memoria antes de la escritura, utilizando transformaciones como `repartition()` o `coalesce()`.

```python
# Supongamos que tenemos un DataFrame 'df_compras'

# 1. Consolidar el número de particiones en memoria para evitar múltiples archivos diminutos de salida[cite: 7, 9]
# El número óptimo dependerá del volumen de datos y los núcleos disponibles[cite: 9]
df_optimizado = df_compras.repartition(10)

# 2. Escribir el DataFrame en formato Parquet, creando carpetas físicas por cada fecha[cite: 3, 4]
(df_optimizado.write
    .mode("overwrite")
    .partitionBy("fecha_creacion")
    .parquet("/datalake/zona_silver/compras_particionadas.parquet"))

```
