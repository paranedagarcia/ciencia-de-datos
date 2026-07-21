---
id: streamlit-graf
title: "Streamlit"
sidebar_label: "💻 Uso de Gráficos"
sidebar_position: 3
description: "Uso de librerias gráficas"
slug: /streamlit-graf
---

<div className="text--center">
![](img/streamlit-logo.webp)
</div>


## Integración de gráficos

Integrar gráficos de **Matplotlib** y **Plotly** en Streamlit es un proceso sencillo gracias a comandos nativos diseñados específicamente para estas bibliotecas. A continuación, se detalla cómo hacerlo para cada una:

### 1. Integración de Matplotlib
Para mostrar gráficos de Matplotlib, se utiliza la función **`st.pyplot()`**.

*   **Procedimiento estándar:** Primero debes crear una figura y uno o más ejes utilizando `plt.subplots()`. Después de generar el gráfico en esos ejes, pasas el objeto de la figura a Streamlit.
*   **Ejemplo de código:**
    ```python
    import matplotlib.pyplot as plt
    import streamlit as st
    import numpy as np

    # Crear la figura y los ejes
    fig, ax = plt.subplots()
    data = np.random.randn(100)
    ax.hist(data, bins=20)

    # Mostrar en Streamlit
    st.pyplot(fig)
    ```
*   **Nota importante:** Se recomienda encarecidamente definir y pasar el objeto `fig` explícitamente. Si se llama a `st.pyplot()` sin argumentos, Streamlit intentará usar la figura global actual, lo que puede causar resultados inesperados o errores de advertencia (`PyplotGlobalUseWarning`).

### 2. Integración de Plotly
Para gráficos interactivos de Plotly, Streamlit ofrece el comando **`st.plotly_chart()`**.

*   **Interactividad:** Una gran ventaja es que toda la interactividad nativa de Plotly (zoom, herramientas de información al pasar el mouse, descarga como imagen) funciona automáticamente dentro de la aplicación.
*   **Uso con Plotly Express u Objects:** Puedes crear la figura usando `plotly.express` (para gráficos rápidos) o `plotly.graph_objects` (para mayor personalización) y luego mostrarla.
*   **Ajuste de ancho:** Es común usar el parámetro `use_container_width=True` para que el gráfico se expanda automáticamente al ancho de la columna o página.
*   **Ejemplo de código:**
    ```python
    import plotly.express as px
    import streamlit as st
    import pandas as pd

    df = pd.DataFrame({"x":, "y":})
    fig = px.line(df, x="x", y="y", title="Gráfico de Plotly")

    # Mostrar con ancho ajustado al contenedor
    st.plotly_chart(fig, use_container_width=True)
    ```

### Comparación rápida entre ambos
| Característica | Matplotlib | Plotly |
| :--- | :--- | :--- |
| **Comando** | `st.pyplot(fig)` | `st.plotly_chart(fig)` |
| **Naturaleza** | Estática (imagen) | Interactiva (web) |
| **Uso ideal** | Visualizaciones estadísticas clásicas | Paneles interactivos y dashboards |

Ambas bibliotecas son compatibles con las funciones de **caching** de Streamlit (`@st.cache_data` o `@st.cache_resource`), lo que permite cargar los datos o generar los objetos de los gráficos de manera eficiente sin repetir cálculos costosos en cada recarga de la página.

### Personalizar gráficos

Para personalizar los colores de un gráfico en Streamlit, puedes utilizar métodos específicos de las bibliotecas de visualización (como Plotly, Matplotlib o Altair) o permitir que el usuario elija los colores mediante widgets interactivos.

A continuación, se detallan las formas principales de lograrlo:

### 1. Uso del widget `st.color_picker`
Streamlit ofrece el comando **`st.color_picker()`**, que permite al usuario seleccionar un color de forma interactiva. Este widget devuelve el color seleccionado como una cadena de texto en formato hexadecimal (por ejemplo, `"#D6266A"`), que luego puedes pasar a tus funciones de graficado.

*   **Con Seaborn/Matplotlib:** Puedes pasar el valor obtenido del selector de color al argumento `color` de la función de gráfico.
    ```python
    graph_color = st.sidebar.color_picker('Elige un color para el gráfico')
    sns.histplot(df['columna'], color=graph_color)
    ```
*   **Con Plotly:** Puedes usar el parámetro `color_discrete_sequence` para aplicar el color seleccionado a las series del gráfico.
    ```python
    fig = px.histogram(df, x="variable", color_discrete_sequence=[graph_color])
    ```

### 2. Personalización según la biblioteca de gráficos
Cada biblioteca integrada con Streamlit tiene sus propios parámetros para gestionar colores:

