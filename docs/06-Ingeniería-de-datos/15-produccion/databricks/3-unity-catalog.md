---
id: unity
title: "Unity Catalog"
sidebar_label: "Unity Catalog"
description: "Unity Catalog"
slug: /unity
---

**Unity Catalog** es la solución de gobernanza de datos e Inteligencia Artificial (IA) unificada, centralizada y de código abierto diseñada por Databricks para su plataforma Lakehouse. 

Históricamente, la gobernanza en entornos Spark dependía del **Hive Metastore (HMS)**. Sin embargo, el HMS presentaba limitaciones críticas: estaba fuertemente acoplado a nivel de *workspace* (lo que fragmentaba la administración de metadatos), carecía de soporte nativo para el gobierno de modelos de machine learning o archivos no estructurados, y dependía de controles de acceso a nivel de infraestructura física. 

Unity Catalog resuelve esta problemática al desacoplar la gestión de identidades y la metadata de los espacios de trabajo individuales, elevando la gobernanza al nivel de la **cuenta global de Databricks**.

---

### Pilares de la Arquitectura

Para comprender su funcionamiento, es necesario analizar sus componentes estructurales y operativos:

#### A. El Metastore Regional y la Jerarquía de Objetos
El corazón de Unity Catalog es el **Metastore Regional**, un contenedor lógico de metadatos que opera a nivel de región de nube. El metastore almacena definiciones de tablas, esquemas, permisos, registros de auditoría y credenciales de almacenamiento. 

Bajo el metastore, se introduce un **espacio de nombres de tres niveles** (*three-level namespace*), superando la clásica nomenclatura bidimensional de Hive:
```
[text{Metastore} \rightarrow \text{Catalog} \rightarrow \text{Schema (Database)} \rightarrow \text{Securable Asset (Table, View, Volume, etc.)}]
```

*   **Catalog (Catálogo):** El primer nivel de agrupación lógica, ideal para separar entornos (v.g., `dev`, `stage`, `prod`) o unidades de negocio.
*   **Schema / Database (Esquema):** Agrupación de segundo nivel que organiza componentes de una aplicación específica.
*   **Securables (Activos Gobernados):** Son los elementos finales sobre los que se aplican permisos de control de acceso ANSI SQL. A diferencia de los catálogos tradicionales que solo controlan tablas y vistas relacionales, Unity Catalog implementa un modelo **multimodal** que unifica:
    *   **Tablas y Vistas:** Datos estructurados.
    *   **Volumes (Volúmenes):** Abstracciones que gobiernan archivos no estructurados y semiestructurados (como imágenes, archivos PDF o audio) almacenados en la nube, indispensables para pipelines de IA.
    *   **Models:** Modelos de machine learning empaquetados mediante el framework MLflow.
    *   **Functions:** Funciones definidas por el usuario (UDFs) para lógica reutilizable.

#### B. Separación de Planos (Control Plane vs. Data Plane)
Unity Catalog opera bajo un estricto modelo de seguridad donde el **Plano de Control** (alojado por Databricks) administra y valida los metadatos y políticas de autorización, pero **los datos reales nunca abandonan el Plano de Datos** (la cuenta de nube del cliente).

---

### Mecanismo de Funcionamiento: 
***Credential Vending* (Despacho de Credenciales)**

Uno de los conceptos más avanzados y pedagógicos de Unity Catalog es cómo evita la exposición de credenciales maestras de la nube a los usuarios finales. 

En el pasado (HMS), para que un clúster de Spark pudiera leer datos de un bucket (por ejemplo, AWS S3 o Azure ADLS), se debía montar el sistema de archivos con una clave de acceso general, permitiendo que cualquier usuario con acceso al clúster pudiera leer todo el contenido del bucket.

Unity Catalog implementa el patrón **Credential Vending**. Su ciclo de vida operativo funciona de la siguiente manera:

```
[Usuario] ──(1. Envía Consulta SQL/API)──> [Clúster Spark]
                                               │
                                       (2. Solicita Token)
                                               ▼
                                    [Servicio Unity Catalog] (Plano de Control)
                                               │
                                    (3. Valida permisos en ACLs)
                                               │
                                 (4. Genera Token Temporal de Nube)
                                               ▼
[Clúster Spark] <──(5. Devuelve Token de Corta Duración con TTL)
      │
(6. Lee datos usando el Token temporal)
      ▼
[Almacenamiento de Nube (S3/ADLS/GCS)]
```

