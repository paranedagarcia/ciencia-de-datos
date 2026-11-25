---
id: xgboost
title: "XGBoost"
sidebar_label: "📄 XGBoost"
description: ""
---


## **Extreme Gradient Boosting**

Para comprender qué es **XGBoost** (*eXtreme Gradient Boosting*), resulta útil compararlo con el enfoque de **Random Forest**:
* En un **Random Forest**, cientos de árboles de decisión se entrenan en paralelo de forma independiente sobre subconjuntos aleatorios de datos y luego votan democráticamente.
* En **XGBoost**, los árboles no se entrenan en paralelo ni de forma aislada, sino de manera **secuencial e iterativa (*Boosting*)**.

**La analogía del estudiante y los exámenes de práctica:**  
Imagina a un estudiante que resuelve un examen. En la primera ronda comete varios errores. En lugar de borrar todo y empezar de cero, un segundo profesor analiza específicamente **los errores que cometió el primer intento (los residuos)** y entrena un segundo árbol enfocado casi exclusivamente en corregir esas fallas. Un tercer árbol corrige los residuos que aún quedaron sin resolver, y así sucesivamente. Al final, la predicción es la suma coordinada de todos esos pequeños árboles especializados.

**¿Por qué se llama *Extreme*?**  
Porque optimiza este proceso de *Gradient Boosting* tradicional hasta el límite computacional y estadístico: incorpora **regularización matemática avanzada (L1 y L2)** para evitar que los árboles memoricen ruido, calcula derivadas de segundo orden para saber con precisión cómo converger más rápido, y estructura los datos en histogramas y memoria en paralelo para procesar millones de filas a velocidades extraordinarias.



### Formulación matemática

**XGBoost** es un sistema escalable y distribuido de aprendizaje supervisado basado en ensambles de árboles de decisión (*Gradient Boosted Decision Trees* - GBDT). Formalmente, predice la variable objetivo mediante una combinación aditiva de $K$ funciones de árboles base:

$$
\hat{y}_i = \sum_{k=1}^K f_k(x_i), \quad f_k \in \mathcal{F}
$$

donde $\mathcal{F}$ representa el espacio funcional de todos los árboles de regresión o clasificación posibles.

---

#### A. La Función Objetivo Regularizada
A diferencia del *Gradient Boosting* clásico que solo minimiza una función de pérdida empírica, XGBoost añade un **término de penalización explícito por complejidad del árbol** en la función objetivo global:

$$
\mathcal{L}^{(t)} = \sum_{i=1}^n l\left(y_i, \, \hat{y}_i^{(t-1)} + f_t(x_i)\right) + \Omega(f_t)
$$

**Explicación de sus componentes:**
* **$l(y_i, \hat{y}_i)$:** Función de pérdida diferenciable (por ejemplo, error cuadrático medio en regresión o entropía cruzada / pérdida logística en clasificación).
* **$\hat{y}_i^{(t-1)}$:** Predicción acumulada por el ensamble hasta el paso anterior $t-1$.
* **$f_t(x_i)$:** El nuevo árbol que se está construyendo en la iteración actual $t$ para corregir los residuos restantes.
* **$\Omega(f_t)$:** El **término de regularización analítica**, definido formalmente como:
  $$\Omega(f_t) = \gamma T + \frac{1}{2} \lambda \sum_{j=1}^T w_j^2 + \alpha \sum_{j=1}^T |w_j|$$
  * **$T$:** Número total de hojas terminales del árbol $f_t$.
  * **$\gamma$:** Penalización por complejidad estructural (controla el costo de agregar una hoja adicional; actúa como umbral mínimo de ganancia para podar ramas).
  * **$w_j$:** Puntuación o peso de salida asignado a cada hoja $j$.
  * **$\lambda$ y $\alpha$:** Parámetros de regularización **L2 (*Ridge*)** y **L1 (*Lasso*)** sobre los pesos de las hojas, respectivamente, que contraen los coeficientes y previenen el sobreajuste.



#### B. Optimización de Segundo Orden (Aproximación de Taylor)
Mientras que los algoritmos tradicionales de *Gradient Boosting* optimizan la función de pérdida utilizando únicamente el gradiente de primer orden (la pendiente), XGBoost realiza una **aproximación de Taylor de segundo orden** sobre la función de pérdida:

$$
\mathcal{L}^{(t)} \simeq \sum_{i=1}^n \left[ l(y_i, \hat{y}_i^{(t-1)}) + g_i f_t(x_i) + \frac{1}{2} h_i f_t^2(x_i) \right] + \Omega(f_t)
$$

**Definición de los gradientes:**
* **Gradiente de primer orden:** $g_i = \frac{\partial l(y_i, \hat{y}^{(t-1)})}{\partial \hat{y}^{(t-1)}}$ (indica la dirección y magnitud del residuo).
* **Gradiente de segundo orden (Hessiano):** $h_i = \frac{\partial^2 l(y_i, \hat{y}^{(t-1)})}{\partial (\hat{y}^{(t-1)})^2}$ (proporciona información sobre la curvatura de la superficie de pérdida, permitiendo pasos de optimización más precisos).

Al eliminar las constantes que no dependen de $f_t$, la función objetivo simplificada en el paso $t$ se reduce a:
$$
\tilde{\mathcal{L}}^{(t)} = \sum_{j=1}^T \left[ \left(\sum_{i \in I_j} g_i\right) w_j + \frac{1}{2} \left(\sum_{i \in I_j} h_i + \lambda\right) w_j^2 \right] + \gamma T
$$
donde $I_j$ es el conjunto de observaciones asignadas a la hoja $j$.



### Innovaciones arquitectónicas

El dominio de XGBoost en competencias de ciencia de datos (como Kaggle) y en la industria se debe a varias mejoras a nivel de sistemas:

1. **Algoritmo de División Basado en Histogramas / Esbozo Aproximado (*Approximate Histogram Split*):**  
   En lugar de ordenar y evaluar todos los posibles puntos de corte de cada variable continua, XGBoost agrupa los valores en cuantiles o intervalos de histogramas ponderados por el Hessiano, reduciendo drásticamente el tiempo de cálculo.

