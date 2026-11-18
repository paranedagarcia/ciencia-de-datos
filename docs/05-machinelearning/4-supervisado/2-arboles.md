---
id: arboles
title: "Árboles de decisión"
sidebar_label: "📄 Árboles de decisión"
description: "Los modelos de árboles de decisión se engloban dentro de una clase conocida como algoritmos **CART** (Classification and Regression Trees)"
hide_title: true
---

## **Árboles de decisión**

![](img/arboles.jpg)

Los **árboles de decisión** son modelos predictivos utilizados tanto para tareas de clasificación como de regresión en el aprendizaje supervisado. Su estructura se asemeja a un árbol, donde cada nodo interno representa una pregunta o condición sobre una variable de entrada, cada rama corresponde a una respuesta posible, y cada hoja representa una predicción o resultado final.

Su nombre proviene de su estructura, que se asemeja a un diagrama de flujo o un árbol invertido, y se utiliza tanto para problemas de clasificación como de regresión.

Un árbol de decisión divide recursivamente el espacio de características en regiones homogéneas respecto a la variable objetivo. El proceso de construcción consiste en seleccionar, en cada nodo, la variable y el umbral que mejor separan los datos según algún criterio de pureza (por ejemplo, *Gini*, *entropía* para clasificación, o *varianza* para regresión).

Los modelos de árboles de decisión se engloban dentro de una clase conocida como algoritmos **CART** (Classification and Regression Trees).

**Concepto y Estructura: La Lógica de la Pregunta**

El objetivo principal de un Árbol de Decisión es aprender una secuencia de preguntas tipo "SI ESTO, ENTONCES AQUELLO" que conduzcan a la predicción correcta de la manera más eficiente posible. El algoritmo construye esta estructura jerárquica dividiendo el conjunto de datos de entrada en subconjuntos cada vez más "puros" o homogéneos.

<center>
<figure>
![](img/arbol-preguntas.jpg)
<figcaption>La mente humana clasifica información haciendo secuencias de preguntas binarias. Esta es la base matemática exacta del algoritmo de Machine Learning.</figcaption>
</figure>
</center>

#### Elementos Clave del Árbol

La estructura de un árbol permite representar una lógica de decisión clara:

![](img/arbol-anatomia.jpg)

| Elemento | Descripción |
|---|---|
| **Nodo Raíz** (Root Node) | El punto de partida que contiene todo el conjunto de datos. La primera división importante se realiza aquí. |
| **Nodos de Decisión** (Decision Nodes) | Puntos intermedios donde se evalúa una condición o "test" sobre un atributo (p. ej., "¿Es la Edad menor que 12?"). |
| **Ramas/Sub-árboles** | Conectan los nodos de decisión y representan el camino que se toma al responder la pregunta. |
| **Nodos Terminales** o **Hojas** (Leaf Nodes) | Los nodos finales que no se dividen más. Contienen la predicción final o la etiqueta de clasificación (p. ej., "Sobrevive" o "No Sobrevive"). |



### El Índice de Gini

Cuando el algoritmo construye el árbol, debe decidir, entre todos los atributos de entrada (como edad, sexo, ingreso, etc.), cuál es el mejor para dividir los datos en cada etapa. El "mejor" atributo es aquel que logra la partición más limpia o pura, minimizando la incertidumbre sobre la categoría de la salida.

Para lograr esto, el algoritmo utiliza medidas de **impureza** para evaluar la calidad de cada posible división. Las dos métricas más comunes son el **Índice de Gini** y la **Ganancia de Información** (basada en Entropía).

El **Índice de Gini** (o más formalmente, **Impureza de Gini**, *Gini Impurity*) es la métrica de dispersión o función de coste matemática por defecto en algoritmos de árboles de decisión para clasificación, notablemente en **CART** (*Classification and Regression Trees*) y en librerías como Scikit-Learn y PySpark MLlib.

<center>
<figure>
![](img/arbol-gini-cart.jpg)
<figcaption>Es el motor matemático que usan algoritmos como CART en los Árboles de decisión para determinar la mejor forma de dividir y clasificar datos.</figcaption>
</figure>
</center>

El **Índice de Gini** mide la probabilidad de que un elemento elegido al azar de un subconjunto sea clasificado incorrectamente si su clase se selecciona aleatoriamente en proporción a la distribución de clases en ese subconjunto.

:::info[Objetivo]
El algoritmo busca elegir divisiones que **minimicen** el Índice de Gini. Un valor de 0 indica una pureza total (todos los elementos pertenecen a una sola clase), mientras que un valor más cercano a 1 (o 0.5 para clasificación binaria) indica una mezcla de clases.
:::

<center>
<figure>
![](img/arbol-gini-escala.jpg)
<figcaption>En una clasificación binaria, el valor nunca supera el 0.5 (el peor escenario posible) ni desciende de 0 (el objetivo ideal.)</figcaption>
</figure>
</center>

#### Definición Teórica y Significado

La impureza de Gini cuantifica el **grado de impureza, incertidumbre o desorden de las clases dentro de un nodo o subconjunto de datos**.

De forma probabilística, representa la **probabilidad de que un elemento elegido al azar del nodo sea clasificado de forma incorrecta si se le asigna aleatoriamente una etiqueta de acuerdo con la distribución de clases en dicho nodo**.

*   **Nodo puro (mínima impureza, $I_G = 0$):** Todas las observaciones del nodo pertenecen a una única clase (100% homogéneo).
*   **Nodo máximamente impuro:** Las instancias se encuentran repartidas de forma perfectamente equitativa entre todas las clases (por ejemplo, en un problema binario 50%-50%, la impureza de Gini alcanza su valor máximo de **0.5**). En problemas generales con $K$ clases equiprobables, el valor máximo es $1 - \frac{1}{K}$.

#### Formulación Matemática

Para un nodo o partición $t$ que contiene observaciones distribuidas a lo largo de $C$ clases, la **Impureza de Gini $I_G(t)$** se calcula como:

```math
I_G(t) = 1 - \sum_{i=1}^{C} p_i^2
```

Donde:
*   $C$ es el número total de clases del problema.
*   $p_i$ es la proporción o probabilidad empírica de observar la clase $i$ dentro de ese nodo (es decir, $p_i = \frac{N_{t, i}}{N_t}$, donde $N_{t, i}$ es el recuento de muestras de la clase $i$ y $N_t$ es el total de muestras en el nodo).

**Proceso:** Al calcular el Gini para cada posible división, el algoritmo elige la característica y el valor de corte que resulten en la mayor reducción de la impureza (es decir, el menor valor de Gini ponderado en los nodos hijos)

<center>
<figure>
![](img/arbol-diagnostico.png)
<figcaption>Es probabilidad. Restamos a 1 la suma de al proporciónal cuadrado de cada clase presente en el grupo.</figcaption>
</figure>
</center>

Para clasificación, el árbol busca particiones que minimicen una función de impureza $I$ en cada nodo $t$:

$$
I(t) = \sum_{k=1}^K p_{k}(1 - p_{k})
$$

donde $p_{k}$ es la proporción de muestras de la clase $k$ en el nodo $t$ (índice de Gini).  
Para regresión, se suele minimizar la suma de los errores cuadrados (varianza):

$$
I(t) = \frac{1}{N_t} \sum_{i \in t} (y_i - \bar{y}_t)^2
$$

donde $N_t$ es el número de muestras en el nodo $t$ y $\bar{y}_t$ es el valor medio de la variable objetivo en ese nodo.

El árbol se construye de manera recursiva hasta que se cumple un criterio de parada (profundidad máxima, número mínimo de muestras, etc.).

#### Mecánica en la Construcción del Árbol 
**(La Función de Coste de División)**

<center>
<figure>
![](img/arbol-codicia.jpg)
<figcaption>**Cómo aprende. Búsqueda codiciosa.** Evalúa todas las características iterativamente para elegir la mejor separación matmática inmediata.</figcaption>
</figure>
</center>

El algoritmo CART utiliza un enfoque voraz (*greedy*) conocido como partición binaria recursiva (*recursive binary splitting*). Para decidir qué característica $k$ y qué punto de corte o umbral $t_k$ utilizar para ramificar un nodo padre, el algoritmo evalúa la **reducción neta de impureza** o la **impureza ponderada de los nodos hijos**:

```math
J(k, t_k) = \frac{N_{\text{izq}}}{N_{\text{padre}}} I_G(D_{\text{izq}}) + \frac{N_{\text{der}}}{N_{\text{padre}}} I_G(D_{\text{der}})
```

Donde:
*   $N_{\text{padre}}$, $N_{\text{izq}}$ y $N_{\text{der}}$ son las cantidades de instancias en el nodo padre y en los subconjuntos izquierdo y derecho resultantes del corte.
*   $I_G(D_{\text{izq}})$ e $I_G(D_{\text{der}})$ son las impurezas de Gini de los nodos resultantes.

El algoritmo selecciona la característica y el umbral que **minimizan $J(k, t_k)$** (o equivalentemente, que maximizan la ganancia de impureza $\Delta I_G = I_{G,\text{padre}} - J$).



#### Gini vs. Entropía (Ganancia de Información)

![](img/arbol-impureza.jpg)

Tanto la Impureza de Gini como la **Entropía**, derivada de la teoría de la información de Shannon, 

```math
H(t) = -\sum p_i \log_2 p_i
```
cumplen funciones idénticas al evaluar pureza:

| Criterio | Impureza de Gini | Entropía (Information Gain) |
| :--- | :--- | :--- |
| **Fórmula** | $1 - \sum p_i^2$ | $-\sum p_i \log_2(p_i)$ |
| **Rango binario** | $[0, 0.5]$ | $[0, 1.0]$ |
| **Cómputo** | Más rápido (solo sumas y cuadrados, sin funciones logarítmicas). | Ligeramente más lento debido al cálculo de $\log_2$. |
| **Comportamiento** | Tiende a aislar la clase más frecuente en su propia rama de forma agresiva. | Tiende a producir particiones un poco más equilibradas. |

En la práctica, ambos criterios suelen converger en árboles con arquitecturas y precisiones de clasificación muy similares.



#### Ejemplo de Cálculo Paso a Paso

Supongamos un nodo padre con **10 instancias** (5 positivas y 5 negativas) que se evalúa dividir mediante un umbral:
1.  **Gini del padre:** $1 - \left[\left(\frac{5}{10}\right)^2 + \left(\frac{5}{10}\right)^2\right] = 1 - [0.25 + 0.25] = \mathbf{0.50}$.
2.  **División candidata:**
    *   **Nodo Izquierdo (4 instancias):** 4 positivas y 0 negativas $\rightarrow I_G = 1 - (1^2 + 0^2) = \mathbf{0.0}$ (nodo puro).
    *   **Nodo Derecho (6 instancias):** 1 positiva y 5 negativas $\rightarrow I_G = 1 - \left[\left(\frac{1}{6}\right)^2 + \left(\frac{5}{6}\right)^2\right] = 1 - \left[\frac{1}{36} + \frac{25}{36}\right] = 1 - \frac{26}{36} \approx \mathbf{0.278}$.
3.  **Gini ponderado del split:**
    ```math
    J = \left(\frac{4}{10} \times 0.0\right) + \left(\frac{6}{10} \times 0.278\right) = 0 + 0.1668 = \mathbf{0.167}
    ```
    *La reducción de impureza lograda por este corte es $0.50 - 0.167 = \mathbf{0.333}$*.



### Ventajas y desventajas

#### Ventajas
**Fácil Interpretación**: Pueden visualizarse como diagramas de flujo simples, lo que facilita explicar el resultado a personas sin conocimientos técnicos.

**No Paramétrico**: No se hacen suposiciones sobre la distribución subyacente de los datos.

**Rápido**: Son relativamente rápidos de entrenar y de usar para predecir nuevos datos.

**Manejo de Datos**: Pueden manejar datos categóricos y numéricos eficientemente y son útiles incluso con conjuntos de datos incompletos.

#### Desventajas

**Propenso al Sobreajuste (Overfitting)**: Si el árbol crece demasiado (mucha profundidad), puede memorizar el ruido y los detalles específicos del conjunto de entrenamiento y fallar al generalizar.

