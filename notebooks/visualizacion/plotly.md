## Visualización Interactiva con Plotly

**Plotly** es una de las herramientas más potentes en Python para generar gráficos interactivos basados en la web, utilizando tecnologías como **D3.js, HTML y CSS**. A diferencia de las librerías estáticas, Plotly permite una comunicación de hallazgos más profunda al integrar herramientas de exploración directa en el navegador.

## Configuración Inicial
Para utilizar Plotly, es común importar su interfaz de alto nivel, `plotly.express`, que permite crear gráficos complejos con muy pocas líneas de código.s


```python
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Cargar datasets de ejemplo integrados
df_gapminder = px.data.gapminder()
df_iris = px.data.iris()
df_tips = px.data.tips()
```

## El Gráfico de Burbujas Interactivo (Estilo Hans Rosling)
Este es uno de los usos más icónicos de Plotly. Permite visualizar tres dimensiones numéricas (ejes X, Y y tamaño de la burbuja) y una categórica (color).

*   **Capacidad Interactiva:** Al pasar el ratón por encima (**hover**), se revelan "detalles bajo demanda" como el nombre del país y valores exactos.


```python
# Visualización de PIB per cápita vs Esperanza de Vida (Año 2007)
# establece tamaño de la figura
px.defaults.width = 1200
px.defaults.height = 600

fig = px.scatter(df_gapminder.query("year==2007"), x="gdpPercap", y="lifeExp",
                 size="pop", color="continent",
                 hover_name="country", log_x=True, size_max=60,
                 title="PIB vs Esperanza de Vida (2007)")

fig.show()
```



## Series Temporales con Zoom Dinámico
Plotly destaca en el manejo de **series temporales**, permitiendo al usuario realizar zoom en intervalos específicos para identificar tendencias o anomalías sin perder la resolución de los datos.


```python
# Ejemplo de evolución de acciones o valores en el tiempo
# establece tamaño de la figura
px.defaults.width = 1200
px.defaults.height = 600

fig = px.line(df_gapminder.query("country=='Chile'"), x='year', y='gdpPercap',
              title='Evolución del PIB en Colombia',
              markers=True)

# Añadir un selector de rango interactivo (Range Slider)
fig.update_xaxes(rangeslider_visible=True)
fig.show()
```



## Matriz de Dispersión (Pair Plots) Interactiva
Útil para explorar correlaciones multidimensionales. En la versión de Plotly, cada subgráfico es interactivo, permitiendo aislar especies o grupos mediante la leyenda.


```python
# Comparación de múltiples variables del dataset Iris
# establece tamaño de la figura
px.defaults.width = 1200
px.defaults.height = 800

fig = px.scatter_matrix(df_iris,
    dimensions=["sepal_length", "sepal_width", "petal_length", "petal_width"],
    color="species", title="Matriz de Dispersión Interactiva - Iris")

fig.show()
```



## Conversión de Matplotlib a Plotly
Una característica fundamental mencionada en las fuentes es la capacidad de **Plotly** para tomar un objeto de figura de **Matplotlib** y convertirlo en una versión interactiva.


```python

import matplotlib.pyplot as plt
import plotly.tools as tls

# Crear un gráfico simple en Matplotlib basado en datos de ejemplo de gapminder, estableciendo el tamaño de la figura y color por continente

px.defaults.width = 1200
px.defaults.height = 800

x="gdpPercap"
y="lifeExp"
plt.plot(df_gapminder[x], df_gapminder[y], 'ro')
plt.xlabel(x)
plt.ylabel(y)
mpl_fig = plt.gcf()

# Convertir a Plotly para interactividad y muestra el nombre de los países al pasar el cursor sobre los puntos
# Add country names as hover text
plotly_fig = tls.mpl_to_plotly(mpl_fig)
plotly_fig.data[0].customdata = df_gapminder['country']
plotly_fig.data[0].hovertemplate = '<b>%{customdata}</b><br>GDP per Capita: %{x}<br>Life Expectancy: %{y}<extra></extra>'

plotly_fig.show()
```



### Funciones Interactivas Clave Destacadas:
*   **Detalles bajo demanda:** Los tooltips (cuadros de información al pasar el ratón) evitan saturar el gráfico con etiquetas de texto innecesarias.
*   **Zoom y Panorámica:** Los controles integrados permiten explorar subsecciones de datos masivos sin recargar la página.
*   **Leyendas Activas:** Al hacer clic en un elemento de la leyenda, el usuario puede filtrar y ocultar/mostrar series de datos dinámicamente.
*   **Range Slider:** Ideal para datos cronológicos, facilitando la navegación en series temporales largas.