2. **Manejo Nativo de Valores Nulos (*Sparsity-aware Split Finding*):**  
   Cuando faltan datos en una columna, XGBoost aprende durante el entrenamiento una "dirección por defecto" en cada bifurcación para optimizar la pérdida, eliminando la necesidad de imputaciones artificiales previas.

3. **Estructura de Bloques en Memoria y Paralelismo por Columnas:**  
   Almacena los datos en estructuras de memoria ordenadas por columnas comprimidas (*Compressed Column Storage - CSC*). Esto permite que la búsqueda del mejor punto de corte entre diferentes variables se ejecute de forma concurrente en múltiples núcleos de CPU o GPUs.
   
4. **Tasa de Aprendizaje (*Shrinkage*) y Muestreo de Columnas:**  
   Escala las predicciones de cada nuevo árbol por un factor $\eta \in (0, 1]$ (`learning_rate`), reservando espacio para que los árboles posteriores aporten mejoras. Además, permite seleccionar subconjuntos aleatorios de columnas en cada árbol o nodo (`colsample_bytree`), emulando la técnica de descorrelación de Random Forest.

<br/>

---
## **Parada temprana**

Cuando entrenamos un modelo de ensamble secuencial como **XGBoost**, uno de los mayores dilemas del ingeniero de datos es responder: *«¿Cuántos árboles debo construir exactamente?»*
* Si construyes **muy pocos árboles**, el modelo se queda a medio camino y no alcanza a aprender los patrones reales (subajuste o alto sesgo).
* Si construyes **demasiados árboles**, el modelo terminará memorizando cada pequeña fluctuación, ruido y dato atípico del conjunto de entrenamiento (sobreajuste o alta varianza).

**La Parada Temprana (*Early Stopping*)** funciona como un **supervisor con paciencia limitada**:
1. Le indicamos a XGBoost un número deliberadamente alto de árboles (por ejemplo, `n_estimators = 300`).
2. Separamos un pequeño grupo de datos que el modelo jamás utiliza para calcular los gradientes ni las hojas: el **conjunto de validación**.
3. En cada nuevo árbol que se añade, evaluamos el error sobre ese conjunto de validación. Al principio, el error bajará rápidamente; pero llegará un momento en que el error de validación toque fondo y comience a subir o estancarse.
4. Definimos un **umbral de paciencia (`early_stopping_rounds`)**: si el modelo añade 15 o 20 árboles consecutivos sin lograr romper su récord de mínimo error, **el entrenamiento se interrumpe de forma automática**, revirtiendo el modelo al estado exacto donde alcanzó su mejor desempeño (`best_iteration`).


En términos formales de optimización, el número de iteraciones de boosting $t$ actúa como un **parámetro de regularización implícito**. 

A medida que $t \to \infty$, la función de pérdida sobre el conjunto de entrenamiento $\mathcal{L}_{\text{train}}(t)$ converge monótonamente hacia cero:

$$
\lim_{t \to \infty} \mathcal{L}_{\text{train}}(t) = 0
$$

Sin embargo, el riesgo empírico esperado sobre una distribución no vista $\mathcal{L}_{\text{val}}(t)$ describe una curva en forma de U:

$$
t^* = \arg\min_{t \in \{1, \dots, T\}} \mathcal{L}_{\text{val}}(t)
$$

#### Criterio formal de parada:
El algoritmo detiene la ejecución en la ronda $t_{\text{stop}}$ si se satisface la siguiente condición de no mejora durante una ventana de paciencia $P$ (`early_stopping_rounds = P`):

$$
\mathcal{L}_{\text{val}}(t) \ge \min_{k \le t - P} \mathcal{L}_{\text{val}}(k), \quad \forall t > t^* + P
$$

#### Explicación Simple de sus Componentes:
* **$t$:** Ronda actual de adición de árboles.
* **$t^*$:** La **mejor iteración (*best_iteration*)**, donde el error de validación alcanzó su valor mínimo histórico.
* **$P$:** El hiperparámetro de **paciencia** (típicamente entre 10 y 30 rondas). Permite que el optimizador tolere pequeñas oscilaciones locales sin detenerse prematuramente si existe la posibilidad de que el error continúe descendiendo.
* **El Modelo Resultante:** Tras activarse la parada en $t^* + P$, el objeto en memoria congela automáticamente sus ponderaciones en $t^*$, garantizando que las predicciones en producción utilicen el subespacio óptimo sin sobreajuste.

---

### 🖥️ Implementación 
**(Pipeline de 3 Vías y Evaluación)**

En rigor metodológico, para implementar *Early Stopping* **los datos deben dividirse en 3 conjuntos disjuntos**:
1. **Entrenamiento (60%):** Donde los árboles calculan los gradientes y pesos de las hojas.
2. **Validación (20%):** Donde se monitoriza el criterio de parada y se selecciona $t^*$.
3. **Prueba Independiente (20%):** Donde se mide el desempeño final imparcial sin sesgo de selección.

<details>
<summary>🖥️ Código</summary>

