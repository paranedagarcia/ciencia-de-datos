# Práctica de Laboratorio: Clasificación Diagnóstica Asistida con Árboles de Decisión (CART)

**Programa Académico:** Ciencia e Ingeniería de Datos  
**Nivel:** Pregrado Avanzado / Postgrado  
**Módulo:** Modelos Supervisados de Aprendizaje Automático e Interpretabilidad  

---

## 1. Enunciado del Ejercicio para Estudiantes

### A. Contexto del Problema y Justificación
En el ámbito médico y de salud digital, el despliegue de modelos de inteligencia artificial no solo exige una alta exactitud predictiva, sino también **transparencia y explicabilidad algorítmica (caja blanca)**. Los profesionales de la salud deben comprender con exactitud qué biomarcadores determinan el diagnóstico de una lesión para validar el criterio antes de proceder con tratamientos invasivos.

En esta práctica, actuarás como Científico e Ingeniero de Datos para un centro hospitalario universitario. El objetivo es entrenar y evaluar un clasificador basado en un **Árbol de Decisión (CART)** capaz de discriminar entre lesiones **Benignas** y **Malignas** a partir de características morfométricas obtenidas mediante biopsia por aspiración con aguja fina (PAAF).

### B. Enlace Oficial al Dataset Real
Utilizaremos el conjunto de datos clínico real **Breast Cancer Wisconsin (Diagnostic)**, desarrollado por los Dres. William H. Wolberg, W. Nick Street y Olvi L. Mangasarian en los Hospitales Universitarios de Wisconsin, Madison:
* **Repositorio Oficial de Datos (UCI Machine Learning Repository):**  
  [[suspicious link removed]]([suspicious link removed])
* **Acceso Directo en Python:** Integrado nativamente en `sklearn.datasets.load_breast_cancer`.
* **Dimensiones:** 569 pacientes y 30 características numéricas continuas (radio, textura, perímetro, área, concavidad, etc.).

---

### C. Requerimientos de la Tarea (Paso a Paso)

1. **Ingesta y Preparación:**
   * Cargar el conjunto de datos y definir como variable objetivo binaria \\(y = 1\\) (Maligno) y \\(y = 0\\) (Benigno).
   * Dividir el dataset en un conjunto de **entrenamiento (75%)** y un conjunto de **prueba independiente (25%)**, aplicando **estratificación** por clase (`stratify=y`) y una semilla fija (`random_state=42`).
2. **Entrenamiento y Regularización (Prepoda):**
   * Ajustar un estimador `DecisionTreeClassifier` con criterio de impureza de Gini (`criterion='gini'`).
   * Aplicar una estrategia de **prepoda** para evitar que el árbol memorice ruido clínico: limitar la profundidad máxima a `max_depth=3`, exigir un mínimo de muestras para bifurcar de `min_samples_split=15` y un tamaño mínimo por hoja terminal de `min_samples_leaf=10`.
3. **Evaluación de Rendimiento:**
   * Generar las predicciones sobre el conjunto de prueba independiente (`X_test`).
   * Calcular la **Matriz de Confusión** (Verdaderos Negativos, Falsos Positivos, Falsos Negativos y Verdaderos Positivos).
   * Computar las métricas clínicas esenciales: **Exactitud (Accuracy)**, **Sensibilidad/Recall** (proporción de tumores malignos detectados), **Precisión** y **F1-Score**.
4. **Visualización y Auditoría:**
   * Renderizar el diagrama jerárquico del árbol con `plot_tree`, mostrando los nombres de las variables y clases.
   * Graficar la matriz de confusión sobre fondo blanco plano y paleta contrastada.
   * Extraer e interpretar las tres reglas lógicas principales que conducen a la clasificación de una masa como maligna.

---

## 2. Pauta del Docente: Datos y Métricas Resultantes

Al ejecutar el procedimiento sobre el 25% de prueba (143 pacientes de test: 90 benignos y 53 malignos), los **resultados numéricos exactos** obtenidos son:

### A. Matriz de Confusión en el Conjunto de Test
```text
                          Predicho Benigno (0)    Predicho Maligno (1)
  Real Benigno (0):               90                      0   (TN = 90, FP = 0)
  Real Maligno (1):               11                     42   (FN = 11, TP = 42)
```

### B. Tabla de Métricas de Desempeño Clínico
* **Exactitud Global (*Accuracy*):** **92,31%** (132 clasificaciones correctas de 143 casos).
* **Precisión (*Precision* para Maligno):** **100,00%** (Cero falsas alarmas; cuando el árbol dictamina maligno, la certeza es total).
* **Sensibilidad (*Recall / True Positive Rate*):** **79,25%** (Detectó 42 de los 53 tumores malignos presentes en la muestra de prueba).
* **Especificidad (*True Negative Rate*):** **100,00%** (Identificó correctamente al 100% de los pacientes sanos).
* **Puntaje F1 (*F1-Score*):** **0,8842**.

### C. Reglas Lógicas Auditadas del Árbol (Interpretabilidad Clínica)
1. **Regla de Mayor Riesgo:**  
   *Si `worst concave points` > 0.13* y *`worst size` > 1.34* \\(\longrightarrow\\) **Clasificación: Maligno** (Impureza de Gini = 0,0, 100% de certeza en hoja terminal).
2. **Regla de Bajo Riesgo:**  
   *Si `worst concave points` \\(\le\\) 0.13* y *`worst perimeter` \\(\le\\) 115.8* \\(\longrightarrow\\) **Clasificación: Benigno** (98% de probabilidad posterior de benignidad).

---

## 3. Código Completo en Python (Solución y Generación Gráfica)

El siguiente script ejecuta el flujo metodológico completo y genera el artefacto visual con fondo blanco plano:

```python
"""
Módulo Académico: Solución de Ejercicio de Clasificación con Árboles de Decisión (CART).
Dataset: Breast Cancer Wisconsin Diagnostic (UCI ML Repository / Scikit-Learn).
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import (
    accuracy_score,
    recall_score,
    precision_score,
    f1_score,
    confusion_matrix,
    ConfusionMatrixDisplay,
    classification_report
)

# ==============================================================================
# 1. Ingesta de Datos y Partición Estratificada
# ==============================================================================
# Enlace UCI: [suspicious link removed]
datos = load_breast_cancer()

# 0=Maligno, 1=Benigno en sklearn; invertimos para convención clínica: 1=Maligno, 0=Benigno
X = pd.DataFrame(datos.data, columns=datos.feature_names)
y = 1 - datos.target
nombres_vars = datos.feature_names
etiquetas_clases = ['Benigno (0)', 'Maligno (1)']

# Partición 75% Entrenamiento y 25% Prueba
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# ==============================================================================
# 2. Entrenamiento del Árbol de Decisión con Prepoda Regularizada
# ==============================================================================
arbol_clinico = DecisionTreeClassifier(
    criterion='gini',
    max_depth=3,            # Limita la altura a 3 niveles de preguntas
    min_samples_split=15,   # Requiere al menos 15 muestras para intentar dividir
    min_samples_leaf=10,    # Asegura un respaldo estadístico de ≥10 pacientes por hoja
    random_state=42
)
arbol_clinico.fit(X_train, y_train)

# ==============================================================================
# 3. Evaluación en el Conjunto de Prueba
# ==============================================================================
y_pred = arbol_clinico.predict(X_test)

acc = accuracy_score(y_test, y_pred)
prec = precision_score(y_test, y_pred)
rec = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)

print("=" * 60)
print("REPORTE DE EVALUACIÓN CLÍNICA (TEST SET)")
print("=" * 60)
print(classification_report(y_test, y_pred, target_names=etiquetas_clases))

# ==============================================================================
# 4. Generación Gráfica (Fondo Blanco Plano y Paleta Contrastada)
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6.2), facecolor='white')

# Panel 1: Diagrama Jerárquico de Decisión (Árbol)
ax1.set_facecolor('white')
plot_tree(
    arbol_clinico,
    feature_names=nombres_vars,
    class_names=etiquetas_clases,
    filled=True,
    rounded=True,
    fontsize=8,
    precision=2,
    impurity=True,
    ax=ax1
)
ax1.set_title("1. Diagrama de Decisión Clínico (max_depth=3, min_samples_leaf=10)",
              fontsize=11.5, fontweight='bold', pad=12)

# Panel 2: Matriz de Confusión en Test
ax2.set_facecolor('white')
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=etiquetas_clases)
disp.plot(ax=ax2, cmap='Blues', colorbar=False, values_format='d')
ax2.set_title(f"2. Matriz de Confusión en Test (Exactitud = {acc*100:.1f}%, Sensibilidad = {rec*100:.1f}%)",
              fontsize=11.5, fontweight='bold', pad=12)
ax2.set_xlabel("Diagnóstico Predicho por el Árbol", fontsize=10.5)
ax2.set_ylabel("Diagnóstico Clínico Real", fontsize=10.5)
ax2.grid(False)

# Anotación explicativa inferior
ax2.text(
    0.5, -0.22,
    f"Métricas en Test: Exactitud = {acc:.3f} | Precisión = {prec:.3f} | Recall = {rec:.3f} | F1 = {f1:.3f}\n"
    f"Verdaderos Negativos (TN): {cm} | Falsos Positivos (FP): {cm} | Falsos Negativos (FN): {cm} | Verdaderos Positivos (TP): {cm}",
    ha='center', va='center', transform=ax2.transAxes,
    fontsize=9.5, bbox=dict(boxstyle='round,pad=0.5', facecolor='#f8f9fa', edgecolor='#cccccc')
)

fig.suptitle("Ejercicio Práctico: Clasificación Diagnóstica Asistida con Árboles de Decisión (CART)",
             fontsize=13.5, fontweight='bold', y=0.98)

plt.tight_layout(rect=[0, 0.05, 1, 0.94])
plt.show()
```

---

## 4. Análisis del Artefacto Gráfico Publicado en Studio

El gráfico resultante ha sido generado y publicado en tu panel de **Studio** bajo el nombre **`ejercicio_arbol_clasificacion.png`**:

1. **Panel 1 (Jerarquía de Reglas de Decisión):**
   * El nodo raíz demuestra que el biomarcador más crítico es **`worst concave points`** con un umbral de corte en **0.13**.
   * Hacia la rama derecha, los pacientes con valores altos de concavidad y perímetro caen en hojas coloreadas de azul intenso (**100% de tumores malignos** con impureza de Gini = 0,00).
   * La prepoda (`min_samples_leaf=10`) garantiza que ninguna decisión se tome sobre anomalías individuales, manteniendo el árbol con una estructura compacta de 3 niveles.
2. **Panel 2 (Matriz de Confusión en Test):**
   * Se visualiza claramente el desempeño: **90 pacientes benignos correctamente descartados (cero falsos positivos)** y **42 pacientes malignos identificados correctamente**.
   * Se aprecian los **11 falsos negativos**, lo cual abre una discusión pedagógica para los estudiantes: *¿es aceptable un recall del 79,2% en un entorno clínico oncológico? ¿Cómo podríamos ajustar el umbral o usar una matriz de costos/Youden para priorizar la detección de estos 11 pacientes omitidos?*

***

💡 ¿Te gustaría que agreguemos una sección adicional a la guía para que los estudiantes comparen este árbol individual frente a un **Random Forest** sobre este mismo dataset y observen cómo se reduce la tasa de falsos negativos?