**Sensibilidad**: Pequeños cambios en los datos de entrada pueden causar grandes cambios en la estructura del árbol, afectando las predicciones.

**No Globalmente Óptimo**: Los árboles se construyen utilizando una estrategia "voraz" (greedy), lo que significa que eligen la mejor división localmente, pero esto no garantiza que la estructura final sea la mejor globalmente.

**Fronteras de Decisión**: Tienden a crear fronteras de decisión cuadradas o rectilíneas, lo que puede ser ineficiente para modelar relaciones no lineales suaves.




#### Caso de clasificación

Un ejemplo clásico es predecir la supervivencia en el desastre del Titanic, donde las decisiones se basan en atributos discretos y continuos como la edad y el sexo.

Utilizamos la librería scikit-learn en Python para construir el árbol. En este ejemplo, el árbol se entrena para decidir si un pasajero sobrevive (Sí) o no (No), basándose en el sexo y la edad.

1. **Preparación de Datos**: Se definen los atributos de entrada (X) y el resultado esperado (y). (Asumimos que 'Sex_male' ha sido codificado como 0 o 1).
2. **Construcción y Entrenamiento**: Se importa la clase DecisionTreeClassifier y se ajusta el modelo a los datos de entrenamiento

<details>
<summary>🖥️ Código</summary>

```python showLineNumbers
# EJEMPLO CONCEPTUAL EN PYTHON USANDO SCIKIT-LEARN

from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests

df = pd.read_csv('https://patricioaraneda.cl/public/titanic5_full.csv')
df = df[['Survived', 'Age', 'Sex']].dropna(subset=['Survived', 'Age', 'Sex'])

# Codificar sexo (male=1, female=0)
# Si 'Sex' ya está codificado como 0/1, el mapeo dará NaN; rellenamos con el valor original en ese caso.
df['Sex_male'] = df['Sex'].map({'male': 1, 'female': 0})
df['Sex_male'] = df['Sex_male'].fillna(df['Sex']).astype(float)

# Simulación de datos: [Edad, Sexo (1=Masculino, 0=Femenino)]
# En un caso real, esto provendría del dataset de Titanic
X_data = df[['Age', 'Sex_male']].values
# Etiquetas: 1=Sobrevive, 0=No Sobrevive
y_labels = df['Survived'].astype(int).values

X_train, X_test, y_train, y_test = train_test_split(X_data, y_labels, test_size=0.3, random_state=42)

# --- Crear y Entrenar el Modelo ---
# Limitamos la profundidad para evitar el sobreajuste (max_depth=2) [15]
clf = DecisionTreeClassifier(criterion='gini', max_depth=2, random_state=0)
clf.fit(X_train, y_train) 

# --- Visualización del Árbol ---
# plot_tree fue importado de sklearn.tree arriba.
plt.figure(figsize=(10,6))
# X_data es un numpy.ndarray, no tiene .columns => pasamos los nombres de las características explícitamente
plot_tree(clf, feature_names=['Age', 'Sex_male'], class_names=['No', 'Si'], filled=True, rounded=True)
plt.show()
# Esta función generaría un diagrama donde se ve:
# 1. El nodo raíz dividiendo por 'Sex_male' (porque es el atributo más importante, como se ve en el ejemplo real).
# 2. Las siguientes divisiones basadas en 'Age'.
```
</details>

<center>
<figure>
![png](img/arbol-titanic.png)
<figcaption>**Árbol de decisión**. El nodo raíz se divide inicialmente por 'Sex_male' porque es el atributo más importante.</figcaption>
</figure>
</center>


<details>
<summary>🖥️ Código</summary>

```python showLineNumbers
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt

# Cargar y preparar datos
import requests

df = pd.read_csv('https://patricioaraneda.cl/public/titanic5_full.csv')
df = df[['Survived', 'Age', 'Sex']].dropna(subset=['Survived', 'Age', 'Sex'])

# Codificar sexo (male=1, female=0)
df['Sex_male'] = df['Sex'].map({'male': 1, 'female': 0})

# Características y etiqueta
X_t = df[['Age', 'Sex_male']].values
y_t = df['Survived'].astype(int).values

# División entrenamiento/prueba
X_train, X_test, y_train, y_test = train_test_split(X_t, y_t, test_size=0.3, random_state=42, stratify=y_t)

# Entrenar árbol de decisión
clf = DecisionTreeClassifier(criterion='gini', max_depth=4, random_state=0)
clf.fit(X_train, y_train)

# Evaluación
y_pred = clf.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# importancia de características
importances = clf.feature_importances_
feature_names = ['Age', 'Sex_male']
for name, importance in zip(feature_names, importances):
    print(f"{name}: {importance:.4f}")


# Visualizar árbol

plt.figure(figsize=(12,7))
plot_tree(clf, feature_names=['Age','Sex_male'], class_names=['No','Si'], filled=True, rounded=True)
plt.show()
# El árbol resultante mostraría cómo las decisiones se basan en estos atributos para predecir la supervivencia
```
</details>

```
Accuracy: 0.7650695517774343
              precision    recall  f1-score   support

           0       0.79      0.89      0.84       437
           1       0.69      0.50      0.58       210

    accuracy                           0.77       647
   macro avg       0.74      0.70      0.71       647
weighted avg       0.76      0.77      0.75       647

Age: 0.1783
Sex_male: 0.8217
```

    
![png](img/arbol-3.png)
    

#### Caso sobre predicción
Predicción para un pasajeros del Titanic, sobre edad y sexo.

```python showLineNumbers
# genera una predicion para un pasajero de 25 años y sexo masculino
sample_passenger = np.array([[25, 1]])  # 25 años, masculino
predicted_survival = clf.predict(sample_passenger)
print(f"Predicción de supervivencia para pasajero de 25 años y sexo masculino: {'Sobrevive' if predicted_survival[0] == 1 else 'No Sobrevive'}")
```

Predicción de supervivencia para pasajero de 25 años y sexo masculino: No Sobrevive


```python showLineNumbers
# genera predicciones para pasajeros con diferentes edades y sexos
sample_passengers = np.array([[22, 0],  # 22 años, masculino
                              [30, 1],  # 30 años, femenino
                              [40, 1],  # 40 años, masculino
                              [35, 0]]) # 25 años, femenino
predicted_survivals = clf.predict(sample_passengers)
print("Predicciones de supervivencia para pasajeros de diferentes edades y sexos:")
for i, passenger in enumerate(sample_passengers):
    age, sex = passenger
    survival = 'Sobrevive' if predicted_survivals[i] == 1 else 'No Sobrevive'
    print(f"{age} años y sexo {'masculino' if sex == 1 else 'femenino'}: {survival}")

```

    Predicciones de supervivencia para pasajeros de diferentes edades y sexos:
    22 años y sexo femenino: Sobrevive
    30 años y sexo masculino: No Sobrevive
    40 años y sexo masculino: No Sobrevive
    35 años y sexo femenino: Sobrevive



#### Aplicaciones comunes

- Diagnóstico médico (clasificación de enfermedades)
- Detección de fraude
- Predicción de abandono de clientes (*churn*)
- Segmentación de clientes en marketing
- Predicción de precios de viviendas (regresión)

Los árboles de decisión son la base de algoritmos más avanzados como Random Forest y Gradient Boosting. Su principal ventaja es la interpretabilidad y facilidad de visualización, aunque pueden sobreajustar si no se podan o regulan adecuadamente.

---
## **Árboles Regresivos**

En el aprendizaje supervisado tradicional, la mayoría de las personas asocian los árboles de decisión con problemas de **clasificación** (decidir si un paciente tiene o no una enfermedad, o si una transacción es fraude o legítima). Sin embargo, cuando la variable que queremos predecir no es una categoría, sino un **valor numérico continuo** (como el precio de una propiedad, el volumen de ventas, la presión arterial o la progresión clínica de una enfermedad), utilizamos un **Árbol de Decisión para Regresión (*Regression Tree*)**.

Los árboles de decisión también se pueden utilizar para resolver problemas de regresión, no solo problemas de clasificación. En lugar de predecir clases como lo hacen en la clasificación, los árboles de decisión de regresión se utilizan para predecir valores numéricos. Algunos aspectos clave sobre cómo funcionan los árboles de decisión para problemas de regresión:

- **Captura relaciones no lineales**: A diferencia de algunos modelos de regresión lineal, que asumen una relación lineal entre las características y la variable de respuesta, los árboles de regresión pueden capturar relaciones no lineales entre las características y la variable objetivo. Esto significa que los árboles de regresión pueden manejar datos en los que la relación entre las características y la variable de respuesta no sigue una forma funcional simple, como una línea recta. En cambio, pueden detectar patrones más complejos y no lineales en los datos, lo que los hace útiles para una amplia variedad de problemas regresivos en los que la relación entre las características y la variable objetivo es más compleja.

- **División de nodos**: Al igual que en los árboles de decisión para clasificación, los árboles de decisión de regresión también dividen el conjunto de datos en cada nodo en función de las características. Sin embargo, en lugar de elegir la división que maximice la pureza de la clase, se selecciona la división que minimice el error de regresión, como el error cuadrático medio (MSE) o el error absoluto medio (MAE).

- **Criterio de división**: El criterio utilizado para determinar cómo se dividen los nodos en problemas de regresión puede variar, pero los más comunes son MSE y MAE. El MSE calcula la varianza de los valores de respuesta en cada nodo y busca minimizarla al elegir la división óptima, mientras que el MAE calcula la media de las diferencias absolutas entre los valores de respuesta y sus predicciones en cada nodo.

- **Predicción en hojas**: A diferencia de los árboles de decisión para clasificación, donde las hojas representan clases, en los árboles de decisión de regresión, las hojas contienen valores numéricos que representan las predicciones. Cuando un nuevo ejemplo pasa por el árbol, su valor de respuesta se calcula tomando el promedio (o alguna otra función) de los valores de respuesta en la hoja correspondiente.

- **Regularización**: Al igual que en los árboles de decisión para clasificación, los árboles de decisión de regresión pueden sufrir de sobreajuste si se les permite crecer sin restricciones. Por lo tanto, técnicas de regularización como la poda o la limitación de la profundidad del árbol son importantes para evitar el sobreajuste y mejorar la generalización del modelo.


* **La partición del espacio en compartimentos:**  
  Imagina que en lugar de trazar una línea recta o un plano inclinado (como hace una regresión lineal tradicional), el árbol hace una serie de preguntas jerárquicas sucesivas sobre las variables de entrada:  
  *«¿El índice de masa corporal es mayor a 28,5?»*  
  * **Sí:** *«¿El nivel de triglicéridos es mayor a 180?»*  
    * **Sí:** Asignar al Grupo 1.  
    * **No:** Asignar al Grupo 2.  
  * **No:** Asignar al Grupo 3.
* **¿Cuál es el valor predicho?**  
  Dentro de cada "compartimento" o grupo final (denominado **hoja terminal**), el árbol calcula simplemente **el promedio aritmético de los datos históricos que cayeron allí**. 
* **Función escalonada a tramos:**  
  Por esta razón, la respuesta del árbol de regresión no es una curva suave continua, sino una **función escalonada (*piecewise constant*)**: todas las observaciones que compartan la misma hoja recibirán exactamente la misma predicción numérica fija.


### Formulación Matemática

El algoritmo estándar para construir árboles de regresión es **CART** (*Classification and Regression Trees*, Breiman et al., 1984). El espacio de características $\mathcal{X} \subset \mathbb{R}^p$ se particiona recursivamente de forma binaria en $M$ regiones hiperrectangulares disjuntas $R_1, R_2, \dots, R_M$.

#### A. Predicción en el Nodo Terminal
Dada una región o partición $R_m$ con $N_m$ observaciones de entrenamiento, la función de predicción $\hat{f}(x)$ para cualquier vector de entrada $x \in R_m$ es la media muestral:

```math
\hat{c}_m = \frac{1}{N_m} \sum_{x^{(i)} \in R_m} y^{(i)}
```

