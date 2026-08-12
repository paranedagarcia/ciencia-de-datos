---
id: airflow-dag
title: "Grafo Acíclico Dirigido"
sidebar_label: "DAG"
description: "Diagrama que representa un flujo de trabajo, canalización o *pipeline* de datos"
---

# Grafo Acíclico Dirigido (DAG)

DAG Directory
```text
airflow/
├── dags/                    # Directorio principal de DAGs
│   ├── etl_pipeline.py
│   ├── ml_pipeline.py
│   └── utils/
├── plugins/                 # Plugins personalizados
├── config/                  # Configuración
├── logs/                    # Logs de ejecución
└── data/                    # Datos temporales
```

Un **DAG** (por sus siglas en inglés, *Directed Acyclic Graph* o **Grafo Acíclico Dirigido**) representa un flujo de trabajo, canalización o *pipeline* de datos individual dentro del ecosistema de orquestación de **Apache Airflow**. 

Conceptualmente, un DAG es una estructura matemática que organiza diversas tareas y define de manera estricta las relaciones y dependencias de ejecución entre ellas. Para comprender su naturaleza a nivel universitario, es necesario descomponer sus tres propiedades fundamentales:

1.  **Directed (Dirigido):** Las conexiones (aristas o bordes) entre las tareas (nodos o vértices) tienen una dirección única y explícita, representada por flechas. Esto determina un flujo hacia adelante donde una tarea descendente (*downstream*) solo puede iniciar su ejecución una vez que sus tareas predecesoras (*upstream*) han concluido con éxito.

2.  **Acyclic (Acíclico):** El grafo no permite la existencia de bucles o ciclos de retroalimentación; es decir, es imposible que el camino de ejecución regrese a una tarea previamente completada. Esta característica evita callejones sin salida lógicos (*deadlocks*), donde dos tareas dependieran mutuamente entre sí para poder iniciar.

3.  **Graph (Grafo):** Es la representación visual y lógica de todo el flujo, mapeando las dependencias estructurales de las operaciones que se desean ejecutar.

---

### Arquitectura de Operación y Ciclo de Vida de un DAG

La ejecución y ciclo de vida de un DAG en un entorno de producción de Airflow se gestiona de forma descentralizada mediante componentes de sistema coordinados que interactúan a través de una base de datos centralizada de metadatos (el *metastore*) y un *API Server*:

```
[Código Python (DAG File)] 
       │
       ▼ (Lectura y parseo periódico)
[DAG Processor] ──(Serialización)──> [Metastore]
                                        ▲
                                        │ (Lectura y verificación de dependencias)
                                 [Scheduler] ──(Asignación de tareas)──> [Executor]
                                                                            │
                                                                            ▼
                                                                     [Workers (Cola)]
```

#### Definición como Código (*Configuration as Code*)
En Airflow, los DAGs se definen dinámicamente mediante archivos de script de **Python**. Esto ofrece la ventaja de aplicar buenas prácticas de ingeniería de software (como el control de versiones con Git o despliegues automatizados mediante CI/CD). 

Las dependencias se configuran de manera intuitiva utilizando el operador de desplazamiento de bits a la derecha o izquierda (`>>` o `<<`) o mediante la función `chain()`.

#### El Ciclo de Operación de los Componentes
Cuando un script de DAG se coloca en el directorio correspondiente (`dags_folder`), Airflow lo opera a través de las siguientes etapas secuenciales:

*   **Fase de Parseo (DAG Processor):** El procesador de DAGs lee e interpreta el código Python, valida que no existan ciclos infinitos y guarda una versión serializada (estructurada) en el *metastore*.
*   **Planificación (Scheduler):** El planificador monitorea continuamente los intervalos de ejecución (*schedule interval*) definidos para el DAG. Al cumplirse las condiciones temporales (o ante un evento de datos), crea una instancia de ejecución lógica conocida como **DAG Run**.
*   **Resolución de Dependencias:** El *Scheduler* revisa cada tarea individual dentro de la ejecución activa (*Task Instances*), evaluando si sus dependencias anteriores han concluido satisfactoriamente. Por defecto, se rige bajo la regla de disparo `all_success`. Una vez autorizada, la tarea pasa al estado `queued` (encolada).
*   **Ejecución Física (Executor y Workers):** El ejecutor (como *Celery* o *Kubernetes*) distribuye la instrucción de ejecución física hacia los *Workers* (trabajadores). El *Worker* procesa la lógica de la tarea de forma aislada y reporta el estado final (`success` o `failed`) al *metastore* a través de llamadas de red seguras al **API Server**.
*   **Optimización Asíncrona (Triggerer):** Si una tarea soporta ejecución diferida (*deferrable tasks*), el *Worker* puede suspenderla temporalmente para liberar memoria y recursos de hardware, delegando el monitoreo asíncrono al componente **Triggerer** hasta que el evento externo se complete.


### Conceptos Clave de Robustez
*   **Idempotencia:** Un principio fundamental para diseñar DAGs estables. Significa que, si un operador o tarea se vuelve a ejecutar múltiples veces con los mismos parámetros de entrada (por ejemplo, al limpiar una tarea fallida desde la interfaz), el resultado final en el almacenamiento analítico debe ser idéntico, evitando duplicaciones o inconsistencias de datos.

*   **Atomicidad:** Cada tarea en el DAG debe realizar exactamente una única operación lógica indivisible. Separar los procesos de extracción, transformación y carga en tareas independientes permite aislar errores, optimizar la computación distribuida y reanudar únicamente el paso exacto que falló, en lugar de reiniciar todo el flujo desde el principio.

### Ejemplos
**Implementación de un DAG de ETL**

La forma recomendada y moderna de escribir DAGs en Airflow es a través de la **API TaskFlow**, la cual utiliza decoradores de Python para simplificar la declaración de tareas, reduciendo el código repetitivo (*boilerplate*) y gestionando de forma automática el paso de datos mediante XCom (comunicación cruzada).

A continuación se muestra un script técnico completo de un pipeline de ETL simulado:

```python showLineNumbers
import uuid
from pendulum import datetime
from airflow.sdk import dag, task

# 1. DEFINICIÓN DEL CONTEXTO DEL DAG MEDIANTE EL DECORADOR @dag
@dag(
    dag_id="pipeline_etl_academico",
    start_date=datetime(2026, 8, 1),
    schedule="@daily",          # Frecuencia de ejecución diaria gestionada por el Scheduler
    catchup=False,              # Evita la ejecución retrospectiva automática de ejecuciones pasadas
    default_args={
        "retries": 2,           # Número de reintentos automatizados ante fallos temporales
        "retry_delay": 120      # Tiempo de espera en segundos entre reintentos
    }
)
def pipeline_etl():

    # 2. DECLARACIÓN DE TAREAS OPERATIVAS CON EL DECORADOR @task
    # Cada función Python se convierte automáticamente en un nodo del DAG
    @task
    def extraer_datos_api() -> dict:
        """
        Simula la ingesta de datos crudos (Capa Bronze).
        """
        payload_crudo = {
            "batch_id": str(uuid.uuid4()),
            "metricas": [120.50, 450.20, 99.90, None]
        }
        print(f"Extracción completada. ID del lote: {payload_crudo['batch_id']}")
        return payload_crudo

    @task
    def transformar_datos(data: dict) -> dict:
        """
        Filtra inconsistencias y limpia nulos (Capa Silver).
        """
        metricas_sucias = data["metricas"]
        # Filtrado de valores None (Calidad del dato)
        metricas_limpias = [float(val) for val in metricas_sucias if val is not None]
        
        data_procesada = {
            "batch_id": data["batch_id"],
            "metricas_limpias": metricas_limpias,
            "registros_procesados": len(metricas_limpias)
        }
        print(f"Transformación finalizada para el lote {data['batch_id']}.")
        return data_procesada

    @task
    def cargar_datos_lakehouse(data_limpia: dict):
        """
        Persiste los datos refinados para consumo analítico (Capa Gold).
        """
        # Aquí se ejecutaría la persistencia en Delta Lake u otros motores
        total_registros = data_limpia["registros_procesados"]
        print(f"Carga exitosa. Se insertaron {total_registros} registros limpios en producción.")

    # 3. DECLARACIÓN DE DEPENDENCIAS Y FLUJO DE DATOS
    # Al pasar la salida de una función decorada como entrada de otra, 
    # Airflow infiere de manera automática las dependencias en el grafo lógico
    datos_crudos = extraer_datos_api()
    datos_limpios = transformar_datos(datos_crudos)
    cargar_datos_lakehouse(datos_limpios)

# 4. INSTANCIACIÓN FINAL DEL FLUJO DE TRABAJO
pipeline_etl()
```


