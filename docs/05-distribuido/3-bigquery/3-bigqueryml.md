---
id: bigqueryml
title: ""
sidebar_label: "💻 BigQuery ML"
description: "BigQuery orientado específicamente a procesar modelos de aprendizaje automático (Machine Learning)"
---

## **BigQuery ML**

**BigQuery ML (BQML)** es una característica nativa de Google BigQuery que permite a los desarrolladores, analistas de datos y científicos de datos **crear, entrenar, evaluar y ejecutar modelos de aprendizaje automático (Machine Learning) utilizando directamente consultas de SQL estándar**.

Su principal ventaja radica en que **los datos permanecen dentro de BigQuery**, lo que elimina la necesidad de exportar volúmenes masivos de información a herramientas o servidores externos de entrenamiento. Esto aporta grandes beneficios en términos de **seguridad, velocidad y cumplimiento de la localidad de datos**. Además, democratiza el Machine Learning al permitir que cualquier persona con conocimientos de SQL desarrolle modelos sin tener que escribir código complejo en lenguajes como Python, Java o R.

---

### ¿Cómo opera BigQuery ML? El ciclo de vida de un modelo

El proceso para trabajar con BigQuery ML sigue un flujo de pasos basados en funciones y extensiones específicas de SQL:

1. **Definición y Preparación de Datos (Preprocesamiento)**:
   Antes del entrenamiento, se seleccionan las características (*features*) y la etiqueta (*label*) a predecir. Se pueden realizar transformaciones de datos utilizando funciones de preprocesamiento de BigQuery, tales como `ML.BUCKETIZE` (para agrupar variables numéricas en contenedores) o `ML.FEATURE_CROSS` (para cruzar variables categóricas). 
   * **Mejor Práctica (Cláusula `TRANSFORM`)**: Es altamente recomendable agrupar estas transformaciones dentro de una cláusula `TRANSFORM` al entrenar el modelo. Esto permite que BigQuery "guarde" las reglas de preprocesamiento y las aplique de forma automática al realizar las predicciones, evitando que el cliente tenga que preprocesar los nuevos datos manualmente antes de consumirlos.

2. **Entrenamiento del Modelo (`CREATE MODEL`)**:
   El entrenamiento se inicia ejecutando una sentencia SQL estructurada similar a la creación de una tabla. Se utiliza la instrucción `CREATE OR REPLACE MODEL`, donde en la sección de `OPTIONS` se define el tipo de modelo y la columna que actúa como etiqueta de predicción:
   ```sql
   CREATE OR REPLACE MODEL dataset.nombre_modelo
   OPTIONS(model_type='linear_reg', input_label_cols=['columna_etiqueta']) AS
   SELECT ... (datos de entrenamiento)
   ```

3. **Evaluación del Modelo (`ML.EVALUATE`)**:
   Una vez que el modelo ha sido entrenado, se evalúa su rendimiento utilizando la función `ML.EVALUATE`. Esta función devuelve métricas estadísticas de calidad del modelo (como el error absoluto medio para regresión, o precisión, recall y curvas ROC para modelos de clasificación).

4. **Predicción (`ML.PREDICT`)**:
   Cuando el modelo alcanza un nivel de precisión aceptable, se implementa para realizar predicciones individuales o masivas (por lotes) sobre datos nuevos utilizando la función `ML.PREDICT`:
   ```sql
   SELECT * FROM ML.PREDICT(MODEL dataset.nombre_modelo, (SELECT ... nuevos_datos))
   ```


### Algoritmos y Modelos Soportados

**BigQuery ML** admite una amplia gama de algoritmos y tipos de modelos diseñados para abordar diferentes problemas de aprendizaje automático (tanto supervisado como no supervisado), integrados directamente dentro del motor de base de datos analítica. 

Los algoritmos y modelos soportados se dividen en las siguientes categorías principales:

#### 1. Modelos de Regresión (para predecir valores numéricos continuos)
*   **Regresión Lineal (`linear_reg`)**: El modelo más simple para estimar o proyectar valores numéricos continuos basados en una relación lineal con las variables de entrada.
*   **Redes Neuronales Profundas (`dnn_regressor`)**: Modelos basados en deep learning que permiten capturar relaciones complejas y no lineales en datos tabulares masivos.
*   **Árboles de Decisión Potenciados (`boosted_tree_regressor`)**: Algoritmo basado en **XGBoost** que es altamente efectivo para problemas estructurados y de regresión en conjuntos de datos dispersos.

#### 2. Modelos de Clasificación (para predecir categorías o etiquetas discretas)
*   **Regresión Logística (`logistic_reg`)**: Se utiliza tanto para **clasificación binaria** (predicciones de dos categorías, como fraudulento/no fraudulento) como para **clasificación multiclase** (más de dos categorías, como etiquetar un artículo en temas como política, deportes o negocios).
*   **Redes Neuronales Profundas (`dnn_classifier`)**: Clasificadores complejos que emplean múltiples capas ocultas para identificar patrones de clasificación no lineales.
*   **Árboles de Decisión Potenciados (`boosted_tree_classifier`)**: Clasificador basado en conjuntos de árboles de decisión secuenciales (XGBoost) para optimizar la precisión en datos estructurados.

#### 3. Modelos de Agrupamiento o Clustering (Aprendizaje No Supervisado)
*   **K-means (`kmeans`)**: Algoritmo utilizado para agrupar y segmentar conjuntos de datos en *clusters* basados en la similitud de sus características físicas o numéricas, sin necesidad de contar con datos previamente etiquetados.

#### 4. Sistemas de Recomendación (Filtrado Colaborativo)
*   **Factorización de Matrices (`matrix_factorization`)**: Algoritmo clásico utilizado para construir sistemas de recomendación (como sugerir películas o productos a usuarios basados en valoraciones históricas) o para tareas de segmentación y prospección de clientes.

#### 5. Importación de Modelos Externos
*   **Modelos de TensorFlow (`tensorflow`)**: BigQuery ML permite **importar modelos de TensorFlow** que hayan sido entrenados externamente para realizar predicciones directamente sobre tus datos en BigQuery mediante consultas SQL estándares.

En resumen, BigQuery ML elimina las barreras tradicionales del Machine Learning, permitiendo a los analistas de datos iterar con rapidez, formular problemas con SQL directo y mantener una estricta seguridad al evitar transferir información fuera de su almacén analítico de confianza.

:::info[*Nota complementaria*] 
Aunque puedes experimentar e iterar con rapidez con los algoritmos anteriores en BigQuery ML, si buscas optimizar el modelo de forma automática sin realizar pruebas manuales, Google Cloud ofrece de manera complementaria **AutoML Tables**, el cual limpia los datos y busca de forma automática la mejor arquitectura entre múltiples algoritmos como regresión lineal, redes profundas, árboles potenciados, AdaNet y ensambles de modelos.
:::


📊 Si quieres, podemos explorar un ejemplo de consulta para evaluar las métricas de un modelo clasificador y entender cómo interpretar su matriz de confusión directamente en SQL.

### Ejemplos SQL para entrenamiento

Para ilustrar cómo entrenar un modelo en BigQuery ML, utilizaremos el conjunto de datos públicos de **alquiler de bicicletas de Londres (`london_bicycles.cycle_hire`)**, el cual ya veníamos explorando. El objetivo en estos ejemplos será **predecir la duración de un viaje en bicicleta** en función de la estación de inicio, el día de la semana y la hora del día.

Dado que la duración es un valor numérico continuo, nos enfrentamos a un problema de **regresión**, por lo que utilizaremos el algoritmo de **Regresión Lineal (`linear_reg`)**.

A continuación, se presentan dos ejemplos: uno básico de entrenamiento y otro aplicando las **mejores prácticas** de preprocesamiento de BigQuery.



