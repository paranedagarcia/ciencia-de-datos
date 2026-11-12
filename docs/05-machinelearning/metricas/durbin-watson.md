---
id: Durbin-Watson
title: "Durbin-Watson"
sidebar_label: "📄 Durbin-Watson"
hide_title: true
slug: /metricas/Durbin-Watson
---
## **Prueba de Durbin-Watson**

La **prueba de Durbin-Watson** es un contraste de hipótesis econométrico y estadístico diseñado para **detectar la presencia de autocorrelación serial de primer orden $AR(1)$ en los residuos** de un modelo de regresión lineal ajustado mediante Mínimos Cuadrados Ordinarios (OLS).

:::info[nota]
La **autocorrelación** o dependencia secuencial es una característica que consiste en que, elementos cercanos en el espacio o en el tiempo se parecen más entre sí que con respecto a elementos más lejanos, solamente por el hecho de estar cerca.​
:::

Uno de los supuestos fundamentales del teorema de Gauss-Márkov para que OLS sea el estimador lineal insesgado óptimo (BLUE) es la **independencia de las perturbaciones**:

```math
\text{Cov}(\epsilon_t, \epsilon_s) = 0 \quad \forall \; t \neq s
```

Cuando se modelan datos con ordenamiento secuencial o temporal, este supuesto suele violarse. Si los residuos están correlacionados en el tiempo, los estimadores OLS siguen siendo insesgados, pero sus errores estándar quedan severamente subestimados, inflando artificialmente las pruebas de significancia (valores $t$ y $F$) y generando conclusiones espurias.


### El estadístico $d$

Desarrollada por James Durbin y Geoffrey Watson (1950, 1951), la prueba evalúa si el término de error en el periodo actual $e_t$ depende linealmente del residuo inmediatamente anterior $e_{t-1}$ bajo un proceso autorregresivo:

```math
e_t = \rho \, e_{t-1} + v_t
```

Donde:
* $e_t = y_t - \hat{y}_t$ es el residuo empírico calculado de la regresión en el periodo $t$.
* $\rho \in [-1, 1]$ es el coeficiente de autocorrelación poblacional de primer orden.
* $v_t$ es una perturbación puramente aleatoria (ruido blanco).

El contraste formula las siguientes hipótesis estadísticas:
* **Hipótesis nula ($H_0$):** $\rho = 0$ (Ausencia de autocorrelación serial de primer orden).
* **Hipótesis alternativa ($H_1$):** $\rho \neq 0$ (Presencia de autocorrelación serial de primer orden).

El estadístico de prueba $d$ se calcula dividiendo la suma de diferencias sucesivas al cuadrado entre la suma total de cuadrados de los residuos:

```math
d = \frac{\sum_{t=2}^{T} (e_t - e_{t-1})^2}{\sum_{t=1}^{T} e_t^2}
```

*   **Explicación de argumentos:**
    *   $T$: Número total de observaciones temporales en la muestra.
    *   $e_t$: Residuo en el periodo actual.
    *   $e_{t-1}$: Residuo rezagado un periodo (lag 1).
    *   El numerador mide la variabilidad del cambio periodo a periodo de los residuos.
    *   El denominador es la suma residual de cuadrados (RSS), que actúa como término normalizador.

#### Relación Algebraica con la Autocorrelación Muestral ($r_1$)
Si expandimos el binomio del numerador y asumimos que para muestras suficientemente grandes 

```math
\sum_{t=2}^T e_t^2 \approx \sum_{t=2}^T e_{t-1}^2 \approx \sum_{t=1}^T e_t^2
```

y dado que la autocorrelación muestral de orden 1 se define como 
```math
r_1 = \frac{\sum e_t e_{t-1}}{\sum e_t^2}
```
el estadístico se simplifica a la relación asintótica:

```math
d \approx 2 (1 - r_1)
```



### Regla de Decisión 
**Rango de Interpretación**

Como $r_1 \in [-1, 1]$, el estadístico $d$ está acotado estrictamente en el intervalo **$$**:

```
                      Autocorrelación Positiva          Ausencia de           Autocorrelación Negativa
                                                      Autocorrelación
                          r₁ ➔ +1                         r₁ ➔ 0                     r₁ ➔ -1
              ◄───────────────────────────────┬───────────────────────────────►
             0.0                             2.0                             4.0
              │          │         │          │          │         │          │
              0         dL        dU                     4-dU      4-dL       4
              └─────────┴─────────┴──────────────────────┴─────────┴──────────┘
               Rechazo H₀  Zona     No rechazar H₀   Zona    Rechazo H₀
               (Positiva)  Incierta (Independencia)  Incierta (Negativa)
```

