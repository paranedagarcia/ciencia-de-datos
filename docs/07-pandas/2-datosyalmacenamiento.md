---
id: pandas-archivos
title: "Manejo de datos en Pandas"
sidebar_label: "Datos en pandas"
sidebar_position: 2
---

La manipulación de datos en **pandas** se centra en sus dos estructuras principales: **Series** (unidimensional) y el **DataFrame** (bidimensional, similar a una tabla SQL o una hoja de Excel). El detalle de el manejo de diferentes fuentes de datos con ejemplos:.

### Archivos CSV (Valores Separados por Comas)
Es el formato más común para el intercambio de datos tabulares entre sistemas informáticos.

*   **Lectura:** Se utiliza `pd.read_csv()`. Admite parámetros críticos como `sep` (delimitador), `header` (fila de encabezados), `names` (nombres de columna personalizados) e `index_col` (columna a usar como índice).
*   **Ejemplo:**
    ```python showLineNumbers
    import pandas as pd
    # Leer especificando nombres de columnas y el índice
    df = pd.read_csv("archivo.csv", names=['A', 'B', 'C'], index_col='A')
    # Leer solo una parte del archivo (chunks) para archivos grandes
    df_chunk = pd.read_csv("grande.csv", nrows=5)
    ```
*   **Escritura:** `df.to_csv("salida.csv", index=False)` permite guardar los datos sin incluir el índice de filas.

### Archivos de Microsoft Excel
Pandas utiliza librerías internas como `openpyxl` (para .xlsx) o `xlrd` (para .xls) para gestionar estos archivos.

*   **Lectura:** `pd.read_excel()` permite cargar una hoja específica mediante `sheet_name`.

*   **Escritura:** `df.to_excel()` requiere a menudo el uso de `pd.ExcelWriter` si se desean guardar múltiples hojas en un solo archivo.
*   **Ejemplo:**
```python showLineNumbers
import pandas as pd

# Lee la primera hoja esto es por default
df = pd.read_excel('data.xlsx')

# Lee una hoja determinada, por su nombre
df_sales = pd.read_excel('data.xlsx', sheet_name='Sales')

# Lee una hoja específica por su índice (0-indexed)
df_costs = pd.read_excel('data.xlsx', sheet_name=1)

# Carga multiles hojas a la vez (obtiene un diccionario de dataframes)
all_sheets = pd.read_excel('data.xlsx', sheet_name=['Sales', 'Costs'])

# Leer una hoja específica por nombre o índice
df = pd.read_excel("datos.xlsx", sheet_name="Hoja1")

# Guardar un dataframe a un archivo excel
df.to_excel('output.xlsx', index=False)  # index=False evita escribir numeros de filas


# Escribir varias hojas
# guarda multiples dataframes en un archivo excel
with pd.ExcelWriter("reporte.xlsx") as writer:
    df1.to_excel(writer, sheet_name="Enero", index=False)
    df2.to_excel(writer, sheet_name="Febrero", index=False)
```
Ajustes comunes duate la importación:
- **Skip rows:** Usa `skiprows=2` si los actuales datos comienzan en algunas determinadas filas abajo.

- **Select columns:** Utiliza `usecols="A:C"` o `usecols=["Name", "Date"]` para cargar solo los datos necesarios.

- **Handle missing data:** Utiliza `na_values=['NA', 'Missing']` para indicar cómo debe tratar a las celdas en blanco.

**Acciones comparadas Excel / Pandas**

**Filtrar filas**: 

```df[df['Status'] == 'Active']```

**VLOOKUP / XLOOKUP**: 

```pd.merge(df1, df2, on='ID', how='left')```

**Pivot Table:** 

```df.pivot_table(values='Sales', index='Region', columns='Year', aggfunc='sum')```

**Remove Duplicates:**

```df.drop_duplicates(subset=['Email'])```

**Text to Columns:**

```df['Full Name'].str.split(' ', expand=True)```


### Archivos de Texto (Planos o Delimitados)
Para archivos `.txt` donde el delimitador no es necesariamente una coma, se emplea `pd.read_table()` o `read_csv()` especificando el separador.