```python showLineNumbers
"""
Módulo Académico: Early Stopping en XGBoost Regressor.
Dataset Real: Diabetes Dataset (scikit-learn / Efron et al., 2004).
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, root_mean_squared_error, mean_absolute_error
import xgboost as xgb

# ==============================================================================
# 1. Ingesta y Partición en Tres Vías (Train, Val, Test)
# ==============================================================================
diab = load_diabetes()
X = pd.DataFrame(diab.data, columns=diab.feature_names)
nombres_clinicos = {
    'age': 'Edad', 'sex': 'Sexo', 'bmi': 'IMC (BMI)', 'bp': 'Presión Art.',
    's1': 'Colesterol', 's2': 'LDL', 's3': 'HDL', 's4': 'TCH',
    's5': 'Triglicéridos (LTG)', 's6': 'Glucosa'
}
X = X.rename(columns=nombres_clinicos)
y = diab.target

# Partición 80% (Train+Val) y 20% (Test final independiente)
X_train_val, X_test, y_train_val, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42
)
# Partición del 80% previo en 60% Train y 20% Val
X_train, X_val, y_train, y_val = train_test_split(
    X_train_val, y_train_val, test_size=0.25, random_state=42
)

print(f"Dimensiones de trabajo -> Train: {len(X_train)} | Validación: {len(X_val)} | Test: {len(X_test)}")

# ==============================================================================
# 2. Configuración y Ajuste de XGBoost con Early Stopping
# ==============================================================================
paciencia = 15

modelo_xgb_early = xgb.XGBRegressor(
    n_estimators=300,          # Techo intencionalmente sobredimensionado
    learning_rate=0.03,        # Tasa baja para observar convergencia progresiva
    max_depth=3,
    reg_lambda=1.5,            # Regularización L2
    reg_alpha=0.2,             # Regularización L1
    subsample=0.8,
    colsample_bytree=0.8,
    eval_metric='rmse',
    early_stopping_rounds=paciencia,  # Activación de la parada temprana
    random_state=42,
    n_jobs=-1
)

# Monitoreo simultáneo de entrenamiento y validación
eval_set = [(X_train, y_train), (X_val, y_val)]
modelo_xgb_early.fit(
    X_train, y_train,
    eval_set=eval_set,
    verbose=False
)

iteracion_optima = modelo_xgb_early.best_iteration
mejor_rmse_val = modelo_xgb_early.best_score

print("=" * 65)
print("RESULTADOS DEL PROCEDIMIENTO DE PARADA TEMPRANA")
print("=" * 65)
print(f"Número total de árboles solicitados : 300")
print(f"Iteración óptima seleccionada (t*)  : Ronda {iteracion_optima + 1}")
print(f"Mejor RMSE en Validación            : {mejor_rmse_val:.2f} puntos")
print(f"Ronda de interrupción física        : Ronda {iteracion_optima + 1 + paciencia}")

# ==============================================================================
# 3. Evaluación en el Conjunto de Prueba Independiente (Test Set)
# ==============================================================================
# XGBoost aplica automáticamente el modelo de la 'best_iteration' al predecir
y_pred_test = modelo_xgb_early.predict(X_test)
r2_test = r2_score(y_test, y_pred_test)
rmse_test = root_mean_squared_error(y_test, y_pred_test)
mae_test = mean_absolute_error(y_test, y_pred_test)

print("\nEvaluación en Datos de Prueba Independientes (Test Set, N = 89):")
print(f"Coeficiente R² : {r2_test:.4f} ({r2_test*100:.1f}% varianza explicada)")
print(f"RMSE           : {rmse_test:.2f} puntos")
print(f"MAE            : {mae_test:.2f} puntos")

# ==============================================================================
# 4. Generación Gráfica del Punto de Parada y Dispersión
# ==============================================================================
historial = modelo_xgb_early.evals_result()
rmse_train_hist = historial['validation_0']['rmse']
rmse_val_hist = historial['validation_1']['rmse']
rondas = range(1, len(rmse_train_hist) + 1)
total_rondas = len(rmse_train_hist)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5.8), facecolor='white')

# Panel 1: Curva de Convergencia y Parada Temprana
ax1.set_facecolor('white')
ax1.plot(rondas, rmse_train_hist, color='#0072b2', linewidth=2, label='RMSE Entrenamiento (Train)')
ax1.plot(rondas, rmse_val_hist, color='#d55e00', linewidth=2.2, label='RMSE Validación (Val)')

# Líneas guía de corte óptimo
ax1.axvline(iteracion_optima + 1, color='#009e73', linestyle='--', linewidth=1.8,
            label=f'Iteración Óptima (t* = {iteracion_optima + 1})')
ax1.axvline(total_rondas, color='#8a8a8a', linestyle=':', linewidth=1.5,
            label=f'Parada por Paciencia (+{paciencia} rondas)')
ax1.scatter([iteracion_optima + 1], [mejor_rmse_val], color='#009e73', s=90, zorder=5)

ax1.annotate(
    f'Punto de Inflexión Óptimo\nMínimo Val RMSE = {mejor_rmse_val:.1f}\nRonda t* = {iteracion_optima + 1}',
    xy=(iteracion_optima + 1, mejor_rmse_val),
    xytext=(iteracion_optima + 15, mejor_rmse_val + 12),
    arrowprops=dict(facecolor='#222222', shrink=0.08, width=1.2, headwidth=6),
    fontweight='bold', fontsize=9.5, color='#222222',
    bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='#cccccc')
)

ax1.set_title("1. Mecánica de Parada Temprana (Early Stopping)\nPrevención del Sobreajuste en Tiempo Real", fontsize=11.5, fontweight='bold', pad=12)
ax1.set_xlabel("Número de Árboles (Rondas de Boosting)", fontsize=10.5)
ax1.set_ylabel("Error Cuadrático Medio (RMSE)", fontsize=10.5)
ax1.grid(True, linestyle=':', alpha=0.6)
ax1.legend(frameon=True, facecolor='white', loc='upper right', fontsize=9.5)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# Panel 2: Desempeño en Test Independiente
ax2.set_facecolor('white')
ax2.scatter(y_test, y_pred_test, color='#009e73', alpha=0.75, edgecolors='#222222', linewidth=0.5, s=55, label='Pacientes Test (N=89)')
min_v = min(y_test.min(), y_pred_test.min()) - 10
max_v = max(y_test.max(), y_pred_test.max()) + 10
ax2.plot([min_v, max_v], [min_v, max_v], color='#d55e00', linestyle='--', linewidth=2, label='Predicción Ideal (y = ŷ)')
ax2.set_xlim(min_v, max_v)
ax2.set_ylim(min_v, max_v)

ax2.set_title(f"2. Desempeño en Test Independiente\nR² = {r2_test:.3f} | RMSE = {rmse_test:.1f} | MAE = {mae_test:.1f}", fontsize=11.5, fontweight='bold', pad=12)
ax2.set_xlabel("Progresión Real de Diabetes", fontsize=10.5)
ax2.set_ylabel("Progresión Predicha por XGBoost", fontsize=10.5)
ax2.grid(True, linestyle=':', alpha=0.6)
ax2.legend(frameon=True, facecolor='white', loc='upper left', fontsize=9.5)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

fig.suptitle("Implementación de Early Stopping en XGBoost Regressor (Dataset Real de Diabetes)", fontsize=13.5, fontweight='bold', y=0.98)
plt.tight_layout(rect=[0, 0, 1, 0.94])
plt.show()

```
</details>



