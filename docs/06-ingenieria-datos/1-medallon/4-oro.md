---
id: oro
title: "Capa Oro"
sidebar_label: "📄 Capa Oro"
description: "Capa Oro"
hide_title: true
---

## **Capa Oro**

Dentro del **modelo medallón** (*Medallion Architecture*), la **capa oro** (*Gold layer*) es la fase final de curación, donde los datos se encuentran completamente procesados, refinados y adaptados para satisfacer las necesidades específicas del negocio y la toma de decisiones. 

En esta etapa, conocida habitualmente como la **zona curada (*curated zone*)** o la **única fuente de la verdad (*single source of truth*)**, los datos limpios y estandarizados provenientes de la capa plata se transforman en conjuntos optimizados para lectura y consumo directo.

---

### 1. Propósito y Características Principales

* **Datos listos para el consumo (*Business-Ready Data*):** La información está lista para ser explotada por aplicaciones analíticas sin necesidad de que el usuario final deba depurarla o aplicar transformaciones estructurales adicionales.
* **Modelado dimensional (Esquema en Estrella):** A diferencia de las capas previas (orientadas a normalización o tablas crudas), en la capa oro los datos suelen estructurarse bajo las reglas del modelado dimensional, materializándose en **tablas de hechos (*fact tables*)** y **tablas de dimensiones (*dimension tables*)**.
* **Agregaciones y métricas de negocio:** Se aplican reglas y lógicas empresariales complejas, resumiendo los datos en niveles de granularidad mayores (por ejemplo, agregaciones de ventas por fecha, región o producto) para optimizar el rendimiento de las consultas.
* **Optimización para lectura masiva:** Se almacena habitualmente en formatos columnares abiertos como **Delta Lake (Delta Parquet)**, permitiendo compatibilidad con tecnologías como *V-Order* y transacciones ACID que maximizan la velocidad de lectura.

---

### 2. Consumidores y Casos de Uso

La capa oro está diseñada para atender a los consumidores finales del dato dentro de la organización:
* **Inteligencia de Negocio y Reportes (BI):** Es el origen preferido para herramientas de visualización como **Power BI**, Tableau o Excel corporativo, habilitando modelos de conexión de alto rendimiento como *Direct Lake* o consultas directas mediante endpoints SQL.
* **Data Marts por departamento:** Los datos pueden agruparse en estructuras específicas orientadas a dominios funcionales (finanzas, ventas, operaciones, marketing).
* **Cuadros de mando y analítica ejecutiva:** Proporciona indicadores clave de rendimiento (KPIs) con calidad auditada y certificada.

---

### 3. La Capa Oro en el Flujo Completo del Modelo Medallón

| Capa | Estado del Dato | Estructura típica | Caso de uso principal |
| :--- | :--- | :--- | :--- |
| **Bronce (*Bronze*)** | **Crudo / Raw** (*as-is*) | Archivos originales o tablas de solo anexado (*append-only*). | Histórico auditable e ingesta general. |
| **Plata (*Silver*)** | **Limpio y validado** | Tablas Delta estandarizadas, deduplicadas y filtradas. | Analítica fundacional, ciencia de datos y preparación. |
| **Oro (*Gold*)** | **Consolidado de negocio** | **Tablas de hechos, dimensiones y vistas agregadas**. | **Reportes BI, dashboards ejecutivos y toma de decisiones**. |


***
## Modelo estrella

El **esquema en estrella (*Star Schema*)** es el patrón de modelado dimensional por excelencia utilizado en sistemas analíticos (OLAP), almacenes de datos (*Data Warehouses*) y en la **capa Oro** de un *lakehouse*. 

Se caracteriza por tener una **tabla de hechos central (*Fact Table*)** rodeada de múltiples **tablas de dimensiones (*Dimension Tables*)**, formando una figura que se asemeja a una estrella.



### Diagrama Conceptual del Esquema en Estrella

A continuación se muestra un ejemplo clásico para el proceso de negocio de **Ventas minoristas (*Retail Sales*)**:

```text
       ┌────────────────────────┐                   ┌────────────────────────┐
       │      Dim_Cliente       │                   │      Dim_Producto      │
       ├────────────────────────┤                   ├────────────────────────┤
       │ PK  ClienteKey (SK)    │                   │ PK  ProductoKey (SK)   │
       │     ID_Cliente_Origen  │                   │     SKU / Codigo       │
       │     Nombre_Completo    │                   │     Nombre_Producto    │
       │     Segmento           │                   │     Categoria          │
       │     Ciudad             │                   │     Subcategoria       │
       │     Pais               │                   │     Marca              │
       └───────────┬────────────┘                   └───────────┬────────────┘
                   │                                            │
                   │ 1                                          │ 1
                   │                                            │
                   │ ∞                                          │ ∞
                 ┌─┴────────────────────────────────────────────┴─┐
                 │                   Fact_Ventas                  │
                 ├────────────────────────────────────────────────┤
                 │ PK/FK  FechaKey               (int)            │
                 │ PK/FK  ClienteKey             (int)            │
                 │ PK/FK  ProductoKey            (int)            │
                 │ PK/FK  TiendaKey              (int)            │
                 │ DD     Numero_Factura         (Degenerate Dim) │
                 ├────────────────────────────────────────────────┤
                 │        Cantidad               (Métrica aditiva)│
                 │        Precio_Unitario        (Métrica)        │
                 │        Monto_Descuento        (Métrica aditiva)│
                 │        Costo_Total            (Métrica aditiva)│
                 │        Monto_Venta_Neto       (Métrica aditiva)│
                 └─┬────────────────────────────────────────────┬─┘
                   │ ∞                                          │ ∞
                   │                                            │
                   │ 1                                          │ 1
       ┌───────────┴────────────┐                   ┌───────────┴────────────┐
       │       Dim_Fecha        │                   │       Dim_Tienda       │
       ├────────────────────────┤                   ├────────────────────────┤
       │ PK  FechaKey (YYYYMMDD)│                   │ PK  TiendaKey (SK)     │
       │     Fecha_Completa     │                   │     Codigo_Sucursal    │
       │     Anio               │                   │     Nombre_Tienda      │
       │     Trimestre          │                   │     Canal (Web/Fisico) │
       │     Mes                │                   │     Region             │
       │     Dia_Semana         │                   │     Gerente_Tienda     │
       └────────────────────────┘                   └────────────────────────┘
```



### Detalle de sus Componentes

#### A. Tabla de Hechos Central (`Fact_Ventas`)
* **Propósito:** Registrar los eventos transaccionales numéricos cuantificables del proceso de negocio.
* **Granularidad (*Grain*):** Una fila por cada línea de producto vendida en cada recibo o factura.
* **Columnas de Claves (Contexto):** Claves foráneas numéricas (`FechaKey`, `ClienteKey`, `ProductoKey`, `TiendaKey`) que apuntan a cada dimensión mediante relaciones de **muchos a uno (*\*:1*)**.
* **Dimensiones Degeneradas (*DD*):** Identificadores como `Numero_Factura`, que no tienen atributos descriptivos adicionales para justificar una tabla propia y se conservan directamente en la tabla de hechos.
* **Métricas (*Measures*):** Valores numéricos típicamente aditivos (`Cantidad`, `Monto_Descuento`, `Monto_Venta_Neto`) que pueden sumarse o promediarse a través de cualquier combinación de dimensiones.

#### B. Tablas de Dimensiones (`Dim_Cliente`, `Dim_Producto`, `Dim_Fecha`, `Dim_Tienda`)
* **Propósito:** Responder a las preguntas de contexto empresarial: *¿Quién compró?*, *¿Qué se vendió?*, *¿Dónde ocurrió?* y *¿Cuándo?*.

* **Desnormalización intencional:** A diferencia de las bases de datos transaccionales (3NF) o del esquema copo de nieve (*Snowflake*), las jerarquías se aplanan en la misma tabla de dimensión (por ejemplo, `Categoria`, `Subcategoria` y `Marca` conviven en `Dim_Producto` sin crear tablas intermedias). Esto minimiza la cantidad de uniones (*joins*) en las consultas analíticas.

* **Claves Subrogadas (*Surrogate Keys - SK*):** Se utilizan identificadores enteros independientes de las claves del sistema de origen para garantizar estabilidad histórica frente a cambios en los sistemas fuente (como en dimensiones de cambio lento o SCD Tipo 2).



### Ejemplo de Consulta Analítica

