---
id: etl
title: "ETL & ELT"
sidebar_label: "💻 ETL & ELT"
description: "Los procesos de integración y preparación de datos son fundamentales en cualquier arquitectura de datos"
slug: /etl
---


Los procesos de integración y preparación de datos son fundamentales en cualquier arquitectura de datos moderna. A continuación, se detallan los significados, las diferencias operativas y las herramientas de uso actual para los enfoques **ETL** y **ELT**.

![](img/ETL_1.png) 


### ¿Qué es el proceso ETL?
**ETL** significa **Extract, Transform, and Load** (Extraer, Transformar y Cargar) . Consiste en un flujo de procesamiento y agregación diseñado para dar a los datos la forma y el formato específicos requeridos antes de almacenarlos . 

El proceso tradicionalmente sigue tres etapas secuenciales ``:
1.  **Extract (Extracción):** Se obtienen los datos de múltiples fuentes (como bases de datos, archivos planos, etc.) . Durante esta fase, es fundamental **validar la información** y rechazar los registros dañados o malformados para asegurar la calidad de entrada.

2.  **Transform (Transformación):** Es la etapa más robusta del flujo, donde se realiza el procesamiento pesado . Incluye la limpieza de datos, estandarización de rangos (por ejemplo, unificar nomenclaturas de género), eliminación de duplicados, transposición, ordenamiento, agregación y la derivación de nuevas características .

3.  **Load (Carga):** Los datos transformados y limpios se cargan en el destino final de manera periódica (por ejemplo, diariamente o por lotes), que típicamente es un **Data Warehouse** (almacén de datos estructurado), base de datos o *feature store*.

### ¿Qué es el proceso ELT?
**ELT** significa **Extract, Load, and Transform** (Extraer, Cargar y Transformar). Este paradigma surgió debido a la enorme dificultad de mantener esquemas estructurados rígidos ante el crecimiento masivo y la velocidad de llegada de los datos. 

En lugar de transformar los datos antes de guardarlos, el enfoque ELT propone:
1.  **Extract (Extracción):** Obtener los datos crudos de las fuentes de origen.

2.  **Load (Carga):** Cargar inmediatamente los datos sin procesar directamente en un repositorio flexible, comúnmente un **Data Lake** (lago de datos).

3.  **Transform (Transformación):** Dejar que la aplicación o el proceso consumidor final extraiga y transforme los datos bajo demanda directamente desde el almacenamiento crudo.

---

### Diferencias Clave entre ETL y ELT

*   **Momento de la Transformación:** En **ETL**, la transformación ocurre en un área intermedia de tránsito antes de guardar los datos en el destino final. En **ELT**, los datos se cargan primero en bruto y la transformación se realiza de manera posterior dentro del propio motor de almacenamiento.

*   **Destino y Estructura:** **ETL** está diseñado para alimentar repositorios altamente estructurados como **Data Warehouses**. **ELT** aprovecha la flexibilidad de almacenamiento masivo y no estructurado de los **Data Lakes**.

*   **Velocidad de Ingesta:** **ELT** permite una **llegada de datos sumamente rápida (*fast arrival*)** debido a que apenas requiere procesamiento inicial antes de ser almacenados. **ETL** puede retrasar la disponibilidad de los datos debido al tiempo que consume la etapa de transformación previa.

*   **Eficiencia en Consultas:** Aunque **ELT** ingiere datos más rápido, buscar y consultar directamente sobre volúmenes masivos de datos crudos no procesados puede volverse ineficiente para el análisis cotidiano. **ETL** ofrece datos ya organizados y optimizados para consultas analíticas rápidas.

---

### Herramientas de Uso Actual

Para desarrollar e implementar estos pipelines de datos se utilizan diversos motores de cómputo, orquestadores y plataformas híbridas según el flujo seleccionado:

1.  **Motores de Cómputo y Transformación:**
    *   **Apache Spark:** Es el estándar de la industria y la herramienta más popular para procesar transformaciones y ejecutar tareas de ETL/ELT distribuidas a gran escala.
    *   **Apache Flink, KSQL y Spark Streaming:** Herramientas clave para procesar y transformar flujos de datos y eventos en tiempo real (*stream processing*).

