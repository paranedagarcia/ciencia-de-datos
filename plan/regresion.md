### 1. Definición en Términos Sencillos y Simples

Imagina que tienes un gráfico de puntos donde cada punto representa una situación real: por ejemplo, la estatura de una persona frente a su peso, o los metros cuadrados de una vivienda frente a su precio de venta. Los puntos no están perfectamente alineados, sino dispersos en el espacio formando una tendencia general.

La **regresión lineal** consiste en **encontrar la mejor línea recta (o plano) que atraviese ese conjunto de puntos**.
* El objetivo es que la distancia vertical entre cada punto real y la recta sea lo más pequeña posible. Esa distancia o desviación se conoce como **residuo o error**.
* Una vez trazada esa recta óptima, el modelo funciona como una regla matemática de predicción: si conoces un dato nuevo en el eje horizontal (por ejemplo, el tamaño de una casa que acaba de salir al mercado), puedes proyectarlo sobre la recta para estimar su valor en el eje vertical (su precio esperado).

En palabras cotidianas: es el método estadístico para **estimar una cantidad continua a partir de una o varias pistas, asumiendo que la relación entre ellas sigue una proporción lineal directa**.

---

### 2. Definición Técnica y Rigurosa para Ciencia e Ingeniería de Datos

En el paradigma del **aprendizaje automático supervisado** (*supervised machine learning*) y la teoría de estimación paramétrica, la regresión lineal es un modelo que aproxima la relación condicional entre una variable escalar dependiente y continua $y \in \mathbb{R}$ (denominada respuesta o *target*) y un vector de $p$ variables explicativas o predictoras $x = [x_1, x_2, \dots, x_p]^T \in \mathbb{R}^p$ (*features* o regresores).

#### A. Formulación Estocástica del Modelo
El modelo asume formalmente que el proceso generador de datos responde a una combinación lineal de las características más una perturbación o término de error estocástico aditivo $\epsilon$:

\\[y = w_0 + w_1 x_1 + w_2 x_2 + \dots + w_p x_p + \epsilon = w_0 + w^T x + \epsilon\\]

Donde:
* **$w_0$** (a menudo denotado $\beta_0$ o $b$): Es el **término de sesgo** o intersección con el eje (*intercept*); representa el valor esperado de $y$ cuando todos los regresores son cero.
* **$w = [w_1, w_2, \dots, w_p]^T$**: Es el vector de **pesos o coeficientes de regresión**. Cada $w_j$ cuantifica el efecto marginal parcial: la variación esperada en $y$ ante un cambio unitario en $x_j$, manteniendo constantes (*ceteris paribus*) todas las demás variables.
* **$\epsilon$**: Es la variable aleatoria no observable que captura el ruido intrínseco, los errores de medición y la variabilidad no explicada por el espacio de características.

Si se absorbe el sesgo $w_0$ en el vector de parámetros extendiendo el vector de entrada con un componente constante $x_0 = 1$, la expresión compacta para una predicción puntual $\hat{y}$ es:
\\[\hat{y} = w^T x\\]

---

#### B. La Función de Coste: Mínimos Cuadrados Ordinarios (OLS)
Para entrenar el modelo sobre una muestra de $N$ observaciones $\{(x^{(i)}, y^{(i)})\}_{i=1}^N$, se define el residuo empírico como $e^{(i)} = y^{(i)} - \hat{y}^{(i)}$. 

El estimador clásico de **Mínimos Cuadrados Ordinarios** (*Ordinary Least Squares*, OLS) busca el vector de parámetros $\hat{w}$ que minimiza la **suma de los errores cuadráticos** (SSE o RSS) o el Error Cuadrático Medio (MSE):

```math
J(w) = \frac{1}{2N} \sum_{i=1}^{N} \Big(y^{(i)} - w^T x^{(i)}\Big)^2 = \frac{1}{2N} \|y - Xw\|_2^2
```

* **Explicación de argumentos:**
  * $X \in \mathbb{R}^{N \times (p+1)}$ es la **matriz de diseño**, cuyas filas corresponden a las observaciones y cuyas columnas albergan los atributos.
  * $y \in \mathbb{R}^N$ es el vector columna de observaciones reales.
  * $\|\cdot\|_2^2$ representa la norma euclidiana al cuadrado en $\mathbb{R}^N$. Elevar los residuos al cuadrado evita la cancelación entre errores positivos y negativos y penaliza de forma convexa los desvíos grandes.

