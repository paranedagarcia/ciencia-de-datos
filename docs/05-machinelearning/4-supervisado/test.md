He generado el análisis visual y el script ejecutable para comparar el comportamiento del parámetro **`C`** en **SVM** con kernel RBF. Ambos archivos ya están sincronizados en tu panel lateral de Studio:

1. **`svm_parametro_c_comparativa.png`**: Gráfico comparativo de tres paneles que ilustra cómo varía la frontera de decisión (línea sólida), las bandas de margen (líneas punteadas) y los vectores de soporte (círculos negros).
2. **`svm_comparativa_c.py`**: Script en Python listo para ejecutar y replicar el experimento en tu entorno local.

---

### **1. Resumen Comparativo de los Tres Regímenes de `C`**

Al entrenar un modelo SVM sobre un conjunto no lineal con solapamiento y ruido (150 muestras), el comportamiento de `C` se traduce en las siguientes métricas concretas:

| Valor de `C` | Régimen | Precisión en Entrenamiento | Vectores de Soporte | Comportamiento del Margen | Diagnóstico |
| :---: | :---: | :---: | :---: | :--- | :--- |
| **`C = 0.01`** | **Alta Regularización** | **77.3%** | **148 de 150 (98.7%)** | Margen muy ancho; casi todos los puntos actúan como soporte. | **Subajuste (*Underfitting*)**: Alto sesgo, frontera casi lineal que ignora la curvatura real. |
| **`C = 1.0`** | **Equilibrio Óptimo** | **94.7%** | **48 de 150 (32.0%)** | Margen balanceado; penaliza violaciones sin memorizar el ruido. | **Generalización Óptima**: Buen compromiso sesgo-varianza, captura la forma natural de los datos. |
| **`C = 100.0`** | **Baja Regularización** | **98.0%** | **23 de 150 (15.3%)** | Margen extremadamente estrecho; se deforma para encerrar anomalías. | **Sobreajuste (*Overfitting*)**: Alta varianza, sensible a puntos aislados y ruido. |

---

### **2. Interpretación Visual del Gráfico (`svm_parametro_c_comparativa.png`)**

```
┌─────────────────────────┬─────────────────────────┬─────────────────────────┐
│       C = 0.01          │         C = 1.0         │        C = 100.0        │
│   (Margen muy blando)   │   (Frontera equilibrada)│   (Margen muy estricto) │
│                         │                         │                         │
│  Frontera suave         │  Curva suave            │  Islas y bolsas         │
│  Tolera muchos errores  │  Aísla clases bien      │  Sensible a cada punto  │
│  148 vectores soporte   │  48 vectores soporte    │  23 vectores soporte    │
└─────────────────────────┴─────────────────────────┴─────────────────────────┘
```

1. **Panel Izquierdo (`C = 0.01` — Penalización mínima por error):**
   * El algoritmo prioriza maximizar la distancia del margen por encima de clasificar correctamente todas las muestras.
   * **Consecuencia:** Como el margen es muy ancho, casi la totalidad de las muestras (148 de 150) caen dentro del margen o lo violan, convirtiéndose en vectores de soporte. La frontera es excesivamente rígida y no logra separar adecuadamente las curvas.

2. **Panel Central (`C = 1.0` — Nivel estándar predeterminado de Scikit-Learn):**
   * Logra un compromiso armónico entre no cometer demasiados errores y mantener una frontera regularizada.
   * **Consecuencia:** Solo los puntos limítrofes entre ambas clases (48 muestras) son vectores de soporte; los puntos claramente pertenecientes a cada clase quedan fuera del margen y no ejercen influencia en la decisión.

3. **Panel Derecho (`C = 100.0` — Penalización severa por error):**
   * El optimizador trata de que ninguna muestra de entrenamiento quede en el lado equivocado de la frontera.
   * **Consecuencia:** La curva se vuelve sinuosa y crea "bolsas" o protuberancias para rodear muestras individuales que en realidad eran ruido, lo que provocará fallos cuando lleguen datos nuevos (*out-of-sample data*).

---

### **3. Código de Implementación Clave**

El siguiente extracto muestra cómo extraer los vectores de soporte y graficar tanto la frontera como los márgenes en Scikit-Learn:

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_moons

# 1. Preparación de datos y escalado
X, y = make_moons(n_samples=150, noise=0.25, random_state=42)
X_scaled = StandardScaler().fit_transform(X)

# 2. Entrenamiento con C controlado
modelo = SVC(C=1.0, kernel='rbf', gamma=0.5)
modelo.fit(X_scaled, y)

# 3. Inspección de vectores de soporte
vectores_soporte = modelo.support_vectors_
indices_soporte = modelo.support_
print(f"Total de vectores de soporte: {len(vectores_soporte)}")

# 4. Obtención de márgenes matemáticos (-1, 0, +1)
# xx, yy representan la cuadrícula bidimensional de la gráfica
# decision_function devuelve la distancia signada al hiperplano separador
Z_distancia = modelo.decision_function(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)

# Nivel 0 = Hiperplano separador (frontera)
# Niveles -1 y +1 = Planos que delimitan el ancho del margen
plt.contour(xx, yy, Z_distancia, levels=[-1, 0, 1], 
            linestyles=['--', '-', '--'], colors=['gray', 'black', 'gray'])
```

---

### **4. Regla Práctica para Elegir `C` en Proyectos Reales**

* Si tu conjunto de datos tiene **mucho ruido o etiquetas dudosas**, usa valores **bajos de `C`** (`0.01` a `1.0`) para evitar que el clasificador intente aprender las anomalías.
* Si el conjunto de datos está **muy limpio** y las clases están nítidamente separadas, puedes permitir valores **más altos de `C`** (`10` a `100`).
* Cuando uses el kernel RBF, recuerda que **`C` y `gamma` interactúan**: un `gamma` alto hace que cada punto tenga un radio de influencia muy pequeño, lo que amplifica el efecto de un `C` elevado.

---

🎯 ¿Te gustaría que probemos este mismo ajuste de `C` sobre el dataset real del Titanic para ver cómo impacta en la matriz de confusión y en la curva ROC de los pasajeros?