---
id: airflow-executor
title: "El Ejecutor (Executor)"
sidebar_label: "Executor"
description: "Define la estrategia de ejecución de las tareas"
slug: /airflow-executor
---

En el ecosistema de **Apache Airflow 3**, un **executor** (ejecutor) es el componente de la arquitectura encargado de definir la **estrategia, el modo y el entorno físico** en el que se ejecutarán las tareas de tu pipeline. 

Para explicarlo de manera simple, mientras que el **Scheduler** (planificador) actúa como el cerebro que decide *cuándo* una tarea es elegible para ejecutarse basándose en sus dependencias lógicas o temporales, el **Executor** es el brazo operativo que determina *cómo y dónde* se ejecuta físicamente dicha tarea, asignando los recursos de cómputo y coordinando a los trabajadores (*workers*).

---

### El rol del Executor 
**en el Ciclo de Vida de una Tarea**

El Scheduler y el Executor interactúan estrechamente a través de un flujo de estados persistido en la base de datos de metadatos:
1. **Planificación y Encolamiento:** El Scheduler identifica que una tarea tiene sus dependencias resueltas y la coloca en una cola de ejecución con el estado de `queued` (encolada). 
2. **Delegación al Executor:** Una vez encolada, la tarea pasa a ser responsabilidad del Executor. Este lee la tarea de la cola y despacha la instrucción física a un trabajador (*worker*) para que inicie la ejecución. 
3. **Monitoreo de Ejecución:** El Executor ejecuta internamente un proceso para monitorear el progreso de la tarea mediante señales periódicas de estado (*heartbeats*) hasta que esta finaliza con éxito (`success`) o con error (`failed`).

---

### La Revolución de Airflow 3
**Aislamiento de Tareas y Remote Execution**

En Airflow 2, los trabajadores interactuaban de forma directa con la base de datos de metadatos, lo que planteaba riesgos de seguridad y limitaba la escalabilidad en grandes entornos. 

Con la llegada de **Airflow 3**, se ha implementado un desacoplamiento arquitectónico absoluto mediante el nuevo **API Server** y el **Task SDK**. En esta versión, los trabajadores ya no acceden directamente a la base de datos; en su lugar, se comunican a través del API Server mediante llamadas de red HTTPS seguras. Esta innovación permite habilitar de forma nativa la **ejecución remota (*Remote Execution*)**, permitiendo que los ejecutores corran tareas de forma segura en nubes privadas, servidores locales (*on-premises*) u otras redes aisladas sin comprometer la base de datos central.

---

### Principales Ejecutores

Airflow 3 ofrece diversas estrategias de ejecución según las necesidades de la infraestructura:

*   **`LocalExecutor`:** Es el ejecutor por defecto en Airflow 3. Ejecuta cada instancia de tarea como un subproceso independiente (*forked process*) en la misma máquina física donde corre el Scheduler. Es ideal para desarrollo local o entornos ligeros.

*   **`CeleryExecutor`:** Diseñado para la escalabilidad horizontal en producción. Distribuye las tareas a través de una cola de mensajería (un *broker* como Redis o RabbitMQ) hacia una flota de procesos trabajadores (*Celery workers*) que corren de manera permanente en máquinas dedicadas.

*   **`KubernetesExecutor`:** Instancia de forma dinámica un **Pod de Kubernetes dedicado** y temporal para ejecutar cada tarea de forma totalmente aislada. Una vez finalizada la tarea, el Pod se destruye. Es la opción ideal cuando se requiere un control estricto de recursos y aislamiento total de librerías.

*   **`EdgeExecutor`:** Una de las novedades más destacadas de Airflow 3. Permite desplegar trabajadores independientes (*Edge workers*) en entornos remotos o locales (detrás de cortafuegos) que solicitan y reportan tareas de forma asíncrona al API Server central de Airflow.

*   **`AstroExecutor`:** Disponible de forma exclusiva en la plataforma Astro de Astronomer. Es un ejecutor optimizado para entornos de Kubernetes en la nube que ofrece un arranque más rápido de las tareas que el `KubernetesExecutor` tradicional y un alto nivel de resiliencia.

---

### Configuración 
**Uso de Múltiples Ejecutores Concurrentes**

Una de las capacidades más avanzadas introducidas en Airflow 3 es la habilidad de utilizar **múltiples ejecutores concurrentes** en el mismo entorno de producción. 

