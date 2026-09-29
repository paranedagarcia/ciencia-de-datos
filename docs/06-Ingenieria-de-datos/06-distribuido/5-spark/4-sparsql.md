---
id: sparksql
title: "Apache Spark SQL"
sidebar_label: "Spark SQL"
description: "Apache Spark SQL"
---


## **Spark SQL**

**Spark SQL** es uno de los módulos nucleares más importantes de **Apache Spark** diseñado específicamente para el **procesamiento de datos estructurados y semiestructurados**. 

Nació en la versión 1.3 de Spark (como sucesor del antiguo proyecto *Shark* y los *SchemaRDDs*) para resolver la opacidad que presentaban las colecciones distribuidas de bajo nivel (los RDDs). Spark SQL introduce una capa relacional de abstracción que permite interrogar y transformar los datos distribuidos utilizando tanto **consultas declarativas en lenguaje SQL** (con soporte para el estándar ANSI SQL:2003) como la **API de DataFrames y Datasets** en lenguajes como Python, Scala, R y Java.

La relevancia de Spark SQL no radica únicamente en permitir escribir sentencias `SELECT`, sino en la **infraestructura de optimización física y en la unificación de APIs** que provee a todo el ecosistema de Spark (incluyendo MLlib para Machine Learning y Structured Streaming para tiempo real).


### Arquitectura Interna

El rendimiento de Spark SQL es idéntico sin importar si el desarrollador escribe una consulta en SQL puro o utiliza la sintaxis funcional de DataFrames. Esto se debe a que ambas interfaces son traducidas a la misma representación lógica interna y optimizadas de forma unificada mediante dos componentes de infraestructura extraordinariamente potentes:

#### A. El Optimizador Catalyst
**Catalyst** es un optimizador de consultas altamente extensible y extensible basado en conceptos de programación funcional. Cuando se envía una consulta a Spark SQL, Catalyst procesa la instrucción a través de cuatro fases de transformación lógica y física:


1.  **Análisis:** Spark genera un árbol de sintaxis abstracta (AST) para la consulta. En esta fase, los nombres de tablas y columnas declarados por el usuario se resuelven consultando el **Catálogo** (que almacena la información de metadatos de las bases de datos y esquemas). Si las columnas o tablas existen y sus tipos coinciden, el plan se convierte en un *Plan Lógico Resuelto*.

2.  **Optimización Lógica:** Catalyst aplica un conjunto de reglas basadas en heurísticas lógicas para simplificar la consulta. Por ejemplo, utiliza la técnica **Predicate Pushdown** (empujar filtros hacia la lectura original para descartar filas antes de moverlas por red) y **Column Pruning** (poda de columnas no requeridas).

3.  **Planificación Física:** A partir del plan lógico optimizado, Spark genera múltiples planes de ejecución física alternativos. A través de un **Modelo de Costo (CBO)**, evalúa variables de hardware (tamaño físico de las tablas, cardinalidad, etc.) para seleccionar el plan físico más eficiente (por ejemplo, eligiendo si realizar un *SortMergeJoin* o un *BroadcastHashJoin*).

4.  **Generación de Código (Whole-Stage Code Generation):** Spark SQL compila el plan físico seleccionado directamente en **Java Bytecode** altamente optimizado para que se ejecute de forma nativa en la máquina virtual (JVM) de los ejecutores, colapsando múltiples fases de transformación en una sola pasada en el CPU de los servidores.

#### B. Project Tungsten: Gestión de Memoria Optimizada
Históricamente, el procesamiento de objetos Java en la memoria de ejecución (*heap*) de la JVM sufría de grandes retrasos debido al costo de serialización y la recolección de basura (*Garbage Collection*) de Java al procesar conjuntos masivos de datos. 

**Tungsten** resuelve este problema estructurando internamente las filas del DataFrame en bloques binarios contiguos directamente en memoria **off-heap** (fuera de la pila de Java) utilizando punteros y direcciones directas de bajo nivel. Para transferir datos de forma instantánea entre la JVM de Spark y las estructuras de Python (como Pandas) sin penalización de velocidad, Spark SQL se apoya opcionalmente en el estándar de buffers de memoria de **Apache Arrow**.