*   **Plotly:** Puedes asignar colores basados en variables específicas del dataset usando el argumento `color` (por ejemplo, `color="especie"`). También puedes definir escalas de colores continuas como "Viridis" en gráficos de dispersión.
*   **Altair:** La personalización se realiza dentro del método `.encode()`, utilizando el parámetro `color` para vincular una columna de datos a una escala cromática.
*   **Mapas (PyDeck):** En gráficos geoespaciales, puedes definir el color de las capas (como `ScatterplotLayer` o `HexagonLayer`) basándote en la densidad de los puntos o en valores específicos.

### 3. Temas globales de la aplicación
Puedes cambiar el esquema de colores de toda la interfaz, lo que afecta indirectamente a cómo se ven los widgets y algunos elementos gráficos, modificando el archivo **`config.toml`** en la carpeta `.streamlit`. Los parámetros clave son:

*   **`primaryColor`**: Cambia el color de acento de los elementos interactivos como botones y deslizadores.
*   **`backgroundColor`**: Define el color del área principal de contenido.
*   **`secondaryBackgroundColor`**: Ajusta el color de la barra lateral y de los fondos de ciertos widgets.
*   **`textColor`**: Cambia el color de la fuente en toda la aplicación.

Estas configuraciones de tema también se pueden previsualizar y ajustar gráficamente desde el menú de **Settings** en la esquina superior derecha de la aplicación Streamlit.

### Otras librerias compatibles

Además de **Matplotlib** y **Plotly**, Streamlit es compatible con una amplia variedad de librerías de visualización de Python, lo que permite desde gráficos estadísticos clásicos hasta mapas interactivos complejos.

Se detallan las librerías principales:

### 1. Librerías de Visualización Estadística e Interactivas
*   **Altair:** Es una librería de visualización estadística declarativa basada en Vega. Streamlit tiene un comando nativo, `st.altair_chart()`, para integrarla de forma fluida. Es ideal para prototipado rápido y visualizaciones web responsivas.

*   **Seaborn:** Basada en Matplotlib, se utiliza para crear gráficos estadísticos más atractivos y con estilos predefinidos. Se despliega en Streamlit usando el comando `st.pyplot()`, al igual que Matplotlib.

*   **Bokeh:** Una librería enfocada en la interactividad dentro de navegadores web. Se integra mediante `st.bokeh_chart()`.

*   **Vega-Lite:** Utiliza una sintaxis JSON compacta para crear gráficos interactivos. Se puede renderizar con `st.vega_lite_chart()`.

### 2. Visualización Geoespacial y de Mapas
*   **PyDeck:** Especializada en visualizaciones de datos espaciales a gran escala y en 3D, construida sobre deck.gl. Se integra con `st.pydeck_chart()`.

*   **Folium:** Permite crear mapas interactivos utilizando la librería Leaflet.js de JavaScript. Existe un componente de la comunidad llamado `st-folium` que permite incluso capturar eventos de clic en el mapa de vuelta hacia Streamlit.

### 3. Visualizaciones Especializadas
*   **Graphviz:** Se utiliza para crear diagramas de red, flujogramas y estructuras de grafos utilizando el lenguaje DOT. Streamlit ofrece el comando `st.graphviz_chart()` para este propósito.

*   **Dagre-D3:** Otra opción para visualizaciones de grafos y redes disponible a través de integraciones.

### 4. Herramientas de Análisis Automático
*   **Pandas-Profiling:** Aunque es más una herramienta de análisis exploratorio de datos (EDA), existe un componente (`streamlit-pandas-profiling`) que genera reportes interactivos completos directamente dentro de una aplicación Streamlit.

**Nota sobre la compatibilidad:** Streamlit permite extender su funcionalidad mediante **componentes personalizados** de terceros, lo que significa que casi cualquier librería de visualización de JavaScript puede ser adaptada para funcionar dentro del entorno de Streamlit si existe el envoltorio (*wrapper*) adecuado.

## Altair

Para usar **Altair** en tus aplicaciones de Streamlit, debes seguir un enfoque **declarativo**, donde defines las relaciones entre las columnas de tus datos en lugar de especificar cada detalle del gráfico manualmente.

A continuación, se detallan los pasos y comandos principales:

#### 1. Preparación e Instalación
Primero, asegúrate de tener instalada la librería en tu entorno:
```bash
pip install altair
```
Luego, impórtala en tu script junto con Streamlit y Pandas:
```python
import streamlit as st
import altair as alt
import pandas as pd
```

#### 2. Comando Principal: `st.altair_chart()`
Para mostrar un gráfico de Altair, se utiliza la función **`st.altair_chart()`**. Un parámetro común es `use_container_width=True`, que ajusta automáticamente el ancho del gráfico al contenedor de la aplicación.

#### 3. Flujo de Trabajo para Crear Gráficos
El proceso estándar consiste en definir un objeto de gráfico y luego pasarlo a Streamlit:

1.  **Definir el gráfico:** Usa `alt.Chart(df)` pasando tu DataFrame.

