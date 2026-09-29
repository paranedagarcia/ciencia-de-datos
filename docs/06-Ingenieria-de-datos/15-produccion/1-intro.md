---
id: produccion
title: "Introducción"
sidebar_label: "💻 Introducción"
description: "Salida a Producción de un proyecto de ciencia de datos"
---

## Despliegue y producción

En la etapa de **despliegue** y puesta en producción de un proyecto de ciencia de datos, las funciones del **científico de datos** y del **ingeniero de datos** (que a menudo trabaja junto con ingenieros de MLOps o de plataforma) están bien delimitadas, pero requieren una estrecha colaboración para evitar fallos sistémicos. 

A continuación se detallan sus responsabilidades y cómo interactúan en esta fase crítica:

### El rol del Científico de Datos
* **Definición de la lógica del modelo:** Su función principal ocurre en la fase de pre-despliegue, donde se encarga de estructurar la lógica del modelo en un entorno de desarrollo. Esto abarca la ingeniería de características (*features*), la selección de algoritmos, la definición de métricas de negocio y el entrenamiento offline.

* **Exportación y entrega (*Hand-off*):** Una vez que el modelo cumple con las métricas de rendimiento y validación, el científico de datos lo exporta (por ejemplo, en un formato binario o serializado) para que sea desplegado. 

* **Monitoreo de rendimiento analítico:** Tras el despliegue, supervisa si las predicciones del modelo siguen siendo precisas o si se degrada debido a cambios en el comportamiento de los usuarios o en los datos de entrada (*data drift*), determinando cuándo es necesario un reentrenamiento.

### El rol del Ingeniero de Datos
* **Suministro de datos de producción:** Se encarga de la ingesta y preparación de datos frescos. En procesos de inferencia o reentrenamiento por lotes (*batch*), el ingeniero de datos diseña los flujos para extraer de forma eficiente y segura la información nueva desde los almacenes de datos (*data warehouses*).

* **Escala y robustez de los pipelines:** Asegura que los pipelines de procesamiento de datos en producción —especialmente los de *streaming* para inferencia en tiempo real con latencias de milisegundos— funcionen de manera ininterrumpida, escalable y con alta disponibilidad.

* **Gobernanza y cumplimiento normativo:** Implementa políticas de seguridad y privacidad en el plano de datos de producción (por ejemplo, para cumplir con regulaciones como el GDPR), aislando entornos de cómputo y configurando zonas de de-identificación para proteger datos sensibles como PII (información de identificación personal).


### Fricciones y Desafíos en la Frontera de Ambos Roles

El despliegue suele ser el punto donde surgen los mayores problemas debido a la separación tradicional de funciones:

* **Inconsistencia de características (*Feature Mismatch*):** Es muy común que el científico de datos cree el pipeline de características en Python para el entrenamiento offline, pero que el ingeniero de datos deba reescribir ese mismo pipeline en lenguajes de alto rendimiento (como Java o C) para la inferencia en tiempo real en producción. Esto duplica el esfuerzo y suele introducir discrepancias matemáticas sutiles que provocan predicciones erróneas en producción.
* **Sobrecarga de comunicación (*Communication Overhead*):** Si el científico de datos simplemente "entrega" el modelo al equipo de ingeniería y se desentiende de la infraestructura, se genera un cuello de botella. El equipo de plataforma tendrá un contexto muy estrecho para diagnosticar fallos en las predicciones, mientras que el científico de datos no tendrá visibilidad ni incentivos para proponer optimizaciones en la infraestructura.



## Ingeniero de datos

Un ingeniero de datos diseña, construye y gestiona los sistemas e infraestructuras necesarios para recopilar, almacenar y transformar grandes volúmenes de datos brutos en información limpia y accesible para que los analistas y científicos de IBM puedan usarlos en sus modelos y decisiones de negocio.

El rol de un **ingeniero de datos** es fundamental en los sistemas modernos de análisis y machine learning, ya que se encarga de diseñar, construir y mantener la infraestructura que permite preparar los datos para su posterior análisis o consumo. Su principal objetivo es transformar los datos crudos y "sucios" en información limpia, estructurada, confiable y fácilmente accesible para científicos de datos, analistas y herramientas de inteligencia de negocio (BI).


