---
id: streamlit-dev
title: "Streamlit"
sidebar_label: "💻 Desarrollo en Streamlit"
sidebar_position: 3
description: "Desarrollo de aplicaciones"
slug: /streamlit-dev
---

Las aplicaciones creadas con Streamlit no son muy  flexibles, como otras, sin embargo, tienen la virtud de ser muy fáciles de construir en comparación, justamente por esa estructura predefinida.
<center>
<figure> 
![png](img/interface.webp)
<figcaption>Anatomia de una interface de aplicación Streamlit.</figcaption>
</figure>
</center>

## Creación de una aplicación

Para crear una aplicación de Streamlit que cargue archivos, muestre indicadores clave de rendimiento (KPIs) y genere gráficos interactivos con **Altair**, puedes seguir este tutorial paso a paso basado en las mejores prácticas de desarrollo y organización de archivos.

#### Paso 1: Preparación e Importación de Librerías
Lo primero es crear un archivo Python (por ejemplo, `dashboard.py`) e importar los módulos necesarios: **Streamlit** para la interfaz, **Pandas** para el manejo de datos y **Altair** para las visualizaciones estadísticas.

```python showLineNumbers showLineNumbers
import streamlit as st
import pandas as pd
import altair as alt
```

#### Paso 2: Configuración de la Página y Título
Configura el diseño de la aplicación para que utilice todo el ancho de la pantalla, lo cual es ideal para tableros con múltiples gráficos. Luego, añade un título descriptivo.

```python showLineNumbers showLineNumbers
st.set_page_config(
    page_title="Plan de Compras",
    layout="wide"
)

st.title("📊 Tablero de Análisis Simple")
```

#### Paso 3: Carga de Archivos
Utiliza el comando **`st.file_uploader`** para permitir que el usuario suba su propio dataset en formato CSV. Es fundamental envolver el resto del código en una condición `if` para asegurar que la aplicación solo intente procesar los datos una vez que el archivo ha sido cargado.

```python showLineNumbers showLineNumbers
uploaded_file = st.file_uploader("Sube tu archivo CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("¡Archivo cargado con éxito!")
```

#### Paso 4: Visualización de KPIs (Card Metrics)
Para mostrar totales generales de forma atractiva, utiliza **`st.columns`** para organizar los widgets horizontalmente y **`st.metric`** para las tarjetas de datos. Las métricas son ideales para resaltar números importantes como ventas totales o conteos de registros.

```python showLineNumbers showLineNumbers
# Ejemplo calculando métricas basadas en el DataFrame
revenue = 12400
users=1024
uptime=99.9

col1, col2, col3 = st.columns(3)
col1.metric("Revenue", revenue, "+8%")
col2.metric("Users", users, "+12%")
col3.metric("Uptime", uptime, "+0.1%")
```
<center>
<figure>
![](img/st.metricas.png)
<figcaption></figcaption>
</figure>
</center>

#### Paso 5: Creación de 3 Gráficos con Altair
Altair utiliza un enfoque **declarativo** donde defines las relaciones entre las columnas de tus datos. Para mostrarlos en Streamlit, usa el comando **`st.altair_chart`** con el parámetro `use_container_width=True` para que se ajusten al diseño.

1.  **Gráfico de Barras:** Útil para comparar categorías usando `mark_bar()`.
2.  **Gráfico de Líneas:** Ideal para ver tendencias temporales con `mark_line()` o `mark_point()`.
3.  **Gráfico de Áreas o Dispersión:** Puedes usar `mark_area()` para totales acumulados o `mark_circle()` para correlaciones.

```python showLineNumbers showLineNumbers
st.subheader("Visualizaciones Estadísticas")

# Gráfico 1: Barras
chart1 = alt.Chart(df).mark_bar().encode(
    x=df.columns, y=df.columns, color=df.columns
).interactive()
st.altair_chart(chart1, use_container_width=True)

# Gráfico 2: Líneas
chart2 = alt.Chart(df).mark_line().encode(
    x=df.columns, y=df.columns
).interactive()
st.altair_chart(chart2, use_container_width=True)

# Gráfico 3: Dispersión
chart3 = alt.Chart(df).mark_circle().encode(
    x=df.columns, y=df.columns, size=df.columns, tooltip=list(df.columns)
).interactive()
st.altair_chart(chart3, use_container_width=True)
```

#### Paso 6: Ejecución de la Aplicación
Finalmente, guarda el archivo y ejecútalo desde tu terminal usando el comando **`streamlit run dashboard.py`**. Esto abrirá automáticamente una pestaña en tu navegador local donde podrás interactuar con tu nueva aplicación.

