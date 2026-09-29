---
id: rdd
title: "RDD"
sidebar_label: "RDD"
description: "RDD"
---

## RDD
Los **RDD (Resilient Distributed Datasets)** son la abstracción de datos fundamental y primaria de Apache Spark. Conceptualmente, se definen como una **colección in-memory de objetos** distribuidos a través de los nodos de un clúster que pueden ser operados en paralelo.

A continuación, se detallan sus conceptos y características fundamentales:

### 1. Significado de sus siglas
El nombre describe con precisión sus propiedades principales:
*   **Resilient (Resiliente):** Son tolerantes a fallos; si un nodo falla, el dataset puede reconstruirse automáticamente utilizando la información de su "linaje" (la secuencia de pasos para crearlo).
*   **Distributed (Distribuido):** Los datos se dividen en una o más **particiones** distribuidas en la memoria de los nodos trabajadores (*Workers*) del clúster.
*   **Dataset (Conjunto de datos):** Consiste en registros identificables, que pueden ser líneas de texto, objetos de Python o registros de bases de datos.

### 2. Características clave
*   **Inmutabilidad:** Una vez creado, un RDD no se puede modificar en su lugar. Cualquier operación que parezca modificarlo (como un filtro) en realidad devuelve un RDD completamente nuevo.

*   **Evaluación perezosa (*Lazy Evaluation*):** Spark no ejecuta inmediatamente las transformaciones solicitadas. En su lugar, registra la operación en un grafo acíclico dirigido (DAG) y solo realiza el cómputo cuando se invoca una **acción** que requiere devolver un resultado. Esto permite a Spark optimizar todo el plan de ejecución antes de procesar los datos.

*   **Tipado fuerte:** El RDD puede representar diversos tipos de datos (Integer, String, o tipos personalizados definidos por el desarrollador).

*   **En memoria:** Están diseñados para almacenarse predominantemente en la memoria RAM, lo que los hace ideales para algoritmos iterativos y análisis interactivos, superando la velocidad de modelos como Hadoop MapReduce que guardan datos intermedios en disco.

### 3. Creación de un RDD
Existen tres formas principales de inicializar un RDD:
*   **Carga de datos externos:** Desde sistemas de archivos como HDFS, S3 o archivos locales, y fuentes como bases de datos SQL (vía JDBC) o JSON.

*   **Paralelización:** Tomando una colección existente en el programa (como una lista o un array) y distribuyéndola en el clúster.

*   **Transformación:** A partir de un RDD ya existente.

### 4. Operaciones con RDDs
Las operaciones se dividen estrictamente en dos categorías:
*   **Transformaciones:** Crean un nuevo RDD a partir de uno existente. Ejemplos comunes incluyen `map` (aplica una función a cada elemento), `filter` (selecciona elementos basados en una condición), `flatMap` y `distinct`.

*   **Acciones:** Son las que disparan el cómputo real y devuelven un valor al programa conductor (*Driver*) o guardan los datos en el almacenamiento. Ejemplos incluyen `collect` (trae todos los datos al driver), `count` (cuenta los registros), `reduce`, `first` y `saveAsTextFile`.

### 5. Persistencia y Caché
Por defecto, los RDD se recomputan cada vez que se llama a una acción sobre ellos. Para optimizar el rendimiento cuando un RDD se usará múltiples veces, Spark permite usar los métodos **`cache()`** o **`persist()`**. Esto guarda las particiones computadas en la memoria (o disco, según el nivel configurado) de los ejecutores para un acceso rápido posterior.

## Trabsformaciones comunes en RDD
Las transformaciones en Spark son operaciones que crean un nuevo RDD a partir de uno existente y se caracterizan por su **evaluación perezosa** (*lazy evaluation*), lo que significa que no se ejecutan hasta que una acción lo solicita.

A continuación, se detallan las transformaciones más comunes clasificadas por su propósito:

### 1. Transformaciones Básicas (Elemento a Elemento)
Estas se aplican a cualquier tipo de RDD:
*   **`map(func)`**: Pasa cada elemento del RDD a través de una función y devuelve un nuevo RDD con los resultados. Es una operación uno a uno.

*   **`filter(func)`**: Evalúa una expresión booleana para cada elemento y solo mantiene aquellos que devuelven `true`.

*   **`flatMap(func)`**: Similar a `map`, pero cada elemento de entrada puede mapearse a cero o más elementos de salida, "aplanando" el resultado final (útil para dividir frases en palabras).

