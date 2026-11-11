---
id: multicolinealidad
title: "Multicolinealidad"
sidebar_label: "📄 Multicolinealidad"
description: "Multicolinealidad"
hide_title: true
sidebar_position: 2
---

## **Multicolinealidad**

La **multicolinealidad** es una condición estadística y numérica que ocurre en modelos de regresión multivariada cuando **dos o más variables explicativas o predictoras (características / *features*) presentan una correlación lineal alta o exacta entre sí**. 

En términos algebraicos, significa que una variable predictora puede expresarse o aproximarse de manera precisa como una combinación lineal de las demás variables independientes del conjunto de datos.



### Multicolinealidad Exacta vs. Aproximada

1. **Multicolinealidad Exacta (o Perfecta):**  
   Existe cuando una o más variables son combinaciones lineales deterministas de otras.  
   *Ejemplo pedagógico:* Incluir simultáneamente en el modelo el peso medido en kilogramos ($x_1$) y el peso en libras ($x_2 = 2.20462 \cdot x_1$), o caer en la llamada «trampa de las variables ficticias» (*dummy variable trap*) al no excluir una categoría base tras aplicar *One-Hot Encoding*.

2. **Multicolinealidad Alta o Aproximada:**  
   No existe una relación matemática perfecta, pero sí una fuerte correlación lineal estocástica.  
   *Ejemplo pedagógico:* En un modelo crediticio, incluir el «ingreso mensual neto», el «ingreso anual bruto» y la «declaración de impuestos sobre la renta». Aunque no son idénticos, comparten casi la misma variabilidad e información subyacente.



### Fundamentos Matemáticos
**¿Por qué Rompe el Estimador OLS?**

Para comprender el impacto destructivo de la multicolinealidad, debemos analizar la formulación de **Mínimos Cuadrados Ordinarios (OLS)** en álgebra matricial.

El vector de coeficientes estimados $\hat{w} \in \mathbb{R}^p$ se obtiene mediante la ecuación normal:

```math
\hat{w} = (X^T X)^{-1} X^T y
```

Donde:
* $X \in \mathbb{R}^{N \times p}$ es la matriz de diseño con $N$ observaciones y $p$ variables explicativas.
* $y \in \mathbb{R}^N$ es el vector de observaciones de la variable de respuesta.
* $X^T X \in \mathbb{R}^{p \times p}$ es la matriz de dispersión (proporcional a la matriz de covarianza no centrada de los regresores).

#### Multicolinealidad Perfecta
Si una columna de $X$ es combinación lineal de otra, las columnas no son linealmente independientes. Por tanto:

```math
\text{rango}(X) < p \implies \det(X^T X) = 0
```

La matriz $X^T X$ es **singular (no invertible)**. El estimador OLS no tiene solución matemática única, existiendo un número infinito de vectores de pesos $\hat{w}$ que minimizan la suma de errores cuadráticos.

#### Multicolinealidad Alta 
**(Mal Condicionamiento / *Ill-Conditioning*)**

Cuando la colinealidad es alta pero no exacta, $\det(X^T X) \neq 0$ y la matriz técnicamente se puede invertir, pero se vuelve **mal condicionada** (*ill-conditioned*).

La matriz de varianzas y covarianzas del estimador OLS viene dada por:
```math
\text{Var}(\hat{w}) = \sigma^2 (X^T X)^{-1}
```

Donde $\sigma^2$ representa la varianza del error irreducible $\epsilon$. Al descomponer $X^T X$ en sus autovalores ($\lambda_1 \ge \lambda_2 \ge \dots \ge \lambda_p > 0$):
* A mayor correlación lineal, el autovalor más pequeño $\lambda_{\min}$ se aproxima asintóticamente a cero.

* Como los autovalores de la inversa $(X^T X)^{-1}$ son $\frac{1}{\lambda_i}$, la varianza de los coeficientes asociados se dispara:

```math
\text{Var}(\hat{w}_j) \propto \frac{1}{\lambda_{\min}} \to \infty
```
* El **número de condición** de la matriz, definido como la razón entre los extremos del espectro de autovalores $\kappa = \frac{\lambda_{\max}}{\lambda_{\min}}$, explota hacia valores gigantescos.



### Consecuencias

1. **Inestabilidad Extrema de Coeficientes:** Pequeñas fluctuaciones o perturbaciones de ruido en los datos de entrenamiento generan cambios drásticos en la magnitud e incluso provocan la **inversión de signos** en los pesos estimados.

2. **Pérdida de Interpretabilidad Estadística:** El error estándar de los coeficientes ($SE(\hat{w}_j) = \sqrt{\text{Var}(\hat{w}_j)}$) se infla desproporcionadamente. Como consecuencia, las pruebas de hipótesis individuales ($t\text{-stat} = \frac{\hat{w}_j}{SE(\hat{w}_j)}$) devuelven valores $p$ muy altos. Esto conduce a la paradoja donde **el modelo global tiene un $R^2$ alto y una prueba $F$ significativa, pero ninguna variable predictora individual resulta estadísticamente significativa**.

3. **Sobreajuste Numérico (*Overfitting*):** Aunque las predicciones dentro del conjunto de entrenamiento pueden parecer precisas, el modelo memoriza las redundancias de la muestra y pierde capacidad de generalización ante datos no vistos.


### Diagnóstico de la Multicolinealidad

Para detectar este fenómeno antes de desplegar un modelo analítico, se utilizan tres herramientas diagnósticas:

#### A. Matriz de Correlación de Pearson ($r$)
Calcula el coeficiente de correlación lineal bivariado entre cada par de características. Valores $|r| > 0.8$ o $0.85$ suelen advertir una colinealidad de cuidado.  
*Limitación:* Solo detecta relaciones lineales por pares; no identifica si una variable depende de una combinación lineal de otras tres o más variables simultáneamente.

#### B. Factor de Inflación de la Varianza (VIF - *Variance Inflation Factor*)
Es la métrica estándar por excelencia en ingeniería de características. Para cada variable predictora $x_j$, se ajusta una regresión lineal auxiliar utilizando a $x_j$ como objetivo dependiente y a las restantes $p-1$ variables como predictoras:

```math
\text{VIF}_j = \frac{1}{1 - R_j^2}
```

Donde:
* $R_j^2$ es el coeficiente de determinación de la regresión auxiliar de $x_j$ sobre las demás variables independientes.
* **Criterio de decisión:**
  * $\text{VIF} = 1$: Ausencia absoluta de colinealidad ($R_j^2 = 0$).
  * $1 < \text{VIF} < 5$: Multicolinealidad baja o moderada (tolerable en la práctica).
  * $\text{VIF} \ge 5\text{ a }10$: **Multicolinealidad severa** ($R_j^2 > 0.90$). La varianza del estimador es al menos diez veces mayor de lo que sería si las variables fuesen ortogonales.

#### C. Índice de Condición ($\kappa$)
Calculado a partir de los valores singulares ($\sigma_i$) de la matriz de diseño escalada: $\kappa = \frac{\sigma_{\max}}{\sigma_{\min}}$. Si $\kappa > 30$, la matriz se considera severamente mal condicionada.



### Estrategias de mitigación

1. **Regularización Ridge ($L_2$):** Es la solución analítica más directa. Al sumar un término $\lambda I$ en la ecuación normal ($\hat{w}_{\text{Ridge}} = (X^T X + \lambda I)^{-1} X^T y$), el espectro de autovalores se desplaza ($\lambda_i + \lambda > 0$), garantizando estabilidad numérica e invertibilidad incluso con correlación extrema.

2. **Selección y Poda de Variables (Lasso / RFE):** Lasso ($L_1$) contrae coeficientes redundantes exactamente a cero, eliminando variables colineales superfluas.

3. **Reducción de Dimensionalidad (PCA):** Transforma el espacio de variables correlacionadas en un nuevo conjunto de **componentes principales ortogonales** descorrelacionados entre sí.

