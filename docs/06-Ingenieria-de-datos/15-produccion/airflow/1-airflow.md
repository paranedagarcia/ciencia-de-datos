---
id: airflow
title: "Apache Airflow"
sidebar_label: "Apache Airflow"
description: "Plataforma de código abierto para crear, programar y monitorear flujos de trabajo (pipelines de datos) de forma programática"
---

![](img/AirflowLogo.png)

# Apache Airflow
https://airflow.apache.org/

Apache Airflow es una plataforma de código abierto para crear, programar y monitorear flujos de trabajo (pipelines de datos) de forma programática, definiéndolos como código Python en estructuras llamadas DAGs (Directed Acyclic Graphs), permitiendo orquestar tareas complejas, gestionar dependencias y automatizar procesos de datos a gran escala, con una interfaz web para visualización y resolución de problemas. 

**Características principales**

- Código como configuración: Los flujos de trabajo se definen en scripts Python, facilitando su versionado, pruebas y colaboración.
- DAGs (Directed Acyclic Graphs): Representan flujos de trabajo con tareas y sus dependencias, asegurando un orden de ejecución sin bucles.
- Orquestación: Actúa como un director, ejecutando tareas en un orden específico, manejando fallos y reintentos.
- Extensible y Conectable: Incluye operadores para interactuar con sistemas externos (Bash, Spark, Bases de Datos, APIs) y permite crear plugins personalizados.
- Interfaz de Usuario (UI): Permite visualizar el progreso, monitorear DAGs, consultar logs y resolver problemas.
Escalable: Arquitectura modular y distribuida, capaz de manejar miles de tareas. 

Apache Airflow es una plataforma para la orquestación de flujos de trabajo (workflows), diseñada para planificar, ejecutar, monitorear y administrar pipelines de datos o procesos automatizados. Airflow permite definir los workflows como código Python (Workflow as Code), lo que facilita:

- versionamiento (Git),
- revisión por pares,
- reproducibilidad,
- reutilización,
- despliegue CI/CD.

**Qué problema resuelve**

En proyectos reales, es común tener procesos dependientes entre sí:

- “extraer datos → transformar → cargar → validar → notificar”
- “si falla X, no ejecutes Y”
- “si termina Z, dispara un pipeline downstream”
- “quiero re-ejecutar solo el día 2026-01-12”

Airflow resuelve esto con una capa robusta de:

- DAGs (grafos de tareas dependientes),
- scheduler (planificación),
- workers (ejecución),
- observabilidad (logs, UI, métricas),
- reintentos, SLAs, alertas.

## Arquitectura

![](img/airflow-3-arch.png)


**Arquitectura lógica**
```text
         ┌──────────────────────────────┐
         │           CI/CD              │
         │ Git + Tests + Deploy (Helm)  │
         └──────────────┬───────────────┘
                        │
┌───────────────────────▼────────────────────────┐
│                Apache Airflow                  │
│  ┌───────────┐   ┌───────────┐   ┌───────────┐ │
│  │ Webserver │   │ Scheduler │   │ Triggerer │ │
│  └─────┬─────┘   └─────┬─────┘   └─────┬─────┘ │
│        │               │               │       │
│        └───────────────┼───────────────┘       │
│                        ▼                       │
│                  Executor (K8s/Celery)         │
│                        ▼                       │
│                   Workers / Pods               │
└────────────────────────┬───────────────────────┘
                         │
          ┌──────────────┴───────────────┐
          │                              │
┌─────────▼──────────┐         ┌─────────▼──────────┐
│ Metadata DB        │         │ Logs / Artifacts   │
│ Postgres (estado)  │         │ S3/GCS/Blob/ELK    │
└─────────┬──────────┘         └─────────┬──────────┘
          │                              │
          └──────────────┬───────────────┘
                         ▼
               ┌───────────────────┐
               │ Sistemas externos │
               │ DBs, APIs, DWH,   │
               │ Spark/dbt/MLflow  │
               └───────────────────┘
```

## Instalación

La instalación solo es soportada oficialmente mediante pip
```bash
pip install 'apache-airflow==3.1.6' \
 --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-3.1.6/constraints-3.10.txt"
 ```

 Instalar con extras como postgresql, google u otros
```bash
pip install 'apache-airflow[postgres,google]==3.1.6' \
 --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-3.1.6/constraints-3.10.txt"
```

Para instalar en ambientes de desarrollo y local revisa este enlace:

https://github.com/apache/airflow/blob/main/INSTALLING.md