2.  **Soluciones Lakehouse (Enfoque Híbrido):**
    *   **Databricks y Snowflake:** Plataformas líderes que unifican la flexibilidad de almacenamiento de un *Data Lake* (ideal para ELT) con la gobernanza, velocidad y estructuras de un *Data Warehouse* (ideal para ETL).

3.  **Servicios en la Nube y Catalogación:**
    *   **AWS Glue:** Funciona como un servicio administrado (con su Hive Metastore) diseñado para catalogar, limpiar y gestionar pipelines de ETL de datos a gran escala.
    *   **Amazon Lake Formation:** Herramienta diseñada para automatizar la recolección, limpieza, eliminación de duplicados y catalogación necesarias para establecer un *Data Lake* eficiente.

4.  **Almacenamiento y Persistencia (Destinos):**
    *   **Sistemas de Archivos y Objetos:** Amazon S3, HDFS y Azure Blob Storage son los destinos de persistencia más comunes para flujos de datos.

    *   **Bases de Datos NoSQL y Analíticas:** Cassandra, HBase, Google BigQuery y Amazon Redshift se utilizan ampliamente para alojar los datos listos para el análisis.

---
## Databricks vs Snowflake

**Arquitecturas Lakehouse en Databricks y Snowflake para ETL/ELT**

La arquitectura Lakehouse no es simplemente una evolución incremental; es una convergencia necesaria que resuelve la fragmentación estructural entre el Data Lake y el Data Warehouse. Como estrategas, debemos entender que el desacoplamiento de cómputo y almacenamiento es el pilar que permite la agilidad moderna. No obstante, la verdadera ventaja competitiva reside en la unificación.

### La arquitectura Lakehouse

Desde una perspectiva de **Teoría de Conjuntos y Funciones** (Contexto 1.2), definimos el Lakehouse como un superconjunto **S**. Sea **A** el conjunto de almacenamiento de objetos (Data Lake), caracterizado por una alta cardinalidad de datos no estructurados, y sea **B** el conjunto de estructuras relacionales (Data Warehouse). La arquitectura Lakehouse es la unión $S = A \cup B$.

El valor estratégico ("So What?") de esta unión es la eliminación del "espacio de latencia". Históricamente, las funciones analíticas requerían transformaciones costosas para mapear elementos de A hacia B. En un Lakehouse, operamos directamente sobre el superconjunto. Al reducir los pasos de extracción y carga, tratamos los datos como una función directa del almacenamiento original, lo que mitiga el riesgo de deriva de datos y reduce drásticamente el costo operativo de mantener silos redundantes.

### Implementación de Databricks

Databricks representa la filosofía de "Data Engineering como Ingeniería de Software". Su motor, Apache Spark, procesa datos mediante un Grafo Acíclico Dirigido (DAG). Matemáticamente, podemos modelar el DAG como una función $f: \{1, \dots, k\} \rightarrow A$, donde asignamos una lista de `k` tareas a un conjunto de recursos de cómputo.

### Optimización y Delta Lake

El motor de optimización (Photon) gestiona la ejecución paralela sobre archivos Parquet. Aplicando la lógica de **Permutaciones en S\_n**, el sistema no solo ejecuta tareas, sino que busca la permutación óptima del orden de ejecución para minimizar el tiempo de finalización.

A diferencia de Snowflake, Databricks gestiona el "image-word" de los archivos a través del **Transaction Log** de Delta Lake. Esta capa ACID garantiza que cada transacción sea una actualización atómica en el registro, permitiendo que cargas de trabajo de Machine Learning accedan a versiones históricas del dato (Time Travel) sin interferir con procesos de ingesta masiva. Esta naturaleza "code-first" permite una flexibilidad arquitectónica superior para datos no estructurados, donde el esquema se define por código y no por rigidez relacional.

### Implementación de Snowflake