**Habilidades técnicas esenciales**

- Programación: Dominio de lenguajes como Python, Java o Scala.
- Bases de datos: Manejo avanzado de sistemas SQL y NoSQL.
- Entornos Cloud: Experiencia en plataformas como AWS, Google Cloud o Microsoft Azure.
- Big Data: Familiaridad con herramientas de procesamiento distribuido como Apache Spark



### Roles y Responsabilidades

1.  **Diseño y Construcción de Pipelines de Datos (ETL/ELT):** Desarrollan flujos automatizados para extraer datos de múltiples fuentes (como bases de datos transaccionales, archivos planos o colas de mensajería en tiempo real) y cargarlos en repositorios centralizados. Creación de bases de datos, almacenes de datos (data warehouses) y lagos de datos (data lakes).

2.  **Limpieza, Integración y Enriquecimiento de Datos:** Aplican transformaciones para corregir inconsistencias, eliminar duplicados, manejar valores nulos y estructurar la información siguiendo el patrón de la **arquitectura de medallón** (refinando progresivamente los datos de capas crudas o *bronze*, a limpias o *silver*, y finalmente agregadas o *gold*).

3.  **Orquestación de Flujos de Trabajo:** Configuran herramientas de programación y monitoreo para asegurar que las tareas de los pipelines se ejecuten en un orden específico mediante **Grafos Acíclicos Dirigidos (DAGs)**, controlando dependencias y programando ejecuciones periódicas o en tiempo real.

4.  **Gobernanza, Seguridad y Trazabilidad (*Data Lineage*):** Implementan políticas de acceso a los datos, catalogación de metadatos, auditoría de consultas y el seguimiento del ciclo de vida del dato para cumplir con regulaciones de privacidad (como el GDPR).



### Herramientas y Operación en las Nubes

Aunque los conceptos y principios de la ingeniería de datos son universales en cualquier entorno, la implementación física varía significativamente entre los proveedores de nube debido a sus servicios nativos, arquitecturas de integración y mecanismos de seguridad:

#### Microsoft Azure (Azure Data Engineering)
En el ecosistema de Azure, el ingeniero de datos trabaja con una fuerte integración nativa y servicios administrados de primera clase:
*   **Servicio de Cómputo Principal:** **Azure Databricks**, que se ofrece como un servicio nativo (*first-party service*) integrado directamente con el Portal de Azure y OneLake en **Microsoft Fabric**.
*   **Orquestación y ETL:** Utilizan principalmente **Azure Data Factory (ADF)** para coordinar pipelines híbridos y flujos de control complejos (actividades como *Lookup, If, ForEach*), así como **Azure Synapse Analytics** para almacenamiento masivo de datos.
*   **Almacenamiento (Data Lake):** Azure Blob Storage y **Azure Data Lake Storage Gen2 (ADLS Gen2)**, que admiten estructuras jerárquicas de archivos.
*   **Seguridad e Identidad:** La autenticación se realiza mediante **Microsoft Entra ID** (antiguo Azure Active Directory), implementando identidades administradas (*Managed Identities*) y cuentas de servicio para un traspaso de credenciales seguro (*credential passthrough*) hacia el almacenamiento ADLS.

#### Amazon Web Services (AWS Data Engineering)
En AWS, la arquitectura tiende a ser muy modular y el ingeniero de datos se enfoca en administrar clústeres elásticos y catálogos de metadatos serverless:
*   **Servicio de Cómputo Principal:** **AWS EMR (Elastic MapReduce)** para levantar clústeres administrados de Hadoop, Apache Spark, Hive y Presto.
*   **Catalogación y ETL Serverless:** Utilizan **AWS Glue** como motor de ETL serverless y como el catálogo de metadatos central (**AWS Glue Data Catalog** / Hive Metastore) para registrar las tablas del data lake en S3.
*   **Consultas y Almacenamiento:** **Amazon S3** es el estándar de almacenamiento para data lakes, mientras que **AWS Athena** (basado en Presto) se usa para realizar consultas SQL directas e interactivas sobre S3 sin mover los datos. Para data warehouses masivos, se utiliza **Amazon Redshift**.
*   **Seguridad e Identidad:** La seguridad y el acceso a los datos se configuran mediante políticas de buckets de S3 y roles de **AWS IAM**, utilizando perfiles de instancia para que los clústeres asuman identidades de forma segura.