1.  **Ejecución:** El usuario o aplicación lanza una consulta sobre un activo (v.g., `SELECT * FROM prod.sales.transactions`).
2.  **Validación:** El motor de Spark en el plano de datos intercepta la petición y consulta al Plano de Control de Unity Catalog.
3.  **Autorización:** Unity Catalog verifica las Listas de Control de Acceso (ACLs) y las políticas del usuario.
4.  **Generación de Token Downscoped:** Si el acceso es autorizado, Unity Catalog utiliza las **Storage Credentials** (v.g., un rol IAM de AWS, una Identidad Administrada de Azure o una cuenta de servicio de GCP registradas internamente) para generar un **token temporal, limitado y de alcance reducido** (*downscoped token*) con un tiempo de vida (TTL) muy corto, asociado específicamente a la ruta del archivo correspondiente.
5.  **Lectura Directa:** Unity Catalog envía este token temporal al clúster Spark, el cual se comunica directamente con el almacenamiento físico de la nube para procesar los datos. El plano de control de Databricks **nunca ve los registros físicos**.

---

### Seguridad Avanzada
**Aislamiento a Nivel de Cómputo con *Lakeguard***

Para garantizar la seguridad en clústeres multiusuario (donde científicos y analistas comparten los mismos recursos de hardware), Databricks integra la tecnología **Lakeguard**. 

En el modo de acceso compartido (*shared access mode*), **Lakeguard** encapsula el código de cada usuario en contenedores aislados de forma segura dentro de las máquinas virtuales de Spark. Utilizando la arquitectura cliente-servidor de **Spark Connect** (disponible a partir de Spark 3.4), aísla el entorno de ejecución (JVM) de cada usuario y restringe el acceso a librerías del sistema operativo o comandos privilegiados, bloqueando cualquier intento de eludir el gobierno de datos.

---

### Ejemplo Práctico de Implementación

A continuación, se presenta un caso de uso técnico en el que se utiliza **SQL** en Databricks para demostrar cómo crear un catálogo y aplicar **Gobernanza de Datos Fina (FGAC)** a través de una función de enmascaramiento dinámico de datos basada en los roles del usuario:

```sql
-- 1. Establecemos el catálogo de producción (Uso del namespace de tres niveles)
USE CATALOG prod_catalog;

-- 2. Creamos un esquema seguro para el departamento de Recursos Humanos
CREATE SCHEMA IF NOT EXISTS hr_schema;
USE SCHEMA hr_schema;

-- 3. Creamos una tabla que contendrá información sensible de los empleados
CREATE TABLE IF NOT EXISTS employees (
    employee_id INT,
    full_name STRING,
    email STRING,
    salary DOUBLE
);

-- Inserción de datos simulados
INSERT INTO employees VALUES 
(1, 'Alicia Gomez', 'alicia.g@company.com', 85000.0),
(2, 'Roberto Morales', 'roberto.m@company.com', 92000.0);

-- 4. Definimos una función de enmascaramiento dinámico (CLM - Column Level Masking)
-- Esta función retornará el valor real solo si el usuario pertenece al grupo 'hr-admins'
CREATE OR REPLACE FUNCTION email_mask(email STRING) 
RETURN CASE
    WHEN is_member('hr-admins') THEN email
    ELSE 'REDACTED_DATA_PII'
END;

-- 5. Aplicamos la función como máscara de columna en la tabla de empleados
ALTER TABLE employees ALTER COLUMN email SET MASK email_mask;

-- 6. Consulta de prueba
-- Un usuario común que ejecute esta consulta verá la columna 'email' redactada,
-- mientras que un administrador del grupo 'hr-admins' visualizará el correo real.
SELECT employee_id, full_name, email, salary FROM employees;
```

### Beneficios Estratégicos
*   **Linaje Automatizado (*Data Lineage*):** Registra y visualiza de forma automática las dependencias columna por columna entre *notebooks*, flujos de trabajo, modelos y tableros.

*   **Interoperabilidad Abierta (UniForm):** Permite que las tablas de Delta Lake generen metadatos de Apache Iceberg o Apache Hudi de forma asíncrona, de modo que herramientas de consulta externas (como Snowflake o Apache Trino) lean los datos como si fueran nativos a través de la API REST de Unity Catalog.

*   **Gobernanza de IA:** Permite catalogar no solo datos, sino también endpoints de inferencia, herramientas de búsqueda vectorial (*Vector Search*) y modelos de lenguaje (LLMs) con la misma matriz de permisos ANSI SQL.


## Linaje de Datos

El **linaje de datos** (*data lineage*) es la disciplina y el conjunto de metadatos que permite **rastrear, registrar y visualizar el origen, el flujo de transformaciones y el destino final de los activos de datos** a lo largo de todo su ciclo de vida. En términos sencillos, actúa como un "mapa de dependencias" detallado que responde de manera precisa a tres preguntas críticas: de dónde provienen los datos, cómo se han modificado y quién o qué herramientas los consumen río abajo (*downstream*).

---

#### **¿Por qué es fundamental el linaje de datos?**