*   **Uso de Regex:** Si los espacios son variables, se puede usar una expresión regular como `sep='\s+'`.

*   **Ejemplo:**
    ```python showLineNumbers
    # Leer un archivo separado por tabuladores
    df = pd.read_table("datos.txt", sep="\t")
    # Omitir filas innecesarias (encabezados o comentarios)
    df = pd.read_csv("logs.txt", skiprows=)
    ```

### Datos Binarios (Pickle, HDF5, Parquet)
Los formatos binarios son más eficientes para el almacenamiento masivo y mantienen los tipos de datos.

*   **Pickle:** Es el formato nativo de Python para serialización rápida de objetos, aunque se recomienda solo para almacenamiento a corto plazo.

*   **HDF5:** Ideal para grandes cantidades de datos científicos; permite compresión y acceso a fragmentos sin cargar todo el archivo en memoria.

*   **Ejemplo:**
    ```python showLineNumbers
    # Guardar y cargar en formato Pickle
    df.to_pickle("modelo.pkl")
    df_recargado = pd.read_pickle("modelo.pkl")

    # Usar HDF5 con una estructura similar a un diccionario
    store = pd.HDFStore("datos.h5")
    store['dataset1'] = df
    ```

### Interacción con API Web (JSON)
La mayoría de las API web devuelven datos en formato **JSON**.

*   **Proceso:** Normalmente se usa la librería `requests` para obtener los datos y luego `pd.json_normalize()` para aplanar estructuras anidadas.

*   **Ejemplo:**
    ```python showLineNumbers
    import requests
    response = requests.get("https://api.datos.com/v1/data")
    data = response.json()
    # Convertir JSON anidado en un DataFrame tabular
    df = pd.json_normalize(data, record_path=['resultados'], meta=['id', 'nombre'])
    ```

### Bases de Datos (SQL)
Pandas puede interactuar con bases de datos relacionales mediante `sqlalchemy` o conectores específicos como `sqlite3`.

*   **Funciones:** `pd.read_sql()` para consultas generales y `df.to_sql()` para cargar datos en una tabla.
*   **Ejemplo:**
    ```python showLineNumbers
    import sqlite3
    con = sqlite3.connect("mi_base.db")
    # Leer el resultado de una consulta SQL
    df = pd.read_sql("SELECT * FROM usuarios WHERE edad > 18", con)
    # Escribir un DataFrame en una tabla nueva o existente
    df.to_sql("clientes", con, if_exists="replace")
    ```

**Nota sobre datos no estructurados:** Para archivos como XML o tablas dentro de páginas HTML, pandas ofrece `pd.read_xml()` y `pd.read_html()` respectivamente, lo que facilita el **web scraping** de datos tabulares directamente desde un navegador.

## PostreSQL

Para conectar **pandas** a una base de datos **PostgreSQL** y cargar datos, se utiliza generalmente la librería **SQLAlchemy** como interfaz unificada y un controlador específico como **psycopg2**.

#### Pasos principales para la conexión

1.  **Instalación de dependencias:** Es necesario tener instaladas las librerías `sqlalchemy` y `psycopg2` (el adaptador de base de datos para PostgreSQL).

2.  **Creación del motor (Engine):** Se utiliza la función `create_engine()` de SQLAlchemy pasando una cadena de conexión (URI) con el formato: `postgresql://usuario:contraseña@host:puerto/nombre_base_datos`.

3.  **Lectura de datos:** Se emplea la función `pd.read_sql()`, la cual acepta una consulta SQL o un nombre de tabla y el objeto de conexión.

#### Ejemplo

El siguiente ejemplo implementa el uso de `with` (como **gestor de contexto** para asegurar que la conexión se cierre automáticamente) y un bloque `try-except` para el manejo de errores:

```python showLineNumbers
import pandas as pd
from sqlalchemy import create_engine

# 1. Definir los parámetros de conexión
# Formato: postgresql://usuario:password@host:puerto/base_de_datos
conn_uri = "postgresql://postgres:mi_password@localhost:5432/mi_base_datos"

try:
    # 2. Crear el motor de conexión de SQLAlchemy
    engine = create_engine(conn_uri)
    
    # 3. Establecer la conexión usando 'with' para garantizar el cierre automático
    with engine.connect() as connection:
        query = "SELECT * FROM ventas WHERE total > 100"
        
        # 4. Cargar los datos directamente a un DataFrame
        df = pd.read_sql(query, connection)
    
    # Mostrar el resultado si la operación fue exitosa
    if not df.empty:
        print("Datos cargados exitosamente:")
        print(df.head())
    else:
        print("La consulta no devolvió resultados.")

except Exception as e:
    # Capturar cualquier error de conexión o sintaxis SQL
    print(f"Ocurrió un error al interactuar con la base de datos: {e}")
```

#### Consideraciones importantes

*   **Context Manager (`with`):** El uso del bloque `with` es una buena práctica porque gestiona la limpieza de recursos de forma automática, cerrando la conexión incluso si ocurre una excepción durante la ejecución.
*   **Manejo de errores:** El bloque `try-except` es vital para capturar problemas comunes como credenciales incorrectas, base de datos fuera de línea o tablas inexistentes.
*   **Alternativa directa:** Si se tiene **SQLAlchemy** instalado, pandas permite pasar la cadena de conexión (URI) directamente a `read_sql()` sin abrir explícitamente la conexión con `with`, aunque esto ofrece menos control sobre el ciclo de vida de la conexión.


## Parquet sobre csv

El formato **Parquet** ofrece diversas ventajas técnicas y de rendimiento sobre el **CSV**, especialmente cuando se trabaja con grandes volúmenes de datos y sistemas distribuidos. A continuación se detallan sus beneficios principales:

#### 1. Almacenamiento Columnar y Eficiencia en Consultas
A diferencia del CSV, que es un formato de texto orientado a filas, Parquet es un formato **binario orientado a columnas**.
*   **Selección selectiva de datos:** Al estar organizado por columnas, el sistema solo recupera los datos de las columnas requeridas por una consulta, en lugar de leer filas completas y descartar lo que no necesita. Esto reduce drásticamente el tiempo de respuesta en análisis de Big Data.
*   **Serialización eficiente:** Proporciona una serialización columnar que optimiza tanto el almacenamiento como el rendimiento de lectura y escritura.

#### 2. Compresión y Ahorro de Espacio
*   **Reducción de volumen:** Parquet está diseñado para soportar algoritmos de **compresión** (como *snappy*, *gzip* o *lzo*), lo que permite reducir significativamente el tamaño de los archivos en disco en comparación con los archivos CSV.
*   **Menor E/S de red:** La compresión reduce el volumen de datos que debe transmitirse a través de una red durante las operaciones de procesamiento, lo que disminuye la latencia.

#### 3. Soporte de Esquemas y Metadatos
*   **Tipado de datos:** A diferencia del CSV, donde pandas debe realizar una "inferencia de tipos" al leer el archivo (lo cual es costoso y propenso a errores), Parquet almacena el **esquema y los tipos de datos** directamente en el archivo.
*   **Estructuras complejas:** Soporta esquemas anidados, de forma similar a JSON, lo que permite representar datos más complejos de manera estructurada.

#### 4. Particionamiento de Datos
*   **Consultas aceleradas:** Parquet permite el **particionamiento**, que consiste en dividir el conjunto de datos en divisiones lógicas (como por año o mes) representadas mediante estructuras de carpetas.
*   **Filtrado eficiente:** Cuando se realiza una consulta con un filtro, el sistema puede leer únicamente la partición correspondiente y omitir el resto del conjunto de datos, mejorando considerablemente el rendimiento.

#### 5. Optimización para Entornos Distribuidos
*   **Interoperabilidad:** Es un formato estándar utilizado por herramientas de alto rendimiento como **Apache Spark** y **Hadoop**.
*   **Sistemas de archivos en la nube:** Está altamente optimizado para el almacenamiento en sistemas como Amazon S3 o HDFS, facilitando el intercambio de datos entre sistemas distribuidos sin pérdida de información.