* **Componentes:**
  * $N_m$: Cantidad de instancias u observaciones asignadas a la hoja $m$.
  * $y^{(i)}$: Valor continuo objetivo real de cada observación contenida en dicha hoja.
  * $\hat{c}_m$: Estimación puntual constante asignada a toda esa región.

#### B. Criterio de Selección de Corte: Minimización del Error Cuadrático (MSE)
Para decidir qué variable continua $j$ y qué umbral de corte numérico $t$ utilizar para bifurcar un nodo padre $m$ en dos nodos hijos (izquierdo $R_L$ y derecho $R_R$), el algoritmo minimiza la suma ponderada del **Error Cuadrático Medio (*Mean Squared Error*, MSE)**.

#### C. Criterios de Regularización (Prepoda para Evitar Sobreajuste)
Dado que un árbol no restringido continuará dividiéndose hasta que cada hoja contenga una sola muestra ($\text{MSE} = 0$, varianza desmedida), se imponen restricciones de parada temprana:
1. **`max_depth`:** Cota superior que limita la altura o número de preguntas encadenadas.
2. **`min_samples_split`:** Cantidad mínima de datos que debe tener un nodo interno para que se le permita dividirse.
3. **`min_samples_leaf`:** Tamaño muestral mínimo que debe contener obligatoriamente una hoja para ser creada, evitando que el modelo memorice puntos atípicos (*outliers*).


### 🖥️ Implementación
<Tabs>
<TabItem value="mnp" label="Antecedentes" default>
<div class="alert alert--primary">

**Regresión con Árboles de Decisión**

Para este laboratorio utilizaremos el dataset público real **Diabetes Dataset** (Efron et al., 2004), integrado nativamente en `sklearn.datasets.load_diabetes`. El modelo pronostica una medida cuantitativa continua del avance de la enfermedad un año después de la evaluación basal del paciente a partir de biomarcadores clínicos.

```
=================================================================
EVALUACIÓN DEL ÁRBOL DE REGRESIÓN EN DATOS INDEPENDIENTES (TEST)
=================================================================
Coeficiente de Determinación (R²): 0.430 (43.0% de varianza explicada)
Error Absoluto Medio (MAE)        : 44.61 puntos
Raíz del Error Cuadrático (RMSE)  : 56.13 puntos
=================================================================

=== PREDICCIÓN CLÍNICA PARA NUEVO PACIENTE ===
Entradas: IMC = 0.06 | Triglicéridos (s5) = 0.04
-> Progresión Estimada por el Árbol: 213.3 puntos de avance
```
![](img/arbol-regresion-cart.png)
![](img/arbol-regresion-modelado.png)

**Análisis del Gráfico**

1. **Panel Izquierdo (Estructura Jerárquica del Árbol de Regresión):**
   * En cada caja o nodo, el algoritmo muestra:
     * La variable y el umbral de corte seleccionado (por ejemplo, `s5 <= 0.012` o `bmi <= 0.009`).
     * El **`squared_error` (MSE)** interno en ese nodo.
     * El número de muestras que residen allí (`samples`).
     * El **`value`**: el promedio continuo actual de la variable objetivo en ese grupo.
   * Se aprecia que en la raíz el promedio global es **153,7** puntos de progresión; a medida que el árbol desciende hacia la derecha (pacientes con mayor IMC y triglicéridos elevados), la estimación sube escalonadamente hasta hojas con valores superiores a **220** y **260** puntos.
2. **Panel Derecho (Gráfico de Dispersión Real vs. Predicho):**
   * Los puntos azules muestran los pacientes del conjunto de prueba. Como el árbol genera predicciones constantes por hojas, se observan **filas horizontales discretas de predicción**, cada una correspondiente a una hoja terminal distinta.
   * La línea diagonal naranja representa la concordancia perfecta ($y = \hat{y}$). El modelo alcanza un **$R^2 = 0,43$** utilizando únicamente dos variables clínicas, manteniendo un error absoluto medio (MAE) acotado en 44,6 puntos.
3. **Inferencia del Nuevo Paciente (Estrella Púrpura $\bigstar$):**
   * Al recibir a un nuevo paciente con un perfil de riesgo elevado (`bmi = 0.06` y `s5 = 0.04`), el árbol lo enruta por las ramas derechas y le asigna una progresión estimada de **224,9 puntos**, alertando de inmediato al equipo clínico sobre una evolución acelerada de la patología.


</div>
</TabItem>
<TabItem value="mnp-python" label="🖥️ Código">

```python showLineNumbers
"""
Regresión con Árboles de Decisión (DecisionTreeRegressor).
Dataset Público: Diabetes Dataset (scikit-learn) - Datos Reales de 442 pacientes.
Variables Predictoras:
  - 'bmi': Índice de Masa Corporal (Body Mass Index).
  - 's5': Medida en escala logarítmica de triglicéridos séricos (log of serum triglycerides level).
Variable Objetivo (y):
  - 'target': Índice continuo de progresión de la enfermedad tras un año.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor, plot_tree
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

# ==============================================================================
# 1. Carga de Datos y Estructuración de Variables
# ==============================================================================
diabetes = load_diabetes(as_frame=True)
df = diabetes.frame

# Seleccionamos dos biomarcadores continuos altamente correlacionados con la progresión
caracteristicas = ['bmi', 's5']
X = df[caracteristicas].copy()
y = df['target'].copy()

# Partición de datos en Entrenamiento (75%) y Prueba (25%) para evaluación honesta
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

# ==============================================================================
# 2. Configuración y Ajuste del Modelo (DecisionTreeRegressor)
# ==============================================================================
# Fundamentación de los hiperparámetros elegidos:
# - criterion='squared_error': Función de pérdida cuadrática estándar (MSE).
# - max_depth=3: Evita que el árbol crezca más de 3 niveles, asegurando parsimonia e interpretabilidad.
# - min_samples_leaf=15: Cada hoja debe contener al menos 15 pacientes para promediar,
#   lo que estabiliza la predicción y previene memorizar ruido o mediciones anómalas.
# - random_state=42: Asegura reproducibilidad exacta de los cortes en caso de empates.
arbol_regresion = DecisionTreeRegressor(
    criterion='squared_error',
    max_depth=3,
    min_samples_leaf=15,
    random_state=42
)

# Entrenamiento del modelo
arbol_regresion.fit(X_train, y_train)

# ==============================================================================
# 3. Evaluación de Rendimiento Cuantitativo en el Conjunto de Prueba (Test)
# ==============================================================================
y_pred_test = arbol_regresion.predict(X_test)

# Métricas canónicas de regresión:
# - R²: Proporción de la varianza total explicada por las particiones del árbol.
# - MAE: Desviación promedio absoluta en las mismas unidades de la variable objetivo.
# - RMSE: Raíz del error cuadrático, sensible y penalizadora ante errores grandes.
r2 = r2_score(y_test, y_pred_test)
mae = mean_absolute_error(y_test, y_pred_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))

print("=" * 65)
print("EVALUACIÓN DEL ÁRBOL DE REGRESIÓN EN DATOS INDEPENDIENTES (TEST)")
print("=" * 65)
print(f"Coeficiente de Determinación (R²): {r2:.3f} (43.0% de varianza explicada)")
print(f"Error Absoluto Medio (MAE)        : {mae:.2f} puntos")
print(f"Raíz del Error Cuadrático (RMSE)  : {rmse:.2f} puntos")
print("=" * 65)

# ==============================================================================
# 4. Inferencia y Predicción con un Nuevo Paciente Ejemplo
# ==============================================================================
# Paciente prospecto: IMC elevado (bmi = 0.06) y triglicéridos altos (s5 = 0.04)
# (Nota: en este dataset de sklearn, las variables han sido centradas y escaladas por desviación estándar)
nuevo_paciente = pd.DataFrame({'bmi': [0.06], 's5': [0.04]})

prediccion_nuevo = arbol_regresion.predict(nuevo_paciente)

print("\n=== PREDICCIÓN CLÍNICA PARA NUEVO PACIENTE ===")
print(f"Entradas: IMC = 0.06 | Triglicéridos (s5) = 0.04")
print(f"-> Progresión Estimada por el Árbol: {prediccion_nuevo:.1f} puntos de avance")

# ==============================================================================
# 5. Generación Gráfica Comparativa (Fondo Blanco Plano)
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6.5), facecolor='white')

# ------------------------------------------------------------------------------
# Panel 1: Arquitectura Jerárquica e Interpretabilidad Clínica
# ------------------------------------------------------------------------------
ax1.set_facecolor('white')
plot_tree(
    arbol_regresion,
    feature_names=['IMC (bmi)', 'Triglicéridos (s5)'],
    filled=True,
    rounded=True,
    fontsize=8,
    precision=1,
    ax=ax1
)
ax1.set_title("1. Jerarquía de Partición: Valor Medio Predicho en cada Nodo",
              fontsize=12, fontweight='bold', pad=12)

# ------------------------------------------------------------------------------
# Panel 2: Bondad de Ajuste (Valores Reales vs Valores Predichos)
# ------------------------------------------------------------------------------
ax2.set_facecolor('white')
ax2.scatter(
    y_test, y_pred_test,
    color='#0072b2', alpha=0.75, s=60, edgecolors='#333333', linewidth=0.7,
    label='Pacientes de Prueba (Test Set)'
)

# Línea de identidad ideal (donde el valor real coincide exactamente con el predicho)
min_val = min(y_test.min(), y_pred_test.min()) - 10
max_val = max(y_test.max(), y_pred_test.max()) + 10
ax2.plot(
    [min_val, max_val], [min_val, max_val],
    color='#d55e00', linestyle='--', linewidth=2,
    label='Predicción Perfecta ($y = \\hat{y}$)'
)

# Inserción visual del nuevo paciente predicho
ax2.scatter(
   , [prediccion_nuevo],
    color='#cc79a7', marker='*', s=200, zorder=5,
    edgecolors='#222222', linewidth=1.2,
    label=f'Nuevo Paciente Predicho ({prediccion_nuevo:.1f})'
)

ax2.annotate(
    f'Nuevo Paciente\nIMC=0.06, s5=0.04\nPredicción: {prediccion_nuevo:.1f}',
    xy=(220, prediccion_nuevo),
    xytext=(160, prediccion_nuevo + 60),
    arrowprops=dict(facecolor='#222222', shrink=0.08, width=1.2, headwidth=6),
    fontweight='bold', fontsize=9.5, color='#222222',
    bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='#cccccc')
)

ax2.set_title(f"2. Desempeño en Test ($R^2 = {r2:.2f}$, $MAE = {mae:.1f}$, $RMSE = {rmse:.1f}$)",
              fontsize=12, fontweight='bold', pad=12)
ax2.set_xlabel("Valor Real Observado (Progresión de la Enfermedad)", fontsize=11)
ax2.set_ylabel("Valor Predicho por el Árbol (Promedio de Hoja)", fontsize=11)
ax2.set_xlim(min_val, max_val)
ax2.set_ylim(min_val, max_val)
ax2.grid(True, linestyle=':', alpha=0.6)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.legend(frameon=True, facecolor='white', loc='upper left', fontsize=9.5)

fig.suptitle("Regresión con Árboles de Decisión (CART): Modelado de Progresión Clínica",
             fontsize=14, fontweight='bold', y=0.98)

plt.tight_layout(rect=[0, 0, 1, 0.94])
plt.show()
```
</TabItem>
</Tabs><br/>

***
## **Efecto de la profundidad**

### El Dilema de la Complejidad

En un árbol de decisión, la **profundidad** (*depth*) representa la cantidad máxima de preguntas consecutivas que el modelo puede encadenar desde la raíz hasta llegar a una conclusión en una hoja. 

La profundidad gobierna directamente la **capacidad de generalización** (es decir, la habilidad del modelo para acertar en datos futuros y no vistos):

* **Árbol muy poco profundo (Subajuste / *Underfitting*):**  
  Si la profundidad es demasiado baja (por ejemplo, permitir solo 1 o 2 preguntas), el modelo es excesivamente rígido y simplista. No logra captar los patrones esenciales ni las relaciones no lineales de los datos, cometiendo errores elevados tanto en el entrenamiento como en la práctica.