### Conectores e Integración con Orígenes de Datos

Spark SQL funciona como una plataforma federada unificada de consulta de Big Data. Esto significa que, con una sola sesión de Spark (`SparkSession`), un ingeniero puede realizar operaciones de cruce (*JOIN*) entre datos almacenados en formatos físicos completamente heterogéneos:

*   **Formatos de Archivo Nativos:** Spark SQL lee y escribe directamente archivos estructurados y auto-descriptivos como **Parquet, Delta Lake, ORC y Avro**. También puede estructurar archivos no descriptivos (como **JSON y CSV**) registrando previamente sus esquemas e infiriendo su estructura mediante opciones de lectura.

*   **Conectividad JDBC/ODBC (Data Federation):** Mediante el conector JDBC integrado, Spark SQL puede mapear tablas de bases de datos relacionales externas (como PostgreSQL, MySQL o Microsoft SQL Server) como si fuesen tablas locales de Spark. Al consultar estas tablas, Spark "empuja" los filtros directamente al motor de la base de datos de origen para minimizar el tráfico de red.

*   **Integración con Apache Hive:** Spark SQL es compatible con el **Hive Metastore**. Esto le permite compartir la definición de catálogos, esquemas y tablas con otras herramientas analíticas de Big Data (como Presto, Trino o HiveQL), actuando como la estructura lógica de gobernanza del Lakehouse.

*   **Conectividad de Herramientas de Inteligencia de Negocio (BI):** A través del componente **Spark Thrift JDBC/ODBC Server (STS)**, herramientas comerciales como Tableau, Power BI o Talend pueden conectarse directamente al clúster de Spark y enviar consultas analíticas que Spark SQL procesará de forma distribuida en segundos.



#### Ejemplo Práctico de Sinergia (Código PySpark)


<Tabs>
<TabItem value="mnp" label="Antecedentes" default>
<div class="alert alert--primary">
**Spark SQL**

El siguiente script de Python simula cómo se interactúa con **Spark SQL**. Se demuestra la **equivalencia absoluta** y el intercambio transparente de lógica entre la API declarativa de DataFrames y las sentencias SQL puras mediante el registro de vistas temporales:

Al inspeccionar la salida de `.explain("simple")` en la consola de ejecución de este código, el estudiante comprobará que **el plan físico final estructurado en RDDs es idéntico para ambas aproximaciones**. Esto dota al ingeniero de datos de una libertad total para alternar dinámicamente entre programar en Python o escribir consultas nativas SQL de acuerdo a la legibilidad y modularidad requerida por el proyecto.
</div>
</TabItem>
<TabItem value="mnp-python" label="💻 Código">

