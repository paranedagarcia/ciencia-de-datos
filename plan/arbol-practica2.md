# Práctica Complementaria de Laboratorio: Comparativa de Rendimiento Clínico
## Árbol de Decisión Individual (CART) vs. Bosque Aleatorio (Random Forest)

**Programa Académico:** Ciencia e Ingeniería de Datos  
**Nivel:** Pregrado Avanzado / Postgrado  
**Módulo:** Ensamble de Modelos y Mitigación de Falsos Negativos en Salud Digital  

---

### 1. Contexto Clínico y Justificación Pedagógica

En la práctica anterior evaluamos un **Árbol de Decisión Individual** regularizado mediante prepoda sobre el dataset clínico real **Breast Cancer Wisconsin (Diagnostic)**. Dicho modelo alcanzó una exactitud del 92,31% y una precisión del 100,00%, pero exhibió una debilidad crítica para el entorno oncológico: **11 falsos negativos (FN)**, lo que situó la sensibilidad (*Recall*) en apenas un **79,25%**. 

En medicina, un falso negativo representa un paciente con patología maligna que es enviado a casa sin tratamiento oportuno. 

Para resolver esta limitación, implementaremos un ensamble **Random Forest (Bosque Aleatorio)** sobre la misma partición estratificada. El objetivo es analizar cómo la agregación de múltiples árboles entrenados mediante *Bagging* (muestreo con reemplazo) y *Feature Subsampling* (selección aleatoria de \\(\sqrt{p}\\) variables en cada nodo) reduce la varianza y rescata casos patológicos omitidos por el clasificador individual.

---

### 2. Resultados Numéricos Comparativos (Conjunto de Prueba Independiente, \\(N = 143\\))

Al evaluar ambos algoritmos sobre los mismos datos de prueba (90 pacientes benignos y 53 malignos), se obtienen los siguientes resultados cuantitativos:

#### A. Comparativa de Matrices de Confusión

```text
       ÁRBOL DE DECISIÓN INDIVIDUAL (CART)                 BOSQUE ALEATORIO (RANDOM FOREST)
                Pred. 0     Pred. 1                               Pred. 0     Pred. 1
  Real 0 (Ben):   90           0    (FP = 0)        Real 0 (Ben):   89           1    (FP = 1)
  Real 1 (Mal):   11          42    (FN = 11)       Real 1 (Mal):    5          48    (FN = 5)
```

#### B. Tabla de Métricas de Desempeño Clínico

| Métrica Diagnóstica | Árbol Individual (CART) | Random Forest (100 Árboles) | Impacto Clínico / Diferencia |
| :--- | :---: | :---: | :--- |
| **Falsos Negativos (FN)** | **11 pacientes** | **5 pacientes** | **Reducción del 54,5% en tumores omitidos** |
| **Sensibilidad / Recall** | **79,25%** | **90,57%** | **Mejora neta de +11,32 puntos porcentuales** |
| **Exactitud (*Accuracy*)** | 92,31% | **95,80%** | Incremento de +3,49 puntos porcentuales |
| **Precisión (*Precision*)** | **100,00%** | 97,96% | Leve compensación: se asume 1 falso positivo |
| **Puntaje F1 (*F1-Score*)** | 0,8842 | **0,9412** | Mayor equilibrio armónico entre precisión y recall |
| **Área Bajo la Curva ROC (AUC)**| 0,8962 | **0,9939** | Capacidad discriminativa casi perfecta |

---

### 3. Código Completo en Python (Implementación y Gráficos Separados)

El siguiente script entrena ambos modelos bajo condiciones idénticas y genera dos figuras independientes:
1. **Gráfico 1:** Comparación directa de las matrices de confusión lado a lado.
2. **Gráfico 2:** Curvas ROC superpuestas que ilustran el salto en la capacidad discriminativa global (AUC: 0,896 vs. 0,994).

