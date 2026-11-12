---
id: Jarque-Bera
title: "Jarque-Bera"
sidebar_label: "📄 Jarque-Bera"
hide_title: true
slug: /metricas/Jarque-Bera
---

## **Prueba de Jarque-Bera**

La **prueba de Jarque-Bera (JB)** (desarrollada por los econometristas Carlos Jarque y Anil K. Bera en 1980 y 1987) es un contraste de hipótesis de tipo ómnibus diseñado para **determinar si un conjunto de observaciones o los residuos de un modelo predictivo provienen de una distribución normal**.

A diferencia de pruebas de bondad de ajuste basadas en distancias de la función de distribución acumulada (como Kolmogorov-Smirnov o Shapiro-Wilk), Jarque-Bera evalúa directamente la forma de la distribución a través de sus momentos centrales estandarizados de orden superior: la **asimetría (*skewness*)** y la **curtosis (*kurtosis*)**.

### Rol y Función

* **El supuesto de normalidad de los residuos:** Al evaluar el ajuste de un modelo (como un modelo ARMA o de regresión), un buen ajuste se caracteriza típicamente porque sus residuos siguen una distribución normal o campana de Gauss. Si los residuos se desvían de este comportamiento, el modelo suele estar omitiendo información relevante, patrones estacionales o rezagos necesarios.

* **Presencia en las tablas de resumen:** En las tablas de evaluación de modelos (como las salidas estándar de modelos de series temporales en Python), **Jarque-Bera (JB)** se reporta como una métrica formal junto a su nivel de significancia probabilística, **Prob(JB)**.

* **Vínculo directo con Skew y Kurtosis:** La prueba de Jarque-Bera evalúa la forma de la distribución residual analizando conjuntamente dos momentos estadísticos clave reportados en la misma tabla de diagnóstico:
  1. **Asimetría (*Skew*):** Cuantifica si los errores se inclinan asimétricamente hacia la izquierda o hacia la derecha respecto al centro.

  2. **Curtosis (*Kurtosis*):** Evalúa el apuntamiento de la distribución y el grosor de sus colas.
* **Interpretación del resultado:** Si el valor **Prob(JB)** es muy bajo (por ejemplo, menor al umbral de 0,05 o 0,01), se rechaza la hipótesis de normalidad, confirmando estadísticamente que los residuos presentan asimetría o colas pesadas y que el modelo requiere revisión en su especificación o transformaciones previas.



El estadístico **Jarque-Bera (JB)** y su probabilidad en tablas de resumen de modelos vinculándolo con el sesgo y la curtosis, pero **no incluyen su formulación matemática explícita** (la suma ponderada de la asimetría al cuadrado y el exceso de curtosis con distribución asintótica $\chi^2$ con 2 grados de libertad) ni su implementación paso a paso en Python.


### Formulación Matemática y Derivación Asintótica

En una distribución normal gaussiana teórica:
1. La asimetría es nula ($S = 0$), lo que indica simetría bilateral respecto a la media.
2. La curtosis teórica es exactamente 3 ($K = 3$), lo que representa una distribución mesocúrtica. Por consiguiente, el **exceso de curtosis** es cero ($K - 3 = 0$).

#### A. Hipótesis del Contraste
* **Hipótesis nula ($H_0$):** Los datos se distribuyen normalmente ($S = 0$ y $K - 3 = 0$).
* **Hipótesis alternativa ($H_1$):** Los datos no siguen una distribución normal ($S \neq 0$ o $K - 3 \neq 0$).

#### B. Estimación de los Momentos Muestrales
Dada una muestra de $n$ observaciones $\{x_1, x_2, \dots, x_n\}$ con media muestral $\bar{x} = \frac{1}{n} \sum_{i=1}^n x_i$:

* **Asimetría muestral ($S$):**
  ```math
  S = \frac{\frac{1}{n} \sum_{i=1}^n (x_i - \bar{x})^3}{\left( \frac{1}{n} \sum_{i=1}^n (x_i - \bar{x})^2 \right)^{3/2}}
  ```
* **Curtosis muestral ($K$):**
  ```math
  K = \frac{\frac{1}{n} \sum_{i=1}^n (x_i - \bar{x})^4}{\left( \frac{1}{n} \sum_{i=1}^n (x_i - \bar{x})^2 \right)^2}
  ```

#### C. El Estadístico $JB$

Bajo el supuesto de normalidad y para muestras grandes (asintóticamente, cuando $n \to \infty$), los estimadores de asimetría y exceso de curtosis convergen a distribuciones normales independientes:

```math
S \xrightarrow{d} \mathcal{N}\left(0, \frac{6}{n}\right) \implies \frac{S}{\sqrt{6/n}} \sim \mathcal{N}(0, 1)
```
```math
(K - 3) \xrightarrow{d} \mathcal{N}\left(0, \frac{24}{n}\right) \implies \frac{K - 3}{\sqrt{24/n}} \sim \mathcal{N}(0, 1)
```