#### Ejemplo

Este ejemplo avanzado de **implementación de un DAG de ETL** está diseñado bajo los estándares modernos de **Apache Airflow 3**, utilizando el paradigma de la **API TaskFlow** combinada con operadores tradicionales, estructurado bajo la arquitectura de refinamiento progresivo **Medallón**.

---
<br />
#### 💻 Ejemplo:
<Tabs>
<TabItem value="mnp" label="Antecedentes" default>
<div class="alert alert--primary">
Ingesta y Procesamiento Diario de Ventas (*E-commerce*)<br />

En entornos corporativos reales, los sistemas transaccionales (OLTP) generan constantemente registros de ventas que se almacenan temporalmente o se exponen mediante APIs. El departamento de Business Intelligence (BI) y el equipo de Data Science requieren que estos datos se integren de forma limpia, consistente e incremental dentro de un repositorio analítico central (un *Data Lakehouse* o *Data Warehouse*) sin sobrecargar los sistemas de origen.

Para resolver esto, diseñaremos un pipeline que se ejecuta de forma diaria y automatizada. Sus etapas son:
1.  **Capa Bronze (Extracción):** Descarga el archivo de transacciones crudas del día desde el servidor de origen y lo almacena de manera inmutable en el lago de datos.
2.  **Capa Silver (Transformación y Calidad):** Limpia el dataset, remueve registros corruptos (valores nulos en campos clave), castea los tipos de datos al formato correcto y calcula métricas derivadas como el subtotal por transacción.
3.  **Capa Gold (Agregación de Negocio):** Agrupa y resume los ingresos totales por país del día correspondiente, exportando estas métricas estructuradas en archivos de consulta SQL listos para su carga.
4.  **Carga (Load):** Ejecuta de forma transaccional el lote de inserciones en la base de datos analítica centralizada (Data Warehouse).
</div>
</TabItem>
<TabItem value="mnp-python" label="Pyhton" default>

```python showLineNumbers
# Implementación en Python

```
</TabItem>
</Tabs><br />



