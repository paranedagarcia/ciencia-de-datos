# context
Para diseñar, construir y mantener un *data pipeline* (canalización de datos) eficiente en un proyecto de ciencia de datos, un ingeniero de datos utiliza un conjunto de herramientas especializadas que cubren distintas etapas del ciclo de vida del dato: desde su extracción hasta que está listo para ser consumido por modelos de Machine Learning o herramientas de análisis.

Basándonos en los estándares de la industria y en las arquitecturas modernas (como las que se mencionan en tus documentos sobre PySpark, Databricks y Azure), aquí tienes las herramientas principales divididas por categoría:

### 1. Procesamiento y Transformación de Datos (ETL/ELT)

Esta es la fase donde los datos crudos se limpian, se transforman y se estructuran.

* **Apache Spark (y PySpark):** Es el motor de procesamiento distribuido estándar de la industria para Big Data. Permite procesar terabytes de datos en memoria a gran velocidad. Es ideal para preparar características (feature engineering) para modelos de Machine Learning.
* **dbt (Data Build Tool):** Una herramienta muy popular moderna que permite a los ingenieros y analistas transformar datos en el almacén de datos (Data Warehouse) utilizando simplemente sentencias SQL.
* **Pandas / Dask:** Para conjuntos de datos más pequeños o medianos, Pandas en Python es la herramienta de facto. Dask permite escalar Pandas para manejar datos que no caben en la memoria RAM de una sola máquina.

### 2. Orquestación de Flujos de Trabajo

Los pipelines tienen múltiples pasos que deben ejecutarse en un orden específico, reintentarse si fallan y monitorearse.

* **Apache Airflow:** Es la herramienta de orquestación más utilizada. Permite programar y monitorear flujos de trabajo como Grafos Acíclicos Dirigidos (DAGs) escritos en Python.
* **Prefect / Dagster:** Son alternativas modernas a Airflow, diseñadas específicamente para flujos de trabajo de datos dinámicos y con un enfoque muy fuerte en el estado y la observabilidad de los datos.
* **Azure Data Factory / AWS Glue:** Servicios administrados en la nube que ofrecen interfaces gráficas y código para orquestar la integración de datos sin necesidad de administrar servidores.

### 3. Almacenamiento (Data Lakes, Data Warehouses y Lakehouses)

Los datos procesados deben almacenarse en lugares accesibles, seguros y optimizados para consultas analíticas.

* **Delta Lake / Apache Hudi / Apache Iceberg:** Son capas de almacenamiento de código abierto que aportan confiabilidad (transacciones ACID) a los Data Lakes tradicionales, creando la arquitectura conocida como *Data Lakehouse*. Son fundamentales en plataformas como Databricks.
* **Cloud Object Storage:** Amazon S3, Azure Data Lake Storage (ADLS) y Google Cloud Storage (GCS) son la base donde aterrizan los datos crudos (arquitectura *Bronze/Silver/Gold*).
* **Data Warehouses Modernos:** Snowflake, Google BigQuery y Amazon Redshift son bases de datos columnares masivamente paralelas optimizadas para consultas analíticas rápidas.

### 4. Ingesta de Datos (Batch y Streaming)

Cómo llegan los datos desde las fuentes (bases de datos transaccionales, APIs, sensores) al sistema de almacenamiento.

* **Apache Kafka:** La plataforma líder para el procesamiento de flujos de eventos en tiempo real (streaming). Es vital si el modelo de ciencia de datos necesita predecir eventos al instante (por ejemplo, detección de fraudes).
* **Apache Flink / Spark Structured Streaming:** Motores que se conectan a Kafka para procesar esos flujos de datos en tiempo real.
* **Fivetran / Airbyte:** Herramientas de ingesta de datos automatizadas que extraen datos de cientos de fuentes (CRMs, bases de datos, APIs) y los cargan directamente en el Data Warehouse.

### 5. Ecosistemas Unificados / Plataformas

Muchas empresas prefieren no ensamblar todas estas piezas por separado y utilizan plataformas que integran almacenamiento, procesamiento y gobierno de datos.

* **Databricks:** Una plataforma de análisis unificada basada en Spark que integra Delta Lake, MLflow (para el ciclo de vida de Machine Learning) y facilita enormemente la colaboración entre Ingenieros de Datos y Científicos de Datos.
* **Microsoft Fabric:** Una solución analítica completa introducida recientemente que unifica Data Engineering, Data Science y Business Intelligence (Power BI) sobre un único lago de datos central llamado OneLake.

**¿Cómo se integran con la Ciencia de Datos?**
El objetivo final del ingeniero de datos es construir un pipeline que deje los datos limpios, particionados y versionados para que herramientas como **scikit-learn, TensorFlow o PyTorch** puedan entrenar modelos sin preocuparse por valores faltantes, formatos corruptos o cuellos de botella en la lectura de los archivos.

# role
actua como experto en ingenieria y ciencia de datos. con amplia experiencia en cloud computing

# task
crea una presentación de diapositivos orientadas a alumnos con conocimintos iniciales

# format
usa un formato horizontal estilo 16:9 con un minimo de 15 diapostivas. con uso de imagenes o diagramas coloridos. utiiza un fono de color blanco y plano para todas as diapositivas a excepcion de a primera. Prioriza las imagenes y esquemas por sobre el texto.