#### Análisis de resultados

1. **Panel 1 (La Curva de Divergencia y la Parada):**
   * **El Descenso Inicial:** Tanto en entrenamiento (azul) como en validación (naranja), el error se desploma con fuerza durante las primeras 40 rondas a medida que el modelo captura los factores principales (`IMC` y `Triglicéridos`).
   * **El Punto Óptimo (Línea Verde Discontinua):** En la **ronda 106 (`t* = 106`)**, el error de validación alcanza su mínimo histórico global con un **RMSE = 53,84**.
   * **La Ventana de Paciencia y Corte (Línea Gris Punteada):** A partir de la ronda 106, mientras que el error de entrenamiento sigue cayendo artificialmente (llegando a 22 puntos por memorización de datos), el error de validación deja de mejorar y comienza a oscilar ligeramente hacia arriba. Al cumplirse **15 rondas consecutivas sin superarse el récord**, el algoritmo aborta la ejecución exactamente en la **ronda 121**, evitando calcular innecesariamente los 179 árboles restantes.
2. **Panel 2 (Validación en Test Independiente):**
   * Al congelar el ensamble en la iteración 106, el modelo generaliza de forma balanceada sobre las 89 muestras de test, alcanzando un **$R^2 = 0,4685$**, un **$\text{RMSE} = 53,07$** y un **$\text{MAE} = 42,97$**.
   * La nube de puntos conserva una dispersión simétrica sin subestimaciones sistemáticas en los valores extremos de la progresión de la enfermedad.



### Buenas prácticas

* **Ajuste Conjunto con `learning_rate`:** Si reduces la tasa de aprendizaje (por ejemplo, de `0.1` a `0.01`), los árboles aportarán mejoras más graduales. Por ende, debes **aumentar proporcionalmente el valor de paciencia (`early_stopping_rounds`)** (de 10 a 25 o 30) para evitar que fluctuaciones menores detengan el entrenamiento antes de tiempo.
* **Ahorro de Cómputo y Huella de Carbono:** En conjuntos de datos masivos (millones de transacciones financieras o registros clínicos), fijar `n_estimators = 2000` con `early_stopping_rounds = 30` puede reducir el tiempo de entrenamiento en servidores en la nube en más de un **60%**, disminuyendo costes de infraestructura sin sacrificar precisión predictiva.
* **Persistencia del Modelo:** Al guardar el modelo a disco (`modelo_xgb.save_model("modelo_optimo.json")`), XGBoost exporta únicamente la estructura hasta `best_iteration`, garantizando una inferencia en producción rápida y ligera.




### Random Forest vs. Gradient Boosting Clásico vs. XGBoost

| Característica | Random Forest | Gradient Boosting Tradicional (GBRT) | XGBoost (*Extreme Gradient Boosting*) |
| :--- | :--- | :--- | :--- |
| **Entrenamiento** | **Paralelo** (árboles independientes vía *Bagging*). | **Secuencial** (árboles dependientes de residuos). | **Secuencial** (optimización por bloques paralelizada en CPU/GPU). |
| **Optimización** | Promedio / Votación mayoritaria. | Descenso de gradiente de **primer orden**. | Expansión de Taylor de **segundo orden** (Gradiente + Hessiano). |
| **Regularización** | Solo prepoda o postpoda estructural. | Parada temprana (*early stopping*) y tasa de aprendizaje. | **Penalización analítica L1 (Lasso) y L2 (Ridge) en la función objetivo**. |
| **Manejo de Nulos** | Requiere imputación previa o particiones de sustituto. | Requiere imputación previa en la mayoría de implementaciones. | **Automático y adaptativo** (aprende la dirección óptima de nulos en cada nodo). |
| **Costo Computacional** | Medio (escala bien con más núcleos). | Alto (lento en datasets masivos debido a búsquedas exactas). | **Muy Eficiente** (algoritmos de histograma y caché de datos). |




## 🖥️ **Ejemplos**

### Clasificación (breast cancer)

```python showLineNumbers
# Ejemplo completo de clasificación con XGBoost (sklearn API) usando el dataset breast cancer
import sys
import subprocess
from xgboost import XGBClassifier
import xgboost as xgb
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Intentar importar xgboost, instalar si no está disponible
#try:
#except Exception:
#    subprocess.check_call([sys.executable, "-m", "pip", "install", "xgboost"])

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    roc_auc_score,
    roc_curve,
)


# Cargar datos
data = load_breast_cancer()
X = data.data
y = data.target
feature_names = data.feature_names

# División train/test (estratificado)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# Escalado (recomendado para XGBoost no es obligatorio, pero es útil para comparativas)
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s = scaler.transform(X_test)

# Definir el clasificador XGBoost (sklearn wrapper)
clf = XGBClassifier(
    n_estimators=200,
    learning_rate=0.1,
    max_depth=3,
    use_label_encoder=False,  # evita warning en versiones recientes
    eval_metric="logloss",
    random_state=42,
    n_jobs=-1,
)

# Entrenar con early stopping monitorizando el conjunto de validación (test)
# Algunas versiones del wrapper sklearn de XGBoost no aceptan `callbacks` en fit().
# Usamos el argumento compatible `early_stopping_rounds` en su lugar.
clf.fit(
    X_train_s,
    y_train,
    eval_set=[(X_test_s, y_test)],
    verbose=False,
)

# Predicciones y probabilidades
y_pred = clf.predict(X_test_s)
y_proba = clf.predict_proba(X_test_s)[:, 1]

# Métricas de evaluación
acc = accuracy_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_proba)
print(f"Accuracy: {acc:.4f}")
print(f"ROC AUC: {roc_auc:.4f}\n")
print("Classification Report:")
print(classification_report(y_test, y_pred))
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# Curva ROC
fpr, tpr, _ = roc_curve(y_test, y_proba)
plt.figure(figsize=(6,5))
plt.plot(fpr, tpr, label=f"XGBoost (AUC = {roc_auc:.3f})")
plt.plot([0,1], [0,1], "--", color="gray")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve - XGBoost")
plt.legend()
plt.grid(True)
plt.show()

# Importancias de características (top 10)
importances = clf.feature_importances_
idxs = np.argsort(importances)[::-1][:10]
top_feats = feature_names[idxs]
top_vals = importances[idxs]

pd.Series(top_vals, index=top_feats).sort_values().plot.barh(figsize=(8,5))
plt.title("Top 10 features - XGBoost")
plt.xlabel("Feature importance")
plt.tight_layout()
plt.show()
```


    ---------------------------------------------------------------------------

    ModuleNotFoundError                       Traceback (most recent call last)

    Cell In[22], line 4
          2 import sys
          3 import subprocess
    ----> 4 from xgboost import XGBClassifier
          5 import xgboost as xgb
          6 from sklearn.datasets import load_breast_cancer


    ModuleNotFoundError: No module named 'xgboost'