Establezca el directorio por defecto para airflow
```bash
export AIRFLOW_HOME=~/airflow
````

Para arrancar Airflow ejecute en la terminal (con el .env adecuado):
```bash
airflow standalone
```
Abra el navegador en http://localhost:8080

## Componentes principales


En la arquitectura de **Apache Airflow** (con especial énfasis en la evolución hacia la versión 3.0), el sistema se divide de manera rigurosa para **desacoplar la ejecución del código de usuario (tareas) del almacenamiento de metadatos**. Este diseño optimiza la seguridad, la escalabilidad y la tolerancia a fallos en entornos de producción distribuidos.

A continuación, se presenta un análisis técnico y pedagógico de los **componentes principales** de Airflow y su función dentro del flujo de trabajo:


#### El API Server (Servidor de API)
En las versiones más recientes, el **API Server** se convierte en el eje central de comunicación de Airflow. 
* **Función:** Actúa como la única puerta de enlace de comunicación (*gateway*) para todos los componentes que necesitan interactuar con la base de datos de metadatos (metastore).
* **Task SDK (Task Execution Interface):** Los trabajadores (*workers*) ya no se conectan directamente a la base de datos. En su lugar, solicitan credenciales de conexión o reportan estados a través de llamadas seguras al API Server. 
* **Interfaz y REST API:** También es responsable de servir la interfaz de usuario (UI) moderna y la API REST pública.

#### El Scheduler (Planificador)
Es el cerebro encargado de coordinar la ejecución del flujo de trabajo.
* **Funcionamiento:** Ejecuta un bucle continuo (*while True loop*) en el que monitorea el estado de las tareas y determina si se han cumplido sus dependencias (como la finalización con éxito de las tareas precedentes o la llegada del intervalo de tiempo programado).
* **Asignación:** Una vez que una tarea cumple con las condiciones requeridas, el Scheduler cambia su estado a `queued` (encolada) y la envía a la cola gestionada por el Ejecutor.

#### El DAG Processor (Procesador de DAGs)
Es el componente que lee e interpreta el código Python para transformarlo en una estructura que Airflow pueda entender.
* **Función:** Escanea periódicamente el directorio de DAGs (`dags_folder`). Interpreta el código y genera una **versión serializada del DAG** que se almacena en el metastore.
* **Aislamiento:** El procesamiento de archivos se ejecuta en un proceso independiente al Scheduler para evitar que un bucle infinito o un fallo de sintaxis en el código de un desarrollador tire abajo todo el planificador del sistema.



#### El Metastore (Base de Datos de Metadatos)
Es la única fuente de verdad sobre el estado del sistema.
* **Función:** Almacena la definición de los DAGs serializados, las variables del sistema, las credenciales de conexión cifradas, el historial de las ejecuciones de los flujos de trabajo (*DAG Runs*) y el estado actual de cada tarea.
* **Tecnología:** Airflow utiliza **SQLAlchemy** (un mapeador objeto-relacional o ORM en Python) para interactuar con la base de datos. En producción, se exige el uso de motores robustos y con soporte de bloqueos a nivel de fila como **PostgreSQL** o **MySQL**.

#### Los Workers (Trabajadores)
Son los componentes que ejecutan las instrucciones computacionales que componen cada tarea.
* **Función:** Monitorean constantemente la cola de ejecución, toman las tareas que se encuentran en estado `queued` e inician un subproceso aislado que ejecuta el comando de terminal `airflow tasks run` para procesar la lógica de negocio.
* **Trazabilidad:** Durante su ejecución, el *worker* escribe los logs directamente en un almacenamiento dedicado (local o en la nube) y reporta latencias o estados mediante el API Server.

#### El Triggerer (Disparador Asíncrono)
Un componente esencial para optimizar recursos cuando se trabaja con tareas de larga espera.
* **Función:** Ejecuta un bucle de eventos asíncrono utilizando la librería de Python `asyncio`.
* **Optimización:** Cuando una tarea (como un sensor que espera un archivo en un almacenamiento S3) se inicia, en lugar de bloquear un hilo completo de un *worker* durante horas de forma pasiva, se "deferiza" (suspende) y se delega al Triggerer. El Triggerer asume la monitorización y, cuando se cumple la condición externa, devuelve la ejecución a un *worker* disponible para finalizar la tarea, reduciendo radicalmente los costes de infraestructura.

#### El Executor (Ejecutor)
Aunque técnicamente corre dentro del proceso del Scheduler, define la **estrategia de ejecución** de los flujos.
* **Tipos de ejecutor:**
  * **`LocalExecutor`:** Ejecuta tareas en paralelo mediante hilos o procesos dentro del mismo servidor del planificador (ideal para desarrollo local).
  * **`CeleryExecutor`:** Distribuye las tareas a través de una cola de mensajería (como Redis o RabbitMQ) a una flota elástica de servidores *workers* dedicados.
  * **`KubernetesExecutor`:** Instancia un pod de Kubernetes temporal y dedicado para ejecutar cada tarea individual de forma aislada en el clúster.

---

### Ejemplo Práctico
**Definición de un DAG en Python (TaskFlow API)**

Para ilustrar cómo se orquestan estas piezas bajo la API moderna de Airflow, este script en Python define un flujo simple de ETL que procesa datos de forma secuencial utilizando decoradores:

```python showLineNumbers title="Definición de un DAG"
from pendulum import datetime
from airflow.sdk import dag, task, chain

# 1. Definición del DAG (Instancia lógica que será serializada por el DAG Processor)
@dag(
    dag_id="pipeline_pedagogico_airflow",
    start_date=datetime(2026, 8, 1),
    schedule="@daily",  # El Scheduler revisará este intervalo para crear una ejecución
    catchup=False
)
def mi_primer_pipeline():

    # 2. Tareas (Lógica que el Worker ejecutará en procesos aislados)
    @task
    def extraer_datos_crudos() -> list:
        # Simulamos la ingesta de datos
        datos =
        print(f"Iniciando ingesta. Datos extraídos: {datos}")
        return datos

    @task
    def transformar_datos(datos: list) -> list:
        # Aplicamos una transformación matemática (multiplicar por un factor)
        datos_transformados = [x * 1.15 for x in datos]
        print(f"Limpieza y transformación completadas: {datos_transformados}")
        return datos_transformados

    @task
    def cargar_al_lakehouse(datos_procesados: list):
        # Envío de la información al almacenamiento final
        print(f"Cargando exitosamente {len(datos_procesados)} registros en la capa Gold.")

    # 3. Declaración explícita de dependencias (Estructura de Grafo o DAG)
    # Airflow infiere las dependencias por el paso de argumentos, 
    # pero podemos reforzarlas explícitamente usando la función 'chain'
    datos_crudos = extraer_datos_crudos()
    datos_limpios = transformar_datos(datos_crudos)
    cargar_al_lakehouse(datos_limpios)

# Ejecución de la función para registrar el DAG en el scope global
mi_primer_pipeline()
```