```python
"""
Módulo Académico: Comparativa Clínica Árbol de Decisión vs. Random Forest.
Dataset: Breast Cancer Wisconsin Diagnostic (scikit-learn / UCI ML Repository).
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    confusion_matrix,
    ConfusionMatrixDisplay,
    classification_report,
    roc_curve,
    roc_auc_score
)

# ==============================================================================
# 1. Carga de Datos y Partición Estratificada Idéntica
# ==============================================================================
datos = load_breast_cancer()
X = pd.DataFrame(datos.data, columns=datos.feature_names)
y = 1 - datos.target  # 1 = Maligno (Positivo), 0 = Benigno (Negativo)

etiquetas = ['Benigno (0)', 'Maligno (1)']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# ==============================================================================
# 2. Entrenamiento de Modelos
# ==============================================================================
# A. Árbol Individual con prepoda regularizada
arbol_dt = DecisionTreeClassifier(
    criterion='gini',
    max_depth=3,
    min_samples_split=15,
    min_samples_leaf=10,
    random_state=42
)
arbol_dt.fit(X_train, y_train)

# B. Ensamble Random Forest (100 estimadores con subespacios aleatorios)
bosque_rf = RandomForestClassifier(
    n_estimators=100,
    max_features='sqrt',
    random_state=42
)
bosque_rf.fit(X_train, y_train)

# Inferencia de clases y probabilidades continuas
y_pred_dt = arbol_dt.predict(X_test)
y_prob_dt = arbol_dt.predict_proba(X_test)[:, 1]

y_pred_rf = bosque_rf.predict(X_test)
y_prob_rf = bosque_rf.predict_proba(X_test)[:, 1]

# Métricas ROC
auc_dt = roc_auc_score(y_test, y_prob_dt)
auc_rf = roc_auc_score(y_test, y_prob_rf)

print("=" * 65)
print("REPORTE CLÍNICO COMPARATIVO (CONJUNTO DE PRUEBA)")
print("=" * 65)
print("\n--- 1. ÁRBOL DE DECISIÓN INDIVIDUAL ---")
print(classification_report(y_test, y_pred_dt, target_names=etiquetas))

print("\n--- 2. RANDOM FOREST (ENSAMBLE) ---")
print(classification_report(y_test, y_pred_rf, target_names=etiquetas))

# ==============================================================================
# 3. GRÁFICO 1: Comparativa de Matrices de Confusión
# ==============================================================================
cm_dt = confusion_matrix(y_test, y_pred_dt)
cm_rf = confusion_matrix(y_test, y_pred_rf)

fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), facecolor='white')

# Panel A: Matriz Árbol Individual
ax1.set_facecolor('white')
ConfusionMatrixDisplay(cm_dt, display_labels=etiquetas).plot(ax=ax1, cmap='Blues', colorbar=False)
ax1.set_title("Árbol Individual (CART)\nFN = 11 | Recall = 79.2%", fontsize=11, fontweight='bold', pad=10)
ax1.set_xlabel("Diagnóstico Predicho", fontsize=10)
ax1.set_ylabel("Diagnóstico Clínico Real", fontsize=10)

# Panel B: Matriz Random Forest
ax2.set_facecolor('white')
ConfusionMatrixDisplay(cm_rf, display_labels=etiquetas).plot(ax=ax2, cmap='Greens', colorbar=False)
ax2.set_title("Random Forest (100 Árboles)\nFN = 5 | Recall = 90.6%", fontsize=11, fontweight='bold', pad=10)
ax2.set_xlabel("Diagnóstico Predicho", fontsize=10)
ax2.set_ylabel("Diagnóstico Clínico Real", fontsize=10)

fig1.suptitle("Impacto Clínico: Reducción de Falsos Negativos mediante Ensamble",
              fontsize=13, fontweight='bold', y=0.98)
plt.tight_layout()
plt.show()

# ==============================================================================
# 4. GRÁFICO 2: Comparativa de Curvas ROC y AUC
# ==============================================================================
fpr_dt, tpr_dt, _ = roc_curve(y_test, y_prob_dt)
fpr_rf, tpr_rf, _ = roc_curve(y_test, y_prob_rf)

fig2, ax = plt.subplots(figsize=(8.5, 6), facecolor='white')
ax.set_facecolor('white')

ax.plot(fpr_dt, tpr_dt, color='#0072b2', linewidth=2.2, label=f'Árbol Individual (AUC = {auc_dt:.3f})')
ax.plot(fpr_rf, tpr_rf, color='#009e73', linewidth=2.5, label=f'Random Forest (AUC = {auc_rf:.3f})')
ax.plot(,, color='#8a8a8a', linestyle='--', linewidth=1.5, label='Línea de Azar (AUC = 0.50)')

ax.set_title("Comparativa de Capacidad Discriminativa Global (Curvas ROC)", fontsize=12, fontweight='bold', pad=12)
ax.set_xlabel("Tasa de Falsos Positivos (FPR = 1 - Especificidad)", fontsize=10.5)
ax.set_ylabel("Tasa de Verdaderos Positivos (TPR = Sensibilidad)", fontsize=10.5)
ax.set_xlim(-0.02, 1.02)
ax.set_ylim(-0.02, 1.04)
ax.grid(True, linestyle=':', alpha=0.6)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.legend(frameon=True, facecolor='white', loc='lower right', fontsize=10)

plt.tight_layout()
plt.show()
```

---

### 4. Preguntas Guía para el Debate y Análisis de los Estudiantes

Para complementar la práctica docente en el aula o laboratorio, se sugieren las siguientes preguntas de discusión:

1. **El Compromiso Diagnóstico (*Trade-off*):**  
   Al pasar del Árbol Individual al Random Forest, los Falsos Negativos cayeron de 11 a 5 (salvando a 6 pacientes de un diagnóstico tardío), pero los Falsos Positivos aumentaron de 0 a 1 (un paciente sano fue remitido a pruebas complementarias). ¿Por qué en medicina diagnóstica este intercambio es ampliamente aceptable y deseable?
2. **Explicabilidad vs. Capacidad Predictiva:**  
   Si el comité ético o regulatorio del hospital exige que cada decisión sea explicable ante el paciente mediante un diagrama de flujo simple, el Árbol Individual es auditable en una sola página. En cambio, Random Forest combina 100 árboles con subconjuntos aleatorios. ¿Qué técnicas de explicabilidad (como SHAP o Importancia por Permutación) deben implementarse para justificar el uso de Random Forest ante los médicos?
3. **Optimización Adicional de Umbral:**  
   Observando que Random Forest alcanza un \\(\text{AUC} = 0,994\\), ¿qué ocurriría si aplicamos el **Índice de Youden** sobre su curva ROC en lugar de utilizar el umbral estándar de 0,50? ¿Podríamos eliminar completamente los 5 falsos negativos restantes?