1. **$d \approx 2$ ($r_1 \approx 0$):** Los residuos son independientes; no hay evidencia de autocorrelación serial de primer orden. Como regla empírica general, valores en el rango $[1.5, 2.5]$ suelen considerarse aceptables.

2. **$d \to 0$ ($r_1 \to +1$):** Fuerte **autocorrelación positiva** (residuos consecutivos con el mismo signo y patrones de persistencia).

3. **$d \to 4$ ($r_1 \to -1$):** Fuerte **autocorrelación negativa** (los residuos alternan bruscamente de signo en cada periodo).

#### Zonas Críticas mediante Tablas de Durbin-Watson ($d_L$ y $d_U$)

A diferencia de pruebas que entregan un único valor crítico (como $z$ o $t$), la distribución exacta de $d$ depende de la matriz de diseño $X$. Durbin y Watson establecieron dos cotas críticas tabuladas para un nivel de significancia $\alpha$, tamaño de muestra $T$ y número de regresores $k$:
* **Cota inferior ($d_L$):** Si $d < d_L$, se rechaza $H_0$ (evidencia estadística de autocorrelación positiva).
* **Cota superior ($d_U$):** Si $d > d_U$, no se rechaza $H_0$ (no hay evidencia de autocorrelación).
* **Zona inconcluyente ($d_L \le d \le d_U$):** La prueba no permite decidir; se recomienda recurrir a pruebas complementarias como el **test de Breusch-Godfrey** o el test de **Ljung-Box**.



### Ejemplo en Python

El siguiente script compara dos escenarios sobre series temporales: una regresión con residuos independientes (ruido blanco) y otra con autocorrelación serial positiva inducida:

```python showLineNumbers
"""
Evaluación de Autocorrelación Residual con Durbin-Watson.
Librería: statsmodels.
"""

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.stattools import durbin_watson

np.random.seed(42)
T = 150  # Número de periodos temporales
t = np.arange(T)

# Variable explicativa: tendencia lineal
X = sm.add_constant(t)

# ==============================================================================
# Escenario A: Residuos Independientes (Ruido Blanco Gaussiano)
# ==============================================================================
epsilon_independiente = np.random.normal(loc=0, scale=5.0, size=T)
y_sin_autocorr = 20.0 + 0.8 * t + epsilon_independiente

modelo_a = sm.OLS(y_sin_autocorr, X).fit()
residuos_a = modelo_a.resid
dw_a = durbin_watson(residuos_a)

# ==============================================================================
# Escenario B: Residuos con Fuerte Autocorrelación Positiva AR(1) inducida
# ==============================================================================
epsilon_ar1 = np.zeros(T)
rho = 0.85  # Coeficiente autorregresivo severo
v = np.random.normal(loc=0, scale=3.0, size=T)

for i in range(1, T):
    epsilon_ar1[i] = rho * epsilon_ar1[i - 1] + v[i]

y_con_autocorr = 20.0 + 0.8 * t + epsilon_ar1

modelo_b = sm.OLS(y_con_autocorr, X).fit()
residuos_b = modelo_b.resid
dw_b = durbin_watson(residuos_b)

# ==============================================================================
# Resumen Diagnóstico
# ==============================================================================
print("=== DIAGNÓSTICO DE DURBIN-WATSON EN MODELOS OLS ===")
print(f"Escenario A (Residuos Independientes): d = {dw_a:.3f}  -> Próximo a 2.0 (Sin autocorrelación)")
print(f"Escenario B (Residuos con AR(1) ρ=0.85): d = {dw_b:.3f}  -> Próximo a 0.0 (Autocorrelación positiva severa)")

# Inspección directa en la tabla de resumen de statsmodels
print("\nExtracto de diagnóstico de Statsmodels (Escenario B):")
print(f"Durbin-Watson reportado en model.summary(): {modelo_b.summary2().tables.iloc}")
```
```=== DIAGNÓSTICO DE DURBIN-WATSON EN MODELOS OLS ===
Escenario A (Residuos Independientes): d = 2.158  -> Próximo a 2.0 (Sin autocorrelación)
Escenario B (Residuos con AR(1) ρ=0.85): d = 0.441  -> Próximo a 0.0 (Autocorrelación positiva severa)

Extracto de diagnóstico de Statsmodels (Escenario B):
Durbin-Watson reportado en model.summary2(): 0.441
```

**Temas clave identificados:**
1. **Contraste de hipótesis sobre $\rho$**: Evalúa formalmente la hipótesis nula de independencia residual ($\rho = 0$) frente a dependencia serial.

2. **Interpretación del rango**: El valor 2 representa independencia; desviaciones hacia 0 señalan persistencia positiva y hacia 4 alternancia negativa.

3. **Diagnóstico e implementación**: Disponible de forma nativa en los resúmenes de regresión de `statsmodels` (`durbin_watson`).