```python showLineNumbers

"""
Clase Maestra: Demostración técnica del uso integrado de Spark SQL y DataFrame API.
"""

from pyspark.sql import SparkSession
import pyspark.sql.functions as F

# 1. Inicialización de la SparkSession (Punto de entrada unificado para Spark SQL)
spark = SparkSession.builder \
    .appName("Arquitectura_Spark_SQL") \
    .master("local[*]") \
    .getOrCreate()

# 2. Ingesta de datos simulando registros limpios de la capa Silver (DataFrame API)
datos_empleados = [
    (1, "Sofia Garcia", "IT", 65000.0),
    (2, "Mateo Rodriguez", "IT", 72000.0),
    (3, "Elena Fernandez", "Finanzas", 81000.0),
    (4, "Lucas Blanco", "Finanzas", 58000.0),
    (5, "Camila Torres", "Marketing", 54000.0)
]
columnas = ["id_empleado", "nombre", "departamento", "salario"]

df_empleados = spark.createDataFrame(datos_empleados, columnas)

# 3. PROMOCIÓN DEL DATAFRAME A TABLA SQL LÓGICA
# Registramos el DataFrame como una vista temporal en el Catálogo de Spark SQL.
# Esta vista es de ámbito de sesión y no persiste datos físicos en almacenamiento.
df_empleados.createOrReplaceTempView("vista_empleados_lógica")


# ==============================================================================
# ENFOQUE A: Consulta utilizando Sintaxis SQL ANSI Pura
# ==============================================================================
# La función spark.sql() compila el String SQL mediante Catalyst y retorna un DataFrame.
print("=== [ENFOQUE A] Agregación de Negocio vía SQL ANSI ===")
df_resultado_sql = spark.sql("""
    SELECT 
        departamento,
        COUNT(id_empleado) AS total_colaboradores,
        AVG(salario) AS salario_medio
    FROM vista_empleados_lógica
    WHERE salario >= 60000.0
    GROUP BY departamento
    ORDER BY salario_medio DESC
""")
df_resultado_sql.show()


# ==============================================================================
# ENFOQUE B: Consulta utilizando la API de DataFrames (DSL)
# ==============================================================================
# Esta sintaxis orientada a objetos utiliza funciones declarativas en Python.
print("=== [ENFOQUE B] Agregación de Negocio vía DataFrame API ===")
df_resultado_api = df_empleados \
    .where(F.col("salario") >= 60000.0) \
    .groupBy("departamento") \
    .agg(
        F.count("id_empleado").alias("total_colaboradores"),
        F.avg("salario").alias("salario_medio")
    ) \
    .orderBy(F.col("salario_medio").desc())
df_resultado_api.show()


# ==============================================================================
# COMPROBACIÓN DE EQUIVALENCIA (Explain Plans)
# ==============================================================================
# Para demostrar que Catalyst genera exactamente el mismo plan físico para ambos enfoques,
# podemos imprimir el plan de ejecución en la consola del Driver.
print("=== PLAN FÍSICO OPTIMIZADO - ENFOQUE SQL ===")
df_resultado_sql.explain("simple")

print("\n=== PLAN FÍSICO OPTIMIZADO - ENFOQUE DATAFRAME API ===")
df_resultado_api.explain("simple")

# Apagado ordenado de la sesión
spark.stop()
```
</TabItem>
</Tabs>


## **Catalyst**

**Catalyst** es el motor de optimización de consultas extensible que impulsa el módulo **Spark SQL** y la API de DataFrames/Datasets en Apache Spark. Diseñado bajo los principios de la programación funcional y desarrollado en Scala, Catalyst permite a Spark traducir las instrucciones declarativas del usuario —ya estén escritas en SQL, Python, Scala o R— en un plan de ejecución física distribuida de rendimiento óptimo.

La gran ventaja técnica de Catalyst es que neutraliza la penalización de rendimiento histórica de lenguajes interpretados como Python (PySpark). Dado que el código del programador no se ejecuta de forma imperativa paso a paso, sino que se compila y optimiza de manera global antes de tocar un solo byte de datos, escribir un pipeline en SQL puro o mediante la API funcional de DataFrames produce exactamente el mismo plan de ejecución física.



### Las 4 Fases del Ciclo de Optimización

Cuando un usuario envía una consulta (SQL o DataFrame), Catalyst somete la instrucción a un flujo de transformación estructurado en cuatro fases sucesivas:

```
      Código del Usuario (SQL / DataFrame)
                       │
                       ▼
         [ FASE 1: ANÁLISIS DE REFERENCIAS ] ────► Consulta al Metastore (Catálogo)
                       │
                       ▼
         Plan Lógico Resuelto (Resolved Plan)
                       │
                       ▼
       [ FASE 2: OPTIMIZACIÓN LÓGICA (RBO) ] ────► Reglas Heurísticas (Pushdown, etc.)
                       │
                       ▼
         Plan Lógico Optimizado (Optimized Plan)
                       │
                       ▼
      [ FASE 3: PLANIFICACIÓN FÍSICA (CBO) ] ────► Evaluación por Modelo de Costo
                       │
                       ▼
          Mejor Plan Físico Seleccionado
                       │
                       ▼
       [ FASE 4: GENERACIÓN DE CÓDIGO (Tungsten) ] ──► Compilación a Java Bytecode
                       │
                       ▼
              Ejecución en el Clúster
```