Snowflake ha ejecutado un pivot estratégico hacia un modelo Lakehouse híbrido. Su adopción de Apache Iceberg representa una rendición estratégica ante la inevitabilidad de los formatos de almacenamiento abiertos. Snowflake se define como "Data Engineering como un Servicio de Utilitario (Utility Service)".

#### Escalabilidad Elástica y Teorema 1.24

Para modelar la arquitectura de "Multi-cluster Shared Data" de Snowflake, recurrimos a la **Propiedad Multiplicativa de Dibujos** (Teorema 1.24). Podemos representar el rendimiento total del sistema $c_k$ como la convolución de recursos asignados:

```math
c_k= ∑_{j=0}^ka_jb_{k−j}
```

 

Donde $a_j$ representa las "extracciones" o asignaciones de recursos para procesos de ingesta y $b_{k-j}$ las asignaciones para consultas analíticas. La genialidad de Snowflake radica en que $a_j$ y $b_{k-j}$ son independientes; la elasticidad de Snowflake permite ajustar los sumandos sin que exista interferencia transversal. Mientras Databricks confía en el Transaction Log local, Snowflake utiliza su **Servicio de Metadatos Global** para orquestar esta distribución, garantizando una concurrencia masiva sin degradación de performance.

### Comparativa de Procesos

La transición hacia el Lakehouse ha difuminado la línea entre ETL y ELT. Sin embargo, la fiabilidad de estas canalizaciones es el factor crítico de éxito.

#### Fiabilidad como Proceso de Bernoulli

Si modelamos un pipeline de n etapas como un **Proceso de Bernoulli**, la integridad de la transformación total es un evento de éxito E. Si cada etapa tiene una probabilidad de éxito p, la probabilidad de que el pipeline completo finalice correctamente es 
```math
P(E) = p^n
```

Las arquitecturas Lakehouse unificadas aumentan la fiabilidad del sistema precisamente porque reducen el valor de n. Al eliminar pasos intermedios de movimiento de datos entre un Lake y un Warehouse, maximizamos P(E).

#### Tabla Comparativa Técnica

| Criterio | Databricks (Software Engineering) | Snowflake (Utility Service) |
| :---- | :---- | :---- |
| **Ingesta de Datos** | Streaming nativo y archivos masivos. | Orientado a tablas externas e Iceberg. |
| **Transformación** | Code-first (Python/Spark). Potencial ilimitado. | SQL-first. Simplicidad absoluta. |
| **Metadatos** | Delta Transaction Log (Descentralizado). | Global Metadata Service (Centralizado). |
| **Eficiencia** | Superior en IA/ML y Data Science pesado. | Superior en BI y concurrencia analítica. |
| **Veredicto del Arquitecto** | Ideal para equipos que construyen software. | Ideal para equipos que consumen servicios. |

### Conclusión y Recomendaciones Estratégicas

La elección entre Databricks y Snowflake no es una cuestión de potencia, sino de filosofía operativa. El Arquitecto de Datos debe basar su decisión en la **Esperanza Matemática** (Contexto 3.1.2) del retorno de inversión (ROI).

Definimos la función de valor esperado como: 
```math
E[X] = \sum (Value_i \cdot P_i) - Cost
```

Utilizando la **Fórmula de Cavalieri**, podemos modelar el ROI no como un punto estático, sino como el área bajo la curva de probabilidad de éxito de nuestros proyectos de datos.

### Recomendaciones Finales

1. **Priorice Databricks** si su estrategia de negocio depende de modelos predictivos complejos y Machine Learning. Aquí, Value\_i aumenta gracias a la flexibilidad del motor Spark para manejar datos no estructurados que Snowflake aún procesa de forma subóptima.  

2. **Priorice Snowflake** si su objetivo es democratizar el dato a través de SQL para analistas de negocio, minimizando el Cost operativo de mantenimiento de infraestructura. 

3. **Interoperabilidad Obligatoria:** Independientemente de la plataforma, el uso de formatos abiertos (Delta o Iceberg) es mandatorio para evitar el *vendor lock-in* y asegurar que la arquitectura mantenga su valor ante futuras permutaciones del ecosistema tecnológico.

