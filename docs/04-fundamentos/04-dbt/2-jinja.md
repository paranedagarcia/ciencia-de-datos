---
id: dbt-jinja
title: ""
sidebar_label: "📄 Plantillas Jinja"
description: ""
slug: /dbt-jinja
---

## **Plantillas Jinja**

En el ecosistema de **dbt (Data Build Tool)**, **Jinja** es un motor de plantillas (heredado de Python) que permite transformar el lenguaje SQL estático en un entorno de programación dinámico, modular y robusto. Gracias a Jinja, los analistas e ingenieros de datos pueden inyectar estructuras de control (como bucles y condicionales), definir variables y encapsular bloques de código reutilizables (macros) para mantener el repositorio bajo el estándar **DRY (*Don't Repeat Yourself*)**.

### Sintaxis y Delimitadores Fundamentales en dbt

Antes de profundizar en los ejemplos prácticos, es indispensable comprender cómo interpreta dbt los delimitadores de Jinja dentro de un archivo `.sql`:

1.  **`{{ ... }}` (Expresiones):** Se utiliza para imprimir texto o el resultado de una función directamente en el script SQL compilado. El caso más común es la referencia de modelos con `{{ ref('nombre_modelo') }}` o fuentes con `{{ source('origen', 'tabla') }}`.

2.  **`{% ... %}` (Sentencias):** Se emplea para la lógica de control de flujo, como condicionales `if`, inicialización de variables con `set` o bucles `for`.

3.  **`{# ... #}` (Comentarios):** Permite documentar el código inline. Todo lo que se encuentre dentro de estos delimitadores es ignorado por dbt durante la compilación.

4.  **`{%-` y `-%}` (Control de Espacios):** Colocar un guion medio al inicio o al final del delimitador indica al compilador que elimine los espacios en blanco y saltos de línea generados por Jinja, asegurando un código SQL limpio tras su compilación.



A continuación, se presenta una serie de **3 ejemplos progresivos** (de menor a mayor complejidad) basados en la base de datos de ejemplo **Northwind** de Microsoft, mostrando la plantilla origen en dbt y su correspondiente traducción física (compilada) tanto para **PostgreSQL** como para **SQL Server (T-SQL)**.



#### Ejemplo 1: Filtrado de Datos según el Entorno (`target.name`)
* **Escenario de Negocio:** En los entornos de desarrollo local (`dev`) no deseamos procesar la totalidad histórica de la tabla `Orders` para evitar costos excesivos de cómputo y latencia. Sin embargo, en el entorno de producción (`prod` o `deploy`) requerimos la extracción completa de los hechos.
* **Solución Jinja:** Evaluamos la propiedad condicional `target.name`. Si el destino actual no es el de despliegue productivo, inyectamos dinámicamente un filtro `WHERE` para limitar los datos a los últimos 3 meses.

**Plantilla dbt (Jinja + SQL)**
```sql
SELECT 
    order_id, 
    customer_id, 
    order_date, 
    freight
FROM {{ ref('stg_northwind_orders') }}

{# Filtro dinámico para optimizar el cómputo en desarrollo #}
{% if target.name != 'prod' -%}
WHERE order_date >= 
    {%- if target.type == 'postgres' -%}
        CURRENT_DATE - INTERVAL '3 months'
    {%- else -%}
        DATEADD(month, -3, GETDATE())
    {%- endif -%}
{%- endif %}
```

**Código Compilado para PostgreSQL**
```sql
SELECT 
    order_id, 
    customer_id, 
    order_date, 
    freight
FROM analytical_db.staging.stg_northwind_orders
WHERE order_date >= CURRENT_DATE - INTERVAL '3 months';
```

**Código Compilado para SQL Server (T-SQL)**
```sql
SELECT 
    order_id, 
    customer_id, 
    order_date, 
    freight
FROM AnalyticalDB.staging.stg_northwind_orders
WHERE order_date >= DATEADD(month, -3, GETDATE());
```


#### Ejemplo 2: Pivotado Dinámico de Datos utilizando un Bucle `for`
* **Escenario de Negocio:** Se requiere analizar las ventas anuales agrupadas y pivotadas por transportista (*Shippers* de Northwind: *Speedy Express*, *United Package*, *Federal Shipping*).
* **Solución Jinja:** En lugar de codificar manualmente tres sentencias `CASE WHEN` idénticas (lo cual viola el principio DRY y dificulta el mantenimiento), declaramos un arreglo en Jinja y lo iteramos con un ciclo `for`, utilizando variables de bucle como `loop.last` para controlar la colocación de las comas de separación relacional.

**Plantilla dbt (Jinja + SQL)**
```sql
{% set shippers = ['Speedy Express', 'United Package', 'Federal Shipping'] -%}

SELECT 
    {% if target.type == 'postgres' -%}
        EXTRACT(YEAR FROM order_date) AS anio,
    {%- else -%}
        YEAR(order_date) AS anio,
    {%- endif %}
    
    {% for shipper in shippers -%}
    SUM(CASE WHEN shipper_name = '{{ shipper }}' THEN subtotal ELSE 0 END) AS ventas_{{ shipper | replace(' ', '_') | lower }}
    {%- if not loop.last %},{% endif %}
    {% endfor %}
FROM {{ ref('int_orders_shipped_details') }}
GROUP BY 
    {% if target.type == 'postgres' -%}
        EXTRACT(YEAR FROM order_date)
    {%- else -%}
        YEAR(order_date)
    {%- endif %}
```

**Código Compilado para PostgreSQL**
```sql
SELECT 
    EXTRACT(YEAR FROM order_date) AS anio,
    SUM(CASE WHEN shipper_name = 'Speedy Express' THEN subtotal ELSE 0 END) AS ventas_speedy_express,
    SUM(CASE WHEN shipper_name = 'United Package' THEN subtotal ELSE 0 END) AS ventas_united_package,
    SUM(CASE WHEN shipper_name = 'Federal Shipping' THEN subtotal ELSE 0 END) AS ventas_federal_shipping
FROM analytical_db.intermediate.int_orders_shipped_details
GROUP BY EXTRACT(YEAR FROM order_date);
```

**Código Compilado para SQL Server (T-SQL)**
```sql
SELECT 
    YEAR(order_date) AS anio,
    SUM(CASE WHEN shipper_name = 'Speedy Express' THEN subtotal ELSE 0 END) AS ventas_speedy_express,
    SUM(CASE WHEN shipper_name = 'United Package' THEN subtotal ELSE 0 END) AS ventas_united_package,
    SUM(CASE WHEN shipper_name = 'Federal Shipping' THEN subtotal ELSE 0 END) AS ventas_federal_shipping
FROM AnalyticalDB.intermediate.int_orders_shipped_details
GROUP BY YEAR(order_date);
```



#### Ejemplo 3: Extracción Dinámica de Columnas mediante la Macro `run_query` (Nivel Avanzado)
* **Escenario de Negocio:** El enfoque del Ejemplo 2 funciona con listas estáticas, pero si el negocio agrega nuevas categorías de productos en la tabla `Categories` (p. ej., *Beverages*, *Condiments*, *Confections*, etc.), el código SQL se volvería obsoleto. Necesitamos que dbt consulte la base de datos **en tiempo de compilación** para determinar qué categorías existen y generar el reporte de ventas por cliente de manera 100% automatizada.

* **Solución Jinja:** Implementamos la función avanzada de dbt **`run_query()`**. Esta ejecuta una consulta física de metadatos upstream durante la compilación, carga el resultado en memoria como una estructura tabular y la inyecta dinámicamente en el modelo para autogenerar las columnas del informe final.

**La Macro: `macros/get_category_names.sql`**
```sql
{% macro get_category_names() %}

{% set category_query %}
    SELECT DISTINCT category_name 
    FROM {{ ref('stg_northwind_categories') }} 
    ORDER BY 1
{% endset %}

-- Ejecutamos la consulta en tiempo de compilación
{% set results = run_query(category_query) %}

{% if execute %}
    -- Extraemos los valores de la primera columna como una lista de Python
    {% set results_list = results.columns.values() %}
{% else %}
    -- En fase de parseo inicial, devolvemos un array vacío seguro
    {% set results_list = [] %}
{% endif %}

{{ return(results_list) }}

{% endmacro %}
```

**El Modelo Consumidor: `marts/fct_customer_category_sales.sql`**
```sql
{{ config(materialized='table') }}

-- Invocamos la macro dinámica para obtener la lista de categorías vigentes
{% set categories = get_category_names() -%}

SELECT 
    customer_id,
    {% for category in categories -%}
    SUM(CASE WHEN category_name = '{{ category }}' THEN total_price ELSE 0 END) AS total_sales_{{ category | replace(' ', '_') | replace('/', '_') | lower }}
    {%- if not loop.last %},{% endif %}
    {% endfor %}
FROM {{ ref('int_product_sales_by_customer') }}
GROUP BY customer_id
```

**Código Compilado para PostgreSQL (Simulando 3 categorías detectadas en Northwind)**
```sql
SELECT 
    customer_id,
    SUM(CASE WHEN category_name = 'Beverages' THEN total_price ELSE 0 END) AS total_sales_beverages,
    SUM(CASE WHEN category_name = 'Condiments' THEN total_price ELSE 0 END) AS total_sales_condiments,
    SUM(CASE WHEN category_name = 'Confections' THEN total_price ELSE 0 END) AS total_sales_confections
FROM analytical_db.intermediate.int_product_sales_by_customer
GROUP BY customer_id;
```

**Código Compilado para SQL Server (T-SQL)**
```sql
SELECT 
    customer_id,
    SUM(CASE WHEN category_name = 'Beverages' THEN total_price ELSE 0 END) AS total_sales_beverages,
    SUM(CASE WHEN category_name = 'Condiments' THEN total_price ELSE 0 END) AS total_sales_condiments,
    SUM(CASE WHEN category_name = 'Confections' THEN total_price ELSE 0 END) AS total_sales_confections
FROM AnalyticalDB.intermediate.int_product_sales_by_customer
GROUP BY customer_id;
```



### Beneficios del Enfoque Jinja en dbt

1.  **Independencia del Motor (Portabilidad):** Como se observa en el Ejemplo 1, se pueden utilizar condicionales de adaptador (`target.type`) para escribir una única lógica en dbt que compile funciones nativas específicas para PostgreSQL o SQL Server sin duplicar los archivos del modelo.

2.  **Mantenimiento Cero:** Mediante patrones avanzados de consulta en compilación (`run_query`), dbt se adapta de manera orgánica a las modificaciones de los datos de origen (p. ej., nuevos productos, países o categorías) sin necesidad de reescribir una sola línea de código SQL downstream.