---

#### C. Solución Analítica: La Ecuación Normal y su Geometría
Dado que la función de coste $J(w)$ es estrictamente convexa y cuadrática (su superficie forma un hiperparaboloide con un único mínimo global), calculando su gradiente con respecto a $w$ e igualando al vector nulo $\nabla_w J(w) = 0$, se obtiene la **Ecuación Normal**:

\\[X^T X \, \hat{w} = X^T y \implies \hat{w}_{\text{OLS}} = (X^T X)^{-1} X^T y\\]

* **Interpretación geométrica en $\mathbb{R}^N$:** El vector de observaciones reales $y$ no pertenece necesariamente al subespacio vectorial generado por las columnas de la matriz $X$ (el espacio columna $\mathcal{R}(X)$). La solución OLS $\hat{y} = X\hat{w} = X(X^T X)^{-1} X^T y$ representa la **proyección ortogonal** de $y$ sobre dicho subespacio. Como consecuencia directa de la ortogonalidad, el vector de residuos $e = y - \hat{y}$ es ortogonal a cada una de las columnas de $X$, cumpliendo $X^T e = 0$.

```
               y (Observación real en R^N)
               ▲
               │ \
               │  \  Residuo e = y - ŷ (Ortogonal al plano)
               │   \
               │    ▼
               └─────●─────────────► Espacio Columna de X: Span{x₁,..., x_p}
                    ŷ = X(X^T X)⁻¹ X^T y  (Proyección Ortogonal OLS)
```

---

#### D. Supuestos Clásicos del Modelo (Condiciones de Gauss-Márkov)
Para que el estimador OLS sea el **Mejor Estimador Lineal Insesgado** (BLUE, *Best Linear Unbiased Estimator*) con mínima varianza, deben cumplirse los supuestos de Gauss-Márkov sobre las perturbaciones:
1. **Linealidad en los parámetros:** La relación entre las variables dependientes e independientes es lineal en sus coeficientes ponderados.
2. **Exogeneidad estricta:** $\mathbb{E}[\epsilon \mid X] = 0$. El valor esperado de los errores condicionado a las características de entrada es cero (no hay correlación entre las características y el error).
3. **Homocedasticidad:** $\text{Var}(\epsilon_i \mid X) = \sigma^2$. La varianza del error es constante para cualquier observación.
4. **No autocorrelación serial:** $\text{Cov}(\epsilon_i, \epsilon_j \mid X) = 0 \quad (\forall i \neq j)$. Los errores de distintas observaciones son estadísticamente independientes entre sí.
5. **Rango completo (ausencia de multicolinealidad perfecta):** $\text{rango}(X) = p + 1 \le N$. La matriz $X^T X$ tiene rango completo y es estrictamente invertible.


---

#### E. Evaluación del Modelo y Extensiones de Regularización
El ajuste global del modelo suele cuantificarse mediante el **coeficiente de determinación ($R^2$)**:
\\[R^2 = 1 - \frac{\sum_{i=1}^N (y^{(i)} - \hat{y}^{(i)})^2}{\sum_{i=1}^N (y^{(i)} - \bar{y})^2} = 1 - \frac{\text{MSE}}{\text{Var}(y)}\\]
El cual mide la fracción de variabilidad total de $y$ que logra explicar el modelo frente a la simple predicción de la media.

Cuando se viola el supuesto de rango completo debido a alta correlación entre variables predictoras (multicolinealidad) o cuando el número de variables supera a las observaciones ($p > N$), OLS sufre de inestabilidad numérica extrema y sobreajuste. En tales circunstancias se recurre a técnicas de **regularización**:
* **Ridge ($L_2$):** Penaliza la norma $\|w\|_2^2$ de los coeficientes, contrayéndolos uniformemente hacia cero para reducir la varianza sin anularlos.
* **Lasso ($L_1$):** Penaliza la norma $\|w\|_1$, forzando a que las variables irrelevantes o colineales tengan pesos de exactamente cero, actuando como un mecanismo automático de selección de variables y parsimonia.