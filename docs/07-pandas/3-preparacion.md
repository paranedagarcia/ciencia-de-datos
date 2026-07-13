---
id: pandas-limpieza
title: "Limpieza y preparación de datos"
sidebar_label: "Limpieza"
sidebar_position: 3
description: "Proceso de depuración y confianza de datos"
---

:::info[Codigo:]
[![](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/19BgqL7U0SE7BoHutwZT_wWGOUDmHHVwB)
:::

El proceso de **limpieza y preparación de datos** en pandas es una etapa crítica que a menudo ocupa la mayor parte del tiempo en un proyecto de análisis.

## Gestión de datos faltantes
Pandas utiliza principalmente el valor centinela **`NaN`** (Not a Number) para representar datos nulos en tipos de punto flotante, aunque también emplea **`pd.NA`** para tipos de extensión como los enteros anulables (`Int64`).
*   **Detección:** Se utilizan los métodos `isna()` y `notna()` para obtener máscaras booleanas que identifican la presencia o ausencia de valores nulos.
*   **Eliminación:** El método `dropna()` permite filtrar etiquetas de eje. Puede configurarse para eliminar filas si contienen al menos un valor nulo, si todos los valores son nulos (`how='all'`), o basándose en un umbral de datos utilizables (`thresh`).
*   **Rellenado:** `fillna()` se usa para reemplazar huecos con valores constantes, diccionarios por columna o estadísticas como la **media** o la **moda**. También existen los métodos `ffill()` (relleno hacia adelante) y `bfill()` (relleno hacia atrás).
*   **Interpolación:** `interpolate()` es útil para series temporales, rellenando valores faltantes mediante métodos lineales o de otro tipo.

Para tratar valores nulos (también conocidos como faltantes o ausentes) en pandas, existen diversos métodos integrados que permiten desde su detección hasta su eliminación o reemplazo. En pandas, estos valores suelen representarse como **`NaN`** (para tipos numéricos de punto flotante), **`None`** (tipos de objeto), **`NaT`** (marcas temporales) o el centinela **`<NA>`** para tipos de datos de extensión como los enteros anulables.

A continuación se detallan los métodos más comunes:

### Detección y diagnóstico
Antes de actuar sobre los nulos, es necesario identificarlos y cuantificar su presencia:
*   **`isna()` / `isnull()`**: Devuelven una máscara booleana (True/False) indicando las posiciones donde los datos son nulos. Ambos nombres se usan de forma intercambiable.
*   **`notna()` / `notnull()`**: Es la negación de los anteriores; devuelven True para los valores que tienen datos válidos.
*   **`info()`**: Proporciona un resumen de la estructura del DataFrame, incluyendo el conteo de valores "no nulos" por cada columna, lo que ayuda a identificar rápidamente dónde faltan datos.
*   **`isna().sum()`**: Es una técnica común para obtener el número total de valores nulos por columna.

### Eliminación de datos
Si los valores nulos no son útiles para el análisis, se pueden descartar:
*   **`dropna()`**: Filtra las etiquetas de los ejes basándose en la presencia de nulos.
    *   Por defecto, elimina cualquier fila que contenga al menos un valor nulo.
    *   **`axis='columns'`**: Permite eliminar columnas completas en lugar de filas.
    *   **`how='all'`**: Solo elimina la fila o columna si todos sus valores son nulos.
    *   **`thresh=n`**: Conserva solo las filas o columnas que tengan al menos `n` valores reales (no nulos).
    *   **`subset`**: Permite especificar columnas específicas para verificar la presencia de nulos antes de eliminar la fila.

### Rellenado y reemplazo
En lugar de borrar datos, se pueden rellenar los huecos mediante diversas estrategias:
*   **`fillna()`**: Permite reemplazar los valores nulos con un valor específico, un diccionario de valores por columna o un objeto de serie.
    *   **Estadísticas**: Es común rellenar con la **media** (`mean()`), la **mediana** o la **moda** de la columna.
    *   **`method='ffill'`** (o el alias **`ffill()`**): Rellena hacia adelante, utilizando el último valor válido observado para completar los nulos siguientes.
    *   **`method='bfill'`** (o el alias **`bfill()`**): Rellena hacia atrás, utilizando el siguiente valor válido para completar los nulos anteriores.
*   **`replace()`**: Aunque es un método general para sustituir valores, es útil para convertir valores centinelas específicos (como -999) en `NaN` o viceversa.

### Métodos especializados
*   **`interpolate()`**: Útil especialmente en series temporales ordenadas; rellena los nulos realizando una interpolación (por defecto lineal) entre los valores válidos circundantes.
*   **`combine_first()`**: Permite "parchear" los datos nulos de un objeto con los valores correspondientes de otro objeto que tenga etiquetas que se solapen.
*   **`transform()` con groupby**: Permite aplicar operaciones de rellenado (como `fillna`) utilizando estadísticas calculadas específicamente por grupo.

## Transformación de datos
Este aspecto abarca el redimensionamiento, la normalización y el ajuste de los datos para su análisis.
*   **Mapeo:** El método `map()` en objetos `Series` aplica transformaciones elemento a elemento mediante funciones o diccionarios.
*   **Aplicación de funciones:** `apply()` permite invocar funciones personalizadas a lo largo de un eje (filas o columnas).
*   **Conversión de tipos:** `astype()` se emplea para transformar columnas a otros tipos de datos, como convertir cadenas a categorías para ahorrar memoria.

## Duplicados
Para eliminar duplicados en Python, especialmente cuando se trabaja con la librería **pandas**, se utilizan principalmente los métodos `drop_duplicates()` y el uso de **conjuntos (sets)** para estructuras de datos básicas.

*   **Identificación:** `duplicated()` devuelve una serie booleana que indica si cada fila es una copia exacta de una fila anterior.
*   **Eliminación:** `drop_duplicates()` filtra las filas duplicadas. Se puede especificar un subconjunto de columnas para la comprobación (`subset`) y decidir cuál instancia conservar (`keep='first'`, `'last'` o `False` para eliminar todos los duplicados).

A continuación se detallan los métodos y sus funcionalidades según las fuentes:

#### 1. El método `drop_duplicates()` en pandas
Es la herramienta principal para limpiar duplicados en `Series` y `DataFrames`.
*   **Funcionamiento básico:** Al llamarlo sin argumentos en un DataFrame, elimina las filas que son copias exactas de una fila anterior.
*   **Parámetro `subset`:** Permite especificar una columna o una lista de columnas para identificar duplicados, ignorando el resto. Por ejemplo, se puede usar para conservar solo un registro por cada categoría o ID específico.
*   **Parámetro `keep`:** Determina qué valor conservar:
    *   `'first'` (predeterminado): Mantiene la primera aparición y elimina las siguientes.
    *   `'last'`: Conserva la última aparición encontrada.
    *   `False`: Elimina todas las filas que tengan duplicados, incluyendo la primera aparición.
*   **Parámetro `inplace=True`:** Modifica el objeto original directamente en lugar de devolver una copia.

#### 2. Identificación con `duplicated()`
Este método devuelve una serie booleana donde `True` indica que una fila es un duplicado de una anterior. Es útil para inspeccionar o filtrar datos antes de eliminarlos definitivamente.

#### 3. Uso de Conjuntos (`set`)
Para colecciones de datos básicas de Python (como listas), el método más sencillo es convertir la colección en un **conjunto**.
*   Un `set` es una colección desordenada de **elementos únicos**.
*   Al pasar una lista con duplicados a la función `set()`, Python identifica y extrae solo los elementos únicos automáticamente.
*   Es ideal para obtener rápidamente valores distintos de una secuencia sin preocuparse por el orden.

#### 4. Otras técnicas y contextos
*   **SQL e ingesta de datos:** En procesos de carga (ETL), se pueden usar sentencias como `INSERT OR IGNORE` para evitar la entrada de registros duplicados en una base de datos.
*   **Duplicados adyacentes:** Si solo se desean eliminar duplicados que aparecen de forma consecutiva (común en series temporales), se puede combinar el método `shift()` con filtros de máscara booleana.
*   **Nombres de usuario únicos:** En flujos lógicos, se suele pasar una lista de nombres a minúsculas antes de compararlos con un conjunto existente para asegurar la unicidad sin distinguir mayúsculas.

```python showLineNumbers title="Eliminación básica de filas idénticas"
"""
Este programa muestra cómo cargar datos y eliminar aquellas filas que son copias 
exactas de una anterior. Por defecto, pandas conserva la primera aparición encontrada
"""
import pandas as pd

# Crear un DataFrame con filas totalmente duplicadas
data = {
    'nombre': ['Ana', 'Luis', 'Ana', 'Pedro', 'Luis'],
    'edad': [7-9]
}
df = pd.DataFrame(data)

# Eliminar duplicados manteniendo la primera aparición (comportamiento por defecto)
df_limpio = df.drop_duplicates()

print("DataFrame original:\n", df)
print("\nDataFrame sin duplicados exactos:\n", df_limpio)
```

```python showLineNumbers title="Uso del parámetro subset y control de registros con keep"
"""
En este ejemplo, se eliminan registros considerando solo una columna específica 
(como una clave o ID), ignorando si el resto de las columnas varían. Además, 
se utiliza el parámetro keep para decidir qué registro preservar:
-'first' (por defecto): Mantiene la primera aparición
-'last': Conserva la última aparición encontrada
-False: Elimina todas las filas que tengan duplicados
"""
import pandas as pd

data = {
    'id_cliente': [15-17],
    'compra': [50.5, 120.0, 75.0, 30.0, 120.0],
    'fecha': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05']
}
df = pd.DataFrame(data)

# Conservar solo la ÚLTIMA compra de cada cliente (basado en 'id_cliente')
df_ultima_compra = df.drop_duplicates(subset=['id_cliente'], keep='last')

# Eliminar cualquier cliente que tenga registros duplicados (no deja ninguna copia)
df_sin_repetidos = df.drop_duplicates(subset=['id_cliente'], keep=False)

print("Última compra por cliente:\n", df_ultima_compra)
print("\nClientes sin registros duplicados:\n", df_sin_repetidos)

```

```python showLineNumbers title="Identificación previa con duplicated() y modificación inplace"
"""
A veces es útil identificar los duplicados antes de borrarlos para realizar inspecciones o marcas. 
El método duplicated() genera una serie booleana donde True indica una repetición.
Asimismo, se puede usar inplace=True para modificar el DataFrame original sin crear una copia nueva
"""
import pandas as pd

df = pd.DataFrame({
    'A': [23-25],
    'B': [23, 25-27]
})

# 1. Crear una máscara para identificar registros duplicados en la columna 'A'
# keep=False marca todas las apariciones de un duplicado como True
mask = df.duplicated(subset=['A'], keep=False)

# 2. Usar la máscara para realizar una acción (ej. poner a 0 otra columna)
df.loc[mask, 'B'] = 0

# 3. Eliminar los duplicados definitivamente modificando el objeto original
df.drop_duplicates(subset=['A'], inplace=True)

print("DataFrame procesado e in-place:\n", df)
```
```python showLineNumbers title="Reinicio del índice al eliminar duplicados"
"""
Cuando se eliminan filas, el índice original se conserva salteando 
los números de las filas borradas. 
Para obtener un nuevo índice secuencial, se utiliza ignore_index=True
"""
import pandas as pd

df = pd.DataFrame({'val': [23-25]})

# Eliminar duplicados y re-indexar automáticamente de 0 a N
df_nuevo_index = df.drop_duplicates(ignore_index=True)

print(df_nuevo_index)
```
***
### Reemplazo de valores
Mientras que `fillna` es para nulos, **`replace()`** ofrece una forma más flexible de sustituir valores específicos.
*   Permite mapear uno o varios valores antiguos a nuevos mediante listas o diccionarios.
*   Soporta el uso de **expresiones regulares** para reemplazos parciales si se activa el parámetro `regex=True`.

### Índices
Los objetos `Index` y `MultiIndex` (para datos jerárquicos) organizan las etiquetas de los ejes.
*   **Configuración:** `set_index()` convierte una o más columnas en el índice de fila.
*   **Reinicio:** `reset_index()` mueve el índice de vuelta a las columnas y genera un nuevo índice entero por defecto.
*   **Reindexación:** `reindex()` crea un nuevo objeto con los valores reordenados para que coincidan con un nuevo índice.

### Discretización
Consiste en separar datos continuos en "contenedores" o intervalos para el análisis.
*   **`pd.cut()`**: Divide los datos en contenedores basados en bordes explícitos o en un número fijo de intervalos de igual longitud.
*   **`pd.qcut()`**: Discretiza basándose en cuantiles de muestra, lo que resulta en contenedores con aproximadamente el mismo número de puntos de datos.

### Valores atípicos (Outliers)
Su detección y filtrado se realiza principalmente mediante operaciones de arrays.
*   Se pueden identificar analizando estadísticas de resumen (como con `describe()`) o aplicando filtros booleanos para encontrar valores que excedan ciertos límites (por ejemplo, 3 veces la desviación estándar).
*   Para limitarlos, se puede usar el método `clip(lower, upper)`, que trunca los valores fuera del rango especificado.

### Permutación y muestreo aleatorio
*   **Permutación:** `np.random.permutation()` genera un nuevo orden aleatorio de los índices, que puede aplicarse al dataframe usando `iloc` o `take()`.
*   **Muestreo:** El método **`sample()`** extrae una cantidad fija (`n`) o una fracción (`frac`) de filas o columnas al azar, con o sin reemplazo.

## Variables dummy o indicadoras
Es el proceso de convertir una variable categórica en una matriz de columnas (codificación *one-hot*).
*   **`pd.get_dummies()`**: Crea un dataframe donde cada columna representa una categoría distinta con valores 1 o 0.
*   **Múltiple pertenencia:** Si una celda contiene varias categorías (ej. "Acción|Drama"), se utiliza **`str.get_dummies()`** especificando el delimitador.

Para crear variables dummy (también conocidas como variables indicadoras o codificación *one-hot*) a partir de categorías en Python, la herramienta principal es la función **`pd.get_dummies`** de la librería pandas. Este proceso consiste en convertir una columna con valores de cadena repetidos en varias columnas numéricas (una por cada categoría), donde un **1** indica la presencia de esa categoría y un **0** su ausencia.

A continuación se detallan las formas de aplicarlo según las fuentes:

#### Uso básico de `pd.get_dummies()`
Puedes pasarle una `Series` o un `DataFrame` completo. Si pasas un dataframe, pandas identificará automáticamente las columnas de tipo cadena o categóricas para transformarlas.

*   **Ejemplo simple:** Si tienes una columna "key" con valores "a", "b" y "c", `pd.get_dummies(df["key"])` generará tres columnas nuevas llamadas "a", "b" y "c" con valores binarios.
*   **Con prefijos:** Para mantener la claridad, es recomendable usar el argumento `prefix` para añadir un texto antes del nombre de la categoría en las nuevas columnas.
    ```python
    # Ejemplo: crear dummies con prefijo
    dummies = pd.get_dummies(df["key"], prefix="key")
    df_con_dummies = df[["otro_dato"]].join(dummies)
    ```

#### Tratamiento de pertenencia múltiple (`str.get_dummies`)
Si una sola celda contiene varias categorías separadas por un delimitador (por ejemplo, géneros de películas como "Acción|Drama"), se debe utilizar el método de serie **`str.get_dummies()`** especificando el separador.
*   **Ejemplo:** `movies["genres"].str.get_dummies("|")` creará una columna para cada género individual, marcando con 1 todas las categorías que aparezcan en esa celda específica.

#### Casos especiales y aplicaciones
*   **Variables discretizadas:** Es una técnica común combinar la creación de dummies con la función `pd.cut()` para convertir datos numéricos continuos en rangos categóricos y luego en columnas indicadoras.
*   **Preparación para modelos:** Este proceso es fundamental en el **aprendizaje automático**, ya que muchos algoritmos no admiten datos de texto y requieren que todas las entradas sean numéricas.
*   **Uso de Patsy:** Para modelos estadísticos complejos, se puede usar la librería **Patsy** (integrada en `statsmodels`), que gestiona automáticamente la creación de variables indicadoras dentro de una fórmula, eliminando usualmente un nivel para evitar problemas de colinealidad (intercepto).

#### Resumen de parámetros útiles en `pd.get_dummies`:
*   **`data`**: El objeto (Series o DataFrame) a convertir.
*   **`prefix`**: Cadena para añadir al inicio de los nombres de las nuevas columnas.
*   **`dummy_na`**: Booleano para añadir una columna que indique si el valor original era nulo (NaN).
*   **`drop_first`**: Booleano para eliminar la primera categoría, útil en modelos estadísticos para evitar la redundancia.


## Ejercicio

:::info
**Descarga el archivo**: [Plan de compras 2025.xlsx]

Plan de compras 2025. MINVU
:::