Desde un punto de vista pedagógico y de ingeniería, el linaje no es solo una funcionalidad de auditoría, sino una herramienta operativa clave con múltiples aplicaciones:

#### **1. Tolerancia a fallos y computación distribuida**
En motores de procesamiento como **Apache Spark**, el linaje es la columna vertebral de la resiliencia. Spark no calcula inmediatamente los datos al aplicar transformaciones (evaluación perezosa o *lazy evaluation*). En su lugar, construye un **Grafo Acíclico Dirigido (DAG)** que define un linaje para el dataset. Si un nodo del clúster falla y se pierde una partición de memoria, Spark consulta este linaje histórico de operaciones y **recomputa únicamente la partición perdida** a partir de los datos de entrada originales.

#### **2. Diagnóstico de modelos (*Debugging*) y sesgo en Machine Learning**
En proyectos de IA, entrenar un modelo con datos de múltiples fuentes sin examinar su calidad puede provocar fallas inexplicables en producción. Si el rendimiento de un modelo decae repentinamente, el linaje de datos permite aislar los registros nuevos de los históricos y rastrear su procedencia (por ejemplo, identificando qué grupo de anotadores etiquetó un lote defectuoso). Esto es vital para mitigar sesgos y asegurar la reproducibilidad de los experimentos.

#### **3. Análisis de impacto y "Alertas Tempranas"**
El linaje mapea las relaciones de dependencia entre tablas, cuadernos, flujos de trabajo (*workflows*) y tableros de BI. Si se detecta un problema de calidad (como valores nulos inesperados) en una ingesta cruda (*upstream*), el linaje sirve como un sistema de alerta temprana que revela de inmediato qué reportes financieros, modelos de machine learning o dashboards de negocio se verán afectados por el fallo.

---

#### Ejemplo Práctico en PySpark 
**Construcción de un Linaje Lógico**

A nivel de programación, cada DataFrame que creas en PySpark no contiene datos físicos inmediatamente, sino una receta de instrucciones que define su linaje.

El siguiente código en Python demuestra cómo PySpark registra la secuencia de transformaciones (linaje lógico) y permite inspeccionarla de forma declarativa mediante el método `.explain()`:

```python showLineNumbers title="Linaje de datos"
from pyspark.sql import SparkSession
import pyspark.sql.functions as F

# 1. Inicializamos la sesión de Spark
spark = SparkSession.builder \
    .appName("EjemploLinajeLogico") \
    .master("local[*]") \
    .getOrCreate()

# 2. Nodo de Origen (Ingesta de datos crudos - Capa Bronze)
# Simulamos un dataset de transacciones
datos_ingesta = [
    (1, "Laptop", "1200.00", "2026-08-01"),
    (2, "Mouse", "25.00", "2026-08-02"),
    (3, "Teclado", None, "2026-08-03")
]
# Este DataFrame define el punto de partida (Padre) en nuestro linaje
df_bronze = spark.createDataFrame(datos_ingesta, ["id", "producto", "precio", "fecha"])

# 3. Transformación 1 (Capa Silver) - Tipado y filtrado de nulos
# Aquí Spark no ejecuta el cálculo, solo añade el paso al linaje lógico
df_silver = df_bronze \
    .dropna(subset=["precio"]) \
    .withColumn("precio", F.col("precio").cast("double"))

# 4. Transformación 2 (Capa Gold) - Agregación de negocio
df_gold = df_silver \
    .groupBy("producto") \
    .agg(F.sum("precio").alias("ventas_totales"))

# 5. Inspección del Linaje Lógico y Físico
# El método .explain() nos permite visualizar el plan de ejecución optimizado
# que Spark ha estructurado gracias al registro del linaje.
print("=== PLAN DE EJECUCIÓN (LINAJE DE OPERACIONES) ===")
df_gold.explain(True)

# Apagamos la sesión de manera limpia
spark.stop()
```

#### **Explicación del Plan de Ejecución Generado:**
Cuando ejecutas `.explain(True)`, Spark te mostrará:
1. **Parsed Logical Plan:** La representación directa de las sentencias que escribiste.
2. **Analyzed Logical Plan:** El plan donde Spark valida contra el catálogo de metadatos que las columnas y tipos realmente existen.
3. **Optimized Logical Plan:** El plan optimizado por el optimizador *Catalyst* (por ejemplo, empujando filtros hacia el origen para leer menos datos).
4. **Physical Plan:** Las instrucciones físicas exactas que ejecutarán los *executors* en el clúster.

Este flujo lógico e incremental garantiza que el motor siempre sepa exactamente cómo reconstruir, optimizar o auditar cada celda del dato desde su nacimiento hasta su consumo.