## Añadir filtros interactivos

Para añadir **filtros interactivos** a tus gráficos en Streamlit, debes combinar el uso de **widgets de entrada** con la manipulación de datos (normalmente a través de la librería Pandas) antes de renderizar la visualización.

A continuación, se detalla el proceso para lograr esta interactividad:

#### 1. Seleccionar el Widget de Filtrado
Dependiendo de qué tipo de datos quieras filtrar, puedes elegir entre varios widgets nativos de Streamlit:
*   **`st.selectbox()`**: Ideal para que el usuario elija una sola opción de una lista.
*   **`st.multiselect()`**: Permite seleccionar múltiples valores para una misma categoría.
*   **`st.slider()`** o **`st.select_slider()`**: Útiles para filtrar rangos numéricos o niveles ordenados (como la granularidad temporal).
*   **`st.radio()`**: Para elegir una opción entre un grupo pequeño y visible.

#### 2. Capturar la Selección y Filtrar el DataFrame
Streamlit sigue un modelo de ejecución en el que el script se vuelve a ejecutar de arriba abajo cada vez que un usuario interactúa con un widget. El valor seleccionado por el usuario se guarda en una variable que luego utilizas para filtrar tus datos con Pandas.

**Ejemplo lógico:**
1.  **Widget:** `especie_seleccionada = st.selectbox("Elige especie", ["Adelie", "Gentoo"])`.
2.  **Filtro:** `df_filtrado = df[df["especie"] == especie_seleccionada]`.
3.  **Gráfico:** `st.altair_chart(alt.Chart(df_filtrado)...)`.

#### 3. Organización en la Barra Lateral (`st.sidebar`)
Para mantener el área principal despejada, es una práctica recomendada colocar los filtros en la barra lateral. Puedes hacerlo simplemente anteponiendo `.sidebar` al comando del widget:
```python showLineNumbers showLineNumbers
# Ejemplo de filtro en la barra lateral
seleccion = st.sidebar.multiselect("Filtrar por categoría", df['categoria'].unique())
if seleccion:
    df = df[df['categoria'].isin(seleccion)]
```

#### 4. Interactividad Nativa de las Librerías
Además de los filtros manuales que tú crees, recuerda que ciertas librerías ya ofrecen interactividad incorporada:
*   **Plotly:** Permite hacer zoom, desplazar el gráfico y ver información al pasar el cursor de forma automática.
*   **Altair:** Puedes añadir interactividad (como zoom y desplazamiento) simplemente agregando el método `.interactive()` al final de tu objeto de gráfico.
*   **Drill-down:** Existen componentes de la comunidad como `streamlit-plotly-events` que permiten capturar clics directamente en los elementos del gráfico para filtrar otros datos.

#### 5. Caching para Optimizar
Si el filtrado requiere procesar datasets muy grandes, usa el decorador **`@st.cache_data`** para cargar los datos originales. Esto asegura que la aplicación solo filtre el dataframe en memoria en lugar de volver a leer el archivo completo del disco en cada cambio de filtro, mejorando drásticamente el rendimiento.

## Añadir varios filtros

Para combinar varios filtros en una misma vista de Streamlit, el enfoque principal consiste en capturar los valores de múltiples **widgets de entrada** y aplicarlos secuencialmente para manipular un DataFrame de Pandas antes de renderizar los gráficos.

A continuación, se detallan algunas de las estrategias recomendadas:

#### 1. Organización en la Interfaz
Para no saturar el área principal de visualización, los filtros suelen organizarse de dos maneras:
*   **Barra lateral (`st.sidebar`):** Permite colocar todos los controles a la izquierda, dejando el espacio central para las métricas y gráficos.

*   **Columnas (`st.columns`):** Útil para colocar varios selectores de forma horizontal en la parte superior del dashboard, lo que ahorra espacio vertical.

#### 2. Filtros Interdependientes (Filtros Inteligentes)
Si deseas que la selección en un filtro (por ejemplo, "Categoría") limite automáticamente las opciones disponibles en otro (por ejemplo, "Producto"), debes seguir un proceso de **filtrado secuencial**. En lugar de obtener todos los valores únicos del dataset original, cada widget posterior debe extraer sus opciones de un DataFrame que ya ha sido filtrado por los widgets anteriores.

#### 3. Aplicación Lógica con Pandas
Una vez capturados los valores de los widgets (almacenados normalmente en variables o un diccionario), se utiliza la **indexación booleana** de Pandas para obtener la porción de datos deseada. Por ejemplo, puedes iterar sobre un diccionario de filtros y aplicar la función `.isin()` para incluir solo las filas que coincidan con las selecciones del usuario.