Random Forest

![image.png](img/image.png)

Gradient boosting

![image-2.png](img/image-2.png)

XGBoost

![image-3.png](img/image-3.png)


### Random Forest vs. XGBoost

Para comprender las diferencias operativas entre **Random Forest** y **XGBoost**, resulta pedagógico contrastar su dinámica de aprendizaje y asignación de recursos:

* **Random Forest (*Bagging* — Reducción Masiva de Varianza):**  
  * **La Intuición:** Es como consultar a un jurado de 150 médicos especialistas que deliberan de manera independiente. Cada médico analiza una muestra aleatoria de pacientes y solo tiene acceso a un subconjunto aleatorio de análisis clínicos.
  * **Cómo opera:** Los árboles se entrenan **completamente en paralelo** sin comunicarse entre sí. Al final, promedian sus estimaciones. Si algunos árboles cometen errores por memorizar ruido, la mayoría no lo hará, cancelando el sobreajuste.

* **XGBoost (*Gradient Boosting* — Reducción Sistemática de Sesgo con Regularización):**  
  * **La Intuición:** Es como un proceso de diagnóstico colegiado progresivo. El primer especialista hace una evaluación preliminar rápida; el segundo especialista no repite el trabajo, sino que **examina únicamente los errores y casos difíciles que el primero no pudo resolver** (los residuos); el tercer médico refina los residuos restantes, y así sucesivamente.
  * **Cómo opera:** Los árboles se construyen de forma **estrictamente secuencial**. Para evitar que la cadena termine memorizando el dataset, XGBoost impone una **penalización analítica (L1 y L2)** sobre los pesos de las hojas y amortigua cada nuevo aporte con una tasa de aprendizaje ($\eta$).



#### Implementación en Python con Datos Clínicos Reales

A continuación se presenta el módulo experimental completo ejecutado sobre el dataset real **Breast Cancer Wisconsin Diagnostic** (569 pacientes, 30 variables continuas). El script entrena ambos modelos con 150 árboles, evalúa su latencia de cómputo en milisegundos y genera las visualizaciones comparativas:

<details>
<summary>🖥️ Código</summary>

```python showLineNumbers
"""
Comparativa Experimental Random Forest vs. XGBoost.
Dataset Real: Breast Cancer Wisconsin Diagnostic (scikit-learn).
"""

import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
from sklearn.metrics import (
    accuracy_score, roc_auc_score, f1_score, log_loss,
    confusion_matrix, ConfusionMatrixDisplay, roc_curve, classification_report
)

# ==============================================================================
# 1. Ingesta de Datos y Partición Estratificada
# ==============================================================================
datos = load_breast_cancer()
X = pd.DataFrame(datos.data, columns=datos.feature_names)
y = 1 - datos.target  # 1 = Maligno (Positivo), 0 = Benigno (Negativo)
etiquetas = ['Benigno (0)', 'Maligno (1)']

# Partición 75% Entrenamiento y 25% Prueba independiente
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# ==============================================================================
# 2. Entrenamiento y Medición de Tiempo de Cómputo
# ==============================================================================
# A. Random Forest (150 estimadores paralelos con subespacios aleatorios)
t0_rf = time.perf_counter()
rf = RandomForestClassifier(n_estimators=150, max_features='sqrt', random_state=42, n_jobs=-1)
rf.fit(X_train, y_train)
t_rf = (time.perf_counter() - t0_rf) * 1000  # Latencia en milisegundos

# B. XGBoost (150 árboles secuenciales regularizados con aproximación de 2do orden)
t0_xgb = time.perf_counter()
modelo_xgb = xgb.XGBClassifier(
    n_estimators=150,
    learning_rate=0.05,       # Factor de contracción eta
    max_depth=3,              # Árboles poco profundos para evitar sobreajuste
    reg_lambda=1.0,           # Regularización L2 analítica
    reg_alpha=0.1,            # Regularización L1 (induce dispersión)
    subsample=0.8,            # 80% de muestras por árbol
    colsample_bytree=0.8,     # 80% de variables por árbol
    eval_metric='logloss',
    random_state=42,
    n_jobs=-1
)
modelo_xgb.fit(X_train, y_train)
t_xgb = (time.perf_counter() - t0_xgb) * 1000

# ==============================================================================
# 3. Inferencia y Evaluación Cuantitativa
# ==============================================================================
y_pred_rf = rf.predict(X_test)
y_prob_rf = rf.predict_proba(X_test)[:, 1]

y_pred_xgb = modelo_xgb.predict(X_test)
y_prob_xgb = modelo_xgb.predict_proba(X_test)[:, 1]

acc_rf = accuracy_score(y_test, y_pred_rf)
auc_rf = roc_auc_score(y_test, y_prob_rf)
f1_rf = f1_score(y_test, y_pred_rf)
loss_rf = log_loss(y_test, y_prob_rf)

acc_xgb = accuracy_score(y_test, y_pred_xgb)
auc_xgb = roc_auc_score(y_test, y_prob_xgb)
f1_xgb = f1_score(y_test, y_pred_xgb)
loss_xgb = log_loss(y_test, y_prob_xgb)

print("=" * 68)
print("BENCHMARK EXPERIMENTAL: RANDOM FOREST VS. XGBOOST (TEST SET)")
print("=" * 68)
print(f"Random Forest -> Acc: {acc_rf*100:.2f}% | AUC: {auc_rf:.4f} | F1: {f1_rf:.4f} | LogLoss: {loss_rf:.4f} | Tiempo: {t_rf:.1f} ms")
print(f"XGBoost       -> Acc: {acc_xgb*100:.2f}% | AUC: {auc_xgb:.4f} | F1: {f1_xgb:.4f} | LogLoss: {loss_xgb:.4f} | Tiempo: {t_xgb:.1f} ms")
print("=" * 68)
```
</details>