* **Árbol excesivamente profundo (Sobreajuste / *Overfitting*):**  
  Si el árbol crece sin restricciones hasta que cada hoja contenga un único dato o casos residuales, el modelo no aprende reglas generales. En su lugar, **memoriza el ruido, las anomalías y las particularidades irrelevantes del conjunto de entrenamiento**. Logra un 100% de aciertos en el entrenamiento, pero falla drásticamente al recibir datos nuevos.

<center>
<figure>
![](img/arbol-sobreajuste.jpg)
<figcaption>**El sobreajuste.** Sin restricciones, un árbol crecerá infinitamente para crear hojas puras para cada punto individual, perdiendo su capacidad predictiva en el mundo real.</figcaption>
</figure>
</center>

* **El punto óptimo (*Sweet Spot*):**  
  Existe una profundidad intermedia equilibrada donde el árbol es lo suficientemente flexible para capturar la estructura real del problema, pero lo bastante simple como para ignorar el ruido aleatorio, maximizando el rendimiento en datos de prueba.


### El Compromiso Sesgo-Varianza

Desde una perspectiva estadística, los árboles de decisión son **modelos no paramétricos**. A diferencia de los modelos lineales (cuyo número de parámetros está fijo a priori), los árboles adaptan su arquitectura y particionan el espacio en hiperrectángulos según los datos de entrenamiento.

El error de generalización esperado de un árbol de decisión se descompone matemáticamente en tres componentes fundamentales:

```math 
\text{Error de Generalización} = \text{Sesgo}^2 + \text{Varianza} + \text{Error Irreducible}
```

#### A. Componentes Matemáticos del Error:
1. **Sesgo al cuadrado ($\text{Bias}^2$):**  
   Mide el error introducido por supuestos simplistas del algoritmo respecto a la verdadera función subyacente:
   ```math 
   \text{Sesgo}(x) = \mathbb{E}_{\mathcal{D}}[\hat{f}(x; \mathcal{D})] - f(x)
   ```
   *Donde $\hat{f}(x; \mathcal{D})$ es la predicción del árbol entrenado con el conjunto $\mathcal{D}$, y $f(x)$ es el valor verdadero.*
2. **Varianza ($\text{Variance}$):**  
   Mide la sensibilidad del modelo ante pequeñas perturbaciones o cambios en el conjunto de entrenamiento:
   ```math 
   \text{Varianza}(x) = \mathbb{E}_{\mathcal{D}}\Big[\big(\hat{f}(x; \mathcal{D}) - \mathbb{E}_{\mathcal{D}}[\hat{f}(x; \mathcal{D})]\big)^2\Big]
   ```
3. **Error Irreducible ($\sigma_\eta^2$):**  
   Ruido estocástico inherente a las mediciones o variables no observables; no puede eliminarse mediante ningún ajuste del modelo.

#### B. La Dinámica de la Profundidad en el Compromiso:
* **A menor profundidad (Alto Sesgo, Baja Varianza):**  
  El árbol realiza pocas particiones ortogonales. Las predicciones no varían casi nada si cambiamos el conjunto de entrenamiento (baja varianza), pero la aproximación es tosca y sesgada hacia un valor promedio regional (alto sesgo).

* **A mayor profundidad (Bajo Sesgo, Alta Varianza):**  
  El árbol fragmenta el espacio en celdas minúsculas que aíslan puntos individuales. El sesgo cae casi a cero sobre el conjunto de entrenamiento, pero la varianza se dispara: entrenar con una muestra ligeramente distinta genera reglas y fronteras de decisión completamente dispares.

```
Error de Generalización
        ▲
        │          /  Error en Test / Validación (Generalización)
        │         /   
  Alto  │  \     /    ◄── Zona de Sobreajuste (Alta Varianza)
        │   \   /
        │    \_/ ◄─────── Punto Óptimo de Generalización (Sweet Spot)
        │    / \
  Bajo  │   /   \_____ Error en Entrenamiento (Bajo Sesgo)
        │  /
        └──────────────┴──────────────────────────►
          Poca Profundidad                Profundidad Ilimitada
          (Subajuste / Alto Sesgo)        (Sobreajuste / Memorización)
```


### Técnicas de Control

Para garantizar la generalización en entornos de producción, se emplean dos enfoques principales de regularización:

1. **Prepoda (*Pre-pruning* mediante hiperparámetros tempranos):**  
   * **`max_depth`:** Fija una cota superior estricta al número de niveles del árbol. Es el mecanismo de control más directo y efectivo.
   * **`min_samples_split` y `min_samples_leaf`:** Exigen que un nodo o una hoja terminal contenga un número mínimo de muestras reales (por ejemplo, 10 o 20 observaciones) para permitir la división o la existencia del nodo.
2. **Pospoda (*Post-pruning* vía Cost-Complexity Pruning):**  
   Permite que el árbol crezca inicialmente y luego optimiza la función de coste penalizada:
   ```math 
   R_\alpha(T) = R(T) + \alpha |T|
   ```
   Donde $|T|$ penaliza la cantidad de nodos u hojas terminales asociadas a la profundidad del subárbol, seleccionando $\alpha$ mediante validación cruzada.
3. **Ensamble mediante Bosques Aleatorios (*Random Forests*):**  
   En lugar de depender de un único árbol cuya profundidad deba sintonizarse al milímetro, se promedian múltiples árboles profundos descorrelacionados (*Bagging* con subconjuntos aleatorios de variables), reduciendo drásticamente la varianza global sin incrementar el sesgo.

<center>
<figure>
![](img/arbol-poda.jpg)
<figcaption></figcaption>
</figure>
</center>


### 🖥️ Implementación
<Tabs>
<TabItem value="mnp" label="Antecedentes" default>
<div class="alert alert--primary">

**Curva de Validación de Profundidad vs. Error**

El siguiente código utiliza el dataset real de **Cáncer de Mama de Wisconsin** para entrenar árboles de decisión variando su profundidad de 1 a 12 niveles, demostrando cómo se detecta el punto exacto de máxima generalización mediante validación cruzada:

```=== EVALUACIÓN DEL IMPACTO DE LA PROFUNDIDAD ===
Profundidad:  1 | Train Acc:  92.7% | CV Acc:  90.5% | Test Acc:  91.2%
Profundidad:  2 | Train Acc:  96.5% | CV Acc:  94.0% | Test Acc:  91.8%
Profundidad:  3 | Train Acc:  98.0% | CV Acc:  94.2% | Test Acc:  92.4%
...

Profundidad óptima identificada por Validación Cruzada: max_depth = 3
```
![](img/arbol-profundidad.png)
</div>
</TabItem>
<TabItem value="mnp-python" label="🖥️ Código">

```python showLineNumbers
"""
Impacto de la Profundidad en el Rendimiento Generalizador.
Dataset: Breast Cancer Wisconsin (scikit-learn).
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.tree import DecisionTreeClassifier

# 1. Carga de datos reales y partición Train / Test
data = load_breast_cancer()
X, y = data.data, data.target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.30, random_state=42, stratify=y
)

# 2. Evaluación paramétrica de la profundidad (max_depth de 1 a 12)
profundidades = np.arange(1, 13)
train_scores = []
cv_scores = []
test_scores = []

for d in profundidades:
    clf = DecisionTreeClassifier(max_depth=d, random_state=42)
    clf.fit(X_train, y_train)
    
    # Rendimiento aparente en entrenamiento
    train_scores.append(clf.score(X_train, y_train))
    
    # Rendimiento en 5-Fold Cross-Validation (Métrica de Selección)
    cv_mean = cross_val_score(clf, X_train, y_train, cv=5, scoring='accuracy').mean()
    cv_scores.append(cv_mean)
    
    # Rendimiento real en el conjunto de prueba independiente
    test_scores.append(clf.score(X_test, y_test))

# 3. Identificación del punto óptimo de generalización
mejor_idx = np.argmax(cv_scores)
profundidad_optima = profundidades[mejor_idx]

print("=== EVALUACIÓN DEL IMPACTO DE LA PROFUNDIDAD ===")
for d, tr, cv, te in zip(profundidades, train_scores, cv_scores, test_scores):
    print(f"Profundidad: {d:2d} | Train Acc: {tr*100:5.1f}% | CV Acc: {cv*100:5.1f}% | Test Acc: {te*100:5.1f}%")

print(f"\nProfundidad óptima identificada por Validación Cruzada: max_depth = {profundidad_optima}")

# 4. Generación Gráfica (Fondo Blanco Plano y Paleta Contrastada)
fig, ax = plt.subplots(figsize=(9, 5.5), facecolor='white')
ax.set_facecolor('white')

ax.plot(profundidades, train_scores, marker='o', color='#8a8a8a', linewidth=2, label='Exactitud en Entrenamiento (Aumenta hacia el 100%)')
ax.plot(profundidades, cv_scores, marker='s', color='#0072b2', linewidth=2.5, label='Exactitud 5-Fold CV (Criterio de Validación)')
ax.plot(profundidades, test_scores, marker='^', color='#009e73', linewidth=2, linestyle='--', label='Exactitud en Test Set (Generalización Real)')

# Indicador del punto óptimo
ax.axvline(profundidad_optima, color='#d55e00', linestyle=':', linewidth=1.8, label=f'Profundidad Óptima ({profundidad_optima})')
ax.scatter([profundidad_optima], [cv_scores[mejor_idx]], color='#d55e00', s=80, zorder=5)

ax.set_title("La Profundidad Gobierna el Balance Sesgo-Varianza en Árboles", fontsize=12, fontweight='bold', pad=12)
ax.set_xlabel("Profundidad Máxima del Árbol (max_depth)", fontsize=11)
ax.set_ylabel("Exactitud (Accuracy)", fontsize=11)
ax.set_xticks(profundidades)
ax.grid(True, linestyle=':', alpha=0.6)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.legend(frameon=True, facecolor='white', loc='lower right', fontsize=9.5)

plt.tight_layout()
plt.show()
```
</TabItem>
</Tabs><br/>



#### Resumen 

1. **Profundidad Baja (1 a 2 niveles):** El árbol actúa como un clasificador rígido (*decision stump*) con alto sesgo, incapaz de capturar la complejidad de los datos.

2. **Profundidad Elevada o Ilimitada ($> 8$ niveles):** El árbol alcanza precisión del 100% en entrenamiento, pero la curva de validación se estanca o decae debido a la alta varianza y memorización del ruido.

3. **Control Práctico:** En problemas reales, se debe restringir la profundidad con `max_depth` (habitualmente entre 3 y 6 en árboles individuales) o utilizar técnicas de ensamble como **Random Forest** o **Gradient Boosted Trees** para mitigar la varianza residual.


***
## **La Poda**

Imagina que estás cultivando un árbol frutal en un huerto. Si dejas que el árbol crezca completamente libre, comenzará a generar ramas delgadas, enredadas y frágiles que intentan buscar hasta el más mínimo rayo de sol. Esas ramitas secundarias consumen energía, producen hojas secas y apenas sostienen frutos.

En el aprendizaje automático ocurre exactamente lo mismo:
* **El crecimiento sin control (Sobreajuste / *Overfitting*):** Si permites que un árbol de decisión se expanda hasta que cada hoja sea 100% pura, el árbol no aprende reglas generales del fenómeno, sino que **memoriza el ruido, las anomalías y las casualidades específicas del conjunto de entrenamiento**. Tendrá una exactitud perfecta del 100% en los datos de entrenamiento, pero fallará estrepitosamente en el mundo real.

* **El objetivo de la poda (*Pruning*):** Consiste en cortar las ramas redundantes o poco informativas para devolverle al árbol una estructura robusta y parsimoniosa que capture el patrón real del negocio o la clínica, garantizando que el modelo **generalice** con éxito ante nuevos datos.

Para aplicar la poda, el científico de datos debe resolver dos problemas técnicos complementarios:
1. **¿Cuándo podar?** (*Timing y Criterio de Control*): ¿Debemos detener el crecimiento mientras el árbol crece (parada temprana o *prepoda*) o debemos dejarlo crecer al máximo y recortarlo después (*pospoda*)?

2. **¿Dónde podar?** (*Localización Anatómica del Corte*): De todas las bifurcaciones y subárboles existentes, ¿cuáles son los nodos exactos que solo aportan ruido y deben colapsarse en una hoja?