#### Fase 1: Análisis (Analysis)
El punto de partida es un árbol de sintaxis abstracta (AST) derivado de la consulta del usuario. En este estado inicial, el plan se denomina **Unresolved Logical Plan (Plan Lógico Sin Resolver)** porque Spark aún no sabe si las tablas, vistas o columnas declaradas realmente existen, ni qué tipo de datos albergan.
*   **El Catálogo (Catalog):** El **Analyzer** de Spark consulta el Catálogo interno (o el metastore de Hive/Unity Catalog) para validar las referencias y comprobar la compatibilidad de tipos de datos de las columnas.
*   **Resultado:** Si todas las referencias son válidas, se genera un **Resolved Logical Plan (Plan Lógico Resuelto)**.

#### Fase 2: Optimización Lógica (Logical Optimization)
En esta etapa, Catalyst aplica un optimizador basado en reglas (RBO - *Rule-Based Optimization*) sobre el plan resolved para simplificarlo estructuralmente sin alterar su semántica lógica. Las optimizaciones clave de esta fase incluyen:
*   **Predicate Pushdown (Poda de predicados):** "Empuja" las condiciones de filtrado (`WHERE` / `.filter()`) directamente al origen de datos físico. Esto garantiza que Spark descarte las filas no deseadas antes de cargarlas en la RAM del clúster o transferirlas por la red.
*   **Projection Pruning (Poda de columnas):** Elimina del flujo de procesamiento las columnas que no se seleccionan en el query final, minimizando drásticamente la lectura de datos pesados desde el disco.
*   **Constant Folding (Plegado de constantes):** Resuelve operaciones aritméticas fijas en tiempo de compilación. Por ejemplo, una expresión como `monto * (1024 * 1024)` es convertida internamente por Catalyst a `monto * 1048576` antes de ejecutarse, ahorrando ciclos de CPU redundantes.

#### Fase 3: Planificación Física (Physical Planning)
A partir del plan lógico optimizado, Spark SQL genera múltiples estrategias alternativas de ejecución física utilizando operadores que interactúan directamente con los recursos distribuidos del clúster.
*   **Modelo de Costo (CBO - *Cost-Based Optimizer*):** Spark evalúa los distintos planes físicos generados frente a un modelo de costo que analiza estadísticas físicas del almacenamiento de las tablas (volumen total en bytes, cardinalidad, estadísticas de particiones, etc.).
*   **Resultado:** El optimizador selecciona el plan físico más eficiente. Por ejemplo, si una tabla es significativamente más pequeña que el umbral de transmisión, Catalyst decidirá de forma inteligente reemplazar una costosa operación de ordenamiento e intercambio (*SortMergeJoin*) por una unión por difusión ultraveloz (*BroadcastHashJoin*).

#### Fase 4: Generación de Código (Code Generation)
Una vez elegido el mejor plan físico, Catalyst actúa como un compilador y traduce el plan físico final en **Java Bytecode** altamente eficiente que se ejecutará nativamente en las JVM de los ejecutores del clúster.
*   **Whole-Stage Code Generation:** Apoyado por el motor físico **Project Tungsten**, Catalyst colapsa múltiples fases y transformaciones estrechas contiguas (como mapeos, filtros y extracciones sobre un mismo registro) en una única función lógica compacta de Java. Esto elimina el costo de realizar llamadas a funciones virtuales intermedias y permite almacenar variables de paso directamente en los registros del CPU, maximizando la velocidad y disminuyendo la huella de memoria.

---

### Spark 3.0+: Optimización Adaptativa de Consultas (AQE)

Antes de Spark 3.0, los planes de consulta calculados por Catalyst eran monolíticos: una vez que se iniciaba el trabajo distribuido, el plan físico se seguía al pie de la letra, sin importar si las estadísticas iniciales estaban desactualizadas o eran inexistentes. 

Para solucionar esto, se introdujo **Adaptive Query Execution (AQE)**, la cual permite a Catalyst **reoptimizar y ajustar el plan físico en caliente** basándose en estadísticas precisas de ejecución recolectadas dinámicamente en los puntos de sincronización y materialización de las etapas del clúster (fases de *Shuffle* o *Broadcast*):

