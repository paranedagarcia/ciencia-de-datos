# Propuesta de Programa Académico

## Diploma Académico en Ciencia e Ingeniería de Datos

### Diseño curricular integrado de Data Science, Data Engineering, Machine Learning, IA y MLOps

---

## 1. Resumen ejecutivo

La evolución del mercado laboral ha generado una convergencia progresiva entre los perfiles de **Data Scientist, Data Engineer, Machine Learning Engineer, Analytics Engineer y AI Engineer**.

Tradicionalmente, estos perfiles se formaban de manera separada. Sin embargo, en la práctica profesional actual existe una creciente interdependencia:

* el Data Scientist necesita comprender cómo se generan, almacenan, transforman y disponibilizan los datos;
* el Data Engineer necesita comprender las características de los datasets que alimentan modelos analíticos y de Machine Learning;
* el ML Engineer necesita dominar tanto pipelines de datos como modelamiento;
* el profesional de IA necesita integrar datos, modelos, APIs, infraestructura y mecanismos de evaluación.

En este contexto se propone el:

> **Diploma Académico en Ciencia e Ingeniería de Datos**

con una duración de **195 horas directas**, distribuidas en **78 sesiones de 2,5 horas**, tres veces por semana, durante aproximadamente **26 semanas**.

El programa integra cinco grandes dimensiones:

1. **Ciencia de Datos**
2. **Ingeniería de Datos**
3. **Machine Learning e Inteligencia Artificial**
4. **Ingeniería de Software, Cloud y MLOps**
5. **Arquitectura, gobierno y operación de soluciones de datos**

El objetivo no es formar especialistas aislados en herramientas, sino profesionales capaces de desarrollar el ciclo completo:

**Datos → Ingeniería → Análisis → Modelamiento → IA → Producción → Monitoreo**

---

# 2. Fundamentación

El principal problema de muchos programas tradicionales es que separan artificialmente:

> Data Science

de

> Data Engineering.

En un entorno productivo, ambos mundos están estrechamente relacionados.

Un modelo predictivo de alto rendimiento puede ser inútil si:

* los datos no llegan correctamente;
* el pipeline no es reproducible;
* existen problemas de calidad;
* el dataset presenta data drift;
* el proceso no está automatizado;
* el modelo no puede desplegarse;
* no existe monitoreo;
* el código solamente funciona dentro de un notebook.

Por otra parte, un excelente Data Engineer necesita comprender:

* qué variables necesita un modelo;
* cómo se genera leakage;
* cómo preparar features;
* cómo evaluar datasets;
* cómo funcionan los modelos;
* qué características debe tener un dataset analítico.

Por ello, el programa propone una formación **T-shaped**:

```text
                    CIENCIA E INGENIERÍA DE DATOS
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
   DATA ENGINEERING      DATA SCIENCE        ML / AI ENGINEERING
          │                    │                    │
      ETL / ELT             Estadística            ML
      SQL                   EDA                    Deep Learning
      Airflow               ML                     GenAI
      Spark                 IA                     MLOps
      Kafka
          │                    │                    │
          └────────────────────┼────────────────────┘
                               │
                        CLOUD / PRODUCCIÓN
```

---

# 3. Objetivo general

### Objetivo general

Formar profesionales capaces de **diseñar, desarrollar, implementar, evaluar y operar soluciones integrales de datos**, combinando fundamentos de Ciencia de Datos, Ingeniería de Datos, Machine Learning, Inteligencia Artificial, arquitectura de software, computación distribuida, cloud computing y MLOps.

---

# 4. Objetivos específicos

Al finalizar el programa, el participante será capaz de:

1. Comprender el ciclo completo de vida de los datos.
2. Programar soluciones de procesamiento y análisis utilizando Python.
3. Diseñar y consultar bases de datos relacionales.
4. Construir procesos ETL/ELT.
5. Diseñar pipelines reproducibles.
6. Orquestar workflows mediante **Apache Airflow**.
7. Comprender e implementar arquitecturas de procesamiento de eventos mediante **Apache Kafka**.
8. Diseñar Data Warehouses, Data Lakes y arquitecturas Lakehouse.
9. Procesar datos distribuidos mediante Apache Spark.
10. Implementar controles de calidad y observabilidad de datos.
11. Realizar análisis estadístico y exploratorio.
12. Desarrollar modelos de Machine Learning.
13. Implementar técnicas avanzadas de ML e IA.
14. Utilizar técnicas de explicabilidad y evaluación de modelos.
15. Implementar prácticas de MLOps.
16. Construir APIs para exponer modelos y servicios de datos.
17. Utilizar Docker y herramientas de integración continua.
18. Desplegar soluciones en ambientes cloud.
19. Diseñar arquitecturas de datos completas.
20. Desarrollar un proyecto integral de datos listo para ser presentado como portfolio profesional.

---

# 5. Perfil de ingreso

El programa está dirigido preferentemente a:

* ingenieros;
* profesionales TI;
* desarrolladores;
* analistas de datos;
* científicos de datos;
* ingenieros de software;
* profesionales de BI;
* arquitectos de datos;
* profesionales interesados en IA.

Se recomienda contar con:

* conocimientos básicos de programación;
* conocimientos matemáticos equivalentes a enseñanza media;
* familiaridad básica con computadores y sistemas de información.

No obstante, el programa puede contemplar un **módulo de nivelación de Python** para participantes que requieran reforzamiento.

---

# 6. Perfil de egreso

El egresado será capaz de:

> Diseñar y desarrollar soluciones de datos completas, desde la adquisición e ingestión de información hasta su procesamiento, almacenamiento, análisis, modelamiento predictivo, implementación de soluciones de inteligencia artificial y despliegue en ambientes productivos.

Además, podrá participar profesionalmente en roles como:

* Data Scientist
* Data Engineer
* Machine Learning Engineer
* Analytics Engineer
* AI Engineer
* Data Analyst avanzado
* ML Engineer
* Data/AI Developer

---

# 7. Estructura curricular

La propuesta contempla **13 módulos y 195 horas directas**.

|        Nº | Módulo                                                      |         Horas |
| --------: | ----------------------------------------------------------- | ------------: |
|         1 | Fundamentos de Ciencia e Ingeniería de Datos                |            15 |
|         2 | Python para Ciencia e Ingeniería de Datos                   |            15 |
|         3 | Bases de Datos y SQL Avanzado                               |            15 |
|         4 | ETL/ELT y Data Pipelines                                    |            15 |
|         5 | **Orquestación de Pipelines con Apache Airflow**            |        **15** |
|         6 | Data Warehouse, Data Lake, Lakehouse y Big Data             |            15 |
|         7 | **Streaming y Arquitecturas Event-Driven con Apache Kafka** |        **15** |
|         8 | Calidad, Gobernanza y Observabilidad de Datos               |            15 |
|         9 | Estadística, EDA y Experimentación                          |            15 |
|        10 | Machine Learning y Modelamiento Predictivo                  |            15 |
|        11 | Machine Learning Avanzado e Inteligencia Artificial         |            15 |
|        12 | Cloud, MLOps, APIs y Producción                             |            15 |
|        13 | Proyecto Integrador de Ciencia e Ingeniería de Datos        |            15 |
| **TOTAL** |                                                             | **195 horas** |

### Distribución temporal

Cada módulo:

**6 sesiones × 2,5 horas = 15 horas**

13 módulos:

**78 sesiones × 2,5 horas = 195 horas**

Con tres sesiones semanales:

**78 / 3 = 26 semanas**

Por lo tanto:

> **Duración aproximada: 6 meses.**

---

# 8. Módulo 1 — Fundamentos de Ciencia e Ingeniería de Datos

### 15 horas

### Contenidos