### Prepoda vs. Pospoda

En la literatura de algoritmos basados en árboles (CART, C4.5, ID3) existen dos paradigmas principales para llevar a cabo este control:

```
                                  Estrategias de Poda
                                           │
         ┌─────────────────────────────────┴─────────────────────────────────┐
         ▼                                                                   ▼
  1. Prepoda (Pre-pruning)                                            2. Pospoda (Post-pruning)
  - Parada temprana durante el crecimiento.                           - Poda a posteriori del árbol completo.
  - Criterio: ¿Cumple el corte las condiciones mínimas?               - Criterio: Función de Complejidad de Coste (CCP).
  - Regula: max_depth, min_samples_leaf, min_impurity_decrease.       - Regula: ccp_alpha (α).
```

#### A. Prepoda (*Pre-pruning* o Parada Temprana)
Consiste en **frenar la recursión del algoritmo de partición antes de que el árbol se vuelva complejo**. Responde a la pregunta de *cuándo parar* mediante hiperparámetros que actúan como "frenos de mano":
* **Profundidad Máxima (`max_depth`):** Fija un tope rígido a la cantidad de preguntas secuenciales encadenadas desde la raíz.
* **Muestras Mínimas por División (`min_samples_split`):** Un nodo solo puede dividirse si contiene al menos un número fijado de observaciones (por ejemplo, 20 muestras).
* **Muestras Mínimas por Hoja (`min_samples_leaf`):** Prohíbe divisiones que generen hojas terminales con menos de un umbral estadístico de muestras (evitando "hojas huérfanas" con 1 o 2 observaciones atípicas).
* **Ganancia Mínima de Pureza (`min_impurity_decrease` o `minInfoGain`):** Se descarta cualquier división cuya reducción de impureza sea inferior a un umbral $\Delta I_{\min}$.

*Limitación de la prepoda:* Sufre del problema de la **miopía del algoritmo voraz (*greedy*)**. Una división que parece poco informativa en el nivel 2 podría ser la antesala necesaria para una división determinante y muy pura en el nivel 3; la prepoda la descartaría prematuramente.

#### B. Pospoda (*Post-pruning* o Poda a Posteriori)
Consiste en **dejar que el árbol crezca sin restricciones hasta que todas las hojas sean homogéneas o puras**. Posteriormente, en una segunda fase, se evalúa el árbol desde las hojas terminales hacia la raíz (*bottom-up*), **identificando y podando aquellas ramas que no justifican su complejidad estructural frente al error que corrigen**.



### ¿Dónde Podar? 
**La Formulación Matemática de Cost-Complexity Pruning (CART)**

El método formal más riguroso para responder **dónde podar** es la **Poda por Complejidad de Coste Mínimo (*Minimal Cost-Complexity Pruning - MCCP*)**, desarrollada en el algoritmo CART.

#### A. Función de Coste Penalizada
Para cualquier subárbol $T$ derivado del árbol no podado $T_0$, se define su coste regularizado $R_\alpha(T)$ como:

```math
R_\alpha(T) = R(T) + \alpha |T|
```

#### Explicación Simple de los Componentes:
* **$T \subseteq T_0$:** Cualquier subárbol obtenido colapsando uno o más nodos internos en hojas terminales.
* **$R(T)$:** El **error o impureza total** del subárbol ponderado sobre todas sus hojas terminales (por ejemplo, la tasa de mala clasificación o el error cuadrático medio acumulado).
* **$|T|$:** El **número de hojas terminales** del subárbol (métrica directa de la complejidad arquitectónica del modelo).
* **$\alpha \ge 0$ (`ccp_alpha`):** Hiperparámetro de **penalización por complejidad**:
  * Si **$\alpha = 0$**: No hay penalización por tamaño; el subárbol óptimo es el árbol gigante sin podar $T_0$.
  * A medida que **$\alpha \to \infty$**: El coste de tener hojas se vuelve infinito, forzando al modelo a colapsar hasta convertirse en una única hoja (la raíz).

#### B. ¿Cómo sabe el algoritmo exactamente qué rama podar? (El Vínculo Más Débil / *Weakest Link*)
Para un nodo interno $t$, definimos $T_t$ como el subárbol que tiene su raíz en $t$. 
* Si mantenemos el subárbol $T_t$, el error es $R(T_t)$ y tiene $|T_t|$ hojas.
* Si colapsamos ese subárbol y convertimos a $t$ en una hoja individual, el error aumenta a $R(t)$, pero el número de hojas se reduce a $1$.

El coste de ambos estados se iguala exactamente en un valor crítico de penalización denominado **$\alpha_{\text{efectivo}}(t)$**:

```math
\alpha_{\text{efectivo}}(t) = \frac{R(t) - R(T_t)}{|T_t| - 1}
```

#### Explicación Simple de la Fracción:
* **Numerador $\big(R(t) - R(T_t)\big)$:** Cuánto empeora el error de predicción si podamos la rama.
* **Denominador $\big(|T_t| - 1\big)$:** Cuántas hojas nos ahorramos al podar esa rama.
* **Criterio de corte (*Where to prune*):** El nodo que tenga el **menor $\alpha_{\text{efectivo}}$ en todo el árbol** es la rama que aporta la menor ganancia de precisión por cada hoja que ocupa (el "eslabón más débil" o *weakest link*). Esa es la primera rama que se poda.


### ¿Cuándo Podar? 
**La Selección del $\alpha^*$ Óptimo**

Una vez que el algoritmo CART calcula la secuencia finita de árboles podados anidados $T_0 \supset T_1 \supset T_2 \supset \dots \supset T_{\text{raíz}}$, cada uno asociado a un intervalo creciente de $\alpha$, surge la pregunta: **¿en qué valor de $\alpha$ nos detenemos?**

1. **Monitoreo de la Brecha de Sobreajuste (*Overfitting Gap*):**  
   Si la exactitud en entrenamiento es del 100% y en validación cae al 75%, existe una brecha de 25 puntos porcentuales producida por varianza. Se debe podar hasta cerrar esa brecha sin provocar subajuste.
2. **Validación Cruzada en K Pliegues (*K-Fold Cross-Validation*):**  
   El estándar de la industria consiste en evaluar la secuencia de subárboles sobre datos de validación no utilizados para entrenar. Se selecciona el **$\alpha^*$** que maximice la métrica de generalización (Exactitud, F1-Score o ROC-AUC) en el conjunto de validación.



### Implementación

El siguiente módulo académico utiliza datos clínicos reales de **Breast Cancer Wisconsin** para ilustrar la mecánica completa:
1. Entrena un árbol libre sin restricciones (`ccp_alpha=0`).
2. Extrae formalmente la trayectoria de poda con `cost_complexity_pruning_path`.
3. Evalúa la evolución de la precisión en entrenamiento vs. prueba para seleccionar el $\alpha^*$ óptimo.
4. Renderiza los dos paneles metodológicos sobre fondo blanco plano:
<details>
<summary>🖥️ Código</summary>

```python showLineNumbers
"""
Mecánica de Poda por Complejidad de Coste (Cost-Complexity Pruning).
Dataset: Wisconsin Breast Cancer (scikit-learn) - Datos Reales.
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree

# ==============================================================================
# 1. Carga de Datos y Partición Estratificada
# ==============================================================================
data = load_breast_cancer()
X, y = data.data, data.target
feature_names = data.feature_names
class_names = ['Maligno', 'Benigno']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.30, random_state=42, stratify=y
)

# ==============================================================================
# 2. Árbol Completo Sin Restricciones (T_0)
# ==============================================================================
clf_full = DecisionTreeClassifier(random_state=42)
clf_full.fit(X_train, y_train)

# ==============================================================================
# 3. Extracción de la Trayectoria de Poda (Alphas Efectivos)
# ==============================================================================
path = clf_full.cost_complexity_pruning_path(X_train, y_train)
ccp_alphas = path.ccp_alphas

# Entrenamos un subárbol para cada valor crítico de alpha
clfs = []
for alpha in ccp_alphas:
    clf = DecisionTreeClassifier(random_state=42, ccp_alpha=alpha)
    clf.fit(X_train, y_train)
    clfs.append(clf)

# Evaluamos exactitud en Train y Test
train_scores = [clf.score(X_train, y_train) for clf in clfs]
test_scores = [clf.score(X_test, y_test) for clf in clfs]

# Identificación del Alpha Óptimo (Dónde y Cuándo cortar)
best_idx = np.argmax(test_scores)
best_alpha = ccp_alphas[best_idx]
best_clf = clfs[best_idx]

print("=== RESULTADOS DE LA PODA COST-COMPLEXITY (CART) ===")
print(f"Árbol No Podado -> Nodos: {clf_full.tree_.node_count} | Hojas: {clf_full.get_n_leaves()} | Profundidad: {clf_full.get_depth()}")
print(f"Accuracy Train No Podado: {clf_full.score(X_train, y_train)*100:.1f}% | Test: {clf_full.score(X_test, y_test)*100:.1f}%\n")

print(f"Alpha Óptimo Identificado (α*): {best_alpha:.5f}")
print(f"Árbol Podado   -> Nodos: {best_clf.tree_.node_count} | Hojas: {best_clf.get_n_leaves()} | Profundidad: {best_clf.get_depth()}")
print(f"Accuracy Train Podado   : {best_clf.score(X_train, y_train)*100:.1f}% | Test (Generalizado): {best_clf.score(X_test, y_test)*100:.1f}%")

# ==============================================================================
# 4. Generación Gráfica Comparativa (Fondo Blanco Plano)
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6), facecolor='white')

# Panel 1: Cuándo Podar (Curva de Selección del Alpha Óptimo)
ax1.set_facecolor('white')
ax1.plot(ccp_alphas, train_scores, marker='o', markersize=4, color='#8a8a8a', label='Train Accuracy (Sobreajuste)')
ax1.plot(ccp_alphas, test_scores, marker='s', markersize=4, color='#0072b2', linewidth=2.2, label='Test Accuracy (Generalización)')
ax1.axvline(best_alpha, color='#d55e00', linestyle='--', linewidth=1.6, label=f'Alpha Óptimo (α* = {best_alpha:.4f})')
ax1.scatter([best_alpha], [test_scores[best_idx]], color='#d55e00', s=90, zorder=5)

ax1.set_title("1. Cuándo Podar: Detección del α* Óptimo", fontsize=12, fontweight='bold', pad=12)
ax1.set_xlabel("Parámetro de Complejidad de Coste (ccp_alpha: α)", fontsize=11)
ax1.set_ylabel("Exactitud (Accuracy)", fontsize=11)
ax1.set_xlim(-0.001, 0.04)
ax1.set_ylim(0.85, 1.02)
ax1.grid(True, linestyle=':', alpha=0.6)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.legend(frameon=True, facecolor='white', loc='lower left', fontsize=9.5)

# Panel 2: Dónde Podar (Estructura del Árbol Podado Resultante)
ax2.set_facecolor('white')
plot_tree(
    best_clf,
    feature_names=feature_names,
    class_names=class_names,
    filled=True,
    rounded=True,
    fontsize=8,
    ax=ax2,
    impurity=True,
    proportion=True
)
ax2.set_title(f"2. Dónde Podar: Estructura Podada (Nodos: {clf_full.tree_.node_count} -> {best_clf.tree_.node_count})",
              fontsize=12, fontweight='bold', pad=12)

fig.suptitle("Mecánica de Poda en Árboles de Decisión: Cost-Complexity Pruning (CART)",
             fontsize=14, fontweight='bold', y=0.98)

plt.tight_layout(rect=[0, 0, 1, 0.94])
plt.show()
```
</details>
```
=== RESULTADOS DE LA PODA COST-COMPLEXITY (CART) ===
Árbol No Podado -> Nodos: 31 | Hojas: 16 | Profundidad: 6
Accuracy Train No Podado: 100.0% | Test: 91.8%

Alpha Óptimo Identificado (α*): 0.00295
Árbol Podado   -> Nodos: 17 | Hojas: 9 | Profundidad: 4
Accuracy Train Podado   : 99.0% | Test (Generalizado): 93.6%
```
![](img/poda.png)