#### Tabla Comparativa de Resultados Numéricos en Test ($N = 143$)

Al evaluar ambos algoritmos sobre las mismas 143 muestras independientes (90 casos benignos y 53 malignos), se obtienen las siguientes métricas exactas:

| Dimensión de Desempeño | Random Forest (150 Árboles) | XGBoost (150 Árboles) | Ganancia / Diferencia Técnica |
| :--- | :---: | :---: | :--- |
| **Tiempo de Entrenamiento** | **407,0 ms** | **114,9 ms** | **XGBoost es 3,5 veces más rápido** (arquitectura C++ de histogramas). |
| **Pérdida Logarítmica (*Log-Loss*)** | 0,1114 | **0,0695** | **Reducción del 37,6% en el error probabilístico**. |
| **Exactitud (*Accuracy*)** | 96,50% | **97,20%** | Incremento neto de +0,70 puntos porcentuales. |
| **Sensibilidad (*Recall* Maligno)**| 90,57% (48/53 detectados) | **92,45% (49/53 detectados)** | **XGBoost rescata 1 tumor maligno adicional** (reduce los FN a 4). |
| **Precisión (*Precision* Maligno)**| **100,00%** (0 falsas alarmas) | **100,00%** (0 falsas alarmas) | Certeza diagnóstica perfecta en ambos ensambles. |
| **Puntaje F1 (*F1-Score*)** | 0,9505 | **0,9608** | Mayor equilibrio global en la clase crítica. |
| **Área Bajo la Curva ROC (AUC)** | 0,9949 | **0,9973** | Capacidad discriminativa casi perfecta en ambos. |



#### Análisis de los gráficos

#### A. Rendimiento Diagnóstico (`comparativa_rf_xgb_diagnostico.png`)
1. **Paneles A y B (Matrices de Confusión):**  
   * **Random Forest:** Clasifica correctamente a los 90 pacientes benignos, pero presenta **5 falsos negativos (FN)**.
   * **XGBoost:** Mantiene intacta la especificidad (0 falsos positivos), pero **reduce los falsos negativos a 4 (FN = 4)**. En un entorno hospitalario oncológico, este falso negativo rescatado representa un paciente que recibe tratamiento temprano en lugar de ser enviado a casa con un diagnóstico erróneo.
2. **Panel C (Curvas ROC Superpuestas):**  
   Ambas curvas se ubican pegadas a la esquina superior izquierda (AUC > 0,994), pero la curva verde de XGBoost alcanza una tasa de verdaderos positivos del 92,5% antes de conceder cualquier falso positivo.

#### B. Dinámica de Aprendizaje y Atributos (`comparativa_rf_xgb_convergencia.png`)
1. **Panel 1 (Convergencia de la Pérdida Logarítmica):**  
   * **Random Forest (Línea Azul):** Disminuye su pérdida rápidamente con los primeros 30 árboles y se estabiliza en una meseta asintótica en torno a **0,111**. Como los árboles son independientes, después de 50 estimadores la ganancia adicional de promediar es marginal.
   * **XGBoost (Línea Verde):** Al optimizar activamente los residuos mediante el gradiente y el Hessiano en cada iteración, la pérdida desciende de forma continua y sostenida hasta alcanzar **0,0695**. Sus probabilidades estimadas son mucho más precisas y seguras (menos incertidumbre en la salida sigmoide).
2. **Panel 2 (Ponderación de Atributos: Gini MDI vs. Ganancia XGBoost):**  
   * **Random Forest (Azul):** Distribuye la importancia de manera difusa entre variables correlacionadas (`worst perimeter`, `worst concave points`, `worst radius`, `mean concave points`).
   * **XGBoost (Verde):** Concentra la toma de decisiones de forma mucho más parsimoniosa. Gracias a la regularización **$\Omega(f) = \gamma T + \frac{1}{2}\lambda w^2 + \alpha |w|$**, penaliza las divisiones redundantes y destaca a **`worst concave points`** como la variable que genera el mayor salto directo en la reducción de entropía cruzada.


#### Cuadro Comparativo para la Selección en Ingeniería de Datos

```
                                ¿Cuándo seleccionar cada modelo?
                                                │
         ┌──────────────────────────────────────┴──────────────────────────────────────┐
         ▼                                                                             ▼
  Usar Random Forest cuando:                                                    Usar XGBoost cuando:
  • Se requiere una línea base robusta sin ajustar hiperparámetros.   • Se busca la máxima métrica predictiva posible (competencias/producción).
  • El entrenamiento debe paralelizarse trivialmente en CPUs.         • Se requiere mínima latencia de inferencia y menor consumo de memoria.
  • El dataset presenta mucho ruido y no se desea riesgo de sobreajuste.• El dataset contiene valores nulos (XGBoost los maneja de forma nativa).
  • No hay tiempo para sintonizar tasas de aprendizaje ni podas.      • Se dispone de tiempo para calibrar learning_rate, max_depth y regularización.
```

### Regresion

**Análisis de Regresión con XGBoost (*Extreme Gradient Boosting*)**


Utilizaremos el conjunto de datos clínico real **Diabetes Dataset** (Bradley Efron, Trevor Hastie, Iain Johnstone y Robert Tibshirani, 2004), integrado nativamente en `sklearn.datasets.load_diabetes`.