#### Ejemplo 1: Entrenamiento Básico de un Modelo

Este código de SQL estándar utiliza la sentencia `CREATE OR REPLACE MODEL` para definir y entrenar el modelo. 

```sql
CREATE OR REPLACE MODEL ch09eu.bicycle_model
OPTIONS(
  model_type='linear_reg',
  input_label_cols=['duration']
) AS
SELECT
  duration,
  start_station_name,
  CAST(EXTRACT(dayofweek FROM start_date) AS STRING) AS dayofweek,
  CAST(EXTRACT(hour FROM start_date) AS STRING) AS hourofday
FROM `bigquery-public-data.london_bicycles.cycle_hire`
WHERE duration IS NOT NULL
```

#### Explicación de los elementos clave:
*   **`CREATE OR REPLACE MODEL`**: Esta instrucción crea el objeto del modelo en tu conjunto de datos (en este caso, en el dataset `ch09eu`). Si el modelo ya existe, lo sobrescribe.
*   **`model_type`**: Especifica el tipo de algoritmo. Para predecir un número continuo, usamos regresión lineal (`linear_reg`).
*   **`input_label_cols`**: Define la columna que queremos predecir (la etiqueta o *label*). Aquí es `duration`.
*   **Casteo a `STRING`**: BigQuery ML interpreta las columnas de tipo texto (`STRING`) automáticamente como **variables categóricas**. Por lo tanto, convertimos el día de la semana (1 a 7) y la hora (0 a 23) a cadenas de texto para que el modelo no las trate como números continuos correlacionados.

---

#### Ejemplo 2: Uso de la cláusula `TRANSFORM` (Mejor Práctica)

En el ejemplo anterior, realizamos transformaciones manuales en el `SELECT`. Sin embargo, la mejor práctica en BigQuery ML es **utilizar la cláusula `TRANSFORM`**. Esto permite que el modelo "grabe" las reglas de preprocesamiento y las aplique automáticamente tanto en el entrenamiento como al momento de hacer predicciones, evitando que los clientes tengan que procesar los datos de entrada de forma manual.

En este ejemplo optimizado, agrupamos los días en *fin de semana* y *día de semana*, y clasificamos las horas del día en contenedores (*buckets*) usando la función nativa `ML.BUCKETIZE`:

```sql
CREATE OR REPLACE MODEL ch09eu.bicycle_model_bucketized
TRANSFORM(
  * EXCEPT(start_date),
  IF(EXTRACT(dayofweek FROM start_date) BETWEEN 2 and 6, 'weekday', 'weekend') AS dayofweek,
  ML.BUCKETIZE(EXTRACT(hour FROM start_date),) AS hourofday
)
OPTIONS(
  model_type='linear_reg',
  input_label_cols=['duration']
) AS
SELECT
  duration,
  start_station_name,
  start_date
FROM `bigquery-public-data.london_bicycles.cycle_hire`
WHERE duration IS NOT NULL
```

#### Explicación de las optimizaciones:
*   **`TRANSFORM`**: Recibe todas las columnas de la consulta `SELECT` excepto `start_date` (usando `EXCEPT`), y aplica transformaciones sobre la marcha.
*   **`ML.BUCKETIZE`**: Divide las 24 horas del día en rangos definidos por los límites ``. Esto agrupa la hora del día en 4 segmentos definidos (por ejemplo: madrugada, mañana, tarde y noche), ayudando al modelo lineal a aprender patrones no lineales con mayor facilidad.

---

### Cómo evaluar y predecir un modelo

Una vez que el modelo se ha entrenado con éxito, puedes interactuar con él usando otras funciones de SQL nativas de BigQuery ML:

#### 1. Evaluación del rendimiento (`ML.EVALUATE`)
Para conocer el margen de error promedio de tu modelo (como el error absoluto medio), simplemente ejecutas:
```sql
SELECT * FROM ML.EVALUATE(MODEL ch09eu.bicycle_model_bucketized)
```