#### Google Cloud Platform (GCP Data Engineering)
La nube de Google se caracteriza por su enfoque altamente serverless y herramientas optimizadas para la analítica a gran escala:
*   **Servicio de Cómputo Principal:** **Google Cloud Dataproc** para desplegar y escalar de forma rápida clústeres administrados de Apache Spark y Hadoop.
*   **Almacenamiento y Analítica Serverless:** **Google Cloud Storage (GCS)** funciona como el data lake principal, y la pieza central de la analítica es **Google BigQuery**, un almacén de datos serverless a escala de petabytes que desacopla almacenamiento y cómputo de manera automática.
*   **Orquestación de Datos:** Uso de herramientas de procesamiento de flujos y lotes como **Google Dataflow**.
*   **Seguridad e Identidad:** Gestión de accesos mediante **Cuentas de Servicio de Google (Service Accounts)** y federación de identidades mediante Google Cloud Identity para el Single Sign-On (SSO).

## Servicios de datos: Azure, AWS, GCP

**Guía de Mapeo y Equivalencia de Servicios de Datos: Azure, AWS y GCP**

### Introducción a la Ingeniería de Datos Multicloud

En el ecosistema actual de Big Data, la portabilidad entre nubes no es simplemente una medida de ahorro, sino un imperativo de resiliencia operativa. Como arquitectos, debemos entender que el diseño de sistemas distribuidos implica gestionar una realidad estadística: a medida que el tamaño del clúster aumenta, la probabilidad de fallo de los nodos también se incrementa (Source: Chapter 1). Apache Spark nació con la promesa original de hacer que la programación distribuida se sintiera como escribir programas regulares (Preface), abstrayendo la complejidad del escalado horizontal frente a las limitaciones de coste y capacidad del escalado vertical.

La piedra angular de estas arquitecturas modernas es el **desacoplamiento absoluto de cómputo y almacenamiento** (Chapter 1). Este principio permite que la infraestructura sea elástica y que el procesamiento trate a un clúster de nodos como una sola unidad lógica. La adopción de estándares abiertos y formatos columnares no es opcional; es la única vía para mitigar el *vendor lock-in* y facilitar una gobernanza unificada. Para ejecutar esta visión, el ingeniero de datos senior debe dominar las herramientas específicas de cada proveedor bajo un marco arquitectónico común.

### Tabla Comparativa de Servicios

La metodología de esta guía agrupa los servicios bajo categorías funcionales, permitiendo una transición fluida entre ecosistemas sin perder la lógica de negocio.

| Categoría Funcional | Microsoft Azure | Amazon Web Services (AWS) | Google Cloud Platform (GCP) |
| :---- | :---- | :---- | :---- |
| **Almacenamiento de Objetos** | ADLS Gen2 | Amazon S3 | Google Cloud Storage (GCS) |
| **Procesamiento Spark (PaaS)** | Azure Databricks | Amazon EMR / AWS Glue | Google Cloud Dataproc |
| **Data Warehousing / Lakehouse** | Synapse Analytics / Fabric | Amazon Redshift | Google BigQuery |
| **Orquestación (Managed)** | Data Factory | AWS Glue / Step Functions | Cloud Composer (Airflow) |
| **NoSQL** | Cosmos DB | DynamoDB | Bigtable |
| **Streaming** | Event Hubs | Kinesis | Pub/Sub |
| **Gobernanza / Metadatos** | Purview | Glue Data Catalog | Data Catalog |

**Nota de Arquitecto:** Aunque estos servicios son equivalentes funcionales, la optimización de costes reside en sus modelos de facturación. La elección entre el modelo basado en *slots* de BigQuery frente a las unidades de almacenamiento de datos (DWU) de Synapse debe ser el factor principal en el diseño de la arquitectura multicloud.

### Análisis por Categoría de Servicio

#### Almacenamiento y Data Lakes