La mayor ventaja del esquema en estrella es que las consultas analíticas son intuitivas y no requieren navegar por cadenas complejas de tablas normalizadas:

```sql
SELECT 
    d.Anio,
    d.Mes,
    p.Categoria,
    t.Region,
    SUM(f.Cantidad)            AS Total_Unidades_Vendidas,
    SUM(f.Monto_Venta_Neto)    AS Ingresos_Totales,
    AVG(f.Monto_Venta_Neto)    AS Ticket_Promedio
FROM Fact_Ventas f
INNER JOIN Dim_Fecha d     ON f.FechaKey = d.FechaKey
INNER JOIN Dim_Producto p  ON f.ProductoKey = p.ProductoKey
INNER JOIN Dim_Tienda t    ON f.TiendaKey = t.TiendaKey
WHERE d.Anio = 2026
GROUP BY 
    d.Anio, 
    d.Mes, 
    p.Categoria, 
    t.Region
ORDER BY 
    Ingresos_Totales DESC;
```



***
## Modelo Copo de nieves

El **esquema copo de nieve (*Snowflake Schema*)** es una variante del modelado dimensional en la que **una o más tablas de dimensiones se encuentran normalizadas** en múltiples subdimensiones o tablas secundarias. 

A diferencia del esquema en estrella —donde las dimensiones se desnormalizan y aplanan en una única tabla por entidad—, el proceso de *snowflaking* divide las jerarquías y atributos repetitivos en tablas separadas por nivel jerárquico. Al representarse gráficamente, las ramificaciones sucesivas de relaciones hacia tablas externas hacen que el modelo adopte la forma visual de un copo de nieve.


En un esquema copo de nieve, la tabla central de hechos se conecta a dimensiones inmediatas, y estas, a su vez, se vinculan con subdimensiones normalizadas:

```text
                                  ┌───────────────────────────┐
                                  │   Dim_Categoria_Producto  │
                                  ├───────────────────────────┤
                                  │ PK  CategoriaKey          │
                                  │     Nombre_Categoria      │
                                  └─────────────┬─────────────┘
                                                │ 1
                                                │
                                                │ ∞
                                  ┌─────────────┴─────────────┐
                                  │ Dim_Subcategoria_Producto │
                                  ├───────────────────────────┤
                                  │ PK  SubcategoriaKey       │
                                  │ FK  CategoriaKey          │
                                  │     Nombre_Subcategoria   │
                                  └─────────────┬─────────────┘
                                                │ 1
                                                │
                                                │ ∞
┌──────────────────┐              ┌─────────────┴─────────────┐
│    Dim_Ciudad    │              │        Dim_Producto       │
├──────────────────┤              ├───────────────────────────┤
│ PK CiudadKey     │              │ PK  ProductoKey           │
│    Nombre_Ciudad │              │ FK  SubcategoriaKey       │
└────────┬─────────┘              │     Nombre_Producto       │
         │ 1                      │     Precio_Unitario       │
         │                        └─────────────┬─────────────┘
         │ ∞                                    │ 1
┌────────┴─────────┐                            │
│  Dim_Geografia   │                            │
├──────────────────┤                            │
│ PK GeoKey        │                            │
│ FK CiudadKey     │                            │
│    Pais / Region │                            │
└────────┬─────────┘                            │
         │ 1                                    │
         │                                      │
         │ ∞                                    │ ∞
       ┌─┴──────────────────────────────────────┴─┐
       │                Fact_Ventas               │
       ├──────────────────────────────────────────┤
       │ PK/FK  FechaKey                          │
       │ PK/FK  ProductoKey                       │
       │ PK/FK  GeoKey                            │
       │ PK/FK  ClienteKey                        │
       ├──────────────────────────────────────────┤
       │        Cantidad                          │
       │        Monto_Total_Venta                 │
       └──────────────────────────────────────────┘
```



### Características Clave del Modelo

1. **Normalización de Dimensiones:** Las jerarquías naturales de los datos (por ejemplo: `Producto` $\rightarrow$ `Subcategoría` $\rightarrow$ `Categoría`, o `Dirección` $\rightarrow$ `Ciudad` $\rightarrow$ `País`) se descomponen en tablas individuales relacionadas entre sí mediante claves primarias y foráneas.