```python showLineNumbers title="Código Completo del DAG en Python"
import os
import json
import pendulum
from airflow.sdk import dag, task, chain
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

# ==============================================================================
# DEFINICIÓN DEL DAG (ORQUESTADOR PRINCIPAL)
# ==============================================================================
@dag(
    dag_id="pipeline_etl_ecommerce_medallon",
    start_date=pendulum.datetime(2026, 8, 1, tz="UTC"),
    schedule="0 2 * * *",  # Se ejecuta diariamente a las 02:00 UTC (al terminar el día de negocio)
    catchup=False,
    template_searchpath="/tmp",  # Permite buscar scripts SQL dinámicos en este directorio
    default_args={
        "retries": 3,                      # Tolerancia a fallos: reintenta hasta 3 veces
        "retry_delay": pendulum.duration(minutes=5),  # Espera 5 minutos entre intentos
    }
)
def etl_ecommerce():

    # 1. CAPA BRONZE (Extracción Inmutable)
    @task
    def extraer_datos_bronze(data_interval_start=None) -> str:
        """
        Descarga el lote de transacciones del día desde el origen.
        Utiliza 'data_interval_start' para asegurar la idempotencia del archivo físico.
        """
        fecha_particion = data_interval_start.strftime("%Y-%m-%d")
        ruta_destino = f"/tmp/bronze_sales_{fecha_particion}.json"

        os.makedirs("/tmp", exist_ok=True)
        
        # Simulación de la lectura física desde la API transaccional externa
        datos_simulados = [
            {"invoice_no": "540468", "stock_code": "20717", "quantity": 10, "price": 2.50, "country": "Spain"},
            {"invoice_no": "540469", "stock_code": "20699", "quantity": 5, "price": 12.00, "country": "France"},
            {"invoice_no": "540470", "stock_code": "20717", "quantity": None, "price": 3.00, "country": "Germany"},  # Registro corrupto
            {"invoice_no": "540471", "stock_code": "10002", "quantity": 1, "price": 45.00, "country": "Spain"}
        ]

        with open(ruta_destino, "w") as f:
            json.dump(datos_simulados, f)

        print(f"Bronze: Datos crudos del {fecha_particion} guardados en {ruta_destino}")
        return ruta_destino

    # 2. CAPA SILVER (Limpieza, Validación y Tipado)
    @task
    def limpiar_datos_silver(ruta_bronze: str, data_interval_start=None) -> str:
        """
        Lee los datos crudos de la capa Bronze, remueve nulos y calcula subtotales.
        """
        fecha_particion = data_interval_start.strftime("%Y-%m-%d")
        ruta_silver = f"/tmp/silver_sales_{fecha_particion}.json"

        with open(ruta_bronze, "r") as f:
            transacciones = json.load(f)

        # Validación del esquema en escritura y limpieza de registros inválidos
        registros_limpios = []
        for t in transacciones:
            # Calidad de datos: descartamos registros sin cantidad o precio
            if t["quantity"] is not None and t["price"] is not None:
                t["quantity"] = int(t["quantity"])
                t["price"] = float(t["price"])
                t["subtotal"] = t["quantity"] * t["price"]  # Característica calculada (enriquecimiento)
                registros_limpios.append(t)

        with open(ruta_silver, "w") as f:
            json.dump(registros_limpios, f)

        print(f"Silver: Datos depurados guardados en {ruta_silver}")
        return ruta_silver

    # 3. CAPA GOLD (Agregación e Idempotencia Lógica)
    @task
    def agregar_datos_gold(ruta_silver: str, data_interval_start=None) -> str:
        """
        Resume las transacciones y genera un archivo SQL dinámico para la carga idempotente (Upsert).
        """
        fecha_particion = data_interval_start.strftime("%Y-%m-%d")
        ruta_queries_sql = f"/tmp/gold_queries_{fecha_particion}.sql"

        with open(ruta_silver, "r") as f:
            datos = json.load(f)

        # Agrupación grupal: calculamos ingresos totales por país
        ventas_por_pais = {}
        for reg in datos:
            pais = reg["country"]
            subtotal = reg["subtotal"]
            ventas_por_pais[pais] = ventas_por_pais.get(pais, 0.0) + subtotal

        # Escritura de sentencias de Upsert SQL para el almacén analítico
        with open(ruta_queries_sql, "w") as f:
            for pais, total in ventas_por_pais.items():
                # El uso de 'ON CONFLICT' garantiza la idempotencia si el pipeline se vuelve a ejecutar
                query = (
                    f"INSERT INTO reporte_ventas_diarias (fecha, pais, total_ventas) "
                    f"VALUES ('{fecha_particion}', '{pais}', {total}) "
                    f"ON CONFLICT (fecha, pais) DO UPDATE SET total_ventas = EXCLUDED.total_ventas;\n"
                )
                f.write(query)

        print(f"Gold: Archivo de carga SQL estructurado en {ruta_queries_sql}")
        return ruta_queries_sql

    # 4. CAPA DE CARGA (Operador Tradicional del Ecosistema de SQL)
    # Se declara utilizando la sintaxis de operador clásica para interactuar con Postgres.
    # Se pasa la plantilla del archivo con el formato Jinja {{ data_interval_start | ds }}
    cargar_a_base_datos_gold = SQLExecuteQueryOperator(
        task_id="cargar_a_base_datos_gold",
        conn_id="postgres_data_warehouse",
        sql="gold_queries_{{ data_interval_start | ds }}.sql",  # Jinja renderizará la ruta final
        autocommit=True
    )

    # ==============================================================================
    # DECLARACIÓN DE DEPENDENCIAS (FLUJO DE DATOS Y EJECUCIÓN)
    # ==============================================================================
    # La API TaskFlow infiere implícitamente las dependencias de los pasos 1, 2 y 3
    # debido a que la salida de un método decorado sirve como entrada del siguiente.
    archivo_bronze = extraer_datos_bronze()
    archivo_silver = limpiar_datos_silver(archivo_bronze)
    archivo_sql_gold = agregar_datos_gold(archivo_silver)

    # Encadenamos la tarea final del operador tradicional usando el operador de bit-shift (>>)
    # Esto asegura que la base de datos se actualice solo tras generarse el archivo SQL de Gold.
    archivo_sql_gold >> cargar_a_base_datos_gold


# Instanciación lógica del pipeline para el motor de Airflow
etl_ecommerce()
```

