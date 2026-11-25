"""
Ejemplo Práctico en Scikit-Learn:
Efecto del Hiperparámetro C en Máquinas de Vectores de Soporte (SVM)

Compara visualmente tres regímenes de regularización:
- C = 0.01: Subajuste (Margen amplio, alta tolerancia a errores, muchos vectores de soporte).
- C = 1.0 : Equilibrio (Frontera regularizada, balance sesgo-varianza).
- C = 100 : Sobreajuste (Penalización severa a errores, frontera sinuosa, pocos vectores de soporte).
"""

import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import make_moons
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

# 1. Generación de datos sintéticos con solapamiento/ruido
X, y = make_moons(n_samples=150, noise=0.25, random_state=42)

# 2. Escalado de características (Paso crítico en SVM)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 3. Configuración del experimento
valores_c = [0.01, 1.0, 100.0]
titulos = [
    "C = 0.01 (Alta Regularización)",
    "C = 1.0 (Regularización Moderada)",
    "C = 100.0 (Baja Regularización)"
]

fig, axes = plt.subplots(1, 3, figsize=(16, 5), sharey=True)

# Malla de puntos para dibujar las regiones de decisión
x_min, x_max = X_scaled[:, 0].min() - 0.5, X_scaled[:, 0].max() + 0.5
y_min, y_max = X_scaled[:, 1].min() - 0.5, X_scaled[:, 1].max() + 0.5
xx, yy = np.meshgrid(np.linspace(x_min, x_max, 400), np.linspace(y_min, y_max, 400))
puntos_malla = np.c_[xx.ravel(), yy.ravel()]

for ax, c_val, titulo in zip(axes, valores_c, titulos):
    # Entrenar modelo SVM con kernel RBF
    modelo = SVC(C=c_val, kernel='rbf', gamma=0.5, random_state=42)
    modelo.fit(X_scaled, y)
    
    precision = modelo.score(X_scaled, y) * 100
    n_vectores = len(modelo.support_vectors_)
    
    # Evaluar la función de decisión sobre la cuadrícula
    Z = modelo.predict(puntos_malla).reshape(xx.shape)
    decision = modelo.decision_function(puntos_malla).reshape(xx.shape)
    
    # Fondo coloreado según la predicción de clase
    ax.contourf(xx, yy, Z, alpha=0.25, cmap=plt.cm.coolwarm)
    
    # Dibujar márgenes (-1, 1) y frontera de decisión (0)
    ax.contour(xx, yy, decision, levels=[-1, 0, 1], linestyles=['--', '-', '--'],
               colors=['gray', 'black', 'gray'], linewidths=[1.0, 2.0, 1.0])
    
    # Dibujar muestras de entrenamiento
    for clase, color in zip([0, 1], ['#0072b2', '#d55e00']):
        ax.scatter(X_scaled[y == clase, 0], X_scaled[y == clase, 1],
                   c=color, label=f'Clase {clase}', edgecolors='white', s=50)
        
    # Resaltar los vectores de soporte (puntos que tocan o violan el margen)
    sv = modelo.support_vectors_
    ax.scatter(sv[:, 0], sv[:, 1], s=100, facecolors='none',
               edgecolors='black', linewidths=1.2, label=f'Vectores Soporte ({n_vectores})')
    
    ax.set_title(f"{titulo}\nPrecisión: {precision:.1f}% | Soporte: {n_vectores} puntos", fontsize=11, fontweight='bold')
    ax.set_xlabel("Característica 1")
    if ax == axes[0]:
        ax.set_ylabel("Característica 2")
        ax.legend(loc="lower left", fontsize=8)

plt.suptitle("Impacto del Hiperparámetro C en la Frontera de Decisión de SVM (Kernel RBF)", fontsize=13, fontweight='bold', y=1.02)
plt.tight_layout()
plt.show()