La capa de persistencia debe ser independiente del modelo de modelado (Chapter 9). Sin embargo, no todos los almacenamientos de objetos son iguales. Mientras que Amazon S3 y GCS son estructuras de objetos "planas" (donde las carpetas son simulaciones de prefijos), **Azure Data Lake Storage (ADLS) Gen2** ofrece un **espacio de nombres jerárquico** mediante el protocolo **ABFS**.

**El "So What?" técnico:** En Spark, esto permite operaciones de metadatos atómicas para directorios. En S3, renombrar una carpeta requiere una operación de "copiar y borrar" de O(n) elementos, lo cual es ineficiente. ADLS Gen2 permite renombrados instantáneos, eliminando cuellos de botella críticos en el rendimiento de los *jobs* de Spark.

#### Procesamiento Spark

Apache Spark es el estándar para el procesamiento *in-memory* (Chapter 1). El éxito de una implementación en Databricks, EMR o Dataproc depende de la **Data Locality**. El *driver* de Spark debe distribuir las tareas a los ejecutores donde residen las particiones de datos para minimizar los *shuffles* de red (Source: Chapter 2).

**El "So What?" técnico:** La utilización de entornos administrados (PaaS) frente a la gestión manual de clústeres no es solo una cuestión de mantenimiento, sino de **productividad del analista**. El acceso a un entorno **REPL** (Read-Eval-Print Loop) permite ciclos de experimentación inmediatos, fundamentales para el desarrollo ágil de modelos de datos complejos sin los tiempos muertos de compilación de los sistemas tradicionales (Chapter 1).

#### Data Warehousing y Lakehouse

La convergencia hacia el modelo Lakehouse permite ejecutar SQL sobre datos no estructurados en el Data Lake. Siguiendo el principio de **desacoplamiento de almacenamiento y modelado** (Chapter 9), herramientas como Microsoft Fabric, Redshift y BigQuery permiten escalar horizontalmente el cómputo de forma independiente.

**El "So What?" técnico:** En una estrategia multicloud, el Lakehouse nos permite mantener una única "versión de la verdad" en formatos abiertos (Parquet/Delta) en el almacenamiento físico, mientras cambiamos el motor de SQL (Synapse, Redshift o BigQuery) según la disponibilidad regional o la eficiencia de costes, sin necesidad de migrar o transformar los datos fuente.

#### Gobernanza, Identidad y Seguridad

La seguridad en entornos masivos exige una capa transversal de identidades administradas. La equivalencia entre Microsoft Entra ID, AWS IAM y GCP Service Accounts es la clave para el acceso **"credential-less"** a los datos, evitando la exposición de llaves en el código.

**El "So What?" técnico:** El **Hive Metastore** (referenciado en el texto fuente como el inventario de tablas) actúa como el "pegamento" que permite que diferentes motores de nube entiendan el esquema de los archivos en el Lake. Sin una gobernanza de metadatos centralizada (Purview o Glue Catalog), la trazabilidad y el linaje se pierden en la inmensidad del almacenamiento.

### Mejores Prácticas para Multicloud

Para evitar el *vendor lock-in* y maximizar la eficiencia, es imperativo seguir estos principios:

1. **Priorización de Formatos Columnares:** Es obligatorio usar **Parquet u ORC**. A diferencia de los formatos de fila (CSV/JSON), los formatos columnares permiten a Spark aplicar **predicate pushdown** y **projections**, leyendo solo las columnas y filas necesarias. Esto reduce el escaneo de datos, que es el factor de coste principal en servicios como BigQuery o Athena.

2. **Desacoplamiento Lógico:** La lógica de procesamiento en **PySpark** debe ser agnóstica a la capa de persistencia física. Al parametrizar las rutas de los datos, el mismo código debe ser capaz de ejecutarse en cualquier proveedor.

3. **Orquestación Agnóstica:** Es preferible utilizar estándares abiertos como **Apache Airflow** (Cloud Composer) o **MLflow** para la gestión del ciclo de vida del dato, garantizando que el flujo de trabajo no dependa de disparadores propietarios de una sola nube.

**Conclusión:** La maestría en ingeniería de datos no reside en conocer la consola de Azure o AWS, sino en la comprensión de los principios arquitectónicos compartidos. Al dominar el desacoplamiento, la localidad de los datos y los formatos abiertos, el arquitecto construye soluciones que no solo sobreviven a la nube, sino que la trascienden.

