---
id: streamlit-dev
title: "Streamlit"
sidebar_label: "💻 Desarrollo en Streamlit"
sidebar_position: 1
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
st.set_page_config(layout="wide")
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
total_registros = len(df)
valor_promedio = df.iloc[:, 1].mean() # Supone que la segunda columna es numérica

col1, col2 = st.columns(2)
col1.metric("Total de Registros", total_registros)
col2.metric("Valor Promedio", f"{valor_promedio:.2f}")
```

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

A continuación, se detallan las estrategias recomendadas según las fuentes:

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