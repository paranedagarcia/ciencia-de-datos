---
id: dbt-macros
title: ""
sidebar_label: "📄 Macros"
description: ""
slug: /dbt-macros
---


## **¿Qué es una Macro en dbt?**

En **dbt (Data Build Tool)**, una **macro** es una porción de código modular y altamente reutilizable. Desde una perspectiva de programación estructurada, **las macros equivalen a las funciones** en lenguajes como Python o JavaScript. 

Su arquitectura de diseño consiste en integrar el motor de plantillas **Jinja** con el lenguaje SQL declarativo. Al encapsular lógicas de negocio, cálculos financieros o conversiones de datos complejas en una macro, se evita la redundancia, alineando el repositorio de datos bajo el principio de desarrollo **DRY (Don't Repeat Yourself)**.

Físicamente, cada macro se define en un archivo con extensión `.sql` y se almacena de manera centralizada en el directorio `/macros` de tu proyecto dbt.


### Anatomía Sintáctica y Creación

Para construir una macro se utilizan etiquetas estructurales de Jinja que delimitan su ámbito de ejecución en la fase de compilación:

1. **Declaración (`{% macro ... %}`):** Establece el inicio del bloque, definiendo el nombre de la macro y los parámetros o argumentos que recibirá como variables de entrada.
2. **Cuerpo:** Espacio donde se desarrolla la consulta SQL combinada con expresiones, variables u operaciones lógicas dinámicas de Jinja.
3. **Cierre (`{% endmacro %}`):** Delimita el término de la función.


### Caso Práctico: Cálculo de Subtotal con Descuento (Northwind)

Para ilustrar este proceso, consideremos la tabla de detalles de órdenes (`Order Details`) de la base de datos **Northwind**. Automatizaremos el cálculo del **subtotal neto** (precio unitario por cantidad, restando el factor porcentual de descuento).

Dado que PostgreSQL y SQL Server poseen diferencias sutiles en la precisión de redondeo y en el formateo de tipos numéricos (*type casting*), crearemos una macro que evalúe el motor destino de nuestra conexión (`target.type`) y compile el SQL correcto para cada entorno:

#### 1. Creación de la Macro: `macros/get_net_subtotal.sql`
Este archivo se coloca dentro de la carpeta `/macros` de tu repositorio:

```sql
{% macro get_net_subtotal(unit_price, quantity, discount) %}
    -- Evaluamos dinámicamente el motor de base de datos en compilación
    {%- if target.type == 'postgres' -%}
        -- Sintaxis optimizada para PostgreSQL (requiere casting explícito a numeric)
        ROUND(({{ unit_price }} * {{ quantity }} * (1.0 - {{ discount }}))::numeric, 2)
    {%- else -%}
        -- Sintaxis optimizada para SQL Server (T-SQL - requiere conversión a DECIMAL)
        ROUND(CAST({{ unit_price }} AS DECIMAL(18,2)) * {{ quantity }} * (1.0 - {{ discount }}), 2)
    {%- endif -%}
{% endmacro %}
```

#### 2. Consumo de la Macro en el Modelo: `models/marts/fct_order_details.sql`
Invocamos la macro en la proyección de nuestro modelo analítico usando el delimitador de expresión `{{ ... }}` y enviando los nombres de las columnas físicas como argumentos de cadena:

```sql
-- models/marts/fct_order_details.sql
{{ config(materialized='table') }}

SELECT 
    order_id,
    product_id,
    unit_price,
    quantity,
    discount,
    -- Invocamos la macro pasando los campos como cadenas
    {{ get_net_subtotal('unit_price', 'quantity', 'discount') }} AS subtotal_neto
FROM {{ ref('stg_order_details') }}
```



### 3. Código SQL Compilado resultante según el Adaptador

Al ejecutar el comando de compilación (`dbt compile`) o de ejecución (`dbt run`), dbt lee la configuración de tu conexión (`profile`) y sustituye automáticamente la firma de la macro por el bloque de código SQL nativo:

#### Versión Compilada para PostgreSQL:
```sql
SELECT 
    order_id,
    product_id,
    unit_price,
    quantity,
    discount,
    ROUND((unit_price * quantity * (1.0 - discount))::numeric, 2) AS subtotal_neto
FROM analytical_db.staging.stg_order_details;
```

#### Versión Compilada para SQL Server (T-SQL):
```sql
SELECT 
    order_id,
    product_id,
    unit_price,
    quantity,
    discount,
    ROUND(CAST(unit_price AS DECIMAL(18,2)) * quantity * (1.0 - discount), 2) AS subtotal_neto
FROM AnalyticalDB.staging.stg_order_details;
```



### Técnicas de Ejecución e Interacción Avanzadas

dbt extiende la flexibilidad de las macros mediante tres mecanismos adicionales:

* **Retorno de Datos (`return`):** Permite que una macro devuelva estructuras lógicas nativas de Jinja (como listas o diccionarios) en lugar de una cadena SQL cruda, útil para centralizar matrices de constantes como listas de países o códigos de productos de Northwind.
* **Bloques de Llamada (`{% call ... %}`):** Sirve para ejecutar una macro contenedora y capturar bloques intermedios de SQL de forma dinámica mediante el objeto estructurado `caller()`.
* **Comando `dbt run-operation`:** Permite invocar y ejecutar una macro directamente desde la Terminal de comandos (CLI) sin tener que compilar ni ejecutar un modelo físico completo. Se utiliza con frecuencia para operaciones administrativas (DDL) de la base de datos, como purga de esquemas o asignación masiva de accesos de seguridad a usuarios.

---

:::info
En dbt, muchas de las macros complejas más comunes (como la creación de llaves subrogadas con algoritmos MD5 o divisiones matemáticas seguras contra el error de división por cero) ya están programadas y empaquetadas en librerías públicas compartidas por la comunidad.
:::
¿Te gustaría que exploremos cómo instalar y utilizar el popular paquete `dbt_utils` para agilizar tus transformaciones analíticas sobre Northwind?

## **db_utils**

**`dbt_utils`** es uno de los paquetes de código abierto más importantes y utilizados en el ecosistema de **dbt (Data Build Tool)**. Desarrollado y mantenido oficialmente por **dbt Labs**, este paquete actúa como una **biblioteca de utilidades estándar** que contiene macros, funciones auxiliares, pruebas genéricas avanzadas y plantillas SQL reutilizables. Su propósito principal es expandir las capacidades nativas de dbt para que los ingenieros de analítica no tengan que "reinventar la rueda" al programar transformaciones complejas, permitiendo mantener un repositorio limpio y bajo el estándar de desarrollo **DRY (*Don't Repeat Yourself*)**.



### Áreas Funcionales Clave de `dbt_utils`

El paquete está diseñado para resolver retos comunes en la preparación y modelado de datos:

1. **Modelado Dimensional (Surrogate Keys):** Facilita la creación de llaves subrogadas hash a partir de claves naturales compuestas, un requerimiento indispensable en arquitecturas de modelado de tipo Kimball.
2. **Lógica SQL Matemática y Operacional:** Provee macros para la manipulación segura de valores, como la evasión de errores catastróficos por división entre cero, transposición de filas a columnas (*pivot*) y operaciones de cadenas.
3. **Generación de Datos Continuos:** Permite construir vectores temporales densos (como calendarios o secuencias numéricas) para resolver la dispersión de datos.
4. **Pruebas de Calidad Avanzadas:** Introduce aserciones genéricas de datos adicionales que complementan las cuatro pruebas nativas de dbt (por ejemplo, validación de rangos, conteo de columnas o cardinalidad entre tablas).



### Ejemplos Prácticos de Compilación en Northwind (PostgreSQL vs SQL Server)

Para comprender cómo traduce dbt estas macros de Jinja a código SQL nativo, analizaremos dos de las operaciones más emblemáticas del paquete (`generate_surrogate_key` y `safe_divide`) aplicadas sobre el esquema relacional de la base de datos **Northwind**.

#### Ejemplo 1: Generación de Llaves Subrogadas (`generate_surrogate_key`)
* **Objetivo de Negocio:** En un Data Mart de ventas, necesitamos crear una clave única (llave subrogada) para la tabla de hechos combinando el identificador del cliente (`customer_id`) y la fecha del pedido (`order_date`) de la tabla `Orders`.
* **Firma Jinja en dbt:**
  ```sql
  {{ dbt_utils.generate_surrogate_key(['customer_id', 'order_date']) }}
  ```

##### Código Compilado para PostgreSQL
En PostgreSQL, `dbt_utils` compila la macro utilizando el algoritmo hash criptográfico `md5`, controlando los nulos mediante un delimitador interno para evitar colisiones:
```sql
SELECT 
    customer_id,
    order_date,
    -- dbt_utils concatena y genera un hash MD5 de 32 caracteres hexadecimales
    MD5(
        COALESCE(CAST(customer_id AS VARCHAR), '_dbt_utils_surrogate_key_null_') || '-' || 
        COALESCE(CAST(order_date AS VARCHAR), '_dbt_utils_surrogate_key_null_')
    ) AS sk_customer_order
FROM orders;
```

##### Código Compilado para SQL Server (T-SQL)
En SQL Server, la concatenación requiere la función `CONCAT` (que maneja de forma segura los tipos de datos) y la función del sistema `HASHBYTES` para computar el hash MD5, formateando la salida a minúsculas para mantener la consistencia:
```sql
SELECT 
    CustomerID,
    OrderDate,
    -- dbt_utils adapta la macro para invocar el motor de encriptación de T-SQL
    LOWER(CONVERT(VARCHAR(32), HASHBYTES('MD5', 
        CONCAT(
            COALESCE(CAST(CustomerID AS VARCHAR(MAX)), '_dbt_utils_surrogate_key_null_'),
            '-',
            COALESCE(CAST(OrderDate AS VARCHAR(MAX)), '_dbt_utils_surrogate_key_null_')
        )
    ), 2)) AS sk_customer_order
FROM dbo.Orders;
```



#### Ejemplo 2: División de Valores Segura contra División por Cero (`safe_divide`)

* **Objetivo de Negocio:** Calcular la tasa de descuento real aplicada en la tabla de transacciones de Northwind (`Order Details`). Dado que la cantidad de un artículo o el precio base podrían ser alterados, debemos protegernos contra un error de división por cero si alguna fila posee valores erróneos de entrada en el denominador.
* **Firma Jinja en dbt:**
  ```sql
  {{ dbt_utils.safe_divide('discount', 'unit_price') }}
  ```

##### Código Compilado para PostgreSQL
La macro intercepta el divisor utilizando `NULLIF`. Si el divisor es `0`, se transforma en `NULL`, lo que propaga el resultado analítico como un nulo seguro en lugar de abortar la transacción:
```sql
SELECT 
    order_id,
    product_id,
    discount,
    unit_price,
    -- Compilación limpia: el cero se convierte a NULL antes de la división
    (discount::numeric / NULLIF(unit_price, 0)::numeric) AS tasa_descuento_segura
FROM order_details;
```

##### **Código Compilado para SQL Server (T-SQL)**
En SQL Server, dbt realiza un casting preventivo a tipos flotantes o decimales de alta precisión para evitar la pérdida de decimales por división entera:
```sql
SELECT 
    OrderID,
    ProductID,
    Discount,
    UnitPrice,
    -- Compilación adaptada para el sistema de tipos de T-SQL
    (CAST(Discount AS FLOAT) / NULLIF(CAST(UnitPrice AS FLOAT), 0)) AS tasa_descuento_segura
FROM dbo.[Order Details];
```


### Cómo Instalar `dbt_utils`

Para incorporar este paquete a tu repositorio dbt, debes seguir un flujo de configuración en dos pasos:

1. Crea o edita el archivo **`packages.yml`** en la raíz de tu proyecto dbt (al mismo nivel jerárquico que `dbt_project.yml`) y declara el paquete:
   ```yaml
   packages:
     - package: dbt-labs/dbt_utils
       version: 1.1.1
   ```
2. Ejecuta el siguiente comando en tu interfaz de línea de comandos (CLI) de dbt para conectarte al repositorio público de dbt Hub y descargar físicamente las dependencias en la carpeta local `/dbt_packages`:
   ```bash
   dbt deps
   ```



## **Prueba de auditoría**

Diseño de una prueba de aserción avanzada utilizando el paquete `dbt_utils` para auditar que el catálogo de productos de Northwind cumpla con un rango específico de columnas y variaciones numéricas.

Para garantizar la confiabilidad y la robustez de un almacén de datos (*Data Warehouse*), la implementación de **mecanismos de control de calidad de datos (*Data Quality Gates*)** en el pipeline de transformaciones es una de las mejores prácticas de la ingeniería de datos analíticos ``. 

En la arquitectura de **dbt (Data Build Tool)**, las pruebas (*tests*) actúan como aserciones sobre los conjuntos de datos ``. A diferencia de los marcos de pruebas unitarias tradicionales del software que validan el comportamiento del código, dbt ejecuta **consultas de validación física** directamente sobre la base de datos ``. La lógica de dbt funciona bajo un principio matemático simple: **busca filas infractoras (registros que violen la regla de negocio definida)** ``. Si la consulta de prueba devuelve **cero filas**, la aserción es exitosa (pasa la prueba); si devuelve **una o más filas**, la prueba falla, alertando sobre anomalías en el sistema ``.

El paquete de utilidades **`dbt_utils`** amplía el catálogo de pruebas genéricas nativas de dbt ``, permitiendo definir aserciones lógicas complejas de manera puramente declarativa en archivos de configuración YAML ``.



### Definición de la Prueba Declarativa en el archivo `schema.yml`

Para auditar el catálogo de productos de **Northwind** (tabla `stg_products`), definiremos dos aserciones avanzadas utilizando `dbt_utils` ``:
1.  **`dbt_utils.accepted_range`:** Validará que el precio unitario (`unit_price`) sea mayor o igual a \$0.01 y menor o igual a \$300.00 ``, previniendo registros erróneos o nulos.
2.  **`dbt_utils.expression_is_true`:** Validará una regla de negocio condicional: *"Si un producto se marca como descontinuado (`discontinued = 1`), las unidades en pedido (`units_on_order`) deben ser estrictamente `0`."*

A continuación, se detalla la parametrización en el archivo de configuración del modelo:

```yaml
version: 2

models:
  - name: stg_products
    description: "Tabla de staging para el catálogo de productos de Northwind."
    columns:
      - name: unit_price
        description: "Precio de venta unitario del producto."
        tests:
          # Prueba 1: Controlar que el precio esté en un rango comercial válido
          - dbt_utils.accepted_range:
              min_value: 0.01
              max_value: 300.00

      - name: units_on_order
        description: "Cantidad de unidades pendientes de recibir en órdenes de compra."
        tests:
          # Prueba 2: Regla de integridad lógica para productos descontinuados
          - dbt_utils.expression_is_true:
              expression: "CASE WHEN discontinued = 1 THEN units_on_order = 0 ELSE TRUE END"
```



### Compilación del Test: PostgreSQL vs. SQL Server (T-SQL)

Cuando se ejecuta el comando `dbt test` ``, dbt procesa el bloque Jinja/YAML y genera dinámicamente un archivo SQL de consulta física en la carpeta `/target` ``. Aquí contrastamos cómo compilan estas pruebas en ambos motores de base de datos.

#### Prueba 1: Rango Aceptado (`dbt_utils.accepted_range` en `unit_price`)

El compilador de dbt busca registros que violen los límites establecidos (valores menores al mínimo o mayores al máximo) ``.

*   **Versión PostgreSQL:**
    ```sql
    SELECT 
        unit_price AS failures
    FROM analytical_db.staging.stg_products
    -- El motor busca infracciones fuera del intervalo cerrado
    WHERE unit_price < 0.01 OR unit_price > 300.00;
    ```

*   **Versión SQL Server (T-SQL):**
    ```sql
    SELECT 
        UnitPrice AS failures
    FROM dbo.stg_products
    -- SQL Server procesa la misma lógica de exclusión de rango
    WHERE UnitPrice < 0.01 OR UnitPrice > 300.00;
    ```



#### Prueba 2: Regla de Coherencia (`dbt_utils.expression_is_true` en `units_on_order`)

La aserción evalúa la expresión condicional de negocio. dbt compila la consulta aplicando una negación lógica (`NOT`) sobre la expresión dada para capturar únicamente los registros incoherentes ``.

*   **Versión PostgreSQL:**
    En PostgreSQL, los predicados lógicos complejos y estructuras condicionales se resuelven de forma directa, permitiendo evaluar la expresión booleana resultante:
    ```sql
    SELECT 
        product_id, 
        product_name, 
        discontinued, 
        units_on_order AS failures
    FROM analytical_db.staging.stg_products
    -- El operador NOT captura las tuplas que no cumplen la condición CASE
    WHERE NOT (
        CASE 
            WHEN discontinued = 1 THEN units_on_order = 0 
            ELSE TRUE 
        END
    );
    ```

*   **Versión SQL Server (T-SQL):**
    Dado que SQL Server no cuenta con un tipo de datos booleano puro que pueda evaluarse directamente en la cláusula `WHERE` (fuera de comparaciones escalares explícitas), dbt inyecta una estructura transaccional adaptada para T-SQL, comparando el resultado de la expresión condicional frente a un entero lógico (`1` para verdadero):
    ```sql
    SELECT 
        ProductID, 
        ProductName, 
        Discontinued, 
        UnitsOnOrder AS failures
    FROM dbo.stg_products
    -- T-SQL requiere comparar el resultado escalar del CASE con 1
    WHERE NOT (
        CASE 
            WHEN Discontinued = 1 THEN 
                CASE WHEN UnitsOnOrder = 0 THEN 1 ELSE 0 END
            ELSE 1 
        END = 1
    );
    ```


### Interpretación y Gestión de Fallas en Producción

Si durante la ejecución nocturna del pipeline se llegase a violar alguna de estas restricciones (por ejemplo, si se registra un precio de `0.00` o si se intentan ordenar unidades de un producto descontinuado como *Chai*), la consulta de prueba devolverá las filas afectadas ``. 

En la CLI de dbt se generará una alerta de **`FAIL`** indicando el número exacto de registros corruptos ``. Estos registros pueden ser persistidos automáticamente en una tabla de auditoría en la base de datos mediante la bandera `--store-failures` para un posterior análisis de causa raíz por parte del equipo analítico ``.