2.  **Elegir la marca (`mark`):** Define el tipo de visualización (barras, líneas, puntos, etc.).

3.  **Codificar canales (`encode`):** Mapea las columnas del DataFrame a los ejes X, Y, colores o tooltips.

4.  **Añadir interactividad:** Usa el método `.interactive()` para permitir que el usuario haga zoom o desplace el gráfico.

#### 4. Ejemplos de Gráficos Comunes
*   **Gráfico de Barras:** Se usa `mark_bar()`. Altair puede resumir datos directamente, por ejemplo, usando `y='count(*):Q'` para contar registros.
*   **Gráfico de Áreas:** Utiliza `mark_area()`, ideal para representar datos cuantitativos basados en series temporales.
*   **Gráfico de Dispersión (Scatter):** Emplea `mark_circle()` o `mark_point()`. Es muy útil para ver correlaciones entre variables.
*   **Gráfico de Cajas (Boxplot):** Usa `mark_boxplot()` para representar cuartiles, promedios y valores atípicos.
*   **Mapa de Calor (Heatmap):** Se utiliza `mark_rect()` para representar la intensidad de valores en dos dimensiones.

#### Datos de Interés
*   **Interacción fluida:** Al ser basado en Vega, los gráficos son web-friendly y responden bien en el navegador.

*   **Uso interno:** Las funciones nativas de Streamlit como `st.line_chart()` y `st.bar_chart()` son, en realidad, llamadas simplificadas a la librería Altair.

*   **Visualización de modelos:** Puedes usar `st.write(chart)` (la "navaja suiza" de Streamlit) para renderizar objetos de Altair directamente si no necesitas configuraciones adicionales.

### Ventajas de Altair

La elección entre **Altair**, **Matplotlib** y **Plotly** depende de las necesidades de interactividad y personalización del proyecto. Según las fuentes, **Altair** presenta ventajas significativas, especialmente en su integración con Streamlit:

#### 1. Enfoque Declarativo vs. Imperativo
*   **Altair:** Es una librería **declarativa**. Esto significa que el desarrollador define las **relaciones entre las columnas** de los datos (qué va en el eje X, qué en el Y, qué determina el color) y Altair se encarga del resto del diseño.

*   **Matplotlib:** Es más **verbosa** y requiere un control detallado de cada elemento del gráfico (enfoque imperativo), lo que puede complicar la creación de visualizaciones complejas.

*   **Plotly:** Aunque potente, puede tener una curva de aprendizaje más pronunciada para funciones avanzadas en comparación con la simplicidad de Altair.

#### 2. Interactividad Nativa y Rendimiento
*   **Altair:** Los gráficos son **interactivos por defecto** (zoom, desplazamiento, herramientas de información al pasar el ratón) y están diseñados para ser amigables con la web y responsivos.

*   **Matplotlib:** Los gráficos son **estáticos por defecto**. No ofrecen interactividad nativa dentro del navegador y, en aplicaciones muy grandes, pueden **ralentizar la ejecución** ya que se renderizan como imágenes estáticas en lugar de componentes web vivos.

*   **Plotly:** Es altamente interactivo y dinámico, pero esto puede hacerlo más **intensivo en recursos** de computación en comparación con la ligereza de Altair.

#### 3. Integración con Streamlit
*   **Altair:** Es la librería que Streamlit utiliza internamente para sus comandos de visualización nativos, como `st.line_chart()`, `st.bar_chart()` y `st.area_chart()`. Se considera la "capa visual" estándar sobre Python para este framework.

*   **Matplotlib:** Requiere definir explícitamente objetos de figura (`plt.subplots()`) y pasarlos al comando `st.pyplot()`, lo que puede generar advertencias globales si no se gestiona correctamente.

#### 4. Estética y Diseño
*   **Altair:** Las fuentes lo describen como una opción que genera gráficos **"generalmente bonitos"** con poco esfuerzo, siguiendo principios modernos de visualización estadística.

*   **Matplotlib:** Es ampliamente adoptado pero se considera **"no particularmente atractivo"** estéticamente sin una configuración manual extensa.

### Resumen Comparativo

| Característica | Altair | Matplotlib | Plotly |
| :--- | :--- | :--- | :--- |
| **Naturaleza** | Declarativa (fácil de programar) | Imperativa (más código) | Interactiva (compleja) |
| **Interactividad** | Alta e integrada | Nula (estática) | Muy alta (dinámica) |
| **Uso en Streamlit** | Motor interno nativo | Renderizado como imagen | Integración bidireccional |
| **Estética** | Moderna y limpia | Clásica y básica | Moderna y profesional |

En conclusión, **Altair ofrece la mejor combinación de simplicidad de código, interactividad web y rendimiento** para la mayoría de los casos de uso en Streamlit, mientras que Matplotlib se reserva para visualizaciones científicas muy específicas y Plotly para dashboards donde se requiera una interactividad bidireccional extremadamente compleja.