* Ecosistema profesional de datos.
* Data Science.
* Data Engineering.
* Machine Learning Engineering.
* Analytics Engineering.
* AI Engineering.
* Ciclo de vida de los datos.
* Data-to-Insight.
* Data-to-ML.
* Data-to-Production.
* Arquitecturas modernas.
* OLTP y OLAP.
* Data Warehouse.
* Data Lake.
* Lakehouse.
* Batch y Streaming.
* Cloud Computing.
* Introducción a proyectos de datos.

### Laboratorio

Diseño de la arquitectura de un sistema de datos.

---

# 9. Módulo 2 — Python para Ciencia e Ingeniería de Datos

### 15 horas

### Contenidos

* Python profesional.
* estructuras de datos;
* funciones;
* programación modular;
* clases;
* excepciones;
* manejo de archivos;
* APIs;
* ambientes virtuales;
* paquetes;
* type hints;
* logging;
* testing;
* configuración.

### Librerías

* NumPy
* Pandas
* Polars
* Pydantic
* SQLAlchemy

### Proyecto

Construcción de un paquete Python para procesamiento de datos.

---

# 10. Módulo 3 — Bases de Datos y SQL Avanzado

### 15 horas

### Contenidos

* Modelo relacional.
* Normalización.
* claves.
* índices.
* constraints.
* SQL avanzado.
* JOIN.
* CTE.
* Window Functions.
* Views.
* transacciones.
* ACID.
* optimización.
* execution plans.

### NoSQL

* documentos;
* key-value;
* columnar;
* bases distribuidas.

### Proyecto

Diseño de una base operacional y un modelo analítico.

---

# 11. Módulo 4 — ETL/ELT y Data Pipelines

### 15 horas

### Contenidos

* ETL vs ELT.
* Ingestion.
* APIs.
* CSV.
* JSON.
* Parquet.
* SFTP.
* procesamiento incremental.
* CDC.
* transformación.
* particionamiento.
* schema evolution.
* idempotencia.
* pipelines reproducibles.

### Arquitectura

```text
Sources
   ↓
Ingestion
   ↓
Validation
   ↓
Transformation
   ↓
Storage
   ↓
Analytical Dataset
```

---

# 12. Módulo 5 — Orquestación con Apache Airflow

### 15 horas

Este módulo será uno de los elementos diferenciadores del diploma.

### Contenidos

* Workflow orchestration.
* Apache Airflow.
* arquitectura.
* DAG.
* Tasks.
* Scheduler.
* Executor.
* Workers.
* Metadata Database.
* Operators.
* Sensors.
* Hooks.
* Connections.
* Variables.
* XCom.

### Desarrollo

* construcción de DAGs;
* dependencias;
* scheduling;
* retries;
* branching;
* task groups;
* dynamic task mapping;
* backfill;
* manejo de errores.

### Operación

* logs;
* monitoring;
* debugging;
* alertas;
* ejecución manual;
* gestión de fallos.

### Proyecto

Orquestar el pipeline construido en el módulo anterior.

---

# 13. Módulo 6 — Data Warehouse, Data Lake, Lakehouse y Big Data

### 15 horas

### Contenidos

* Data Warehouse.
* Data Lake.
* Lakehouse.
* arquitectura dimensional.
* Star Schema.
* Snowflake Schema.
* Fact Tables.
* Dimensions.
* Slowly Changing Dimensions.
* Data Marts.
* Parquet.
* particionamiento.

### Apache Spark

* Spark architecture.
* PySpark.
* DataFrames.
* Spark SQL.
* particiones.
* shuffle.
* joins.
* optimización.

### Proyecto

Construcción de un Lakehouse analítico.

---

# 14. Módulo 7 — Streaming y Apache Kafka

### 15 horas

La incorporación de Kafka permite que el programa cubra tanto **batch engineering** como **streaming engineering**.

### Contenidos

* Batch vs Streaming.
* Event-driven architecture.
* Apache Kafka.
* brokers.
* topics.
* partitions.
* producers.
* consumers.
* consumer groups.
* offsets.
* replication.
* fault tolerance.

### Arquitectura

