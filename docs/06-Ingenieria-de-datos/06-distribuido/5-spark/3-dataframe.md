---
id: dataframe
title: "Spark Dataframe"
sidebar_label: "Spark Dataframe"
description: "Representa una tabla de datos con filas y columnas"
---


Un **Spark DataFrame** es una estructura de datos bidimensional distribuida en memoria que organiza la información en filas y columnas estructuradas bajo un esquema definido. 

Conceptualmente, es el **análogo directo de una tabla en una base de datos relacional, una hoja de cálculo con encabezados, o un DataFrame de la librería Pandas**. Sin embargo, la diferencia fundamental radica en su almacenamiento físico: mientras que un DataFrame de Pandas o de R reside estrictamente en la memoria local de un único computador, **un Spark DataFrame distribuye sus datos (en fragmentos lógicos llamados particiones) a lo largo de un clúster de múltiples computadoras**, permitiendo procesar volúmenes masivos de datos (escala de petabytes) de manera paralela y elástica.

---

### Propiedades Fundamentales

Para comprender la ingeniería detrás de un Spark DataFrame, es necesario analizar sus tres pilares arquitectónicos:

*   **Inmutabilidad (*Immutability*):** Al igual que las estructuras primitivas de Spark, un DataFrame es estrictamente inmutable. Esto significa que no es posible modificar celdas o columnas en caliente; en su lugar, cualquier manipulación (como agregar una columna o aplicar un filtro) genera internamente un **nuevo DataFrame** que hereda el estado anterior.

*   **Evaluación Perezosa (*Lazy Evaluation*):** El proceso de creación y transformación de un DataFrame (mediante métodos de transformación como `select()`, `where()`, `filter()` o `groupBy()`) no ejecuta inmediatamente ningún cálculo computacional distribuido ni carga los datos en memoria. Spark se limita a registrar las transformaciones de manera lógica en una bitácora llamada **lineaje de datos** o Grafo Acíclico Dirigido (DAG). El cómputo solo se dispara físicamente cuando el usuario ejecuta una **acción** (como `show()`, `count()`, `collect()` o `write()`).

*   **Catalyst Optimizer (Planificación y Optimización):** Gracias a que el DataFrame posee un esquema de datos que expone de forma explícita nombres de columnas y tipos de datos, Spark no ve las operaciones como código de caja negra. Por el contrario, al activarse una acción, el optimizador **Catalyst** analiza el DAG de transformaciones lógicas y lo reordena (por ejemplo, aplicando técnicas como *predicate pushdown* para filtrar registros antes de su lectura física), compilándolo en un plan de ejecución de bytes ultraeficiente para los nodos trabajadores del clúster.



### Diferencia con los RDD 

El RDD (Resilient Distributed Datasets) es el objeto de datos primitivo e inmutable de bajo nivel en Apache Spark. En las primeras versiones de Spark, toda la programación se realizaba mediante RDDs. No obstante, presentan limitaciones fundamentales de rendimiento que el DataFrame resuelve:

*   **Opacidad del Dato:** Un RDD es una colección distribuida de objetos opacos (es decir, Spark no conoce ni entiende qué atributos o estructuras internas tiene el objeto, interpretándolo simplemente como una lambda funcional). Un DataFrame, en cambio, estructura el registro en la clase especializada **`pyspark.sql.Row`**, permitiendo operaciones relacionales estructuradas sobre columnas explícitas.

*   **Diferencias por Lenguaje:** Al operar con RDDs, el código escrito en Python sufría un fuerte impacto de rendimiento debido a la constante serialización de datos entre la máquina virtual de Java (JVM) y el intérprete de Python. Con el API de DataFrames, dado que toda la lógica declarativa se compila mediante Catalyst directamente a código binario optimizado en la JVM de los ejecutores, **el rendimiento de escribir código en Python (PySpark) es idéntico al de Scala o Java**.

*   **Soporte de Tipado en la JVM:** En lenguajes de tipado estático (como Scala y Java), un DataFrame es en realidad un alias para un conjunto de datos sin tipar en tiempo de compilación (`Dataset[Row]`). En Python, debido a la naturaleza dinámica del lenguaje, no existe el concepto de *Datasets* fuertemente tipados; **todo el procesamiento estructurado se maneja exclusivamente a través del objeto DataFrame**.



#### Ejemplo en Python (PySpark)
<Tabs>
<TabItem value="mnp" label="Ejemplo" default>
<div class="alert alert--primary">
**Spark DataFrame**