Esto se configura listando los ejecutores en el archivo de configuración `airflow.cfg`:
```ini
[core]
executor = CeleryExecutor, KubernetesExecutor
```

De este modo, los autores de los DAGs pueden declarar con precisión qué ejecutor utilizar a nivel de tarea individual mediante el parámetro `executor`:

```python showLineNumbers
from pendulum import datetime
from airflow.sdk import dag, task
from airflow.providers.standard.operators.bash import BashOperator

@dag(
    dag_id="pipeline_hibrido_airflow_3",
    start_date=datetime(2026, 8, 1),
    schedule=None,
    catchup=False
)
def mi_pipeline():

    # Tarea ligera y rápida: Se ejecuta inmediatamente en la infraestructura de Celery
    descargar_data = BashOperator(
        task_id="descargar_data",
        executor="CeleryExecutor",  # Sobrescribe el ejecutor a nivel de tarea
        bash_command="curl -o /tmp/data.csv https://api.origen.com/ventas"
    )

    # Tarea pesada o aislada: Se ejecuta en un pod temporal de Kubernetes
    # El decorador @task permite heredar e interactuar con el Task SDK de Airflow 3
    @task(
        executor="KubernetesExecutor",  # Ejecución aislada en un Pod dedicado
        retries=3
    )
    def procesar_model_ml():
        import pandas as pd
        print("Procesando datos a gran escala y entrenando modelo con aislamiento total de dependencias.")
        # La lógica de tu modelo va aquí...

    descargar_data >> procesar_model_ml()

mi_pipeline()
```

Esta aproximación híbrida e interoperable garantiza que juegues con las fortalezas de cada ejecutor: utilizando la rapidez y el bajo coste de `CeleryExecutor` para tareas sencillas de integración de datos, y el aislamiento robusto del `KubernetesExecutor` para computaciones complejas o tareas de Machine Learning.

***

---
---

En la arquitectura de **Apache Airflow 3**, el **ejecutor** (*executor*) es el componente encargado de definir la estrategia de ejecución de las tareas. Su función consiste en tomar las tareas encoladas por el planificador (*scheduler*) y asignarles los recursos físicos para su procesamiento.

Con el lanzamiento de **Airflow 3**, la arquitectura ha sufrido una reestructuración fundamental: **la ejecución de tareas se ha desacoplado por completo de la base de datos de metadatos (*metastore*)**. A través de un nuevo **Task SDK** y el **API Server**, los *workers* que ejecutan el código ya no tienen acceso directo a la base de datos, lo que incrementa radicalmente la seguridad, reduce el número de conexiones simultáneas y permite la ejecución de tareas en entornos remotos de forma nativa.

---

### Tabla Comparativa

A nivel de producción y diseño de infraestructura, la elección del ejecutor depende críticamente de la topología de tu red, el nivel de aislamiento requerido y la naturaleza de tus flujos de trabajo.

| Ejecutor | ¿Distribuido? | Complejidad de Instalación | Caso de Uso Ideal / Fortaleza Principal |
| :--- | :---: | :---: | :--- |
| **`LocalExecutor`** | No | Baja (Fácil) | Desarrollo local, pruebas o entornos monolíticos de bajo volumen. |
| **`CeleryExecutor`** | Sí | Moderada | Cargas de producción que exigen escalabilidad horizontal con tiempos de arranque mínimos. |
| **`KubernetesExecutor`** | Sí | Alta (Compleja) | Cargas con dependencias conflictivas o que requieren aislamiento estricto y recursos dedicados por tarea. |
| **`EdgeExecutor`** | Sí | Moderada | Ejecución de tareas en redes remotas o infraestructura *on-premises* aislada. |
| **`AstroExecutor`** *(Exclusivo de Astro)* | Sí | Administrada | Entornos en la nube optimizados para balancear la velocidad de Celery y la flexibilidad de Kubernetes. |

---

### Análisis Técnico Ejecutor

#### LocalExecutor (Ejecución Monolítica)
*   **Funcionamiento:** En lugar de distribuir el cómputo, este ejecutor lanza cada tarea como un **subproceso local** (*forked process*) a partir del proceso del planificador. Utiliza una cola interna de tipo FIFO (First-In, First-Out) administrada en memoria.
*   **Ventajas:** Es extremadamente sencillo de configurar (solo requiere apuntar a una base de datos relacional robusta como PostgreSQL o MySQL).
*   **Limitaciones:** La escalabilidad está estrictamente acotada por los recursos de CPU y RAM de la máquina única que aloja al planificador. Además, no provee aislamiento real de dependencias a nivel de sistema operativo.