```text
                    KAFKA
                      │
        ┌─────────────┼─────────────┐
        ↓             ↓             ↓
     Producer      Producer      Producer
        │             │             │
        └─────────────┼─────────────┘
                      ↓
                    Topic
                      │
             ┌────────┴────────┐
             ↓                 ↓
          Consumer          Consumer
             │                 │
             ↓                 ↓
          Database         Data Lake
```

### Proyecto

Implementar un pipeline de eventos utilizando Kafka.

---

# 15. Módulo 8 — Calidad, Gobernanza y Observabilidad

### 15 horas

### Data Quality

* completitud;
* unicidad;
* consistencia;
* validez;
* exactitud;
* oportunidad.

### Data Governance

* Data Owner.
* Data Steward.
* Data Custodian.
* Data Architect.
* políticas de datos.

### Metadata

* Data Catalog.
* Data Lineage.
* Business Glossary.
* Schema Management.

### Observabilidad

* freshness;
* volume;
* distribution;
* schema drift;
* anomaly detection.

### Proyecto

Implementación de un sistema automatizado de calidad de datos.

---

# 16. Módulo 9 — Estadística, EDA y Experimentación

### 15 horas

### Contenidos

* estadística descriptiva;
* probabilidad;
* distribuciones;
* muestreo;
* intervalos de confianza;
* hipótesis;
* correlación;
* covarianza;
* regresión;
* análisis multivariado;
* EDA;
* outliers;
* missing data;
* sesgo;
* data leakage.

### Herramientas

* NumPy
* Pandas
* Polars
* SciPy
* Statsmodels
* Matplotlib

---

# 17. Módulo 10 — Machine Learning y Modelamiento Predictivo

### 15 horas

### Contenidos

* supervised learning;
* unsupervised learning;
* train/validation/test;
* cross-validation;
* feature engineering;
* pipelines;
* regresión;
* clasificación;
* árboles;
* Random Forest;
* Gradient Boosting;
* XGBoost;
* LightGBM;
* clustering;
* PCA.

### Evaluación

* MAE;
* RMSE;
* accuracy;
* precision;
* recall;
* F1;
* ROC-AUC;
* calibration.

---

# 18. Módulo 11 — Machine Learning Avanzado e Inteligencia Artificial

### 15 horas

### Machine Learning avanzado

* ensembles;
* boosting;
* hyperparameter optimization;
* imbalance;
* feature selection;
* explainability;
* SHAP;
* interpretabilidad;
* fairness.

### Deep Learning

* redes neuronales;
* MLP;
* CNN;
* embeddings;
* transfer learning.

### IA Generativa

* LLM;
* embeddings;
* vector databases;
* RAG;
* prompt engineering;
* evaluación de aplicaciones LLM.

### Proyecto

Construcción de una solución ML/IA aplicada.

---

# 19. Módulo 12 — Cloud, MLOps, APIs y Producción

### 15 horas

Este módulo integra ingeniería de software con Machine Learning.

### Software Engineering

* Git;
* GitHub;
* Clean Code;
* testing;
* documentación;
* code review.

### APIs

* REST;
* FastAPI;
* Pydantic;
* OpenAPI.

### Containers

* Docker;
* imágenes;
* containers;
* Docker Compose.

### MLOps

* experiment tracking;
* MLflow;
* model registry;
* reproducibilidad;
* CI/CD;
* model deployment;
* model monitoring;
* data drift;
* model drift.

### Cloud

Se recomienda seleccionar una plataforma principal:

* Microsoft Azure
* AWS
* Google Cloud

y enseñar los conceptos transferibles a las otras.

---

# 20. Módulo 13 — Proyecto Integrador

### 15 horas directas

El proyecto debe integrar **todos los componentes del programa**.

El producto final deberá contener, como mínimo:

```text
                 DATA SOURCES
                      │
                      ▼
                 INGESTION
                      │
                      ▼
              DATA QUALITY
                      │
             ┌────────┴────────┐
             ▼                 ▼
          BATCH             STREAMING
             │                 │
          Airflow            Kafka
             │                 │
             └────────┬────────┘
                      ▼
                 DATA LAKE
                      │
                      ▼
               TRANSFORMATION
                      │
                      ▼
               DATA WAREHOUSE
                      │
             ┌────────┴────────┐
             ▼                 ▼
            EDA                ML
                               │
                               ▼
                            MLOps
                               │
                               ▼
                             API
                               │
                               ▼
                            Docker
                               │
                               ▼
                             Cloud
```

---

# 21. Metodología de enseñanza

Cada sesión de 2,5 horas tendrá una estructura aproximada:

| Actividad            |      Tiempo |
| -------------------- | ----------: |
| Conceptos            |   35–40 min |
| Demostración técnica |      20 min |
| Laboratorio          |      70 min |
| Desafío / proyecto   |   20–25 min |
| **Total**            | **150 min** |

Esto genera una formación predominantemente práctica.

### Distribución estimada

* **30% teoría y fundamentos**
* **50% laboratorio**
* **20% proyecto/desafíos**

---

# 22. Proyecto transversal

El proyecto integrador comenzará desde el primer módulo.

Cada estudiante o equipo seleccionará un problema real, por ejemplo:

* mantenimiento predictivo;
* predicción de demanda;
* segmentación de clientes;
* fraude;
* movilidad;
* salud;
* energía;
* logística;
* gestión pública;
* ventas;
* riesgo financiero.

Durante el programa, el proyecto evolucionará:

```text
Módulo 1 → Problema + arquitectura

Módulo 2 → Código Python

Módulo 3 → Base de datos

Módulo 4 → ETL

Módulo 5 → Airflow

Módulo 6 → Lakehouse + Spark

Módulo 7 → Kafka

Módulo 8 → Data Quality

Módulo 9 → EDA

Módulo 10 → ML

Módulo 11 → IA

Módulo 12 → MLOps + API

Módulo 13 → Producto final
```

Esto es particularmente importante porque el estudiante termina con **un proyecto de portfolio profesional**, no simplemente con una colección de notebooks.

---

# 23. Evaluación

Propongo una evaluación basada en competencias.

| Evaluación                |     Peso |
| ------------------------- | -------: |
| Laboratorios individuales |      20% |
| Desafíos técnicos         |      15% |
| Evaluaciones conceptuales |      15% |
| Proyecto integrador       |      35% |
| Defensa técnica           |      15% |
| **Total**                 | **100%** |

La aprobación debería exigir tanto un mínimo académico global como un desempeño mínimo en el proyecto integrador.

---

# 24. Requisitos tecnológicos

El alumno debería trabajar principalmente con:

### Lenguaje

**Python**

### Data Engineering

* SQL
* PostgreSQL
* DuckDB
* Pandas
* Polars
* PySpark
* Apache Airflow
* Apache Kafka

### Data Science

* NumPy
* SciPy
* Statsmodels
* Scikit-learn
* XGBoost
* LightGBM

### IA

* PyTorch
* herramientas LLM
* embeddings
* vector databases

### MLOps

* Git
* GitHub
* Docker
* MLflow
* FastAPI

### Cloud

Una plataforma principal:

**Azure / AWS / GCP**

---

# 25. Competencias profesionales resultantes

Al finalizar el diploma, el participante debería poder:

### Data Engineering

**Diseñar y construir pipelines de datos productivos.**

### Orquestación

**Automatizar y administrar workflows mediante Airflow.**

### Streaming

**Diseñar soluciones de procesamiento de eventos mediante Kafka.**

### Big Data

**Procesar datos distribuidos utilizando Spark.**

### Data Science

**Construir análisis estadísticos y modelos predictivos.**

### Machine Learning

**Desarrollar, evaluar y explicar modelos.**

### IA

**Construir aplicaciones basadas en modelos modernos de IA.**

### MLOps

**Llevar modelos desde notebooks a ambientes productivos.**

### Software Engineering

**Construir código mantenible, testeable y versionado.**

### Cloud

**Implementar arquitecturas de datos en infraestructura cloud.**

---

# 26. Diferenciación académica