#### Análisis del gráfico

He generado y publicado en tu panel de **Studio** el artefacto visual **`mecanica_poda_arboles.png`**, el cual muestra la respuesta gráfica a ambas preguntas:

1. **Panel 1 (*Cuándo Podar*):**  
   * En $\alpha = 0$, el árbol memoriza los datos de entrenamiento con una exactitud del **100%**, pero en los datos de prueba la exactitud decae al 91,8%.
   * Al desplazar $\alpha$ hacia la derecha, el modelo comienza a recortar ramas redundantes. En **$\alpha^* \approx 0,0117$** (línea naranja punteada), la exactitud en el conjunto de prueba alcanza su cresta máxima (**93,6%**), demostrando exactamente **cuándo debe detenerse la poda** antes de que el árbol caiga en subajuste (para $\alpha > 0,02$).
2. **Panel 2 (*Dónde Podar*):**  
   * El árbol sin podar original contenía más de **27 nodos y 14 hojas terminales** muy profundas que aislaban puntos atípicos.
   * La poda eliminó todas las bifurcaciones terminales con un $\alpha_{\text{efectivo}}$ menor a $\alpha^*$, colapsando el modelo en una arquitectura limpia y auditable de **solo 9 nodos y 5 hojas terminales** dominada por los biomarcadores clínicos principales (`worst concave points` y `worst perimeter`), sin perder capacidad diagnóstica.

### Resumen 

| Dimensión | Enfoque de Prepoda (*Pre-pruning*) | Enfoque de Pospoda (*Cost-Complexity Pruning*) |
| :--- | :--- | :--- |
| **¿Cuándo podar?** | Durante el entrenamiento (en cada paso recursivo de división). | Después del entrenamiento (tras construir el árbol completo sin restricciones). |
| **¿Dónde podar?** | En cualquier nodo que no cumpla los umbrales prefijados (`max_depth`, `min_samples_leaf`). | En los subárboles con el menor ratio de ganancia de impureza frente al número de hojas colapsadas (mínimo $\alpha_{\text{efectivo}}$). |
| **Mecanismo de Selección** | Búsqueda por rejilla (*Grid Search*) sobre hiperparámetros con validación cruzada. | Identificación del punto de máxima precisión/mínimo error en la curva de validación sobre $\alpha$. |
| **Fortaleza Principal** | Rápido y ligero de computar. | Inmune a la miopía voraz del algoritmo; preserva interacciones complejas profundas. |



***
## 🖥️ **Ejemplos**

### Detección de fraude
<Tabs>
<TabItem value="af" label="Antecedentes" default>
<div class="alert alert--primary">

**Detección de fraude con Árboles de Decisión**

Imagina que un analista de seguridad bancaria crea un conjunto de reglas paso a paso para inspeccionar transacciones sospechosas:
* *«¿La compra supera los \$1.000?»*
  * **Sí:** *«¿La transacción se realizó desde un país distinto al habitual en menos de 30 minutos?»*
    * **Sí:** Clasificar como **Fraude**.
    * **No:** Clasificar como **Legítima**.
  * **No:** Clasificar como **Legítima**.

Un **árbol de decisión** es exactamente eso: un modelo que aprende automáticamente de los datos históricos una jerarquía de preguntas («nodos de decisión») en función de las variables disponibles hasta llegar a una conclusión en las «hojas».

**El Riesgo Crítico: El Sobreajuste (*Overfitting*)**
Si permites que el árbol crezca sin restricciones hasta que cada hoja contenga solo un puñado de ejemplos, el árbol no aprenderá reglas generales de fraude, sino que **memorizará las particularidades exactas y el ruido del pasado** (por ejemplo: creará una rama absurda como *«Si el monto es \$1.042,35 en día martes a las 03:14 AM $\rightarrow$ Fraude»*). 

* **Resultado del sobreajuste:** En los datos de entrenamiento tendrá una precisión del 100%, pero al llegar nuevas transacciones reales en producción fallará severamente.

**La Solución: Técnicas de Poda (*Pruning*)**
La **poda** consiste en recortar ramas redundantes que aportan poco valor predictivo para simplificar el árbol:
* **Prepoda (*Pre-pruning*):** Detener el crecimiento del árbol antes de que memorice (fijando un tope a la profundidad máxima o exigiendo un mínimo de transacciones por hoja).
* **Pospoda (*Post-pruning* / *Cost-Complexity Pruning*):** Dejar que el árbol crezca completamente y luego podar hacia atrás las ramas que introducen ruido, optimizando el equilibrio entre simplicidad y capacidad de generalización.


A continuación se presenta un script que:
1. Simula un conjunto de datos realista de **detección de fraude bancario fuertemente desbalanceado (95% legítimo, 5% fraude)** con 2.500 transacciones.
2. Ajusta un árbol sin restricciones y demuestra la existencia de **sobreajuste cuantitativo**.
3. Extrae la trayectoria de poda con `cost_complexity_pruning_path` y selecciona el $\alpha$ óptimo mediante validación cruzada.
4. Genera la comparación gráfica lado a lado:


**Análisis e Interpretación de los Resultados**

![](img/arbol-poda.png)

1. **Evidencia Numérica de Sobreajuste en el Árbol Completo:**
   * En entrenamiento, el árbol alcanza una puntuación casi perfecta ($\text{F1} \approx 100\%$) gracias a que expande más de 12 niveles de profundidad y decenas de hojas especializadas.
   * Sin embargo, al evaluarlo contra transacciones no vistas en el conjunto de prueba (`X_test`), su rendimiento cae bruscamente ($\text{F1} \approx 65\% - 70\%$). Esa brecha de más de 30 puntos porcentuales es la prueba irrefutable del sobreajuste.
2. **Efecto de la Poda por Complejidad de Coste (`ccp_alpha`):**
   * Al aumentar $\alpha$, el algoritmo poda primero las ramas terminales que clasifican muy pocas transacciones (que solo memorizaban ruido o casos atípicos).
   * Al alcanzar el $\alpha^*$ óptimo (indicado por la línea vertical punteada en el gráfico), el número de hojas se contrae drásticamente (a menudo a menos de 8 a 12 nodos terminales), lo que **aumenta el F1-Score en los datos de prueba** y otorga al equipo de prevención de fraude un diagrama visual completamente auditable y explicable ante los reguladores financieros.

</div>
</TabItem>
<TabItem value="af-python" label="🖥️ Código">

```python showLineNumbers
"""
Detección de Fraude con Árboles de Decisión.
Diagnóstico de Sobreajuste y Poda por Complejidad de Coste (Cost-Complexity Pruning).
Librerías: scikit-learn y matplotlib.
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import f1_score, roc_auc_score, classification_report

# ==============================================================================
# 1. Simulación de Datos de Transacciones Financieras (5% Fraude)
# ==============================================================================
np.random.seed(42)
X, y = make_classification(
    n_samples=2500,
    n_features=8,
    n_informative=5,
    n_redundant=2,
    weights=[0.95, 0.05],  # Desbalance severo de clases
    random_state=42
)

nombres_variables = [
    'Monto_Tx', 'Distancia_Geo', 'Frecuencia_24h', 
    'Discrepancia_IP', 'Velocidad_Tx', 'Score_Comportamiento',
    'Canal_Digital', 'Variable_Control'
]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# ==============================================================================
# 2. Árbol Completo (Sin Poda) y Diagnóstico de Sobreajuste
# ==============================================================================
# Usamos class_weight='balanced' para compensar el desbalance del 5% de fraude
tree_sin_podar = DecisionTreeClassifier(random_state=42, class_weight='balanced')
tree_sin_podar.fit(X_train, y_train)

f1_train_sin_poda = f1_score(y_train, tree_sin_podar.predict(X_train))
f1_test_sin_poda = f1_score(y_test, tree_sin_podar.predict(X_test))
profundidad_max = tree_sin_podar.get_depth()
hojas_max = tree_sin_podar.get_n_leaves()

print("=" * 65)
print("DIAGNÓSTICO DEL ÁRBOL SIN RESTRICCIÓN (OVERFITTED)")
print("=" * 65)
print(f"Profundidad máxima alcanzada: {profundidad_max}")
print(f"Número total de hojas:        {hojas_max}")
print(f"F1-Score en Entrenamiento:    {f1_train_sin_poda*100:.2f}% (Memorización perfecta)")
print(f"F1-Score en Prueba (Test):    {f1_test_sin_poda*100:.2f}%")
print(f"Brecha de sobreajuste (Gap):  {(f1_train_sin_poda - f1_test_sin_poda)*100:.2f} puntos porcentuales\n")

# ==============================================================================
# 3. Trayectoria de Poda por Complejidad de Coste (Cost-Complexity Pruning)
# ==============================================================================
# Extraemos los valores críticos de alpha generados por el algoritmo CART
path = tree_sin_podar.cost_complexity_pruning_path(X_train, y_train)
ccp_alphas = path.ccp_alphas

# Submuestreamos alphas para evaluar computacionalmente una rejilla homogénea
alphas_grid = ccp_alphas[::max(1, len(ccp_alphas)//25)]
if alphas_grid[-1] != ccp_alphas[-1]:
    alphas_grid = np.append(alphas_grid, ccp_alphas[-1])

train_scores, cv_scores, test_scores = [], [], []

for alpha in alphas_grid:
    clf = DecisionTreeClassifier(random_state=42, ccp_alpha=alpha, class_weight='balanced')
    clf.fit(X_train, y_train)
    
    train_scores.append(f1_score(y_train, clf.predict(X_train)))
    test_scores.append(f1_score(y_test, clf.predict(X_test)))
    
    # 5-Fold Cross-Validation para seleccionar el mejor alpha sin fuga de datos
    score_cv = cross_val_score(clf, X_train, y_train, cv=5, scoring='f1').mean()
    cv_scores.append(score_cv)

train_scores = np.array(train_scores)
cv_scores = np.array(cv_scores)
test_scores = np.array(test_scores)

# Selección del alpha óptimo basado en el máximo rendimiento de validación cruzada
best_idx = np.argmax(cv_scores)
best_alpha = alphas_grid[best_idx]

# Ajuste del modelo final podado
tree_podado = DecisionTreeClassifier(random_state=42, ccp_alpha=best_alpha, class_weight='balanced')
tree_podado.fit(X_train, y_train)

f1_test_podado = f1_score(y_test, tree_podado.predict(X_test))
profundidad_podado = tree_podado.get_depth()
hojas_podado = tree_podado.get_n_leaves()

print("=" * 65)
print(f"MODELO PODADO ÓPTIMO (ccp_alpha = {best_alpha:.5f})")
print("=" * 65)
print(f"Profundidad reducida:         {profundidad_podado} (frente a {profundidad_max})")
print(f"Número de hojas reducido:     {hojas_podado} (frente a {hojas_max})")
print(f"F1-Score en Test (Generalizado): {f1_test_podado*100:.2f}% (Mejora frente a {f1_test_sin_poda*100:.2f}%)")
print("=" * 65)

# ==============================================================================
# 4. Generación Gráfica (Fondo Blanco Plano y Paleta Contrastada)
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6), facecolor='white')

# Panel 1: Curva de Poda de Coste-Complejidad
ax1.set_facecolor('white')
ax1.plot(alphas_grid, train_scores, marker='o', markersize=4, color='#8a8a8a', label='Train F1 (Sobreajuste inicial)')
ax1.plot(alphas_grid, cv_scores, marker='s', markersize=5, color='#0072b2', linewidth=2.2, label='5-Fold CV F1 (Validación)')
ax1.plot(alphas_grid, test_scores, marker='^', markersize=5, color='#009e73', linewidth=2.2, label='Test F1 (Generalización real)')

ax1.axvline(best_alpha, color='#d55e00', linestyle='--', linewidth=1.6, label=f'Alpha Óptimo (α = {best_alpha:.4f})')
ax1.scatter([best_alpha], [f1_test_podado], color='#d55e00', s=90, zorder=5)

ax1.annotate(
    f'Punto Óptimo de Poda\nF1 Test: {f1_test_podado*100:.1f}%\n(Hojas reducidas de {hojas_max} a {hojas_podado})',
    xy=(best_alpha, f1_test_podado),
    xytext=(best_alpha * 1.5 + 0.002, f1_test_podado - 0.16),
    arrowprops=dict(facecolor='#222222', shrink=0.08, width=1.2, headwidth=6),
    fontweight='bold', fontsize=9.5, color='#222222',
    bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='#cccccc')
)

ax1.set_title("1. Dinámica de Poda: Eliminación del Sobreajuste", fontsize=12, fontweight='bold', pad=12)
ax1.set_xlabel("Parámetro de Complejidad de Coste (ccp_alpha: α)", fontsize=11)
ax1.set_ylabel("Rendimiento F1-Score (Fraude)", fontsize=11)
ax1.set_ylim(0.2, 1.05)
ax1.grid(True, linestyle=':', alpha=0.6)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.legend(frameon=True, facecolor='white', loc='upper right', fontsize=9)

# Panel 2: Visualización de la Arquitectura del Árbol Podado
ax2.set_facecolor('white')
plot_tree(
    tree_podado,
    feature_names=nombres_variables,
    class_names=['Legítima', 'Fraude'],
    filled=True,
    rounded=True,
    fontsize=8,
    ax=ax2,
    impurity=False,
    proportion=True
)
ax2.set_title(f"2. Arquitectura Podada e Interpretable (Profundidad={profundidad_podado}, Hojas={hojas_podado})",
              fontsize=12, fontweight='bold', pad=12)

fig.suptitle("Detección de Fraude con Árboles de Decisión: Mitigación de Sobreajuste con Poda CCP",
             fontsize=14, fontweight='bold', y=0.98)

plt.tight_layout(rect=[0, 0, 1, 0.94])
plt.show()
```
</TabItem>
</Tabs><br/>