4. **Ingeniería de Características:** Consolidar variables en ratios (por ejemplo, en lugar de incluir «deuda total» e «ingreso total», utilizar «ratio deuda/ingreso») o calcular promedios compuestos de variables sinérgicas.



### Demostración en Python

El siguiente script ilustra el cálculo del **Factor de Inflación de la Varianza (VIF)**, demuestra cómo la multicolinealidad genera inestabilidad numérica en OLS y cómo la **Regresión Ridge** estabiliza el modelo:

```python
"""
Módulo de Estudio: Detección y Mitigación de Multicolinealidad en Python
"""

import numpy as np
import pandas as pd
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.preprocessing import StandardScaler

# 1. Simulación de un conjunto de datos con multicolinealidad inducida
np.random.seed(42)
n_muestras = 250

# Variables base independientes
x1 = np.random.normal(loc=10, scale=2, size=n_muestras)
x2 = np.random.normal(loc=5, scale=1.5, size=n_muestras)

# x3 y x4 inducidas con altísima dependencia lineal respecto a x1 y x2
x3 = 2.5 * x1 + np.random.normal(loc=0, scale=0.1, size=n_muestras) # Colineal a x1
x4 = 1.2 * x1 + 0.8 * x2 + np.random.normal(loc=0, scale=0.05, size=n_muestras) # Combinación lineal

# Variable objetivo continua y
y = 3.0 * x1 - 2.0 * x2 + np.random.normal(loc=0, scale=1.0, size=n_muestras)

df_features = pd.DataFrame({'X1': x1, 'X2': x2, 'X3_colineal': x3, 'X4_combinada': x4})

# ==============================================================================
# 2. Diagnóstico Formal mediante VIF (Variance Inflation Factor)
# ==============================================================================
# Estandarizamos para evaluar VIF en igualdad de condiciones
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_features)

vif_data = pd.DataFrame()
vif_data["Variable"] = df_features.columns
vif_data["VIF"] = [
    variance_inflation_factor(X_scaled, i) for i in range(X_scaled.shape)
]

print("=== DIAGNÓSTICO DE MULTICOLINEALIDAD (VIF) ===")
print(vif_data.round(2).to_string(index=False))
print("\nNota: Valores de VIF > 10 señalan colinealidad crítica.\n")

# ==============================================================================
# 3. Comparativa: Inestabilidad de OLS frente a la Estabilidad de Ridge
# ==============================================================================
# Ajustamos Mínimos Cuadrados Ordinarios (OLS)
ols = LinearRegression()
ols.fit(X_scaled, y)

# Ajustamos Regresión Ridge (L2 con parámetro de contracción alpha=10.0)
ridge = Ridge(alpha=10.0, random_state=42)
ridge.fit(X_scaled, y)

# Inspección de coeficientes resultantes
df_comparativa = pd.DataFrame({
    'Variable': df_features.columns,
    'Coeficiente OLS (Inestable)': ols.coef_,
    'Coeficiente Ridge (Regularizado)': ridge.coef_
})

print("=== IMPACTO EN LOS PESOS DEL MODELO ===")
print(df_comparativa.round(4).to_string(index=False))

# Evaluación del número de condición de la matriz X^T X
matriz_dispersion = np.dot(X_scaled.T, X_scaled)
autovalores = np.linalg.eigvals(matriz_dispersion)
kappa = np.sqrt(np.max(autovalores) / np.min(autovalores))
print(f"\nNúmero de Condición del sistema (kappa): {kappa:.2f} (> 30 indica mal condicionamiento)")
```

Al ejecutar este código, el VIF de las variables $X_3$ y $X_4$ superará con creces el umbral de 10 (alcanzando cientos o miles), demostrando que OLS divide arbitrariamente el peso entre las variables colineales asignando valores con signos contrarios e inestables, mientras que la regularización Ridge redistribuye y contrae armónicamente los pesos hacia estimaciones consistentes.

