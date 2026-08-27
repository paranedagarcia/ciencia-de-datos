---
id: dbt-airflow
title: ""
sidebar_label: "📄 Integración con Airflow"
description: ""
slug: /dbt-airflow
---

## **Integración con Airflow 3**

**Reporte Técnico: Integración Avanzada de dbt y Airflow 3 mediante el Framework Cosmos**

### La Necesidad de Integración

La evolución de la ingeniería de datos ha transitado desde la simple gestión de flujos de trabajo hacia la construcción de ecosistemas donde la orquestación y la transformación convergen para mitigar el "cuello de botella en la productividad del analista". Como se subraya en los fundamentos de la analítica a escala (*Ch. 1, p. 9*), el desafío central no reside únicamente en la capacidad de cómputo, sino en permitir que el profesional de datos se enfoque en la "iteración" y la "experimentación" en lugar de quedar atrapado en la "fontanería" técnica de los sistemas. La convergencia entre **dbt (data build tool)** y **Apache Airflow** es la respuesta estratégica a la naturaleza "desordenada" del dato crudo (*Ch. 2*), permitiendo que la limpieza, el munging y la fusión se realicen bajo una abstracción que oculte la complejidad de los sistemas distribuidos.

Tradicionalmente, la ejecución de dbt mediante el `BashOperator` ha sido el estándar, pero bajo un análisis riguroso, este enfoque resulta insuficiente para entornos de producción de misión crítica. Esta insuficiencia se manifiesta en tres dimensiones:

1. **Opacidad de las dependencias:** La lógica interna del DAG de dbt se pierde, transformándose en una "caja negra" para el orquestador.  
2. **Ilegibilidad de logs agrupados:** La centralización de logs en un solo proceso de Bash impide una depuración granular, contraviniendo el principio de observabilidad.  
3. **Fragilidad ante fallos y pérdida de productividad:** Un error en un único modelo obliga a reiniciar el proceso completo, desperdiciando recursos y tiempo de analista, lo cual es inaceptable en ciclos de vida de datos que requieren una iteración constante.

Cosmos surge para eliminar estas fricciones, permitiendo que Airflow "entienda" la estructura lógica de dbt y la ejecute de forma nativa.

### Cómo Opera Astronomer Cosmos

La importancia estratégica de Cosmos radica en delegar el *parsing* del grafo de dbt a un framework que permite a Airflow interpretar la semántica de la transformación. El modelo mental para entender esta operación es el **Spark Adaptive Query Execution (AQE)** introducido en Spark 3.0 (*Ch. 1, p. 8*). Así como el AQE adapta el plan de ejecución físico en tiempo de ejecución para reducir la complejidad de la optimización manual, Cosmos realiza un parsing dinámico (ya sea mediante el `manifest.json` o en *runtime*) para que Airflow adapte dinámicamente sus tareas a la estructura de dbt, eliminando la necesidad de definiciones manuales y estáticas.

#### Mapeo de Entidades y Topología

Cosmos traduce fielmente la ontología de dbt a entidades de Airflow, asegurando que la topología del proyecto se refleje en el orquestador:

* **Models:** Se transforman en `Tasks` individuales o `TaskGroups`, permitiendo paralelismo real.  
* **Tests:** Se integran como tareas de validación post-ejecución, garantizando la integridad antes de que los procesos dependientes consuman el dato.  
* **Seeds y Snapshots:** Se mapean como tareas de preparación y versionado histórico, respectivamente.

Este mapeo granular garantiza que, al igual que los planes físicos de Spark optimizan la ejecución de datos, Airflow pueda gestionar la re-ejecución selectiva de nodos fallidos, optimizando el uso del clúster.

### Arquitectura de Gobernanza y Observabilidad