El siguiente script ilustra cómo declarar un esquema de forma explícita utilizando los bloques de tipo de PySpark, crear un DataFrame a partir de datos locales y ejecutar operaciones de transformación secuenciales (Lazy) y acciones (Eager):
</div>
</TabItem>
<TabItem value="mnp-python" label="💻 Código">


```python showLineNumbers title="Creación, transformación y acción sobre un Spark DataFrame"
"""
Ejemplo: Creación, transformación y acción sobre un Spark DataFrame.
Estilo: Técnico, explícito y de alta legibilidad.
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit
# Importamos los tipos nativos para definir el esquema de datos (Schema)
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType

# 1. Inicialización de la sesión de Spark (Driver)
spark = SparkSession.builder \
    .appName("Entendiendo_Spark_DataFrames") \
    .master("local[*]") \
    .getOrCreate()

# 2. DEFINICIÓN DEL ESQUEMA (Best Practice en producción)
# En lugar de usar la inferencia de esquemas (la cual fuerza a Spark a leer los datos dos veces),
# definimos de forma explícita las columnas, tipos y si aceptan nulos (True) o no (False).
esquema_estudiantes = StructType([
    StructField("id_alumno", IntegerType(), False),
    StructField("nombre", StringType(), True),
    StructField("nota_promedio", DoubleType(), True),
    StructField("sede", StringType(), True)
])

# 3. CREACIÓN DEL DATAFRAME
# Ingesta desde una colección local (proceso Driver) utilizando el esquema explícito
datos_locales = [
    (1, "Sofia Garcia", 6.8, "Madrid"),
    (2, "Mateo Rodriguez", 5.2, "Barcelona"),
    (3, "Elena Fernandez", 4.1, "Sevilla"),
    (4, "Lucas Blanco", 6.2, "Madrid")
]

df_estudiantes = spark.createDataFrame(datos_locales, schema=esquema_estudiantes)

# Acción inmediata para inspeccionar el esquema de tipo árbol en consola
print("=== ESQUEMA DEL DATAFRAME ===")
df_estudiantes.printSchema()

# 4. TRANSFORMACIONES (Operaciones Perezosas - Lazy)
# Aplicamos filtros y columnas calculadas. No se ejecuta computación física en el clúster.
df_filtrado_enriquecido = df_estudiantes \
    .where(col("nota_promedio") >= 5.0) \
    .withColumn("aprobado", lit(True)) \
    .select("nombre", "nota_promedio", "sede", "aprobado")

# 5. ACCIÓN (Operación Eager)
# Aquí Spark ejecuta el plan de optimización Catalyst y distribuye el cómputo en el clúster
print("=== RESULTADO DE LA ACCIÓN (Estudiantes Aprobados) ===")
df_filtrado_enriquecido.show()

# Apagamos la sesión de Spark de forma limpia
spark.stop()
```
</TabItem>
</Tabs>




## **Lazy Evaluation**

La **evaluación perezosa** (*Lazy Evaluation*) es uno de los principios de diseño y rendimiento más fundamentales de Apache Spark. Esta propiedad determina que **Spark no ejecuta de manera inmediata las transformaciones de datos que declaras en el código**; en su lugar, difiere cualquier computación física real hasta el último momento posible, específicamente hasta que se invoca una **acción**.

Cuando escribes transformaciones en Spark (como filtrar registros, seleccionar columnas o agrupar datos), el sistema no carga ni procesa los datos en memoria en ese instante. En su lugar, el nodo controlador (*driver*) registra estas instrucciones en una bitácora o plano lógico inmutable, construyendo un **lineaje de datos** representado mediante un **Grafo Acíclico Dirigido (DAG)**.

---

### La Frontera Técnica: Transformaciones vs. Acciones

Para comprender cómo opera la evaluación perezosa, es mandatorio diferenciar el conjunto de operaciones de Spark en dos categorías lógicas:

*   **Transformaciones (Perezosas / *Lazy*):** Operaciones que toman un DataFrame o RDD y devuelven uno nuevo (debido a la inmutabilidad de los datos) sin alterar la fuente ni realizar cómputos físicos. Ejemplos clave de transformaciones son `select()`, `filter()`, `where()`, `join()`, y `groupBy()`. Incluso la lectura inicial de datos (`spark.read`) se considera una transformación perezosa.
*   **Acciones (Impacientes / *Eager*):** Operaciones que devuelven un valor final al programa conductor o escriben datos físicamente en un medio de almacenamiento externo. Las acciones actúan como el interruptor que **dispara de manera inmediata la ejecución de toda la cadena de transformaciones pendientes** en el DAG. Ejemplos de acciones son `show()`, `count()`, `collect()`, y `write` (ej. `write.parquet()` o `write.csv()`).