Al elevar al cuadrado cada variable estandarizada, se obtienen variables independientes con distribución chi-cuadrado con 1 grado de libertad cada una ($\chi^2(1)$). La suma de ambas variables resulta en el estadístico $JB$, el cual sigue asintóticamente una **distribución Chi-cuadrado con 2 grados de libertad ($\chi^2(2)$)**:

```math
JB = \frac{n}{6} \left( S^2 + \frac{(K - 3)^2}{4} \right) = n \left( \frac{S^2}{6} + \frac{(K - 3)^2}{24} \right)
```

*   **Explicación de los argumentos:**
    *   $n$: Tamaño muestral (número de observaciones o residuos evaluados).
    *   $S^2 / 6$: Ponderación del sesgo al cuadrado, normalizado por la varianza asintótica de la asimetría ($6/n$).
    *   $(K - 3)^2 / 24$: Ponderación del exceso de curtosis al cuadrado, normalizado por su varianza asintótica ($24/n$).

---

### Regla de Decisión y Cálculo del $p$-valor

Dado que el estadístico es una suma de cuadrados multiplicada por constantes positivas, **siempre es no negativo ($JB \ge 0$)**:
* Si los datos son estrictamente normales, $S = 0$ y $K = 3$, por lo que $JB = 0$.
* Cuanto más se alejen los datos de la simetría o de colas gaussianas, mayor será el valor de $JB$.

Para la distribución $\chi^2(2)$, el valor de probabilidad ($p$-valor o `Prob(JB)`) tiene una solución cerrada:
```math
p\text{-valor} = P(\chi^2_2 \ge JB) = 1 - F_{\chi^2_2}(JB) = \exp\left(-\frac{JB}{2}\right)
```

* **Criterio de decisión:** A un nivel de significancia típico $\alpha = 0,05$ (cuyo valor crítico en $\chi^2(2)$ es $5,99$):
  * Si $JB > 5,99$ (o $p\text{-valor} < 0,05$), **se rechaza la hipótesis nula $H_0$**: existe evidencia estadística concluyente de que los residuos no son normales.
  * Si $JB \le 5,99$ (o $p\text{-valor} \ge 0,05$), **no se rechaza $H_0$**: los residuos son compatibles con una distribución normal.

---

### Implementación en Python

El siguiente código muestra cómo calcular la prueba de Jarque-Bera utilizando tanto `scipy.stats` como `statsmodels`, comparando una muestra gaussiana frente a una muestra con colas pesadas:

```python showLineNumbers
"""
Evaluación de Normalidad con la Prueba de Jarque-Bera (JB).
Librerías: scipy.stats y statsmodels.
"""

import numpy as np
from scipy import stats
from statsmodels.stats.stattools import jarque_bera

np.random.seed(42)
n_muestras = 1500

# ==============================================================================
# 1. Caso A: Distribución Normal (H0 verdadera)
# ==============================================================================
datos_normales = np.random.normal(loc=0.0, scale=1.0, size=n_muestras)

# Cálculo mediante scipy.stats
res_scipy = stats.jarque_bera(datos_normales)
print("=== CASO A: DATOS CON DISTRIBUCIÓN NORMAL ===")
print(f"Estadístico JB: {res_scipy.statistic:.4f}")
print(f"p-valor:        {res_scipy.pvalue:.4f}  (p >= 0.05 -> No se rechaza normalidad)\n")

# ==============================================================================
# 2. Caso B: Distribución No Normal con Colas Pesadas (t-Student df=3)
# ==============================================================================
datos_t = np.random.standard_t(df=3, size=n_muestras)

# Cálculo mediante statsmodels (desglosa estadístico, p-valor, sesgo y curtosis)
jb_val, p_val, skew, kurtosis = jarque_bera(datos_t)
print("=== CASO B: DATOS CON COLAS PESADAS (t-Student df=3) ===")
print(f"Estadístico JB:     {jb_val:.2f}")
print(f"p-valor:            {p_val:.4e} (p < 0.05 -> Se rechaza normalidad)")
print(f"Asimetría (Skew):   {skew:.3f}   (Normal esperada = 0.0)")
print(f"Curtosis (Kurt):    {kurtosis:.3f}  (Normal esperada = 3.0)")
```
```=== CASO A: DATOS CON DISTRIBUCIÓN NORMAL ===
Estadístico JB: 1.1095
p-valor:        0.5742  (p >= 0.05 -> No se rechaza normalidad)

=== CASO B: DATOS CON COLAS PESADAS (t-Student df=3) ===
Estadístico JB:     55291.36
p-valor:            0.0000e+00 (p < 0.05 -> Se rechaza normalidad)
Asimetría (Skew):   1.280   (Normal esperada = 0.0)
Curtosis (Kurt):    32.633  (Normal esperada = 3.0)
```




