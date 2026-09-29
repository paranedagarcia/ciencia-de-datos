---
id: ml-scikitlearn
title: "Introducción a Scikit-Learn"
sidebar_label: "📦 Scikit-Learn"
description: "Herramientas simples y efectivas para análisis predictivo de datos"
---


**Scikit-learn** es la biblioteca de **aprendizaje automático** (machine learning) más popular y prominente para el lenguaje de programación Python. Es un proyecto de código abierto, distribuido bajo la licencia permisiva BSD, lo que permite su uso tanto en entornos académicos como comerciales sin restricciones.

## Reseña General
La biblioteca fue creada originalmente por **David Cournapeau en 2007** como parte de un proyecto de Google Summer of Code. Desde entonces, ha sido liderada por un equipo de investigadores del Instituto Francés de Investigación en Informática y Automática (**Inria**) y, más recientemente, por Probabl.ai. 

Se ha consolidado como un estándar en la industria gracias a su **documentación extensa y de alta calidad**, así como a una comunidad activa de desarrolladores que aseguran su constante mejora y fiabilidad mediante pruebas automatizadas. Scikit-learn no está diseñado para el procesamiento de "Big Data" en clústeres distribuidos, sino que se centra en algoritmos eficientes para una sola máquina, integrándose perfectamente con el ecosistema científico de Python.

## Funcionalidades Principales
Scikit-learn ofrece una amplia gama de herramientas para las tareas fundamentales del aprendizaje automático:

*   **Clasificación:** Identificación de a qué categoría pertenece un objeto (ej. detección de spam o reconocimiento de imágenes).
*   **Regresión:** Predicción de variables continuas asociadas a un objeto (ej. precios de viviendas).
*   **Clustering:** Agrupación automática de objetos similares en grupos sin etiquetas previas.
*   **Reducción de Dimensionalidad:** Disminución del número de variables aleatorias a considerar (ej. PCA).
*   **Preprocesado:** Transformación y normalización de datos antes del entrenamiento.
*   **Selección de Modelos:** Comparación, validación y elección de parámetros y modelos (ej. búsqueda en cuadrícula o validación cruzada).

## Características y Principios de Diseño
El éxito de la biblioteca radica en su **API limpia, uniforme y optimizada**, diseñada bajo principios que facilitan su uso:

1.  **Consistencia:** Todos los objetos comparten una interfaz común basada en métodos limitados y coherentes.
2.  **Interfaz de Estimadores:** Cualquier objeto que aprenda de los datos se denomina **estimador** y utiliza el método `fit()` para ajustar los parámetros del modelo.
3.  **Transformadores y Predictores:** Los objetos que transforman datos usan `transform()`, mientras que los modelos que realizan predicciones usan `predict()`.
4.  **Composición:** Es posible encadenar múltiples pasos de procesamiento (como escalado y clasificación) en un solo objeto denominado **Pipeline**, lo que reduce errores y simplifica el flujo de trabajo.
5.  **Fundamentación Técnica:** Está construida sobre las librerías fundamentales **NumPy** (para manejo eficiente de arreglos), **SciPy** (para computación científica) y **Matplotlib** (para visualización). Además, interactúa de forma nativa con **Pandas**, permitiendo trabajar directamente con estructuras de datos tabulares.