2. **Eliminación de Redundancia de Datos:** Al separar los niveles jerárquicos en tablas secundarias, los valores repetitivos (como el nombre de la categoría en cada producto) se almacenan una sola vez.

3. **Múltiples Saltos de Relación (*Multi-hop Joins*):** Para consultar un atributo de nivel superior (como las ventas totales agrupadas por `Categoria`), la consulta analítica debe unir obligatoriamente la tabla de hechos con `Dim_Producto`, luego con `Dim_Subcategoria_Producto` y finalmente con `Dim_Categoria_Producto`.



### Estrella vs. Copo de Nieve

| Criterio | Esquema en Estrella (*Star*) | Esquema Copo de Nieve (*Snowflake*) |
| :--- | :--- | :--- |
| **Normalización** | Dimensiones completamente desnormalizadas y aplanadas. | Dimensiones normalizadas en subdimensiones. |
| **Redundancia** | Mayor redundancia intencional en las dimensiones. | Menor redundancia de almacenamiento. |
| **Complejidad de consultas** | Sencilla; solo un `JOIN` directo entre hecho y dimensión. | Mayor; requiere encadenar múltiples `JOIN` sucesivos. |
| **Rendimiento analítico** | Optimizado para lecturas rápidas y motores columnares / Power BI. | Puede penalizar el rendimiento por el costo computacional de múltiples uniones. |
| **Comprensión para el usuario** | Intuitivo y fácil de explorar en herramientas de autoservicio. | Menos intuitivo y más complejo de navegar para usuarios de negocio. |



### ¿Cuándo se Justifica?

Aunque en plataformas analíticas modernas (como Microsoft Fabric, Azure Synapse o Power BI) el esquema en estrella es casi siempre la opción recomendada, existen situaciones específicas donde el copo de nieve es útil o necesario:

* **Dimensiones Monstruosas (*Monster Dimensions*):** Si una dimensión desnormalizada acumula cientos de atributos y millones de filas con cadenas de texto repetidas, el espacio consumido y la ineficiencia de lectura pueden justificar la normalización de sus jerarquías.

* **Múltiples Tablas de Hechos con Distinta Granularidad:** Si en el mismo almacén conviven hechos a diferente nivel de detalle (por ejemplo, `Fact_Ventas` a nivel de producto individual y `Fact_Metas_Objetivo` a nivel de categoría general), normalizar la jerarquía en `Dim_Producto` y `Dim_Categoria` permite enlazar cada tabla de hechos directamente con la tabla correspondiente a su nivel de agregación.

* **Modelos Híbridos u Óptimos:** Existen variantes donde los atributos se conservan tanto en la tabla principal como en la normalizada, o se heredan las claves foráneas de subniveles directamente en la tabla de hechos para evitar saltos en cascada en las consultas más frecuentes.



***
## 🖥️ Practico de implementacion

A continuación se presenta cómo estructurar y materializar la **Capa Oro** utilizando el modelado dimensional en **esquema en estrella (*star schema*)**, junto con un ejemplo práctico en **PySpark** y consultas de agregación analítica listas para herramientas de Business Intelligence (BI).


### Arquitectura del Modelo en Estrella en Capa Oro

A partir de los datos transaccionales limpios de la **capa Plata**, la capa Oro organiza la información separando las métricas de negocio cuantificables de los contextos analíticos:

*   **Tabla de Hechos (`fact_ventas`):** Contiene las métricas numéricas acumuladas o eventos transaccionales (monto vendido, cantidad de productos, descuentos aplicados) junto con claves foráneas (*surrogate keys* o claves de negocio) que apuntan a cada dimensión.
*   **Tablas de Dimensiones (`dim_cliente`, `dim_tiempo`, `dim_producto`, `dim_tienda`):** Almacenan los atributos descriptivos para filtrar, agrupar y segmentar los datos (nombre del cliente, categoría de producto, mes, trimestre, país o región).



### Implementación del Pipeline en PySpark hacia Capa Oro

El siguiente flujo lee la tabla curada `silver.transacciones`, genera una dimensión temporal estructurada, calcula la tabla de hechos con agregaciones y persiste el resultado en **Delta Lake**:

```python
from pyspark.sql.functions import col, year, month, quarter, dayofmonth, sum as _sum, count, avg, current_timestamp
from delta.tables import DeltaTable

# -------------------------------------------------------------------------
# 1. Lectura de las tablas limpias de la Capa Plata
# -------------------------------------------------------------------------
silver_transacciones = spark.read.table("silver.transacciones")

# -------------------------------------------------------------------------
# 2. Creación / Transformación de la Dimensión Tiempo (dim_tiempo)
# -------------------------------------------------------------------------
dim_tiempo = (
    silver_transacciones
    .select("fecha_transaccion")
    .distinct()
    .filter(col("fecha_transaccion").isNotNull())
    .withColumn("anio", year("fecha_transaccion"))
    .withColumn("trimestre", quarter("fecha_transaccion"))
    .withColumn("mes", month("fecha_transaccion"))
    .withColumn("dia", dayofmonth("fecha_transaccion"))
)

dim_tiempo.write.format("delta").mode("overwrite").saveAsTable("gold.dim_tiempo")

# -------------------------------------------------------------------------
# 3. Construcción de la Tabla de Hechos Agregada (fact_ventas_diarias)
# -------------------------------------------------------------------------
fact_ventas_oro = (
    silver_transacciones
    .groupBy("fecha_transaccion", "id_cliente", "codigo_moneda")
    .agg(
        _sum("monto").alias("monto_total_venta"),
        count("id_transaccion").alias("cantidad_transacciones"),
        avg("monto").alias("ticket_promedio")
    )
    .withColumn("fecha_actualizacion_gold", current_timestamp())
)

# -------------------------------------------------------------------------
# 4. Materialización en Delta Lake con Particionamiento y Z-Order
# -------------------------------------------------------------------------
gold_table_name = "gold.fact_ventas_diarias"

(
    fact_ventas_oro.write
    .format("delta")
    .mode("overwrite")
    .partitionBy("codigo_moneda")
    .saveAsTable(gold_table_name)
)

# Optimización para lectura analítica rápida (Data Skipping)
spark.sql(f"OPTIMIZE {gold_table_name} ZORDER BY (id_cliente, fecha_transaccion)")
```

### Explotación Analítica en Capa Oro (SQL para BI y Cuadros de Mando)

Una vez estructuradas las tablas de hechos y dimensiones en la capa Oro, las herramientas de visualización (como Power BI, Tableau o endpoints SQL de Synapse/Fabric) pueden ejecutar consultas analíticas rápidas con agregaciones directas:

```sql
SELECT 
    t.anio,
    t.trimestre,
    v.codigo_moneda,
    COUNT(DISTINCT v.id_cliente)           AS clientes_activos,
    SUM(v.cantidad_transacciones)         AS total_operaciones,
    ROUND(SUM(v.monto_total_venta), 2)    AS ingresos_totales,
    ROUND(AVG(v.ticket_promedio), 2)       AS promedio_venta_por_ticket
FROM gold.fact_ventas_diarias v
INNER JOIN gold.dim_tiempo t
    ON v.fecha_transaccion = t.fecha_transaccion
GROUP BY 
    t.anio, 
    t.trimestre, 
    v.codigo_moneda
ORDER BY 
    t.anio DESC, 
    t.trimestre DESC;
```

---

### Buenas Prácticas y Optimización en la Capa Oro

1. **Pre-agregación selectiva:** Aunque se mantenga una tabla de hechos detallada al nivel de granularidad más bajo, es común crear vistas o tablas agregadas adicionales para métricas recurrentes de dashboards ejecutivos (KPIs mensuales o trimestrales).

2. **Direct Lake y Modo Importación en BI:** En herramientas como Microsoft Fabric y Power BI, el formato Delta Lake en la capa Oro habilita el modo **Direct Lake**, permitiendo leer archivos Parquet directamente desde OneLake/ADLS sin necesidad de importar datos ni duplicar memoria.

3. **Imposición de Claves Subrogadas (*Surrogate Keys*):** Para dimensiones que cambian con el tiempo (SCD Tipo 2, como clientes que cambian de dirección o categoría), se recomienda generar identificadores enteros secuenciales o *hashes* para mantener la integridad histórica de los reportes.

---

⭐ Si quieres, podemos revisar cómo orquestar todo el pipeline (Bronce ➔ Plata ➔ Oro) de principio a fin utilizando herramientas como Azure Data Factory o Apache Airflow.