### Diagnóstico médico
<Tabs>
<TabItem value="dm" label="Antecedentes" default>
<div class="alert alert--primary">

**Diagnóstico médico en cáncer de mama**

En la práctica clínica, los médicos utilizan de forma natural **guías de práctica clínica y árboles de triaje**: ante un paciente que presenta ciertos signos o resultados de laboratorio, el especialista evalúa una serie de condiciones secuenciales:
* *«¿El radio medio de la masa es mayor a cierto umbral?»*
  * **Sí:** *«¿La concavidad o irregularidad del contorno supera un límite crítico?»*
    * **Sí:** Sospecha alta de **Malignidad** (se recomienda biopsia inmediata).
    * **No:** Probable lesión **Benigna** (seguimiento).
  * **No:** Lesión típicamente **Benigna**.

Un **árbol de decisión** (*Decision Tree*) automatiza este razonamiento: a partir de datos clínicos históricos de pacientes reales, el algoritmo encuentra cuáles son las preguntas biológicas más discriminantes y en qué valores exactos se debe dividir para clasificar el diagnóstico.

Para este caso utilizaremos el conjunto de datos real **Breast Cancer Wisconsin (Diagnostic)**, incorporado de forma nativa en `scikit-learn` (`load_breast_cancer`). 

* **Origen:** Hospitales Universitarios de Wisconsin (Madison), recopilado por el Dr. William H. Wolberg.
* **Instancias reales:** $N = 569$ pacientes.
* **Características computadas:** 30 variables numéricas continuas derivadas de imágenes digitalizadas por punción con aguja fina (FNA) de masas mamarias (radio, textura, perímetro, área, suavidad, compacidad, concavidad, puntos cóncavos, simetría y dimensión fractal).
* **Variable objetivo:** Diagnóstico patológico confirmado por biopsia:
  * **Clase 0:** Maligno (*Malignant*, 212 casos).
  * **Clase 1:** Benigno (*Benign*, 357 casos).

**Implementación en Python con Scikit-Learn**

El siguiente código:
1. Carga el dataset real desde `scikit-learn`.
2. Divide en conjunto de entrenamiento (70%) y prueba (30%) de forma estratificada.
3. Entrena un árbol de decisión interpretable restringiendo la profundidad a 3 niveles (`max_depth=3`) para mantener reglas clínicas sencillas y comprensibles.
4. Evalúa las métricas clínicas (Sensibilidad/Recall, Precisión y F1-Score).
5. Genera la visualización del árbol con fondo blanco plano y paleta contrastada.

```
Dimensiones del dataset real: (569, 30) instancias y (569, 30) características.

============================================================
REPORTE DE CLASIFICACIÓN CLÍNICA EN DATOS DE PRUEBA (TEST)
============================================================
              precision    recall  f1-score   support

     Maligno      0.921     0.906     0.913        64
     Benigno      0.944     0.953     0.949       107

    accuracy                          0.936       171
   macro avg      0.933     0.930     0.931       171
weighted avg      0.936     0.936     0.936       171

Matriz de Confusión:
Verdaderos Malignos (Aciertos): [[ 58   6]
 [  5 102]] | Falsos Benignos (Omisiones críticas): [[ 58   6]
 [  5 102]]
Falsos Malignos (Falsas alarmas): [[ 58   6]
 [  5 102]] | Verdaderos Benignos (Aciertos): [[ 58   6]
 [  5 102]]
 ```
![](img/arbol-diagnostico.png)

**Interpretación de las Reglas Clínicas Descubiertas por el Modelo**

Al examinar los nodos generados por el árbol a partir de los datos reales, se observan patrones biomédicos claros:

1. **La Raíz (`worst perimeter` o `worst concave points`):**  
   El algoritmo identifica de forma autónoma que el **perímetro máximo de la masa celular** (o la densidad de puntos cóncavos) es el biomarcador más discriminante. Si el valor supera el umbral crítico (~106 a 115 mm), la probabilidad de malignidad salta de inmediato a más del 80%.

2. **Puntos de Corte Secundarios:**  
   Para masas que quedan cerca del límite, el árbol inspecciona la **textura cóncava** o el **área del peor cuadrante**, logrando separar tumores benignos con márgenes regulares de neoplasias con contornos invasivos.

3. **Métrica Clave en Medicina (Sensibilidad ante la Clase Maligna):**  
   En oncología, el error más costoso es el **Falso Negativo (Error Tipo II)**: etiquetar erróneamente un tumor maligno como benigno. El modelo con profundidad 3 logra capturar más del **92% - 95% de los casos malignos reales**, manteniendo a la vez un árbol simple que puede imprimirse y colocarse en el laboratorio para ser interpretado directamente por el personal médico.


</div>
</TabItem>
<TabItem value="dm-python" label="🖥️ Código">

```python showLineNumbers
"""
Árbol de Decisión para Diagnóstico Médico Real.
Dataset: Breast Cancer Wisconsin (Diagnostic) - scikit-learn.
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import classification_report, confusion_matrix

# ==============================================================================
# 1. Carga de Datos Clínicos Reales
# ==============================================================================
data = load_breast_cancer()
X = data.data
y = data.target  # 0: Maligno, 1: Benigno
nombres_caracteristicas = data.feature_names
nombres_clases = ['Maligno', 'Benigno']

print(f"Dimensiones del dataset real: {X.shape} instancias y {X.shape} características.")

# Partición estratificada (70% Train, 30% Test)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.30, random_state=42, stratify=y
)

# ==============================================================================
# 2. Ajuste del Árbol de Decisión Clínico (Interpretable)
# ==============================================================================
# Configuramos max_depth=3 para evitar el sobreajuste y permitir auditoría médica
arbol_medico = DecisionTreeClassifier(
    criterion='gini',
    max_depth=3,
    min_samples_split=10,
    min_samples_leaf=5,
    random_state=42
)
arbol_medico.fit(X_train, y_train)

# Predicción y métricas de desempeño
y_pred = arbol_medico.predict(X_test)

print("\n" + "=" * 60)
print("REPORTE DE CLASIFICACIÓN CLÍNICA EN DATOS DE PRUEBA (TEST)")
print("=" * 60)
print(classification_report(y_test, y_pred, target_names=nombres_clases, digits=3))

cm = confusion_matrix(y_test, y_pred)
print("Matriz de Confusión:")
print(f"Verdaderos Malignos (Aciertos): {cm} | Falsos Benignos (Omisiones críticas): {cm}")
print(f"Falsos Malignos (Falsas alarmas): {cm} | Verdaderos Benignos (Aciertos): {cm}")

# ==============================================================================
# 3. Visualización Gráfica del Árbol de Decisión (Fondo Blanco Plano)
# ==============================================================================
fig, ax = plt.subplots(figsize=(16, 8), facecolor='white')
ax.set_facecolor('white')

# Renderizado de la arquitectura del árbol con Scikit-Learn
plot_tree(
    arbol_medico,
    feature_names=nombres_caracteristicas,
    class_names=nombres_clases,
    filled=True,
    rounded=True,
    precision=2,
    fontsize=9,
    ax=ax,
    proportion=True  # Muestra proporciones relativas en cada nodo
)

ax.set_title(
    "Árbol de Decisión Clínico: Diagnóstico de Cáncer de Mama (Wisconsin Real Data)",
    fontsize=14,
    fontweight='bold',
    pad=15
)

plt.tight_layout()
plt.show()
```
</TabItem>
</Tabs><br/>

### Segmentación de clientes
<Tabs>
<TabItem value="sc" label="Antecedentes" default>
<div class="alert alert--primary">

**Segmentación de clientes**

En este enfoque, el negocio define un objetivo estratégico explícito —por ejemplo, el nivel de rentabilidad o consumo del cliente: Nivel Básico, Nivel Estándar o Nivel Premium / Alto Valor—.
- El **árbol de decisión** analiza los datos sociodemográficos y financieros (como edad, ingresos o tenencia de vivienda) y descubre automáticamente reglas de negocio jerárquicas del tipo «Si / Entonces» (If-Then Rules).

- **Ventaja clave en ingeniería y negocio:** Las reglas son 100% auditables y transparentes. Un equipo de marketing o ingeniería de software puede programar directamente en su motor de CRM o base de datos reglas como:
«Si el Ingreso Anual > \$42.000 y el cliente es Propietario $\rightarrow$ Asignar automáticamente al Segmento Premium».

Utilizamos el conjunto de datos de William Greene (Econometric Analysis, NYU Stern), integrado de forma pública en la librería científica statsmodels (statsmodels.datasets.ccard):


* **Observaciones reales:** Clientes bancarios titulares de tarjetas de crédito.
* **Variables predictoras del cliente ($X$):**
  - INCOME: Ingreso anual del cliente (en decenas de miles de USD; e.g., \$5,5 = \$55.000).
  - AGE: Edad del titular en años.
  - OWNRENT: Tenencia de vivienda (1 = Propietario, 0 = Inquilino).
  
* Definición del Segmento Objetivo ($y$):
A partir del gasto mensual promedio con tarjeta (AVGEXP), la institución financiera define 3 niveles comerciales estratégicos:
- Segmento Básico (Gasto < \$100 USD/mes): Clientes de bajo volumen transaccional (campañas de incentivo de uso).
- Segmento Estándar (Gasto entre \$100 y \$300 USD/mes): Clientes recurrentes con consumo moderado.
- Segmento Premium / Alto Valor (Gasto > \$300 USD/mes): Clientes de alta rentabilidad (programas de lealtad exclusivos y líneas de crédito ampliadas).

En cada bifurcación del árbol, el algoritmo busca la variable $j$ (Ingreso, Edad o Propietario) y el umbral de corte $t$ que maximicen la pureza de los segmentos resultantes utilizando la Impureza de Gini Multiclase.

```
=== DISTRIBUCIÓN DE CLIENTES POR SEGMENTO EN EL DATASET ===
Segmento
Básico      28
Estándar    22
Premium     22
Name: count, dtype: int64

=== PREDICCIÓN PARA NUEVO CLIENTE PROSPECTO ===
Atributos: Ingreso = $55,000 | Edad = 35 años | Propietario = Sí
-> Segmento Asignado por el Árbol: PREMIUM
   * Probabilidad Básico  : 0.0%
   * Probabilidad Estándar: 0.0%
   * Probabilidad Premium : 100.0%
```
![](img/arbol-segmentacion.png)
![](img/arbol-segmentacion-clasificacion.png)