En Databricks, este linaje se captura automáticamente de manera granular a nivel de tabla y columna mediante herramientas como Unity Catalog. 

### Implementación en Unity

La implementación del **linaje de datos (*data lineage*)** en **Unity Catalog** se realiza de manera **automática y centralizada** a nivel de metastore, ofreciendo tanto una representación visual en la interfaz de usuario como un registro detallado en tablas de sistema estructuradas.

A continuación, se detalla la arquitectura, el funcionamiento técnico y los métodos de consumo de este componente de gobernanza.

---

#### 1. Captura en Tiempo de Ejecución (*Runtime Data Lineage*)
Unity Catalog captura el linaje de datos de manera dinámica y en tiempo de ejecución para todas las consultas y tareas de procesamiento ejecutadas sobre los activos gobernados. 
*   **Automatización completa:** Cada vez que un usuario o un proceso ejecuta una consulta (ya sea a través de un clúster de Spark o un SQL Warehouse), el motor registra la relación entre los datos de origen y de destino.
*   **Ámbito multimodal:** No se limita únicamente a datos tabulares; rastrea de forma nativa dependencias entre tablas, vistas, volúmenes (archivos no estructurados), funciones y modelos de Machine Learning.

#### 2. Tablas de Sistema para la Observabilidad del Linaje
El linaje de datos se persiste de forma estructurada en tablas Delta de solo lectura dentro del catálogo `system`. Esto permite a los ingenieros de datos realizar auditorías y análisis de impacto personalizados mediante consultas SQL. Las dos tablas principales alojadas en el esquema `system.access` son:
*   **`system.access.table_lineage`:** Registra las dependencias y el flujo de información a nivel de tablas y rutas físicas.
*   **`system.access.column_lineage`:** Desglosa la trazabilidad a nivel granular de columna, identificando exactamente cómo se derivan y transforman los campos individuales.

##### Ejemplo de implementación programática (Python / PySpark)
Para extraer y analizar el linaje de una tabla específica de forma programática, un ingeniero de datos puede interactuar con las tablas de sistema mediante la API de DataFrame de Spark:

```python showLineNumbers
def obtener_linaje_tabla(nombre_tabla, ruta_tabla=None):
    """
    Consulta la tabla de sistema de Unity Catalog para extraer el linaje 
    río arriba (upstream) y río abajo (downstream) de una tabla específica.
    """
    # Leer la tabla de sistema que almacena el linaje a nivel de tabla
    df_lineage = spark.read.table("system.access.table_lineage")
    
    # Filtrar por el nombre de la tabla o por su ruta física en el almacenamiento
    return df_lineage.where(
        (df_lineage.source_table_full_name == nombre_tabla) | 
        (df_lineage.target_table_full_name == nombre_tabla) |
        (df_lineage.source_path == ruta_tabla) | 
        (df_lineage.target_path == ruta_tabla)
    )

# Visualizar el linaje de la tabla 'gold_clientes'
df_resultado = obtener_linaje_tabla("datawarehousing.gold.gold_clientes")
display(df_resultado)
```

#### 3. Visualización de Dependencias en la UI (DAG)
La plataforma procesa estos metadatos y genera automáticamente un **mapa de dependencias** en la interfaz de usuario de Databricks, estructurado como un Grafo Acíclico Dirigido (DAG). Este mapa permite a los usuarios rastrear visualmente qué activos consumen o alimentan una tabla:
*   **Elementos de origen y destino (*Upstream/Downstream*):** Muestra de forma interactiva la procedencia de los datos (tablas de origen o rutas de almacenamiento) y los consumidores finales, tales como *notebooks*, flujos de trabajo (*workflows* o *pipelines*), tableros de control de BI (*dashboards*), consultas guardadas, modelos de ML y endpoints de inferencia.

#### 4. Linaje de "Primera y Última Milla" (*Bring Your Own Lineage*)
Para evitar silos fuera de la plataforma Databricks, Unity Catalog permite la ingesta de linaje personalizado de herramientas externas mediante su API. 
*   **Definición externa:** Los administradores del espacio de trabajo con los privilegios adecuados pueden especificar orígenes externos río arriba (como colas de mensajería de Apache Kafka) y destinos finales río abajo (como reportes de Power BI), conectándolos visualmente con los metadatos y dependencias existentes en Unity Catalog.

#### 5. Limitaciones Importantes
*   **Restricción del Metastore:** El linaje de datos se genera y se acota exclusivamente dentro de los límites de un metastore regional.
*   **Pérdida en Delta Sharing:** Cuando se utiliza *Delta Sharing* para compartir datos entre diferentes metastores, nubes o cuentas, metadatos críticos como las etiquetas y el linaje de datos **no se propagan** al metastore del receptor, quedando localizados en la infraestructura del proveedor.

