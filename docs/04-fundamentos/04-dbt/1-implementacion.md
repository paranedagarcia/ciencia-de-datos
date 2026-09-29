---
id: dbt-implementa
title: "Implementación dbt desde cero"
sidebar_label: "📄 Implementación"
description: ""
slug: /dbt-implementa
---

## **Implementación**

La implementación de **dbt (Data Build Tool)** desde cero es un proceso estructurado que traslada los principios de la ingeniería de software (control de versiones, modularidad, pruebas automatizadas y documentación) al modelado analítico de bases de datos. 

A continuación, se presenta un manual metodológico y paso a paso para desplegar un entorno de dbt Core y conectar un pipeline de datos transaccional con un motor analítico (Warehouse) como **[Google BigQuery](/docs/bigquery)** o Snowflake.


### Fase 1: Preparación del Entorno Virtual

El aislamiento de entornos es una práctica mandatoria para evitar conflictos de librerías globales. El desarrollo local con dbt Core requiere inicializar un entorno virtual de Python:

1.  **Crear el directorio del proyecto** en el terminal:
    ```bash
    mkdir dbt_analytics_platform
    cd dbt_analytics_platform
    ```
2.  **Crear y activar el entorno virtual**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  **Instalar dbt-core y el adaptador específico del Warehouse**. En este caso, utilizaremos Google BigQuery:
    ```bash
    python3 -m pip install --upgrade pip
    python3 -m pip install dbt-core dbt-bigquery
    ```
    :::info
     Si utilizas otra base de datos, debes instalar el adaptador correspondiente, por ejemplo, `dbt-snowflake`, `dbt-redshift` o `dbt-databricks`).
     :::

---

### Fase 2: Autenticación y Credenciales de Seguridad

Para permitir que dbt ejecute transformaciones físicas dentro de la base de datos analítica, requiere permisos de escritura y lectura. 
*   **Best Practice de Seguridad:** Las credenciales nunca deben guardarse dentro de la carpeta del proyecto de Git para evitar fugas de secretos (*security leaks*) en repositorios públicos.

*   **En BigQuery:** Se debe crear una cuenta de servicio (*Service Account*) en Google Cloud Platform con el rol de **Administrador de BigQuery (BigQuery Admin)** o **Usuario de Trabajos (Job User)** y **Editor de Datos (Data Editor)**, descargar la clave en un archivo seguro en formato **JSON** (p. ej., `dbt_credentials.json`) y almacenarla en una carpeta aislada del usuario (p. ej., `~/.dbt/`).



### Fase 3: Inicialización del Proyecto

Con el entorno configurado y las credenciales listas, se inicia el andamiaje del proyecto ejecutando el comando de arranque:

```bash
dbt init
```

Este comando interactivo solicitará los siguientes parámetros de inicialización:
1.  **Project Name:** Nombre lógico de tu repositorio (ej. `dbt_book`).
2.  **Database Adapter:** Selecciona el motor instalado (p. ej., `1` para `bigquery`).
3.  **Authentication Method:** Selecciona `2` para autenticarse con cuenta de servicio (`service_account`).
4.  **Keyfile Path:** Ruta física absoluta del JSON descargado (ej. `/home/usuario/.dbt/dbt_credentials.json`).
5.  **Project ID:** El ID de tu proyecto en la nube.
6.  **Dataset:** El nombre de tu esquema/dataset de desarrollo (ej. `nyc_bikes` o `dbt_dev`).
7.  **Threads:** El número de hilos de ejecución paralelos concurrentes para procesar el Grafo (típicamente `4` para desarrollo).

#### ¿Qué ocurre tras bambalinas?
*   dbt crea de forma transparente un archivo central de conexión en tu directorio de inicio local, concretamente en **`~/.dbt/profiles.yml`**, aislando la seguridad de tu código de negocio.
*   Genera la estructura de carpetas unificada de dbt dentro del directorio local.


### Fase 4: Anatomía de un Proyecto dbt

La estructura estándar autogenerada se desglosa en los siguientes directorios clave:

```
dbt_project/
├── dbt_project.yml       # Archivo de configuración central de dbt
├── packages.yml          # Declaración de dependencias de paquetes (dbt_utils, dbt_date)
├── models/               # El core de las transformaciones SQL (.sql)
│   ├── staging/          # Capa de preparación atómica (vistas lógicas)
│   └── marts/            # Capa de modelos de negocio finales (tablas físicas/hechos y dim)
├── seeds/                # Archivos CSV estáticos de baja volatilidad (ej. códigos postales)
├── snapshots/            # Modelos SCD Tipo 2 para trazar históricos de tablas mutables
├── tests/                # Pruebas unitarias de calidad de datos singulares (.sql)
└── target/               # SQL compilado y optimizado generado automáticamente por dbt
```

#### Configuración del `dbt_project.yml`
Este es el archivo rector donde se parametriza la metadata del proyecto y los valores de materialización por defecto a nivel de carpeta:

```yaml
# dbt_project.yml
name: 'dbt_book'
version: '1.0.0'
config-version: 2

profile: 'dbt_book' # Debe coincidir exactamente con el nombre en profiles.yml

model-paths: ["models"]
seed-paths: ["seeds"]
test-paths: ["tests"]
analysis-paths: ["analyses"]
macro-paths: ["macros"]

# Materializaciones por defecto para la arquitectura en capas
models:
  dbt_book:
    staging:
      +materialized: view      # Todo en staging se materializa como vista (baja latencia)
    marts:
      +materialized: table     # Todo en marts se materializa físicamente como tabla
```


### Fase 5: Verificación de la Conexión

Para validar que dbt-core se comunica de forma bidireccional y transaccional con tu base de datos, muévete a la subcarpeta del proyecto y ejecuta el diagnóstico:

```bash
cd dbt_book
dbt debug
```

Si todo está configurado correctamente, el sistema procesará la conexión del adaptador y retornará el mensaje de éxito **`All checks passed!`**.



### Fase 6: Ciclo de Desarrollo de Modelos

Un pipeline modular bajo dbt nunca realiza transformaciones en caliente sobre tablas crudas directas. Se deben definir los orígenes y estructurar el flujo (Staging a Marts).

#### 1. Definición de Fuentes (`_sources.yml`)
Declaramos formalmente nuestras fuentes crudas de origen utilizando YAML para que dbt entienda de dónde provienen y exponga el linaje de datos:

```yaml
# models/staging/_sources.yml
version: 2
sources:
  - name: jaffle_shop
    database: dbt-project-437116
    schema: jaffle_shop_raw
    tables:
      - name: customers
      - name: orders
```

#### 2. Modelo de Staging
Mapeamos la fuente 1:1, limpiando esquemas, casteando tipos de datos y renombrando de forma estandarizada (`stg_customers.sql`):

```sql showLineNumbers
-- models/staging/stg_customers.sql
-- dbt heredará la materialización 'view' configurada en el dbt_project.yml

WITH raw_source AS (
    -- La macro source desacopla la ubicación física del dato de origen
    SELECT * FROM {{ source('jaffle_shop', 'customers') }}
)

SELECT
    CAST(id AS INT64) AS customer_id,
    TRIM(first_name) AS customer_first_name,
    TRIM(last_name) AS customer_last_name
FROM raw_source
```

#### 3. Modelo Mart Final (`dim_customers.sql`)
Consolida las lógicas transformadas y unificadas, entregando el producto final denormalizado para BI o analistas de negocio. Consumirá los modelos previos usando la función **`{{ ref() }}`** para consolidar el linaje lógicamente:

```sql showLineNumbers
-- models/marts/dim_customers.sql
-- Este modelo se materializará físicamente como una TABLA en producción

WITH customers AS (
    SELECT * FROM {{ ref('stg_customers') }}
),

orders_summary AS (
    SELECT
        customer_id,
        MIN(order_date) AS first_order_date,
        COUNT(order_id) AS total_orders
    FROM {{ ref('stg_orders') }}
    GROUP BY customer_id
)

SELECT
    c.customer_id,
    c.customer_first_name,
    c.customer_last_name,
    COALESCE(o.total_orders, 0) AS total_orders,
    o.first_order_date
FROM customers c
LEFT JOIN orders_summary o ON c.customer_id = o.customer_id
```

#### 4. Ejecución del Pipeline (`dbt run`)
Para compilar estas plantillas SQL compuestas con macros Jinja y ejecutarlas dentro del clúster de cómputo del Data Warehouse, ejecuta el comando de ejecución:

```bash
dbt run
```
*Si deseas procesar un modelo individual de forma selectiva para no reconstruir todo el DAG, utiliza el filtro de selección:*
```bash
dbt run --select dim_customers
```


### Fase 7: Gobernanza de Datos, Pruebas y Trazabilidad

Un pipeline no se considera en estado de producción si no cuenta con aserciones automáticas de calidad y documentación observable.

#### 1. Configuración de Pruebas Genéricas y Documentación
Asigna aserciones de consistencia e integridad relacional directamente sobre el esquema:

```yaml
# models/marts/_core_models.yml
version: 2
models:
  - name: dim_customers
    description: "Dimensión maestra consolidada que expone el comportamiento analítico de clientes."
    columns:
      - name: customer_id
        description: "Clave primaria única e inmutable para cada cliente."
        tests:
          - unique    # Valida que no existan registros duplicados en el ID
          - not_null  # Valida la ausencia de valores nulos
```

#### 2. Ejecutar Pruebas (`dbt test`)
Para evaluar si tus bases de datos cumplen de forma rigurosa con estas reglas, ejecuta la batería de pruebas genéricas y de integridad referencial:

```bash
dbt test
```

#### 3. Generar el Portal de Documentación
dbt compila los metadatos de tus esquemas, pruebas, descripciones e historial de dependencias y genera de forma automática un mapa interactivo de linaje de datos de extremo a extremo:

```bash
dbt docs generate
dbt docs serve
```
:::info[nota]
Este comando inicializa un servidor web local en `http://localhost:8080` donde cualquier analista o ejecutivo puede auditar la lógica corporativa y navegar por el Grafo Acíclico Dirigido (DAG) interactivo.
:::

