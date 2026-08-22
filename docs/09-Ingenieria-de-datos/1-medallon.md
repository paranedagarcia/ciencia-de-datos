---
id: medallon
title: "Arquitectura Medallon"
sidebar_label: "💻 Arquitectura Medallon"
sidebar_position: 4
description: "Esta arquitectura se prefiere para cargas de trabajo analíticas ya que garantiza transacciones **ACID**"
slug: /medallon
---

La **arquitectura de medallón** (también conocida como **arquitectura multi-hop** o de múltiples saltos) es un patrón de diseño que organiza los datos de manera lógica en una estructura de almacenamiento multicapa. Su propósito fundamental es mejorar progresivamente la estructura, la calidad y la utilidad de la información a medida que fluye por las diferentes etapas de procesamiento y transformación. 

Esta arquitectura se prefiere para cargas de trabajo analíticas (OLAP) debido a que garantiza transacciones **ACID** (atomicidad, consistencia, aislamiento y durabilidad) a lo largo del flujo y permite la coexistencia integrada de cargas de trabajo híbridas (tanto por lotes como en tiempo real en una misma canalización).

---

### Las tres capas

1. **Capa Bronze (Datos Crudos / Raw Ingestion):**
   * Es el punto de partida y la base de la ingesta de datos. Aquí se recibe y almacena la información procedente de diversos sistemas de origen (como bases de datos operacionales, archivos estructurados o flujos de eventos en tiempo real de plataformas como Kafka) en su formato más crudo.
   * Los datos en esta capa se guardan **sin transformaciones ni modificaciones**. Esto asegura la preservación total de los registros originales, previniendo la pérdida de datos y facilitando tareas de auditoría, trazabilidad (*data lineage*) y solución de problemas.
   * Con fines de control y auditoría, los registros en esta capa suelen complementarse únicamente con metadatos clave, como el tiempo de llegada (*arrival time*) y el archivo de origen.

2. **Capa Silver (Datos Limpios e Integrados / Cleansed & Enriched):**
   * En esta fase intermedia, el enfoque se desplaza hacia la **limpieza, normalización y validación** de los datos provenientes de la capa Bronze.
   * Se filtran los registros incorrectos o irrelevantes y se resuelven las inconsistencias para garantizar la confiabilidad de la información.
   * Además de la limpieza, esta etapa a menudo involucra el **enriquecimiento de datos**, lo cual consiste en combinar o integrar tablas de distintas fuentes operativas mediante uniones (*joins*) para ofrecer una vista consolidada y coherente del negocio. Esto prepara la información para tareas analíticas que exigen un alto grado de integridad y precisión.

3. **Capa Gold (Datos de Negocio / Curated & Aggregated):**
   * Es la capa final donde los datos alcanzan su estado más refinado, estructurado y listo para el negocio. 
   * A diferencia del nivel de detalle de las capas previas, aquí los datos se almacenan en un **diseño optimizado para lectura** y se estructuran en formatos **altamente agregados y resumidos** (como indicadores de rendimiento, resúmenes financieros o perfiles consolidados de clientes) para responder a necesidades estratégicas de la empresa.
   * Estas tablas optimizadas alimentan de manera rápida y directa herramientas de **Business Intelligence (BI)**, reportería, tableros de control (*dashboards*) y algoritmos de modelado avanzado para **Machine Learning e Inteligencia Artificial**.

---

### Beneficios clave
* **Simplicidad:** Representa un modelo intuitivo y fácil de entender que reduce drásticamente la complejidad operativa y de mantenimiento del almacén de datos.
* **ETL Incremental:** Permite la transformación y carga incremental de datos a medida que llegan a la plataforma.
* **Reconstrucción de tablas:** Si se detecta un problema de calidad o un error en la lógica de negocio río abajo, se pueden borrar las tablas afectadas y volver a generarlas en cualquier momento a partir de los datos históricos e inmutables de la capa Bronze.
* **Gobernanza y Sencillez en la Distribución:** Facilita la orquestación del flujo de datos sin duplicar espacio de almacenamiento físico; por ejemplo, permitiendo que las tareas de procesamiento de Bronze y Silver se administren de manera interna (capas de producción) y que el resultado de la capa Gold se escriba directamente en un catálogo de publicación para que los usuarios finales lo consuman sin acceder al almacenamiento crudo.