---

### Análisis Técnico de las Buenas Prácticas Aplicadas

Para que un pipeline de datos sea estable y robusto en producción, este script implementa de forma nativa tres principios fundamentales de ingeniería de software:

#### 1. Idempotencia Estricta (*"Same In - Same Out"*)
Si un pipeline falla en el paso final de carga debido a un corte en la conexión con la base de datos, el orquestador reintentará la tarea. Al volver a ejecutar el pipeline para el mismo periodo de tiempo, **no deben generarse registros duplicados o inconsistencias**.
*   **A nivel de archivos:** En lugar de utilizar `datetime.now()`, el script utiliza el parámetro contextual de Airflow `data_interval_start`. Esto asegura que el archivo descargado y procesado pertenezca únicamente a la ventana lógica de tiempo correspondiente a la ejecución programada, incluso si se realiza un rellenado de datos históricos (*backfilling*) meses después.
*   **A nivel de base de datos:** La sentencia SQL generada en la capa Gold utiliza el patrón **UPSERT** (`INSERT ... ON CONFLICT (fecha, pais) DO UPDATE SET ...`). Si la tarea se ejecuta varias veces para la misma fecha y país, simplemente sobrescribe y actualiza los valores existentes en lugar de duplicarlos.

#### 2. Atomicidad del Flujo de Trabajo
Cada tarea del DAG tiene un único propósito delimitado y bien definido. Al separar la extracción (Bronze), la limpieza (Silver) y la agregación (Gold) en procesos aislados, logramos que, en caso de fallar la conexión al almacén de datos (Gold), **no tengamos que volver a realizar la llamada a la API externa de origen** (Bronze). Simplemente se limpia el estado de la tarea de carga en Airflow y se reinicia desde el paso fallido de forma localizada, ahorrando ancho de banda y costes de cómputo.

#### 3. Interoperabilidad de la API TaskFlow y Operadores Tradicionales
Airflow 3 permite la convivencia armoniosa del código moderno de Python (decorado con `@task`) con clases de operadores tradicionales e integrados de proveedores externos (como `SQLExecuteQueryOperator`). La API de TaskFlow expone el atributo de salida `.output` de los métodos decorados, el cual puede ser renderizado en las propiedades plantillables (*templated fields*) de los operadores tradicionales mediante sintaxis Jinja.

