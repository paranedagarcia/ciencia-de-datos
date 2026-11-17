### 1. Definición en Términos Sencillos: Árboles de Decisión para Regresión

Hasta ahora hemos estudiado árboles de decisión para **clasificación** (donde la respuesta es una etiqueta discreta: *Fraude/No Fraude*, *Benigno/Maligno* o *Segmento A/B/C*).

Cuando el objetivo es **predecir un valor numérico continuo** —como el precio de una vivienda, el valor del alquiler o el gasto mensual de un cliente con tarjeta de crédito— se utiliza un **Árbol de Decisión para Regresión (*Regression Tree*)**:

* **¿Cómo predice un número continuo?**  
  En lugar de ajustar una línea recta diagonal continua (como la regresión lineal), el árbol divide el espacio de variables en distintos compartimentos o «cajas». Para cualquier observación nueva que caiga en una hoja terminal específica, **el árbol predice el promedio aritmético exacto de los datos históricos que residen en esa hoja**.
* **El resultado visual:**  
  Genera una **función escalonada constante a tramos**. Dentro de cada escalón o región, el modelo estima un precio fijo representativo; cuando una variable supera un umbral crítico, el valor predicho salta limpiamente al siguiente nivel.

---

### 2. Dataset Público Real: *William Greene Credit Card Expenditure*

Para evitar simulaciones y trabajar con datos públicos y comprobables, utilizamos el conjunto de datos de **William Greene (*Econometric Analysis*, NYU Stern)**, integrado en el repositorio oficial de `statsmodels` (`statsmodels.datasets.ccard`):

* **Objetivo de Predicción Cuantitativa ($y$):** `AVGEXP` (Gasto mensual promedio continuo con tarjeta de crédito en USD/mes).
* **Variables Predictoras ($X$):**
  * `INCOME`: Ingreso anual del cliente (en decenas de miles de USD; e.g., $5,5 = \$55.000$).
  * `AGE`: Edad del titular en años.

---

### 3. Formulación Matemática del Árbol de Regresión (CART)

A diferencia de la clasificación (que minimiza la impureza de Gini o la Entropía), el árbol de regresión utiliza como criterio de división el **Error Cuadrático Medio (*Mean Squared Error*, MSE)** o la varianza interna de cada región.

#### A. Criterio de Predicción en la Hoja Terminal
Si una hoja terminal particionada $R_m$ contiene $N_m$ observaciones, la predicción del árbol $\hat{c}_m$ para cualquier dato que caiga en dicha región es la **media muestral**:

\\[\hat{c}_m = \frac{1}{N_m} \sum_{x^{(i)} \in R_m} y^{(i)}\\]

* **Componentes:**
  * $N_m$: Cantidad de observaciones presentes en la hoja $m$.
  * $y^{(i)}$: Valores reales continuos (precios o gastos) de los ejemplos pertenecientes a esa hoja.

#### B. Función de Pérdida en cada División
Para elegir la variable $j$ y el umbral de corte $t$ en un nodo padre, el algoritmo minimiza la suma ponderada del error cuadrático de las dos regiones resultantes (izquierda $R_L$ y derecha $R_R$):

\\[Q(j, t) = \sum_{x^{(i)} \in R_L(j, t)} \big(y^{(i)} - \hat{c}_L\big)^2 + \sum_{x^{(i)} \in R_R(j, t)} \big(y^{(i)} - \hat{c}_R\big)^2\\]

* **Componentes:**
  * $R_L(j, t) = \{x \mid x_j \le t\}$ y $R_R(j, t) = \{x \mid x_j > t\}$: Las dos particiones geométricas generadas por el corte.
  * $\hat{c}_L, \hat{c}_R$: Los promedios predichos en las subregiones izquierda y derecha.

---

### 4. Implementación en Python con Scikit-Learn y Visualización