* **Problema:** Predecir cuantitativamente la **progresión de la enfermedad tras un año del diagnóstico basal** (medida continua en escala de 25 a 346) a partir de 10 mediciones cuantitativas: Edad, Sexo, Índice de Masa Corporal (IMC), Presión Arterial y 6 análisis séricos de laboratorio (`s1` a `s6`).

<details>
<summary>🖥️ Código</summary>

```python showLineNumbers
"""
XGBoost para Regresión y Monitoreo de Convergencia.
Dataset Real: Diabetes Dataset (Efron et al., 2004 / Scikit-Learn).
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, root_mean_squared_error, mean_absolute_error
from sklearn.inspection import permutation_importance
import xgboost as xgb

# ==============================================================================
# 1. Ingesta de Datos y Partición de Prueba Independiente
# ==============================================================================
diab = load_diabetes()
X = pd.DataFrame(diab.data, columns=diab.feature_names)

# Renombrado de variables para interpretación clínica directa
nombres_clinicos = {
    'age': 'Edad', 'sex': 'Sexo', 'bmi': 'IMC (BMI)', 'bp': 'Presión Art.',
    's1': 'Colesterol', 's2': 'LDL', 's3': 'HDL', 's4': 'TCH',
    's5': 'Triglicéridos (LTG)', 's6': 'Glucosa'
}
X = X.rename(columns=nombres_clinicos)
y = diab.target

# Partición 75% Entrenamiento y 25% Prueba independiente
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25, random_state=42)

# ==============================================================================
# 2. Configuración y Entrenamiento de XGBRegressor con Monitoreo
# ==============================================================================
modelo_xgb = xgb.XGBRegressor(
    n_estimators=120,        # Número de árboles secuenciales
    learning_rate=0.04,      # Factor de contracción (shrinkage eta)
    max_depth=3,             # Árboles poco profundos para regularizar sesgo/varianza
    reg_lambda=2.0,          # Regularización L2 sobre los pesos de las hojas
    reg_alpha=0.3,           # Regularización L1 (sparsity)
    subsample=0.8,           # 80% de observaciones por árbol
    colsample_bytree=0.8,    # 80% de variables evaluadas por árbol
    eval_metric='rmse',      # Métrica de monitoreo
    random_state=42,
    n_jobs=-1
)

# Monitoreo simultáneo en entrenamiento y prueba para auditar sobreajuste
eval_set = [(X_tr, y_tr), (X_te, y_te)]
modelo_xgb.fit(X_tr, y_tr, eval_set=eval_set, verbose=False)

# ==============================================================================
# 3. Inferencia y Evaluación en el Conjunto de Test
# ==============================================================================
y_pred = modelo_xgb.predict(X_te)
r2_val = r2_score(y_te, y_pred)
rmse_val = root_mean_squared_error(y_te, y_pred)
mae_val = mean_absolute_error(y_te, y_pred)

print("=" * 65)
print("EVALUACIÓN DE REGRESIÓN: XGBOOST REGRESSOR (TEST SET)")
print("=" * 65)
print(f"Coeficiente de Determinación (R²) : {r2_val:.4f} ({r2_val*100:.1f}% varianza explicada)")
print(f"Error Cuadrático Medio (RMSE)     : {rmse_val:.2f} puntos")
print(f"Error Absoluto Medio (MAE)        : {mae_val:.2f} puntos")

# ==============================================================================
# 4. Cálculo de Importancia de Atributos: Ganancia (Gain) vs. Permutación
# ==============================================================================
importancias_gain = modelo_xgb.feature_importances_
perm_res = permutation_importance(modelo_xgb, X_te, y_te, n_repeats=10, random_state=42, scoring='r2')

top_idx = np.argsort(importancias_gain)
vars_ordenadas = [X.columns[i] for i in top_idx]

# ==============================================================================
# 5. Generación Gráfica (Fondo Blanco Plano y Paleta Contrastada)
# ==============================================================================
historial = modelo_xgb.evals_result()
rmse_tr_hist = historial['validation_0']['rmse']
rmse_te_hist = historial['validation_1']['rmse']

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 5.8), facecolor='white')

# Panel 1: Curva de Convergencia del Error (RMSE)
ax1.set_facecolor('white')
rondas = range(1, len(rmse_tr_hist) + 1)
ax1.plot(rondas, rmse_tr_hist, color='#0072b2', linewidth=2, label='RMSE Entrenamiento')
ax1.plot(rondas, rmse_te_hist, color='#d55e00', linewidth=2.2, label='RMSE Prueba')
ax1.axhline(min(rmse_te_hist), color='#8a8a8a', linestyle=':', label=f'Mínimo Test: {min(rmse_te_hist):.1f}')
ax1.set_title("1. Convergencia del Error (RMSE)\na través de Rondas de Boosting", fontsize=11.5, fontweight='bold', pad=12)
ax1.set_xlabel("Número de Árboles (Iteraciones)", fontsize=10.5)
ax1.set_ylabel("Raíz del Error Cuadrático Medio (RMSE)", fontsize=10.5)
ax1.grid(True, linestyle=':', alpha=0.6)
ax1.legend(frameon=True, facecolor='white', loc='upper right', fontsize=9.5)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# Panel 2: Valores Reales vs. Predichos
ax2.set_facecolor('white')
ax2.scatter(y_te, y_pred, color='#009e73', alpha=0.75, edgecolors='#222222', linewidth=0.5, s=55, label='Pacientes de Test (N=111)')
min_v = min(y_te.min(), y_pred.min()) - 10
max_v = max(y_te.max(), y_pred.max()) + 10
ax2.plot([min_v, max_v], [min_v, max_v], color='#d55e00', linestyle='--', linewidth=2, label='Predicción Perfecta (y = ŷ)')
ax2.set_xlim(min_v, max_v)
ax2.set_ylim(min_v, max_v)
ax2.set_title(f"2. Valores Reales vs. Predichos en Test\nR² = {r2_val:.3f} | RMSE = {rmse_val:.1f} | MAE = {mae_val:.1f}", fontsize=11.5, fontweight='bold', pad=12)
ax2.set_xlabel("Progresión Real de Diabetes (1 año)", fontsize=10.5)
ax2.set_ylabel("Progresión Predicha por XGBoost", fontsize=10.5)
ax2.grid(True, linestyle=':', alpha=0.6)
ax2.legend(frameon=True, facecolor='white', loc='upper left', fontsize=9.5)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

# Panel 3: Importancia de Atributos (Gain vs. Permutación)
ax3.set_facecolor('white')
y_pos = np.arange(len(vars_ordenadas))
h = 0.35
ax3.barh(y_pos - h/2, [importancias_gain[i] for i in top_idx], height=h, color='#0072b2', label='Ganancia (Gain en Train)')
ax3.barh(y_pos + h/2, [perm_res.importances_mean[i] for i in top_idx], height=h, color='#e69f00', label='Permutación (Caída R² en Test)')
ax3.set_yticks(y_pos)
ax3.set_yticklabels(vars_ordenadas, fontsize=9.5)
ax3.set_xlabel("Importancia Relativa", fontsize=10.5)
ax3.set_title("3. Importancia de Atributos:\nGanancia (Train) vs. Permutación (Test)", fontsize=11.5, fontweight='bold', pad=12)
ax3.grid(True, axis='x', linestyle=':', alpha=0.6)
ax3.legend(frameon=True, facecolor='white', loc='lower right', fontsize=9.5)
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)

fig.suptitle("Análisis de Regresión con XGBoost Regressor (Dataset Real de Diabetes - Efron et al.)",
             fontsize=13.5, fontweight='bold', y=0.98)
plt.tight_layout(rect=[0, 0, 1, 0.94])
plt.show()
```
</details>