---

### Ventajas de Ingeniería

Bajo el capó, esta pereza computacional no es una limitación, sino la estrategia que otorga a Spark su sobresaliente velocidad y eficiencia en Big Data:

#### A. Optimización Global del Plan (Catalyst Optimizer)
Al no ejecutar el código paso a paso, Spark dispone del flujo completo de operaciones antes de tocar un solo byte de datos. El optimizador de consultas de Spark (**Catalyst**) analiza el DAG y compila un plan físico óptimo. Un ejemplo de esto es el **Predicate Pushdown** (poda por predicado): si aplicas un filtro al final de un pipeline complejo, Catalyst "empuja" ese filtro directamente al momento de la lectura física del archivo, evitando escanear gigabytes de datos innecesarios.

#### B. Reducción de Huella de Memoria e I/O
En sistemas de evaluación impaciente (como Pandas local), cada paso secuencial crea y manifiesta un DataFrame intermedio en la memoria RAM. En Spark, al encadenar transformaciones estrechas (*narrow dependencies*, como filtros o proyecciones), el motor aplica una técnica llamada **pipelining** (canalización). Esto significa que los registros se transforman en una sola pasada en la CPU de forma contigua, reduciendo drásticamente la huella de memoria y los accesos a disco.

#### C. Tolerancia a Fallos y Resiliencia Eficiente
Dado que Spark almacena de forma determinista el lineaje completo de transformaciones de cada partición de datos, si un nodo ejecutor falla en medio de un proceso, Spark no requiere reiniciar todo el pipeline desde el principio. Simplemente lee la porción de datos de origen requerida y **vuelve a aplicar de forma selectiva el lineaje registrado** sobre el subconjunto afectado, logrando resiliencia con un costo computacional mínimo.

---

#### Demostración en Python (PySpark)

<Tabs>
<TabItem value="mnp" label="Ejemplo" default>
<div class="alert alert--primary">
**Evaluación Perezosa en Spark**

El siguiente script ilustra cómo se comporta la evaluación perezosa en un entorno de ejecución distribuido de PySpark:
</div>
</TabItem>
<TabItem value="mnp-python" label="💻 Código">

```python showLineNumbers title="Evaluación Perezosa en Spark"
"""
Ejemplo: Demostración de la Evaluación Perezosa en Spark.
"""

from pyspark.sql import SparkSession
import time

# 1. Inicialización del Driver de Spark
spark = SparkSession.builder \
    .appName("ClaseMaestra_LazyEvaluation") \
    .master("local[*]") \
    .getOrCreate()

# Ruta simulada
ruta_datos = "s3://mi-bucket-seguro/ventas_grandes.parquet"

print(">>> Fase 1: Creando el DataFrame (Operación Perezosa)")
inicio_df = time.time()

# Esta instrucción NO lee el archivo Parquet completo en memoria.
# Spark simplemente abre el archivo para validar el esquema y los metadatos.
df_ventas = spark.read.format("parquet").load(ruta_datos)

fin_df = time.time()
print(f"✓ DataFrame registrado lógicamente en {fin_df - inicio_df:.4f} segundos.\n")


print(">>> Fase 2: Aplicando Transformaciones (Operaciones Perezosas)")
inicio_trans = time.time()

# Aplicamos transformaciones lógicas. No hay cómputo físico en el clúster.
# Spark construye el DAG lógicamente incorporando estas transformaciones.
df_filtrado = df_ventas.where("monto_total > 500.0")
df_resultado = df_filtrado.select("id_cliente", "monto_total")

fin_trans = time.time()
print(f"✓ Lineaje (DAG) construido en {fin_trans - inicio_trans:.4f} segundos.")
print("Nota: Aún no se ha procesado ninguna fila del archivo en el clúster.\n")


print(">>> Fase 3: Invocando una Acción (Operación Impaciente / Eager)")
print("Disparando la computación física en el clúster...")
inicio_accion = time.time()

# La acción .count() fuerza a Spark a compilar el plan con Catalyst,
# ejecutar la lectura, aplicar el filtro y retornar el entero resultante al driver.
total_registros_filtrados = df_resultado.count()

fin_accion = time.time()
print(f"✓ Acción completada con éxito.")
print(f"• Total de registros que cumplen la condición: {total_registros_filtrados}")
print(f"• Tiempo de procesamiento físico real: {fin_accion - inicio_accion:.4f} segundos.\n")

spark.stop()
```
</TabItem>
</Tabs>