#### CeleryExecutor (Escalabilidad Basada en Cola de Mensajería)
*   **Funcionamiento:** Distribuye las tareas enviando mensajes de ejecución a un *broker* de mensajería (como **Redis** o **RabbitMQ**). Una flota elástica de *workers* de Celery, que corren de manera permanente en máquinas dedicadas, lee la cola y procesa las tareas en paralelo.
*   **Ventajas:** Ofrece un **tiempo de arranque casi instantáneo** (*warm workers*) debido a que los procesos de ejecución ya están activos y listos para recibir tareas.
*   **Limitaciones:** Requiere que todos los nodos *workers* tengan acceso idéntico al directorio de DAGs (`dags_folder`) y que compartan exactamente el mismo entorno de dependencias y librerías de Python, lo que facilita los conflictos de dependencias entre diferentes equipos de desarrollo.

#### KubernetesExecutor (Aislamiento Dinámico en Contenedores)
*   **Funcionamiento:** Por cada instancia de tarea que el planificador decide ejecutar, este realiza una llamada a la API de Kubernetes para instanciar un **Pod temporal y dedicado** en el clúster. Tan pronto como la tarea finaliza, el Pod se destruye por completo.
*   **Ventajas:**
    *   **Aislamiento absoluto:** Cada tarea corre en su propio entorno de contenedores, evitando colisiones de librerías.
    *   **Eficiencia de recursos:** Permite parametrizar las necesidades de hardware a nivel de tarea (por ejemplo, solicitar acceso a una GPU para una tarea de entrenamiento de Machine Learning y liberar el recurso de inmediato al terminar).
*   **Limitaciones:** Introduce una **latencia de arranque** (*cold start*) debido a la sobrecarga del clúster para descargar la imagen de Docker, inicializar el Pod e inyectar el volumen de almacenamiento.

#### EdgeExecutor (Ejecución Híbrida y Remota)
*   **Funcionamiento:** Es una de las innovaciones más potentes de **Airflow 3**. Permite desplegar *Edge Workers* independientes en zonas de red de difícil acceso (por ejemplo, servidores locales detrás de firewalls corporativos o nubes privadas). El *Edge Worker* se conecta de forma segura hacia el plano de control central de Airflow a través de llamadas de red HTTPS al API Server.
*   **Ventajas:** Facilita la gobernanza y el cumplimiento normativo (GDPR, HIPAA, etc.). Los datos confidenciales se extraen, procesan y almacenan de forma local en la red remota, y el *worker* solo reporta el estado final (`success`/`failed`) y metadatos operativos hacia la base de datos central.

---

### La Revolución en Airflow 3

**Ejecución Multiejecutor (*Multi-Executor*)**

Históricamente en Airflow 2, para mezclar estrategias de ejecución, los ingenieros de datos dependían de ejecutores híbridos estáticos y rígidos codificados en el núcleo (como el `CeleryKubernetesExecutor`). 

**Airflow 3 elimina esta restricción e introduce el soporte de múltiples ejecutores concurrentes**. Ahora es posible configurar una lista de ejecutores activos en el archivo de configuración:

```ini
[core]
executor = LocalExecutor, CeleryExecutor, KubernetesExecutor
```

Esta flexibilidad te permite programar tus flujos de trabajo con precisión quirúrgica, asignando el ejecutor idóneo a nivel de tarea individual mediante el parámetro `executor` en tus DAGs:

```python showLineNumbers
# Tarea ligera de bajo coste ejecutada de inmediato en Celery
tarea_ingesta = BashOperator(
    task_id="ingesta_rapida",
    executor="CeleryExecutor",
    bash_command="curl -o /tmp/raw_data.json https://api.origen.com"
)

# Tarea pesada que requiere aislamiento y GPUs ejecutada en Kubernetes
tarea_entrenamiento = PythonOperator(
    task_id="entrenar_red_neuronal",
    executor="KubernetesExecutor",
    python_callable=entrenar_modelo_gpu
)
```



📊 ¿Te gustaría que prepare una guía de laboratorio práctico en tu panel de **Studio** que detalle paso a paso cómo configurar y levantar un entorno multiejecutor híbrido utilizando el nuevo estándar de Airflow 3?