***

## Medallon vs Data Warehouse

La diferencia entre la **arquitectura de medallón** (implementada en un entorno de *Data Lakehouse*) y un **Data Warehouse tradicional** radica en cómo se estructuran, procesan, almacenan y gobiernan los datos. Las principales diferencias técnicas son las siguientes:

#### Esquema de Datos (*Schema-on-write* vs. *Schema-on-read* / Progresivo)
*   **Data Warehouse tradicional:** Opera bajo el principio de **esquema en escritura (*schema-on-write*)**. Esto exige que los datos sean limpiados, estructurados y adaptados a un esquema rígido predefinido antes de que puedan ser cargados físicamente en el repositorio.
*   **Modelo de Medallón:** Los datos se ingieren primero en su estado nativo y bruto en la capa **Bronze** sin un esquema estricto. El esquema y las validaciones de calidad se aplican de manera **incremental y progresiva** a medida que los datos avanzan hacia las capas **Silver** (limpieza/validación) y **Gold** (agregación de negocio).

#### Tipos de Datos Soportados
*   **Data Warehouse tradicional:** Está diseñado casi exclusivamente para almacenar y procesar **datos estructurados** organizados en tablas relacionales de filas y columnas. Presenta serias limitaciones o incapacidad para manejar formatos no estructurados o semiestructurados directamente.
*   **Modelo de Medallón:** Al construirse sobre un *Data Lake*, tiene la flexibilidad de almacenar, organizar y refinar **datos estructurados, semiestructurados y no estructurados** (como archivos JSON, logs, imágenes, video o audio) dentro de la misma infraestructura de almacenamiento unificado.

#### Acoplamiento de Cómputo y Almacenamiento
*   **Data Warehouse tradicional:** Tradicionalmente acopla de manera estrecha el motor de procesamiento con el almacenamiento físico y los índices en disco, lo que limita la capacidad de escalar ambos componentes de forma independiente en entornos locales (*on-premises*) (aunque almacenes en la nube modernos han comenzado a desacoplarlos).
*   **Modelo de Medallón:** Funciona con un **desacoplamiento total de cómputo y almacenamiento**. Los datos (ficheros abiertos como Parquet o Delta) residen en un almacenamiento de objetos de bajo costo (como Amazon S3 o Azure ADLS), mientras que los motores de cómputo distribuidos (como Apache Spark) se activan de forma elástica para procesar las capas solo cuando es necesario.

#### Trazabilidad e Historial de Datos (*Data Lineage*)
*   **Data Warehouse tradicional:** En los procesos ETL tradicionales, los datos brutos de la zona de tránsito (*staging*) suelen eliminarse después de ser transformados y cargados al almacén final. Esto significa que los usuarios pierden el acceso a la historia de los datos en su estado original e inmutable.
*   **Modelo de Medallón:** La capa **Bronze** actúa como un histórico inmutable que replica exactamente los sistemas de origen. Si las reglas de negocio cambian o se detecta un fallo de calidad en las capas superiores, es posible **borrar las tablas Silver/Gold y regenerarlas completamente** desde el principio a partir de los datos crudos almacenados en Bronze.

#### Ingesta y Unificación de Procesos (*Batch* y *Streaming*)
*   **Data Warehouse tradicional:** Se diseñó históricamente para cargas masivas por lotes (*batch*) programadas de forma periódica (por ejemplo, procesos nocturnos), sufriendo de latencia para soportar la ingesta en tiempo real.
*   **Modelo de Medallón:** Permite la **unificación nativa** de flujos de datos históricos (*batch*) y continuos en tiempo real (*stream processing*) sobre la misma tabla y almacenamiento físico mediante motores de *streaming* estructurado y formatos transaccionales como Delta Lake.