La principal fortaleza del programa es que no se presenta como:

> "Diplomado de Ciencia de Datos con algunas herramientas de Data Engineering."

Ni como:

> "Diplomado de Data Engineering con un módulo de Machine Learning."

La propuesta académica es:

> **Ciencia e Ingeniería de Datos como una disciplina integrada.**

Su diferencial está en conectar:

**Python + SQL + ETL + Airflow + Lakehouse + Spark + Kafka + Data Quality + Estadística + ML + IA + MLOps + APIs + Cloud.**

Esto permite formar un profesional que comprenda tanto:

### ¿Cómo obtengo y preparo los datos?

como:

### ¿Cómo extraigo conocimiento de ellos?

y finalmente:

### ¿Cómo convierto ese conocimiento en un producto tecnológico que funcione en producción?

---

# 27. Carga académica recomendada

Las **195 horas directas** no deberían presentarse como la totalidad de la dedicación del estudiante.

Recomiendo establecer:

| Actividad                          |         Horas |
| ---------------------------------- | ------------: |
| Clases directas                    |       **195** |
| Trabajo autónomo                   |        80–100 |
| Proyecto integrador                |         40–50 |
| Lecturas/evaluaciones              |         20–30 |
| **Carga académica total estimada** | **335–375 h** |

Esto posicionaría el programa como un **Diploma Académico exigente**, en lugar de un curso extendido de herramientas.

---

# 28. Duración

### Modalidad propuesta

**Presencial / online sincrónica / híbrida**

### Frecuencia

**3 sesiones por semana**

### Duración sesión

**2,5 horas**

### Duración total

**26 semanas**

### Horas directas

**195 horas**

### Sesiones

**78 sesiones**

---

# 29. Denominación propuesta

Recomiendo mantener:

# **Diploma Académico en Ciencia e Ingeniería de Datos**

y utilizar como subtítulo:

### **Data Engineering, Data Science, Machine Learning, Inteligencia Artificial y MLOps**

Esto permite comunicar inmediatamente que no se trata de un diplomado tradicional de Data Science.

Una alternativa comercial/académica sería:

> **Diploma Académico en Ciencia e Ingeniería de Datos: Arquitecturas de Datos, Machine Learning e Inteligencia Artificial**

Personalmente prefiero la primera denominación porque es **más limpia, transversal y escalable**.

---

# 30. Síntesis final

La propuesta de **195 horas directas** permite construir un programa significativamente más completo que un diplomado convencional de Ciencia de Datos.

La secuencia pedagógica queda:

**Fundamentos → Python → SQL → ETL → Airflow → Lakehouse/Spark → Kafka → Data Quality → Estadística → ML → IA → MLOps/Cloud → Proyecto**

Y conceptualmente:

```text
                       CIENCIA E INGENIERÍA
                              DE DATOS
                                  │
              ┌───────────────────┴──────────────────┐
              │                                      │
       INGENIERÍA DE DATOS                    CIENCIA DE DATOS
              │                                      │
       SQL / ETL / ELT                         Estadística / EDA
       Airflow                                Machine Learning
       Spark                                  Deep Learning
       Kafka                                  IA Generativa
       Lakehouse
              │                                      │
              └───────────────────┬──────────────────┘
                                  │
                            ML ENGINEERING
                                  │
                         MLOps / APIs / Docker
                                  │
                                  ▼
                               CLOUD
                                  │
                                  ▼
                            PRODUCCIÓN
```

**La incorporación de Airflow y Kafka es especialmente acertada:** Airflow cubre la **orquestación y automatización de workflows**, mientras Kafka introduce la dimensión de **event streaming y arquitecturas orientadas a eventos**. De esta manera, el alumno no aprende solamente a "procesar datos", sino a **construir y operar sistemas modernos de datos**.

El resultado sería un perfil profesional híbrido con una combinación de competencias que puede cubrir buena parte de las responsabilidades que actualmente aparecen distribuidas entre **Data Scientist, Data Engineer y ML Engineer**.