1.  **Coalescencia Dinámica de Particiones de Shuffle:** Detecta si las tareas de intercambio generaron particiones demasiado pequeñas o vacías, y las fusiona dinámicamente para reducir la sobrecarga de scheduling.
2.  **Conversión Dinámica de Joins:** Si durante la ejecución se descubre que el tamaño real de una tabla filtrada es menor que el límite de transmisión de Spark, AQE cambia de inmediato un *SortMergeJoin* por un *BroadcastHashJoin*, evitando shuffles pesados por la red.
3.  **Remedio Dinámico de Sesgo de Datos (*Skew Join*):** Si se detecta una partición desproporcionadamente más grande que las demás (lo que retrasaría todo el trabajo), AQE la divide dinámicamente en subparticiones y las distribuye uniformemente en el clúster para acelerar el procesamiento paralelo.

---

### Ejemplo Práctico (Python)
<Tabs>
<TabItem value="mnp" label="Ejemplo" default>
<div class="alert alert--primary">
**Inspeccionando a Catalyst con `.explain()`**

Para demostrar el comportamiento y los planes lógicos que Catalyst construye de manera perezosa (*Lazy Evaluation*), un Ingeniero de Datos puede utilizar de forma pedagógica el método **`.explain()`** sobre un DataFrame.

El siguiente código PySpark simula un pipeline común (lectura, filtrado y agregación) e inspecciona cómo Catalyst reorganiza las operaciones.

Al ejecutar este código, el método `.explain(True)` imprimirá en pantalla las siguientes fases de Catalyst de forma legible:

*   **`Parsed Logical Plan` (Plan Lógico Analizado):** Muestra el mapeo exacto de las operaciones tal cual las declaraste en tu código Python de arriba hacia abajo (con el cálculo del impuesto antes del filtro de categoría).
*   **`Analyzed Logical Plan` (Plan Lógico Validado):** Muestra el plan tras validar las columnas en el catálogo y verificar la inyección de tipos en Spark.
*   **`Optimized Logical Plan` (Plan Lógico Optimizado):** Aquí verás la magia de Catalyst. El filtro de `categoria == 'Tecnología'` se habrá movido al principio del todo (justo encima de la carga de archivos, aplicando *Predicate Pushdown*) y se habrán eliminado las columnas no utilizadas (*Column Pruning*).
*   **`Physical Plan` (Plan Físico):** Muestra cómo se ejecutará realmente sobre RDDs de bajo nivel en el hardware, indicando los puntos donde ocurrirá *WholeStageCodegen* y el intercambio distribuido de datos (*Exchange* por *Shuffle*).
</div>
</TabItem>
<TabItem value="mnp-python" label="💻 Código">

```python showLineNumbers title="Uso de Catalyst"

"""
Ejemplo: Inspección de los estados de optimización de Catalyst
"""

from pyspark.sql import SparkSession
import pyspark.sql.functions as F

# 1. Crear la sesión de Spark de forma gobernada
spark = SparkSession.builder \
    .appName("Clase_Maestra_Catalyst") \
    .master("local[*]") \
    .getOrCreate()

# 2. Simulación de carga de datos (Se asume formato Parquet optimizado)
ruta_ventas = "s3://silver-zone/ventas_globales.parquet"
df_ventas = spark.read.format("parquet").load(ruta_ventas)

# 3. Encadenamiento de transformaciones declarativas (Lazy)
# A pesar de que el filtro se declara después del cálculo del total_impuesto,
# Catalyst optimizará el flujo e invertirá las operaciones (Predicate Pushdown).
df_reporte = df_ventas \
    .withColumn("total_impuesto", F.col("monto_bruto") * 0.19) \
    .select("cliente_id", "categoria", "total_impuesto") \
    .where(F.col("categoria") == "Tecnología") \
    .groupBy("cliente_id") \
    .agg(F.sum("total_impuesto").alias("impuesto_acumulado"))

# 4. Inspección de los planos de Catalyst
# Usamos explain(True) para desglosar detalladamente el viaje del query en la consola
print("=== INSPECCIÓN DE PLANES DEL OPTIMIZADOR CATALYST ===")
df_reporte.explain(True)

# Apagar sesión de Spark
spark.stop()
```
</TabItem>
</Tabs>