*   **`distinct()`**: Elimina los elementos duplicados del RDD para devolver un conjunto de elementos únicos.

### 2. Transformaciones de Conjuntos y Estructura
Permiten combinar RDDs o cambiar su organización física:
*   **`union(otherRDD)`**: Devuelve un nuevo RDD que contiene la unión de los elementos del RDD original y el proporcionado como argumento.

*   **`intersection(otherRDD)`**: Devuelve solo los elementos que están presentes en ambos RDDs.

*   **`subtract(otherRDD)`**: Elimina del RDD original los elementos que también aparecen en el RDD de entrada.

*   **`sortBy(func, ascending)`**: Devuelve un RDD con los elementos ordenados según el criterio especificado.

*   **`repartition(num)` y `coalesce(num)`**: Se utilizan para cambiar el número de particiones. `repartition` puede aumentar o disminuir el número y causa un *shuffle* total, mientras que `coalesce` solo disminuye particiones y es más eficiente al evitar el movimiento masivo de datos si es posible.

### 3. Transformaciones para RDDs de Clave-Valor (*PairRDDs*)
Estas operaciones son fundamentales para el análisis de datos estructurados:
*   **`reduceByKey(func)`**: Agrupa los valores para cada clave y los combina usando una función asociativa y conmutativa. Es muy eficiente porque realiza una reducción local antes del intercambio de datos (*shuffle*).
*   **`groupByKey()`**: Agrupa todos los valores de una misma clave en una sola secuencia. Se recomienda usar `reduceByKey` en su lugar si el objetivo es agregar datos, debido al alto coste de red que genera.
*   **`mapValues(func)`**: Aplica una función solo a los valores de los pares clave-valor, manteniendo las claves originales intactas.
*   **`join(otherRDD)`**: Realiza un *inner join* basado en las claves de dos RDDs, devolviendo pares de la forma `(clave, (valor1, valor2))`.
*   **`leftOuterJoin` / `rightOuterJoin` / `fullOuterJoin`**: Versiones del *join* que permiten mantener registros de uno o ambos lados aunque no haya coincidencia de clave.
*   **`keys()` y `values()`**: Devuelven un nuevo RDD compuesto únicamente por las claves o por los valores del RDD original, respectivamente.

## Tipos de archivos soporta Spark para cargar RDDs
Apache Spark ofrece una amplia variedad de opciones para cargar datos en **RDD (Resilient Distributed Datasets)**, soportando tanto formatos de texto plano como formatos binarios y serializados.

Los tipos de archivos soportados se dividen principalmente en las siguientes categorías:

### 1. Archivos de Texto
*   **Texto plano:** El método `sc.textFile()` permite leer archivos de texto donde cada línea se convierte en un registro del RDD.
*   **Directorios de texto:** El método `wholeTextFiles()` permite leer múltiples archivos de texto pequeños en un directorio, devolviendo pares de clave-valor donde la clave es el nombre del archivo y el valor es su contenido completo.
*   **Formatos estructurados en texto:** Spark puede procesar archivos **JSON** (un objeto por línea), **CSV** y **XML**.

### 2. Formatos Binarios y Serializados
*   **SequenceFiles:** Un formato binario de Hadoop muy común para almacenar pares clave-valor.
*   **ObjectFiles:** Archivos que contienen objetos de Java serializados.
*   **Archivos Pickle:** Formato de serialización específico de Python, útil para persistir datos entre aplicaciones PySpark.
*   **Protocol Buffers (Protobufs):** Spark soporta formatos codificados binarios serializados como estos.

### 3. Formatos Columnares
Aunque estos suelen cargarse inicialmente como **DataFrames**, pueden convertirse fácilmente a RDDs:
*   **Parquet:** Formato de almacenamiento columnar optimizado para el ecosistema Hadoop y Spark.
*   **ORC (Optimized Row Columnar):** Formato eficiente para datos estructurados, común en entornos Hive.
*   **Avro:** Formato de serialización binario compacto y dependiente del esquema.

### 4. Soporte para Compresión
Spark puede leer de forma nativa varios formatos de archivos comprimidos, siempre que los códecs correspondientes estén disponibles en el sistema:
*   **Gzip** y **ZIP** (usando el método DEFLATE).
*   **BZIP2**.
*   **Snappy**, **LZO**, **LZ4** y **LZF**.

Es importante destacar que Spark intenta leer estos archivos desde sistemas de almacenamiento distribuidos como **HDFS, Amazon S3 o Azure Storage**, aprovechando la localidad de los datos para optimizar el rendimiento.