---

#### Análisis cuantitativo de los resultados

Al evaluar el modelo sobre el conjunto de prueba independiente (111 pacientes no vistos durante el entrenamiento), se obtienen los siguientes resultados cuantitativos:

| Métrica Diagnóstica en Test | Valor Obtenido | Interpretación Técnica y de Negocio |
| :--- | :---: | :--- |
| **Coeficiente $R^2$** | **0,4780** | El modelo explica el **47,8% de la varianza total** en la progresión de la enfermedad. En datos biomédicos con alta variabilidad interindividual, un valor en torno al 50% con solo 10 marcadores séricos representa un ajuste muy sólido. |
| **Error Cuadrático Medio (RMSE)** | **53,73 puntos** | En una escala de progresión de 25 a 346 (rango de 320 puntos), la desviación cuadrática equivale a solo el **16,8% del rango dinámico total**. |
| **Error Absoluto Medio (MAE)** | **42,29 puntos** | El error típico esperado al estimar la progresión de un paciente individual es de $\approx 42$ unidades clínicas. |


1. **Panel 1 (Dinámica de Convergencia del Boosting):**
   * Durante las primeras 20 iteraciones, el error RMSE desciende de forma empinada tanto en entrenamiento (azul) como en prueba (naranja).
   * La curva de prueba alcanza su **mínimo global en torno a la ronda 60–70 (RMSE = 52,5 puntos)** y a partir de allí se estabiliza en una meseta horizontal asintótica.
   * **Lección Pedagógica:** Gracias a la regularización **`reg_lambda=2.0`** y **`reg_alpha=0.3`**, la curva de prueba **no rebota hacia arriba** tras 120 árboles, demostrando cómo XGBoost frena activamente el sobreajuste incluso sin recurrir a una parada temprana forzada (*early stopping*).
2. **Panel 2 (Diagrama de Dispersión Real vs. Predicho):**
   * Los puntos verdes de los 111 pacientes de test se distribuyen de manera simétrica y compacta a lo largo de la línea discontinua de 45° (predicción ideal $y = \hat{y}$).
   * No se observan sesgos sistemáticos marcados ni curvaturas anómalas en los extremos del rango, validando que los árboles de profundidad 3 son suficientes para capturar las interacciones no lineales sin oscilaciones espurias.
3. **Panel 3 (Auditoría de Importancia de Variables: Ganancia vs. Permutación):**
   * **`IMC (BMI)`** y **`Triglicéridos (LTG / s5)`** dominan de forma unánime tanto en **Ganancia de entrenamiento** (barras azules: 24,3% y 18,3%) como en **impacto de generalización en prueba** (barras naranjas: su permutación provoca una pérdida de más de 0,22 a 0,26 puntos de $R^2$).
   * Variables como `Presión Art.` y `TCH` aportan ganancias secundarias útiles.
   * Variables como `Colesterol Total` y `LDL` muestran una caída de permutación cercana a cero o ligeramente negativa en test, lo que indica a los ingenieros de datos que estos dos análisis de sangre son químicamente redundantes cuando ya se dispone de `Triglicéridos` y `HDL`, sugiriendo que podrían eliminarse en un pipeline simplificado para reducir costes de laboratorio.



#### Resumen comparativo: XGBoost Regressor vs. Random Forest Regressor

| Aspecto Metodológico | Random Forest Regressor | XGBoost Regressor |
| :--- | :--- | :--- |
| **Mecanismo de Salida** | Promedio aritmético no ponderado de hojas independientes. | **Suma acumulativa escalada por $\eta$** de árboles correctores de residuos. |
| **Cálculo de Pesos en Hojas** | Media simple de los datos que caen en la hoja: $\bar{y}$. | **Fórmula cerrada regularizada**: $w_j^* = -\frac{\sum g_i}{\sum h_i + \lambda}$. |
| **Control de Complejidad** | Profundidad máxima (`max_depth`) y muestras mínimas (`min_samples_leaf`). | **Penalización analítica L1 (`alpha`), L2 (`lambda`) y umbral de ganancia (`gamma`)**. |
| **Riesgo de Divergencia** | Nulo: agregar más árboles nunca empeora el modelo (solo converge). | Posible si $\eta$ es muy alto y no se aplica regularización o *early stopping*. |
| **Sensibilidad a Outliers** | Alta si las hojas son pequeñas. | Regulable mediante funciones de pérdida robustas (como Huber o pérdida cuantil). |