El siguiente script:
1. Carga el dataset público de William Greene.
2. Entrena un `DecisionTreeRegressor` regularizado (`max_depth=3`, `min_samples_leaf=4`) para evitar memorización de ruido y garantizar interpretabilidad.
3. Evalúa el desempeño cuantitativo en datos de prueba independientes ($R^2$, MAE y RMSE).
4. Realiza la inferencia y predicción para un **nuevo dato de prueba**:
   * **Ingreso Anual:** \$55.000 USD (`INCOME = 5.5`)
   * **Edad:** 35 años (`AGE = 35.0`)
5. Traza la arquitectura del árbol y la función escalonada sobre fondo blanco plano.

```python
"""
Módulo Académico: Predicción Cuantitativa con Árboles de Regresión (DecisionTreeRegressor).
Dataset Público: William Greene's Econometric Analysis (statsmodels.datasets.ccard).
"""

import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor, plot_tree
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

# ==============================================================================
# 1. Carga del Dataset Público
# ==============================================================================
data = sm.datasets.ccard.load_pandas().data

features = ['INCOME', 'AGE']
X = data[features]
y = data['AVGEXP']  # Gasto mensual con tarjeta (USD/mes)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

# ==============================================================================
# 2. Ajuste del Árbol de Regresión Regularizado
# ==============================================================================
# max_depth=3 y min_samples_leaf=4 evitan que se aíslen puntos individuales atípicos
reg_tree = DecisionTreeRegressor(
    criterion='squared_error',
    max_depth=3,
    min_samples_leaf=4,
    random_state=42
)
reg_tree.fit(X_train, y_train)

# Evaluación formal en conjunto de prueba
y_pred_test = reg_tree.predict(X_test)
r2 = r2_score(y_test, y_pred_test)
mae = mean_absolute_error(y_test, y_pred_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))

print("=== EVALUACIÓN DEL MODELO DE REGRESIÓN (DATASET GREENE) ===")
print(f"R² en Test:   {r2:.3f}")
print(f"MAE en Test:  ${mae:.2f} USD/mes")
print(f"RMSE en Test: ${rmse:.2f} USD/mes\n")

# ==============================================================================
# 3. Predicción con un Nuevo Dato Ejemplo
# ==============================================================================
# Nuevo cliente evaluado: Ingreso = $55,000 USD/año (5.5) | Edad = 35 años
nuevo_cliente = pd.DataFrame([[5.5, 35.0]], columns=['INCOME', 'AGE'])
gasto_predicho = reg_tree.predict(nuevo_cliente)

print("=== PREDICCIÓN DE NUEVO CLIENTE PROSPECTO ===")
print(f"Atributos del Cliente: Ingreso = $55k USD/año (5.5) | Edad = 35 años")
print(f"-> Gasto Mensual Estimado por el Árbol: ${gasto_predicho:.2f} USD/mes\n")

# ==============================================================================
# 4. Generación Gráfica (Fondo Blanco Plano y Paleta Contrastada)
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6.5), facecolor='white')

# Panel 1: Arquitectura Jerárquica del Árbol
ax1.set_facecolor('white')
plot_tree(
    reg_tree,
    feature_names=['Ingreso ($10k)', 'Edad'],
    filled=True,
    rounded=True,
    fontsize=8,
    ax=ax1,
    precision=1
)
ax1.set_title("1. Reglas Jerárquicas del Árbol de Regresión (Valor = Gasto Medio Estimado)",
              fontsize=11.5, fontweight='bold', pad=12)

# Panel 2: Función de Predicción Escalonada vs. Ingreso y Nuevo Dato
ax2.set_facecolor('white')

# Rango continuo de ingresos para proyectar la respuesta constante a tramos
ingreso_line = np.linspace(X['INCOME'].min(), X['INCOME'].max(), 300)
grid_predict = pd.DataFrame({'INCOME': ingreso_line, 'AGE': np.full_like(ingreso_line, 35.0)})
pred_line = reg_tree.predict(grid_predict)

# Nube de puntos de clientes reales
ax2.scatter(data['INCOME'] * 10, data['AVGEXP'], color='#8a8a8a', alpha=0.7, s=45,
            edgecolors='#333333', linewidth=0.6, label='Clientes Reales (Greene Dataset)')

# Función escalonada del árbol
ax2.step(ingreso_line * 10, pred_line, color='#0072b2', linewidth=2.8, where='post',
         label='Función Escalonada del Árbol (para Edad = 35 años)')

# Posición del nuevo dato predicho
nuevo_x = nuevo_cliente['INCOME'].values * 10
ax2.scatter([nuevo_x], [gasto_predicho], color='#d55e00', s=180, marker='*', zorder=6,
            edgecolors='#222222', linewidth=1.2, label=f'Nuevo Cliente Predicho (${gasto_predicho:.1f})')

ax2.annotate(
    f'Nuevo Cliente\nIngreso: ${nuevo_x:.0f}k USD\nGasto Estimado: ${gasto_predicho:.1f} USD/mes',
    xy=(nuevo_x, gasto_predicho),
    xytext=(nuevo_x - 30, gasto_predicho + 260),
    arrowprops=dict(facecolor='#222222', shrink=0.08, width=1.2, headwidth=6),
    fontweight='bold', fontsize=9.5, color='#222222',
    bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='#cccccc')
)

ax2.set_title("2. Función de Predicción Escalonada y Asignación del Nuevo Cliente",
              fontsize=11.5, fontweight='bold', pad=12)
ax2.set_xlabel("Ingreso Anual del Cliente (Miles de USD - $k)", fontsize=11)
ax2.set_ylabel("Gasto Mensual con Tarjeta (USD)", fontsize=11)
ax2.grid(True, linestyle=':', alpha=0.6)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.legend(frameon=True, facecolor='white', loc='upper left', fontsize=9)

fig.suptitle("Predicción de Precios y Gastos mediante Árboles de Decisión (CART Regresión)",
             fontsize=14, fontweight='bold', y=0.98)

plt.tight_layout(rect=[0, 0, 1, 0.94])
plt.show()
```