#### 2. Generación de predicciones (`ML.PREDICT`)
Gracias a que usamos `TRANSFORM`, para obtener una predicción solo necesitas enviarle la fecha y hora original en formato de marca de tiempo (*timestamp*). BigQuery se encargará del resto:
```sql
SELECT * FROM ML.PREDICT(
  MODEL ch09eu.bicycle_model_bucketized,
  (SELECT 'Park Lane, Hyde Park' AS start_station_name,
          CURRENT_TIMESTAMP() AS start_date)
)
```

### Predicciones masivas

En BigQuery ML, realizar una **predicción masiva o por lotes (batch prediction)** es un proceso sumamente directo porque aprovecha el motor de consultas SQL de la plataforma. En lugar de pasar una sola fila con datos manuales, le entregas a la función `ML.PREDICT` una subconsulta o una tabla completa que contenga **miles o millones de registros**.

Dado que BigQuery separa el cómputo del almacenamiento y distribuye el procesamiento entre miles de workers de forma instantánea, puede resolver millones de predicciones en paralelo en cuestión de segundos.

A continuación te muestro cómo se vería un ejemplo estructurado en SQL para predecir la duración de todos los viajes iniciados durante un período específico de tiempo y guardar los resultados de forma automática en una nueva tabla analítica:

```sql
-- Crear o reemplazar una tabla con el resultado de las predicciones masivas
CREATE OR REPLACE TABLE ch09eu.predicciones_viajes_agosto AS
SELECT 
  predicted_duration,
  start_station_name,
  start_date
FROM ML.PREDICT(
  MODEL ch09eu.bicycle_model_bucketized,
  (
    SELECT start_station_name, start_date
    FROM `bigquery-public-data.london_bicycles.cycle_hire`
    WHERE start_date BETWEEN '2026-08-01' AND '2026-08-31'
  )
)
```

#### ¿Qué ocurre en esta predicción masiva?

1. **La consulta de origen de datos**: La subconsulta interna recopila los datos masivos que queremos evaluar (por ejemplo, todos los viajes ocurridos en agosto de 2026).

2. **El beneficio de usar `TRANSFORM`**: Como definimos un bloque `TRANSFORM` al momento de entrenar el modelo, no necesitas preprocesar manualmente tus columnas de entrada antes de predecir. BigQuery ML aplica automáticamente a toda la tabla de entrada las mismas reglas que guardó durante el entrenamiento (como categorizar en "weekday/weekend" y agrupar las horas en rangos específicos). Tú solo le entregas las columnas crudas (`start_station_name` y `start_date`).

3. **Procesamiento paralelo**: Google distribuye la carga de trabajo de predicción entre múltiples hilos de ejecución (*slots*). Así, evaluar un conjunto masivo de datos se realiza con una latencia extremadamente baja.

4. **Almacenamiento directo de resultados**: Al envolver la consulta en una sentencia `CREATE OR REPLACE TABLE`, los registros resultantes (incluyendo la nueva columna autogenerada `predicted_duration`) se materializan de inmediato en BigQuery. Esto te permite conectar la tabla resultante a dashboards interactivos de Looker o Google Data Studio para su visualización.

### Evaluación con ML.EVALUATE

La función **`ML.EVALUATE`** se utiliza en BigQuery ML para medir el rendimiento, la precisión y la calidad general de tus modelos entrenados. Dependiendo de si tu modelo resuelve un problema de **regresión**, **clasificación** o **clustering (agrupamiento)**, BigQuery ML calculará y devolverá un conjunto de métricas estadísticas específicas adaptadas al algoritmo.

Existen dos formas principales de ejecutar esta evaluación en SQL estándar:

#### 1. Evaluación con el conjunto de datos de validación automático (Default)
Cuando entrenas un modelo, BigQuery ML reserva de forma automática una porción de tus datos originales para evaluar la calidad del entrenamiento (por defecto, el **20%** en conjuntos de tamaño moderado). 