El lanzamiento de **Airflow 3**, con su arquitectura orientada a *API Server* y un *Task SDK* renovado, establece un nuevo paradigma para la gobernanza a escala. En esta versión, la orquestación adopta el **modelo de datos paralelos** (*Ch. 2, p. 13*): así como en Spark el particionamiento de datos permite el procesamiento paralelo en múltiples ejecutores, el Task SDK de Airflow 3 permite un escalamiento horizontal de las tareas de transformación, permitiendo que cada modelo de dbt se ejecute con independencia operativa y de logs.

La integración con estándares de **OpenLineage** y sistemas de metadatos (como Unity Catalog o los mencionados en el contexto de ADAM en el *Capítulo 9*) permite una trazabilidad de punta a punta. Al conectar Airflow 3 con Cosmos, los ingenieros pueden capturar el linaje desde la ingesta hasta el modelo final, reduciendo el tiempo de inactividad. Esta arquitectura es vital para satisfacer las necesidades de **seguimiento de experimentos** y **servicio de modelos** descritas en el ciclo de vida de ML (*Ch. 11*), asegurando que cualquier anomalía en el dato pueda rastrearse hasta su origen físico.

<details>
<summary>💻 **Ejemplo Práctico de Código en Python (Nivel Producción)**</summary>

La implementación bajo Airflow 3 y Cosmos destaca por su simplicidad declarativa, separando la lógica de negocio de la configuración de infraestructura.

```python showLineNumbers
from datetime import datetime
from pathlib import Path
from airflow.decorators import dag
from cosmos import DbtTaskGroup, ProjectConfig, ProfileConfig, ExecutionConfig
from cosmos.profiles import PostgresUserPasswordProfileMapping

# Ruta del proyecto dbt (Abstracción del sistema de archivos)

DBT_ROOT_PATH = Path("/usr/local/airflow/dbt")
DBT_PROJECT_NAME = "analytics_v3"

@dag(
    schedule_interval="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['production', 'airflow3'],
)

def dbt_airflow3_integration():
    """
    Pipeline de transformación avanzado utilizando Airflow 3 Task SDK y Cosmos.
    """
    # NOTA PEDAGÓGICA: Decoupling Storage from Modeling (Ch. 9, p. 162)
    # Siguiendo los principios de sistemas distribuidos, desacoplamos el perfil de 
    # conexión (Storage) de la lógica de transformación (Modeling). 
    # Esto facilita la portabilidad entre entornos (Dev/Prod).

    profile_config = ProfileConfig(
        profile_name="modern_stack",
        target_name="prod",
        profile_mapping=PostgresUserPasswordProfileMapping(
            conn_id="warehouse_db",
            profile_args={"schema": "gold_layer"},
        ),
    )

    # NOTA: Al igual que en Spark 3.0, el modo de ejecución debe ser 
    # determinista para evitar la complejidad en el debugging de sistemas distribuidos (Ch. 1, p. 4).
    transform_data = DbtTaskGroup(
        group_id="transform_layer",
        project_config=ProjectConfig(DBT_ROOT_PATH / DBT_PROJECT_NAME),
        profile_config=profile_config,
        execution_config=ExecutionConfig(
            execution_mode="local", # O "kubernetes" para escalado horizontal
        ),
    )

dbt_airflow3_integration_dag = dbt_airflow3_integration()
```
</details>


### Mejores Prácticas en MLOps y CD4ML

Dentro del **Ciclo de Vida del Aprendizaje Automático**, la consistencia del dato entre las etapas de entrenamiento y servicio es crítica. La integración dbt-Airflow mitiga el **Training-Serving Skew** al garantizar que la ingeniería de características (*feature engineering*) sea una "fuente única de verdad".

Al utilizar Cosmos para orquestar dbt, aseguramos que la limpieza de datos —esa tarea "tediosa pero fundamental" sea reproducible. Esta arquitectura permite que herramientas como **MLflow** capturen metadatos precisos sobre la versión del dataset utilizado, conectando la observabilidad técnica con la reproducibilidad científica. En última instancia, esta integración transforma el pipeline de datos en un activo estratégico, reduciendo la fricción operativa y elevando la robustez de las aplicaciones de datos en producción.