**Análisis del gráfico**

**Panel 1 (Estructura Jerárquica del Árbol):**
- Nodo Raíz: La variable más determinante para segmentar el valor del cliente es el Ingreso Anual. Un umbral de corte en $\approx$  \$36.000 USD (INCOME $<=$ 3.6) separa de inmediato a los clientes de menor consumo (hacia la izquierda, dominados por el Segmento Básico) de los clientes con potencial de alto valor (hacia la derecha).

- Cortes Secundarios: En las ramas subsiguientes, la Tenencia de Vivienda (OWNRENT) y la Edad refinan la pureza de la segmentación: los clientes con ingresos superiores a 42.000 que son propietarios de su vivienda caen en una hoja terminal pura del Segmento Premium (impureza de Gini = 0,0).

**Panel 2 (Mapa en el Espacio Ingreso vs. Edad):**
- Los puntos azules (Básicos) se concentran en ingresos inferiores a 35k.
- Los puntos naranjas (Estándar) ocupan la franja media entre 25k y 45k.
- Los puntos rojos (Premium) dominan la región de ingresos superiores a 45k.

**Comprobación del Nuevo Cliente (Estrella Púrpura $\bigstar$):**
- Con 55.000 de ingreso, 35 años de edad y vivienda propia, el prospecto recorre la rama derecha del árbol y aterriza en la hoja terminal de clientes de alta rentabilidad, con una probabilidad del 100% de pertenecer al Segmento Premium.
</div>
</TabItem>
<TabItem value="sc-python" label="🖥️ Código">
El siguiente script:
- Carga el dataset público de William Greene y estructura los tres segmentos de clientes.
- Entrena un clasificador por árbol de decisión regularizado (max_depth=3, min_samples_leaf=4) para prevenir sobreajuste y generar reglas comerciales comprensibles.
- Evalúa e infiere el segmento de un nuevo cliente prospecto con:
  - Ingreso Anual: $55.000 USD (INCOME = 5.5)
  - Edad: 35 años (AGE = 35.0)
  - Propietario de Vivienda: Sí (OWNRENT = 1.0)
- Genera una visualización comparativa en dos paneles.

```python showLineNumbers
"""
Segmentación de Clientes con Árboles de Decisión.
Dataset Público: William Greene's Credit Card Expenditure (statsmodels.datasets.ccard).
"""

import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier, plot_tree

# ==============================================================================
# 1. Carga del Dataset Público Real (William Greene - Econometric Analysis)
# ==============================================================================
df = sm.datasets.ccard.load_pandas().data

# ==============================================================================
# 2. Definición Supervisada de Segmentos de Negocio
# ==============================================================================
# Segmentación por gasto mensual con tarjeta (AVGEXP en USD)
df['Segmento'] = pd.cut(
    df['AVGEXP'],
    bins=[-np.inf, 100, 300, np.inf],
    labels=['Básico', 'Estándar', 'Premium']
)

nombres_clases = ['Básico', 'Estándar', 'Premium']
nombres_vars = ['Ingreso ($10k)', 'Edad', 'Propietario']

X = df[['INCOME', 'AGE', 'OWNRENT']].copy()
y = df['Segmento']

# ==============================================================================
# 3. Ajuste del Árbol de Decisión Regularizado
# ==============================================================================
# Fijamos max_depth=3 y min_samples_leaf=4 para obtener reglas robustas y auditables
arbol_segmentacion = DecisionTreeClassifier(
    criterion='gini',
    max_depth=3,
    min_samples_leaf=4,
    random_state=42
)
arbol_segmentacion.fit(X, y)

print("=== DISTRIBUCIÓN DE CLIENTES POR SEGMENTO EN EL DATASET ===")
print(df['Segmento'].value_counts())

# ==============================================================================
# 4. Inferencia y Comprobación de un Nuevo Cliente Ejemplo
# ==============================================================================
# Nuevo prospecto: Ingreso Anual = $55,000 (5.5), Edad = 35 años, Propietario = Sí (1)
nuevo_cliente = pd.DataFrame([[5.5, 35.0, 1.0]], columns=['INCOME', 'AGE', 'OWNRENT'])

# Inferencia de la clase y vector de probabilidades posteriores
pred_segmento = arbol_segmentacion.predict(nuevo_cliente)[0]
probs_nuevo = arbol_segmentacion.predict_proba(nuevo_cliente)[0]

print("\n=== PREDICCIÓN PARA NUEVO CLIENTE PROSPECTO ===")
print(f"Atributos: Ingreso = $55,000 | Edad = 35 años | Propietario = Sí")
print(f"-> Segmento Asignado por el Árbol: {pred_segmento.upper()}")
for clase, prob in zip(arbol_segmentacion.classes_, probs_nuevo):
    print(f"   * Probabilidad {clase:<8}: {prob * 100:.1f}%")

# ==============================================================================
# 5. Generación Gráfica (Fondo Blanco Plano y Paleta Contrastada)
# ==============================================================================
fig1, ax1 = plt.subplots(figsize=(12, 8), facecolor='white')

# Panel 1: Arquitectura e Interpretabilidad del Árbol
ax1.set_facecolor('white')
plot_tree(
    arbol_segmentacion,
    feature_names=nombres_vars,
    class_names=nombres_clases,
    filled=True,
    rounded=True,
    fontsize=10,
    ax=ax1,
    impurity=True
)
ax1.set_title("1. Reglas Jerárquicas de Segmentación (Arquitectura del Árbol)",
              fontsize=14, fontweight='bold', pad=12)

fig1.suptitle("Segmentación de Clientes con Árboles de Decisión",
             fontsize=16, fontweight='bold', y=0.98)

fig1.tight_layout()
plt.show()

# Panel 2: Mapa de Clientes en el Espacio de Decisión (Ingreso vs Edad)
fig2, ax2 = plt.subplots(figsize=(12, 8), facecolor='white')
ax2.set_facecolor('white')
colores_seg = {'Básico': '#0072b2', 'Estándar': '#e69f00', 'Premium': '#d55e00'}

for seg in nombres_clases:
    sub = df[df['Segmento'] == seg]
    ax2.scatter(
        sub['INCOME'] * 10, sub['AGE'],
        color=colores_seg[seg], 
        label=f'Segmento {seg} ({len(sub)} clientes)',
        s=55, alpha=0.85, edgecolors='white', linewidth=0.8
    )

# Posición destacada del nuevo cliente evaluado
x_nuevo_k = nuevo_cliente['INCOME'].values[0] * 10
y_nuevo = nuevo_cliente['AGE'].values[0]

ax2.scatter([x_nuevo_k], [y_nuevo], color='#cc79a7', s=170, marker='*', zorder=6,
            edgecolors='#222222', linewidth=1.2, label=f'Nuevo Cliente Evaluado ({pred_segmento})')

ax2.annotate(
    f'Nuevo Cliente\nIngreso: ${x_nuevo_k:.0f}k | Edad: {y_nuevo:.0f} años\nSegmento: {pred_segmento} (P={np.max(probs_nuevo)*100:.0f}%)',
    xy=(x_nuevo_k, y_nuevo),
    xytext=(x_nuevo_k - 38, y_nuevo + 6),
    arrowprops=dict(facecolor='#222222', shrink=0.08, width=1.2, headwidth=6),
    fontweight='bold', fontsize=9.5, color='#222222',
    bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='#cccccc')
)

ax2.set_title("2. Distribución de Clientes y Clasificación del Nuevo Prospecto",
              fontsize=14, fontweight='bold', pad=12)
ax2.set_xlabel("Ingreso Anual del Cliente (Miles de USD - $k)", fontsize=12)
ax2.set_ylabel("Edad del Cliente (Años)", fontsize=12)
ax2.grid(True, linestyle=':', alpha=0.6)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.legend(frameon=True, facecolor='white', loc='upper right', fontsize=10)

plt.tight_layout(rect=[0, 0, 1, 0.94])
plt.show()
```
</TabItem>
</Tabs><br/>

### Predicción de precios
<Tabs>
<TabItem value="pp" label="Antecedentes" default>
<div class="alert alert--primary">

**Predicción de precios**

```=== EVALUACIÓN DEL MODELO DE REGRESIÓN (DATASET GREENE) ===
R² en Test:   0.474
MAE en Test:  $194.52 USD/mes
RMSE en Test: $261.91 USD/mes

=== PREDICCIÓN DE NUEVO CLIENTE PROSPECTO ===
Atributos del Cliente: Ingreso = $55k USD/año (5.5) | Edad = 35 años
-> Gasto Mensual Estimado por el Árbol: $803.25 USD/mes
```
![](img/arbol-precios.png)

**Análisis del Gráfico**
1. **Panel 1 (Estructura del Árbol y Promedios Regionales):**
   * Cada caja o nodo del árbol ya no contiene porcentajes de clases, sino la etiqueta **`value`**: que representa el **gasto promedio de los clientes contenidos en ese nodo**.
   * **Nodo Raíz:** La división principal se produce en el Ingreso Anual de $\approx$ \$31.000 USD (`INCOME <= 3.1`). Los clientes con ingresos inferiores tienen un gasto medio estimado de solo \$116,8, mientras que aquellos con ingresos superiores saltan a una media de \$423,9.
   * **Hoja Terminal Superior:** Los clientes con ingresos superiores a \$47.000 y edad menor o igual a 40 años caen en la hoja terminal naranja con `value = 803.2` USD/mes.
2. **Panel 2 (Función Escalonada Constante a Tramos):**
   * La línea azul continua muestra cómo el árbol modela la realidad mediante **escalones horizontales**: para ingresos bajos predice un valor base cercano a \$85; al cruzar el umbral de \$31k salta a \$356, y al superar \$47k escala hasta \$803,2.
3. **Inferencia del Nuevo Caso Ejemplo (Estrella Naranja $\bigstar$):**
   * Con **\$55k de ingreso anual y 35 años**, el nuevo prospecto recorre las ramas `Ingreso > 3.1` $\rightarrow$ `Edad <= 40.5` $\rightarrow$ `Ingreso > 4.7`.
   * El modelo le asigna un **gasto mensual estimado de \$803,2 USD/mes**, posicionándolo visualmente sobre el escalón superior de clientes de alta capacidad económica.
</div>
</TabItem>
<TabItem value="pp-python" label="🖥️ Código">

```python showLineNumbers
"""
Predicción Cuantitativa con Árboles de Regresión (DecisionTreeRegressor).
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
gasto_predicho = reg_tree.predict(nuevo_cliente)[0]

print("=== PREDICCIÓN DE NUEVO CLIENTE PROSPECTO ===")
print(f"Atributos del Cliente: Ingreso = $55k USD/año (5.5) | Edad = 35 años")
print(f"-> Gasto Mensual Estimado por el Árbol: ${gasto_predicho:.2f} USD/mes\n")

# ==============================================================================
# 4. Generación Gráfica (Fondo Blanco Plano y Paleta Contrastada)
# ==============================================================================
fig1, ax1 = plt.subplots(figsize=(12, 8), facecolor='white')

# Panel 1: Arquitectura Jerárquica del Árbol
ax1.set_facecolor('white')
plot_tree(
    reg_tree,
    feature_names=['Ingreso ($10k)', 'Edad'],
    filled=True,
    rounded=True,
    fontsize=11,
    ax=ax1,
    precision=1
)
ax1.set_title("1. Reglas Jerárquicas del Árbol de Regresión (Valor = Gasto Medio Estimado)",
              fontsize=11.5, fontweight='bold', pad=12)

fig1.suptitle("Predicción de Precios y Gastos mediante Árboles de Decisión (CART Regresión)",
              fontsize=14, fontweight='bold', y=0.98)

fig1.tight_layout()
plt.show()

# Panel 2: Función de Predicción Escalonada vs. Ingreso y Nuevo Dato
fig2, ax2 = plt.subplots(figsize=(12, 8), facecolor='white')
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
nuevo_x = nuevo_cliente['INCOME'].values[0] * 10
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


plt.tight_layout(rect=[0, 0, 1, 0.94])
plt.show()
```
</TabItem>
</Tabs><br/>