Para consultar las métricas de rendimiento calculadas sobre este conjunto de datos que el modelo ya tiene retenido, solo necesitas indicar el nombre de tu modelo:

```sql
SELECT * FROM ML.EVALUATE(MODEL ch09eu.bicycle_model_bucketized)
```

#### Métricas de salida en Regresión:
Si ejecutas esto sobre nuestro modelo lineal de duración de viajes (`bicycle_model_bucketized`), la consulta te devolverá una única fila con columnas como:
*   **`mean_absolute_error` (MAE)**: El error absoluto promedio de las predicciones (en este caso, unos 901 segundos o 15 minutos). Es la métrica más recomendada para regresiones debido a su equilibrio y resistencia ante valores atípicos (*outliers*).
*   **`mean_squared_error` (MSE)** y **`mean_squared_log_error` (MSLE)**.
*   **`median_absolute_error`**.
*   **`r2_score`**: El coeficiente de determinación, que mide la proporción de variabilidad que el modelo es capaz de explicar.

---

#### 2. Evaluación con un conjunto de datos nuevo y personalizado (Test Data)
La mejor práctica recomendada para estimar con rigurosidad cómo se comportará tu modelo tras ser desplegado en producción es evaluarlo con **datos completamente nuevos** que nunca vio durante el entrenamiento o el ajuste de hiperparámetros.

Para lograrlo, se le pasa un **segundo argumento** a la función `ML.EVALUATE` consistente en una subconsulta SQL que proporciona los registros de prueba. 

En nuestro ejemplo de bicicletas de Londres, si quisieras evaluar el rendimiento del modelo utilizando exclusivamente un mes de prueba independiente (por ejemplo, septiembre de 2026), la estructura se vería así:

```sql
SELECT * FROM ML.EVALUATE(
  MODEL ch09eu.bicycle_model_bucketized,
  (
    SELECT duration, start_station_name, start_date
    FROM `bigquery-public-data.london_bicycles.cycle_hire`
    WHERE start_date BETWEEN '2026-09-01' AND '2026-09-30'
  )
)
```

:::info[Nota]
Para que funcione, la subconsulta de prueba debe incluir tanto la columna de la etiqueta real (`duration`) como las características crudas requeridas por el modelo (`start_station_name` y `start_date`), ya que el bloque `TRANSFORM` se aplicará de forma automática sobre ellas antes de evaluar.
:::



#### 3. Evaluación para Clasificación y Clustering

La sintaxis para consultar las métricas es idéntica, pero las columnas de salida cambiarán según el tipo de modelo:

*   **Para Clasificación** (por ejemplo, el modelo `bicycle_model_longrental` que clasifica si un viaje durará más de 30 minutos):
    ```sql
    SELECT * FROM ML.EVALUATE(MODEL ch09eu.bicycle_model_longrental)
    ```
    Esta consulta te entregará las métricas típicas de un clasificador:
    *   **`precision`**: Precisión de las predicciones positivas.
    *   **`recall`**: Capacidad para identificar todos los casos positivos reales.
    *   **`accuracy`**: Exactitud global del clasificador.
    *   **`f1_score`**: Media armónica de precisión y recall.
    *   **`log_loss`**: Pérdida logarítmica (cross-entropy).
    *   **`roc_auc`**: Área bajo la curva ROC.

*   **Para Clustering / K-means** (por ejemplo, el modelo `london_station_clusters` para segmentar estaciones):
    ```sql
    SELECT * FROM ML.EVALUATE(MODEL ch09eu.london_station_clusters)
    ```
    Al no existir etiquetas reales en el aprendizaje no supervisado, la evaluación de un modelo K-means devuelve la columna **`davies_bouldin_index`**. Esta métrica te ayuda a identificar el número óptimo de clusters (un índice más bajo representa grupos más compactos y mejor delimitados).