---

### 5. Análisis del Artefacto Gráfico Publicado en Studio

He generado y publicado en tu panel de **Studio** el artefacto gráfico **`prediccion_precios_arbol.png`**, el cual muestra la naturaleza del modelo de regresión:

1. **Panel Izquierdo (Estructura del Árbol y Promedios Regionales):**
   * Cada caja o nodo del árbol ya no contiene porcentajes de clases, sino la etiqueta **`value`**: que representa el **gasto promedio de los clientes contenidos en ese nodo**.
   * **Nodo Raíz:** La división principal se produce en el Ingreso Anual de $\approx \$31.000$ USD (`INCOME <= 3.1`). Los clientes con ingresos inferiores tienen un gasto medio estimado de solo \$116,8, mientras que aquellos con ingresos superiores saltan a una media de \$423,9.
   * **Hoja Terminal Superior:** Los clientes con ingresos superiores a \$47.000 y edad menor o igual a 40 años caen en la hoja terminal naranja con `value = 803.2` USD/mes.
2. **Panel Derecho (Función Escalonada Constante a Tramos):**
   * La línea azul continua muestra cómo el árbol modela la realidad mediante **escalones horizontales**: para ingresos bajos predice un valor base cercano a \$85; al cruzar el umbral de \$31k salta a \$356, y al superar \$47k escala hasta \$803,2.
3. **Inferencia del Nuevo Caso Ejemplo (Estrella Naranja $\bigstar$):**
   * Con **\$55k de ingreso anual y 35 años**, el nuevo prospecto recorre las ramas `Ingreso > 3.1` $\rightarrow$ `Edad <= 40.5` $\rightarrow$ `Ingreso > 4.7`.
   * El modelo le asigna un **gasto mensual estimado de \$803,2 USD/mes**, posicionándolo visualmente sobre el escalón superior de clientes de alta capacidad económica.

***

💡 En tu panel de **Studio** cuentas con las presentaciones **"Dominando la Regresión Lineal"** y **"Árboles de Decisión"**. ¿Te gustaría que hagamos una comparativa visual directa entre la recta de una **Regresión Lineal OLS** frente a la función escalonada del **Árbol de Regresión** sobre este mismo conjunto de datos para analizar sus ventajas y desventajas?