#### 4. Optimización con Formularios y Caching
*   **Uso de `st.form`:** Cuando se tienen muchos filtros, cada interacción del usuario provocaría un reinicio completo del script. Al envolver los filtros en un formulario, el usuario puede ajustar todas sus opciones y aplicarlas de una sola vez al hacer clic en el botón de envío (`st.form_submit_button`), lo que mejora la experiencia de uso.

*   **Caching:** Es esencial proteger la carga de los datos pesados con el decorador **`@st.cache_data`**. Esto garantiza que el filtrado múltiple se realice sobre el objeto en memoria y no requiera leer el archivo original desde el disco en cada cambio.

#### Ejemplo de flujo lógico:
1.  Se cargan los datos y se guardan en el **estado de sesión** o caché.
2.  El usuario selecciona opciones en un `st.multiselect` y define un rango en un `st.date_input`.
3.  El script calcula un nuevo DataFrame (`main_df`) aplicando todas las condiciones booleanas simultáneamente.
4.  Los widgets de salida, como **`st.metric`** y **`st.plotly_chart`**, se actualizan automáticamente para mostrar los resultados del nuevo DataFrame filtrado.

## Secrets

Para utilizar **`st.secrets`** con el fin de conectar de forma segura a una base de datos, debes seguir un proceso que implica la creación de un archivo de configuración local y el uso de un objeto similar a un diccionario en tu código Python.

Aquí tienes los pasos detallados:

#### Configuración local (`secrets.toml`)
Para el desarrollo en tu máquina local, debes crear un archivo donde se almacenarán las credenciales sin exponerlas en el código principal.

El archivo global secrets de estar en:

- ~/.streamlit/secrets.toml for **macOS/Linux**
- %userprofile%/.streamlit/secrets.toml for **Windows**:

1.  En la carpeta raíz de tu proyecto, crea un directorio oculto llamado **`.streamlit`**.
2.  Dentro de esa carpeta, crea un archivo llamado **`secrets.toml`**.
3.  Define las credenciales: Escribe tus datos sensibles siguiendo el formato TOML (Tom's Obvious Minimal Language), que utiliza pares de clave-valor y permite organizar la información en secciones mediante corchetes.

- Ejemplo de formato simple: api_key = "tu_clave_aqui".

Ejemplo con secciones:
Este formato se mapea internamente a un diccionario anidado en Python

**Ejemplos de formato:**
*   **Para una cadena de conexión general (ej. PostgreSQL):**
    ```toml title="secrets.toml"
    [config]
    connection_string = "postgresql://usuario:password@localhost:5432/nombre_db"
    ```
*   **Para conectar a un servicio snowflake**
    ```toml title="secrets.toml"
    [snowflake]
    user = "mi_usuario"
    password = "mi_password"
    account = "identificador_de_cuenta"
    warehouse = "COMPUTE_WH"

    api_key = "ejemplo de api key"
    ```
:::warning[Seguridad]
Seguridad y .gitignore: Es una práctica fundamental no incluir nunca el archivo secrets.toml en tu sistema de control de versiones (como Git). Debes añadir la ruta `.streamlit/` a tu archivo `.gitignore` para evitar que las credenciales se publiquen accidentalmente en repositorios públicos como GitHub.
:::

#### Acceso desde el código Python
Streamlit carga automáticamente el contenido de este archivo en el objeto **`st.secrets`**. Puedes acceder a los datos de la siguiente manera:

*   **Acceso directo:** `db_url = st.secrets["config"]["connection_string"]`.
*   **Paso de parámetros en bloque:** Para conectores que aceptan diccionarios (como Snowflake o PostgreSQL con `psycopg2`), puedes usar el operador `**` para pasar todas las credenciales de una sección a la vez:
    ```python
    import snowflake.connector
    import streamlit as st

    # Se desempaquetan todas las claves de la sección [snowflake]
    conn = snowflake.connector.connect(**st.secrets["snowflake"])
    ```

#### Seguridad y Despliegue
*   **Archivo `.gitignore`:** Es fundamental **no subir nunca el archivo `secrets.toml` a un repositorio público** (como GitHub). Debes añadir la carpeta `.streamlit/` a tu archivo `.gitignore` para evitar filtraciones de credenciales.

*   **En la nube (Streamlit Community Cloud):** Una vez desplegada tu aplicación, ve a la configuración del app (**Settings > Secrets**) y pega allí el contenido de tu archivo TOML. Streamlit los cifrará y los servirá de forma segura en tiempo de ejecución.

#### Recomendación de rendimiento
Dado que Streamlit ejecuta el script de arriba abajo en cada interacción, se recomienda envolver la creación de la conexión en una función decorada con **`@st.cache_resource`**. Esto garantiza que la conexión a la base de datos se inicialice solo una vez y se comparta entre todas las sesiones, mejorando drásticamente la velocidad de la aplicación.


## Bases de datos

Conectar una aplicación de Streamlit a una base de datos implica configurar las credenciales de forma segura, establecer la conexión utilizando la librería adecuada y optimizar el rendimiento mediante el uso de funciones de caché.

A continuación, se detallan los pasos y las mejores prácticas para realizar esta integración:

#### Gestión de Credenciales (Secrets Management)
Nunca debes escribir contraseñas o claves de API directamente en el código de tu aplicación. Streamlit utiliza un sistema de gestión de secretos para manejar información sensible:
*   **Localmente:** Crea una carpeta llamada `.streamlit` en el directorio raíz de tu proyecto y dentro de ella un archivo `secrets.toml`.

*   **En la nube (Community Cloud):** Configura los secretos en el panel de control de la aplicación bajo la pestaña "Secrets".

*   **Acceso en el código:** Puedes acceder a estos valores usando `st.secrets["nombre_del_secreto"]`.

#### Conexión a Bases de Datos Relacionales (SQL)
Para bases de datos como PostgreSQL, Snowflake o BigQuery, el proceso es similar: se define una función que crea el objeto de conexión y se decora para que no se ejecute en cada recarga de la página.

*   **Snowflake:** Requiere la librería `snowflake-connector-python`. Se recomienda inicializar la conexión y cachearla con `@st.cache_resource` para que persista entre sesiones de usuario. También existe un método más reciente llamado `st.experimental_connection`.

*   **Google BigQuery:** Necesitas una cuenta de servicio de Google Cloud y sus credenciales en formato JSON (que deben convertirse a TOML para el archivo de secretos). Utiliza `@st.cache_resource` para el cliente de BigQuery.

*   **PostgreSQL:** Se suele utilizar `psycopg2` o `SQLAlchemy`. Al igual que con las anteriores, la conexión debe mantenerse en un "pool" compartido mediante `@st.cache_resource` para que sea eficiente entre múltiples usuarios.

Ejemplo de conexión:
```toml title=".streamlit/secrets.toml"
# .streamlit/secrets.toml
[postgres]
host = "localhost"
port = 5432
database = "tu_base_de_datos"
user = "tu_usuario"
password = "tu_password"
```
En tu script principal, utiliza el decorador `@st.cache_resource` para inicializar la conexión. Esto es crucial porque permite que la conexión se cree una sola vez y se comparta entre todas las sesiones, mejorando el rendimiento y evitando saturar el servidor de base de datos.

```python showLineNumbers title="app.py"
import streamlit as st
import psycopg2

# 1. Función para inicializar la conexión utilizando caché
# Se utiliza **st.secrets para desempaquetar el diccionario de credenciales directamente
@st.cache_resource
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

conn = init_connection()

# 2. Función para ejecutar una consulta
# El uso de 'with conn.cursor() as cur' garantiza que el cursor se cierre automáticamente [7]
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

st.title("Conexión Segura a PostgreSQL")

# Ejecutar una consulta de prueba
try:
    rows = run_query("SELECT * FROM mi_tabla LIMIT 10;")
    
    # Mostrar los resultados
    for row in rows:
        st.write(f"Registro: {row}")
except Exception as e:
    st.error(f"Error al conectar o consultar la base de datos: {e}"
```
:::info
**Despliegue en la nube:** Si despliegas en algún servicio de la nube, deberás copiar el contenido del archivo TOML en la configuración de Settings > Secrets del panel de control de tu aplicación.

**Gestión de Cursors:** Se recomienda usar context managers (with conn.cursor() as cur) para asegurar que los recursos de memoria se liberen correctamente tras cada consulta.
:::

#### Conexión a Bases de Datos No Relacionales (NoSQL)
*   **MongoDB:** Permite almacenar datos no estructurados como documentos JSON. Se utiliza la librería `pymongo` y se establece un cliente cacheado para evitar reconexiones costosas.

#### Optimización y Buenas Prácticas
*   **Caché de la conexión:** Usa **`@st.cache_resource`** para el objeto de conexión (base de datos o modelos ML), ya que estos no son datos en sí, sino recursos compartidos.

*   **Caché de los resultados:** Usa **`@st.cache_data`** para las funciones que ejecutan consultas SQL (`SELECT`), guardando los resultados en memoria para mejorar la velocidad y reducir costos de computación.

*   **Seguridad:** Utiliza siempre **parametrización** en tus consultas SQL (evita concatenar strings directamente con las entradas del usuario) para prevenir ataques de inyección SQL.

*   **Limpieza de recursos:** Puedes usar el módulo nativo de Python `atexit` para registrar funciones que cierren automáticamente todas las conexiones a la base de datos cuando el servidor de Streamlit se apague.

#### Ejemplo de flujo lógico (Snowflake):
1.  Defines las credenciales en `secrets.toml`.
2.  Creas una función `init_connection` decorada con `@st.cache_resource` que devuelva `snowflake.connector.connect(...)`.
3.  Creas una función `run_query` decorada con `@st.cache_data` que reciba la conexión y el SQL, y devuelva un DataFrame de Pandas.
4.  Llamas a estas funciones en tu script principal para mostrar los datos.

### Conectar un grafico a base de datos

Es **totalmente posible** y una de las prácticas recomendadas para crear tableros de control profesionales y dinámicos. Streamlit permite actuar como un puente entre tus datos almacenados en servidores externos y las visualizaciones interactivas de tu aplicación.

A continuación, se detalla el proceso para conectar los gráficos a una base de datos:

#### Gestión Segura de Credenciales
Nunca debes escribir tus contraseñas directamente en el código. Streamlit ofrece el sistema **`st.secrets`**, que permite almacenar información sensible (como `host`, `user` y `password`) en un archivo llamado `secrets.toml` de forma segura.

#### Establecer la Conexión
Puedes utilizar conectores estándar de Python según el tipo de base de datos:
*   **Bases de datos SQL**: Librerías como `psycopg2` o `SQLAlchemy` para **PostgreSQL**, `sqlite3` para **SQLite**, o conectores específicos para **Snowflake** y **Google BigQuery**.

*   **Bases de datos NoSQL**: Librerías como `pymongo` para conectar con **MongoDB**.

#### Optimización con Caching
Para evitar que la aplicación se vuelva lenta al reconectarse a la base de datos en cada recarga de la página, se deben usar decoradores de caché:
*   **`@st.cache_resource`**: Ideal para almacenar el objeto de **conexión** (pool de conexiones) y compartirlo entre todas las sesiones de usuario.

*   **`@st.cache_data`**: Se utiliza para almacenar los **resultados de las consultas** SQL, evitando ejecuciones repetitivas de consultas costosas si los parámetros no han cambiado.

#### Flujo de Datos hacia el Gráfico
El flujo lógico para alimentar un gráfico es el siguiente:
1.  **Consulta**: Se ejecuta una sentencia SQL (como `SELECT * FROM tabla`).
2.  **Conversión**: Los resultados se transforman en un **Pandas DataFrame**.
3.  **Visualización**: El DataFrame se pasa a la función de gráfico deseada (ej. `st.plotly_chart(df)` o `st.altair_chart(df)`).

#### Consultas Dinámicas (Mutating Charts)
Puedes integrar **filtros interactivos** (como un deslizador o un selector de fechas) directamente en tus consultas SQL. Por ejemplo, al mover un `st.slider` para elegir un rango de días, Streamlit puede re-ejecutar la consulta con ese nuevo parámetro y actualizar el gráfico automáticamente con los datos filtrados de la base de datos.

## Logo en sidebar

Para agregar el logo de tu empresa a la barra lateral (sidebar) de Streamlit, puedes utilizar la función **`st.sidebar.image()`**.

Prácticamente cualquier elemento o widget de Streamlit (excepto `st.echo` y `st.spinner`) se puede invocar dentro del sidebar simplemente anteponiendo el prefijo `.sidebar` al comando.

#### Uso nativo con `st.sidebar.image()`
Puedes insertar una imagen local o desde una URL directamente en la parte superior del sidebar:

```python showLineNumbers
import streamlit as st

# Usando una imagen local o una URL
st.sidebar.image("logo_empresa.png", caption="Nombre de la Empresa", use_column_width=True)
```

**Parámetros clave para el logo:**
*   **`image`**: La ruta local del archivo, un objeto de imagen (como PIL) o una URL de internet.
*   **`use_column_width`**: Si se establece en `True`, el logo se ajustará automáticamente al ancho del sidebar.
*   **`width`**: Permite definir un ancho específico en píxeles si no deseas que ocupe todo el espacio.

#### Logo en aplicaciones multipágina
Si estás desarrollando una aplicación con múltiples páginas y deseas que el logo aparezca específicamente arriba de la lista de navegación en el sidebar, existe una herramienta en la librería de la comunidad llamada **`streamlit-extras`**.

La función `app_logo` de esta librería permite colocar un logo en la parte superior izquierda, justo encima de los enlaces a las diferentes páginas. Esto es útil porque, en las versiones estándar, los elementos agregados con `st.sidebar` a veces aparecen debajo de la lista de navegación automática.

#### Consideración de diseño
Para una mejor estética, puedes combinar el logo con un título o un texto descriptivo en el mismo contenedor del sidebar:

```python showLineNumbers
with st.sidebar:
    st.image("logo.png")
    st.title("Panel de Control")
    st.write("Bienvenido al sistema corporativo.")
```

Esta organización mediante el bloque `with` permite agrupar el logo con otros widgets de forma ordenada.

## Aplicación completa

Se presenta un ejemplo de una aplicación completa con todas las secciones básicas. De es manera puedes usarlo como plantilla para aplicar desde lo básico de la creación en Streamlit. Usalo como punto de partida.

<center>
<figure>
![](img/st-aplicacion.png)
<figcaption>Ejemplo completo de una Aplicación en Streamlit.</figcaption>
</figure>
</center>

El siguiente ejemplo carga una planilla Excel y realiza algunas transformaciones sobre algunas columnas particulares.

:::info
**Descarga la planilla acá:** https://patricioaraneda.cl/public/plan_de_compras_2025.xlsx

Plan de compras de MINVU año 2025. Documento público
:::

### Plan de trabajo

1. carga un dataframe desde la planilla excel
2. Convierte los titulos de las columnas en lowercase

### Transformaciones
Realiza las transformaciones solicitadas en el orden indicado:

1. Convierte los titulos de las columnas en lowercase.
2. Solicitar el ingreso de un 'codigo' de proyecto, y eliminar los registros que en el valor de la columna 'id proyecto' no terminen en el 'codigo' ingresado (evaluado en uppercase).
3. crea una nueva columna llamada 'anexo' que debe contener los 4 ultimos digitos de la columna 'teléfono responsable' extraidos a partir del segundo guión '-'.
4. elimina espacios, y todos los guiones ('-') dentro de la columna 'teléfono responsable'. 

### Analisis exploratorio

Realiza un análisis exploratorio para detectar y mostrar:

- Cantidad de valores nulos por columna, en cantidad y mostrar porcentaje de nulos.

- Propone eliminar la columna con los valores nulos mas altos. Para ello espera respuesta (SI/NO) y elimina si responde 'SI'.

### Resumenes

Crea y visualiza las siguientes tablas resumenes:
- totales de 'monto total íem año 2025' agrupados por 'nombre responsable', ordenados en forma descendente.

- los 10 itemes más caros basados en 'monto unitario ítem', ordenados en forma descendente. incluye 'nombre ítem' y 'nombre responsable'.

- los itemes mas comprados basados en 'nombre ítem' y 'monto unitario ítem´. agrupados por 'nombre ítem'. ordenados en forma descendente.

### Gráficos

Crea un gráfico para cada una de las tablas resumenes solicitadas previamente (graficos en figuras separadas).


<details>
<summary>💻 Código</summary>

```python showLineNumbers
import streamlit as st
import streamlit.components.v1 as components
# accesorios
from streamlit_extras.metric_cards import style_metric_cards
from millify import millify
import numpy as np

import matplotlib.pyplot as plt
import plotly.express as px

import pandas as pd
import io

st.set_page_config(
    page_title="Plan de Compras",
    layout="wide"
)


st.title("📊 Análisis de Plan de Compras")

##############################################################
# SIDEBAR
##############################################################

st.sidebar.header("Configuraciones")

archivo = st.sidebar.file_uploader(
    "Seleccione archivo Excel",
    type=["xlsx", "xls"]
)

# Mijael
# codigo_year = st.sidebar.selectbox(
#     "codigo_year",
#     [2022, 2023, 2024, 2025],
#     index=3
# )
codigo_year=2025

codigo_proceso = f"PC{str(codigo_year)[-2:]}"

st.sidebar.info(f"Código proceso: {codigo_proceso}")



##############################################################
# CARGA
##############################################################

if archivo is not None:
    #status = st.status("Procesando archivo...", expanded=True)
    #status.write("Carga: leyendo archivo Excel.")

    df = pd.read_excel(archivo)

    ##############################################################
    # COLUMNAS LOWERCASE
    ##############################################################

    df.columns = (
        df.columns
        .str.lower()
        .str.strip()
    )


    ##############################################################
    # TRANSFORMACIONES
    ##############################################################
    #status.write("Carga: normalizando columnas y aplicando transformaciones iniciales.")
    # 1
    df = df[
        df["id proyecto"]
        .astype(str)
        .str.upper()
        .str.endswith(codigo_proceso.upper())
    ].copy()

    # 2
    df["anexo"] = (
        df["teléfono responsable"]
        .astype(str)
        .str.split("-")
        .str[-1]
        .str[-4:]
    )

    # 3
    df["teléfono responsable"] = (
        df["teléfono responsable"]
        .astype(str)
        .str.replace("-", "", regex=False)
        .str.replace(" ", "", regex=False)
    )

    #status.write("Carga: actualizando nombres de proyecto con el catálogo de códigos.")

    # -------------------------------------------------------------
    # modificar el nombre del proyecto segun el nombre de la planilla 
    # # codigos_unicos
    # ---------------------------------------------
    # transformacion de nombre de proyecto basado en codigos unicos
    codigos = pd.read_excel('codigos_unicos.xlsx')
    # Asegurar que las columnas de cruce tengan formato string sin espacios extra
    df['código presupuestario'] = df['código presupuestario'].astype(str).str.strip()
    codigos['Codigo'] = codigos['Codigo'].astype(str).str.strip()

    # Realizar el Join entre df y codigos
    df_merged = df.merge(
        codigos[['Codigo', 'Nombre']], 
        left_on='código presupuestario', 
        right_on='Codigo', 
        how='left'
    )
    # Reemplazar los valores en 'Nombre Proyecto' con el nuevo 'Nombre' obtenido del join
    # Se mantiene el valor original en caso de que no haya coincidencia
    df['nombre proyecto'] = df_merged['Nombre'].fillna(df['nombre proyecto'])

    #status.write("Análisis: preparando métricas y revisión exploratoria de datos.")

    ##############################################################
    # HEADER TARJETAS
    ##############################################################

    total_registros = len(df)

    monto_total = df["monto total ítem año 2025"].sum()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Total registros",
        f"{total_registros:,}",
        delta="30",
    )

    c2.metric(
        "Monto Total",
    millify(monto_total, precision=2),
    delta=millify(monto_total - 1000000, precision=2)
    )

    c3.metric(
        "Monto promedio",
        millify(df["monto total ítem año 2025"].mean(), precision=2),
        delta="-50"
    )
    c4.metric(
        "Valor máximo",
        millify(df["monto total ítem año 2025"].max(), precision=2)
    )

    style_metric_cards()

    st.divider()

    ##############################################################
    # ANALISIS EXPLORATORIO
    ##############################################################


    st.header("Análisis Exploratorio")
    st.divider()
    # walker = pyg.walk(df) # exploración de datos esilo Tableau

    st.dataframe(df.head(500), use_container_width=True)

    data = st.data_editor(df, num_rows="dynamic", use_container_width=True) 

    nulos = pd.DataFrame({

        "Columna": df.columns,

        "Nulos": df.isnull().sum().values,

        "Porcentaje": (
            df.isnull().mean()*100
        ).round(2)

    })

    st.dataframe(nulos, use_container_width=True)


    columna_eliminar = (
        nulos
        .sort_values("Nulos", ascending=False)
        .iloc[0]["Columna"]
    )

    st.warning(
        f"Se propone eliminar la columna **{columna_eliminar}** "
        "por ser la que posee más valores nulos."
    )

    eliminar = st.radio(
        "¿Desea eliminarla?",
        ["NO", "SI"],
        horizontal=True
    )

    if eliminar == "SI":
        df = df.drop(columns=[columna_eliminar])
        st.success("Columna eliminada.")

    ##############################################################
    # TABLAS RESUMEN
    ##############################################################
    #status.write("Tablas: generando resúmenes para responsables e ítems.")
    
    st.header("Resúmenes")

    resumen1 = (
        df.groupby("nombre responsable", as_index=False)
        ["monto total ítem año 2025"]
        .sum()
        .sort_values(
            "monto total ítem año 2025",
            ascending=False
        ).head(10)
    )

    resumen2 = (
        df[
            [
                "nombre ítem",
                "nombre responsable",
                "monto unitario ítem"
            ]
        ]
        .sort_values(
            "monto unitario ítem",
            ascending=False
        )
        .head(6)
    )

    resumen3 = (
        df
        .groupby("nombre ítem", as_index=False)
        .agg({
            "monto unitario ítem":"sum"
        })
        .sort_values(
            "monto unitario ítem",
            ascending=True
        ).head(10)
    )

    st.subheader("Monto por Responsable")
    st.dataframe(resumen1, use_container_width=True)

    st.subheader("10 Ítems más caros")
    st.dataframe(resumen2, use_container_width=True)

    st.subheader("Ítems más comprados")
    st.dataframe(resumen3, use_container_width=True)

    ##############################################################
    # GRAFICOS
    ##############################################################



    #status.write("Gráficos: construyendo visualizaciones del resumen.")

    st.header("Gráficos")

    fig1 = px.bar(
        resumen1,
        x="nombre responsable",
        y="monto total ítem año 2025",
        title="Monto Total por Responsable"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    fig2 = px.bar(
        resumen2,
        x="nombre ítem",
        y="monto unitario ítem",
        color="nombre responsable",
        title="10 Ítems más caros"
    )
    fig2.update_layout(height=600)
    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    fig3 = px.bar(
        resumen3,
        x="monto unitario ítem",
        y="nombre ítem",
        title="Ítems más comprados",
        orientation="h",
        color="monto unitario ítem",
    )
    fig3.update_layout(height=600)
    st.plotly_chart(
        fig3,
        use_container_width=True
    )

    #status.update(label="Proceso completado", state="complete", expanded=False)

    ##############################################################
    # DESCARGA ARCHIV
    ##############################################################
    output_bytes = io.BytesIO()
    with pd.ExcelWriter(output_bytes, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)
    st.download_button(
        label="Descargar Excel procesado",
        data=output_bytes.getvalue(),
        file_name="plan_de_compras_2025_procesado.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


else:
    st.info("Por favor, suba un archivo Excel para comenzar el análisis.")

```
</details>

## Una app multipáginas

Crear una aplicación multipágina en Streamlit se puede lograr de dos maneras principales: mediante la **estructura de carpetas estándar** o de forma programática utilizando **`st.navigation`**.

### Método Estándar
Este método (estuctura de carpetas) el método más sencillo y se basa en organizar tus archivos en el sistema de archivos de tu proyecto. Streamlit detecta automáticamente los archivos dentro de una carpeta específica y los muestra en la barra lateral.

**Estructura del proyecto:**
*   **`home.py`**: El archivo principal que ejecutarás con `streamlit run`. Este actúa como la página de inicio.

*   **`pages/`**: Una carpeta que debe llamarse exactamente así, ubicada en el mismo directorio que tu archivo principal.
    *   **`pagina_2.py`**: Los archivos dentro de esta carpeta se convertirán en páginas adicionales.
    *   **`pagina_3.py`**: Streamlit usará los nombres de los archivos para crear los enlaces de navegación en el sidebar.

**Reglas clave:**
*   Solo los archivos `.py` dentro de la carpeta `pages` se cargarán como páginas.
*   Este método funciona en versiones de Streamlit superiores a la **1.10**.

```raw title="Estructura de proyecto"
carpeta_proyecto/
├── pages/
│   ├── pagina_1.py
│   └── pagina_2.py
└── app.py
```



### Método Programático

Este método utiliza `st.navigation` y `st.Page` para aplicaciones más complejas que requieren un control dinámico de la navegación, se utilizan los objetos **`st.Page`** y la función **`st.navigation`**.

**Pasos para este método:**

1.  **Definir las páginas:** Crea objetos `st.Page` especificando la ruta del archivo, el título y un icono opcional.
    ```python
    pagina_inicio = st.Page("inicio.py", title="Inicio", icon=":material/home:")
    pagina_datos = st.Page("datos.py", title="Datos", icon=":material/analytics:")
    ```
2.  **Configurar la navegación:** Pasa una lista de estos objetos a `st.navigation`.
    ```python
    pg = st.navigation([pagina_inicio, pagina_datos])
    ```
3.  **Ejecutar la página seleccionada:** Llama al método `.run()` del objeto devuelto por la navegación.
    ```python
    pg.run()
    ```
```raw title="Estructura de proyecto"
carpeta_proyecto/
├── pagina_1.py
├── pagina_2.py
└── app.py
```
```python title="Navegación por páginas"
import streamlit as st

pg = st.navigation([st.Page("pagina_1.py"), st.Page("pagina_2.py")])
pg.run()
```

### Beneficios y Herramientas Adicionales

*   **Estado compartido:** El **`st.session_state`** se comparte entre todas las páginas de la aplicación, lo que permite que los datos o selecciones del usuario persistan mientras navega.

*   **Iconos:** Puedes añadir iconos a las páginas usando la sintaxis `:material/nombre_del_icono:` de la librería Material Symbols de Google.

*   **Librerías de la comunidad:** Existen herramientas como **`st-pages`** que permiten añadir funcionalidades extra, como agrupar páginas en secciones o añadir emojis a los enlaces de forma más flexible.

Para una organización óptima, se recomienda mantener las funciones de carga de datos pesadas centralizadas y utilizar **`@st.cache_data`** para que la navegación sea rápida y no recargue datos innecesariamente en cada página.