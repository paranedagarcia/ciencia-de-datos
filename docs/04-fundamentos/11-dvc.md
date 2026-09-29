---
id: dvc
title: "Data Versión Control"
sidebar_label: "​📚 Data Versión Control"
description: ""
slug: /dvc
---

## **DVC**

:::info
- https://dvc.org/
- https://www.youtube.com/watch?v=07pzs-fjFvI
:::

**DVC (Data Version Control)** es una herramienta de código abierto diseñada específicamente para gestionar el **versionamiento de datos**, modelos y flujos de trabajo de Machine Learning. A diferencia de las herramientas tradicionales como Git, que están optimizadas para archivos de texto pequeños (código), DVC está construido para manejar los desafíos de los **grandes volúmenes de datos** y los artefactos binarios que Git no puede gestionar de manera eficiente.

<center>
<figure>
![](img/dvc-1.png)
<figcaption>Versionando modelos de datos.</figcaption>
</figure>
</center>


#### ¿Cómo se usa DVC en el versionamiento de datos?

<center>
<figure>
![](img/dvc-0.png)
<figcaption>Versionando modelos de datos.</figcaption>
</figure>
</center>

El uso de DVC en el ciclo de vida de un proyecto se centra en los siguientes pilares:

*   **Gestión de archivos pesados:** El versionamiento de código tradicional (Git) funciona comparando líneas de texto (diffs), lo cual no tiene sentido para datos binarios o archivos de millones de caracteres. Además, Git guarda copias completas de archivos antiguos, lo que haría inviable duplicar datasets masivos repetidamente. **DVC evita esto** gestionando los archivos grandes fuera de Git, pero manteniendo un puntero o referencia ligera dentro del repositorio.

*   **Seguimiento mediante Checksums:** DVC registra un cambio (diff) únicamente si el **checksum (suma de verificación)** del directorio total ha cambiado o si se ha añadido/eliminado un archivo. Esto permite saber con precisión si los datos han sido alterados sin necesidad de procesar cada línea de información. Si el hash cambia, DVC registra un diff. Git solo almacena el ligero archivo de metadatos .dvc.

*   **Garantía de Reproducibilidad:** En ML, los sistemas son una combinación de código y datos. DVC permite vincular una versión específica del código (en Git) con una versión específica de los datos (en DVC). Esto es vital para **replicar experimentos**; si un modelo dio buenos resultados hace semanas, DVC permite recuperar exactamente el dataset y los hiperparámetros utilizados en esa corrida específica.

*   **Seguimiento de Experimentos:** Aunque nació como una herramienta de versionamiento, DVC ha evolucionado para incluir el **rastreo de experimentos**. Permite registrar artefactos generados durante el entrenamiento, como gráficas de curvas de pérdida, logs y resultados intermedios, facilitando la comparación entre diferentes versiones del modelo.

*   **Colaboración y Almacenamiento Remoto:** DVC permite que varios colaboradores trabajen en el mismo proyecto compartiendo los datos a través de un **almacenamiento en la nube** (como Amazon S3, Google Cloud Storage o Azure), mientras Git solo se encarga de sincronizar los pequeños archivos de metadatos que indican qué versión de los datos se debe descargar.

<center>
<figure>
![](img/dvc-flujo.jpg)
<figcaption>DVC no sude los datos a Git. Calcula un checksum del directorio o archivo.</figcaption>
</figure>
</center>

En resumen, DVC se utiliza como un **complemento de Git**: mientras Git rastrea el "qué hacer" (código), DVC rastrea el "con qué se hizo" (datos y modelos), asegurando que todo el flujo de trabajo de ciencia de datos sea **auditable y reproducible**.

#### Ejemplo

Un ejemplo práctico de uso de **DVC (Data Version Control)** se centra en la necesidad de gestionar archivos de datos que son demasiado grandes para Git, permitiendo que el equipo de ciencia de datos pueda revertir no solo el código, sino también los conjuntos de datos a versiones anteriores de forma eficiente.

Un flujo de trabajo práctico y los comandos lógicos necesarios:

**Escenario: Evolución de un Dataset de Entrenamiento**

Imagine que está entrenando un modelo de detección de fraude. Comienza con un archivo `datos_fraude.csv` de 1 GB. Git no puede rastrear este archivo de forma eficiente porque intentaría guardar copias completas de cada cambio, saturando el repositorio.

#### 1. Configuración inicial
Primero, debe inicializar DVC en su repositorio de Git.
```bash
# Iniciar DVC en el proyecto
dvc init
# Git registrará la configuración de DVC
git commit -m "Inicializar DVC"
```

#### 2. Rastrear el conjunto de datos
En lugar de añadir el archivo directamente a Git, se lo entrega a DVC.
```bash
# Añadir el archivo pesado a DVC
dvc add datos_fraude.csv
```
**¿Qué sucede internamente?**
*   DVC calcula un **checksum (suma de verificación)** único para el archivo.
*   Mueve el archivo real a un "caché" oculto y crea un pequeño archivo de puntero llamado `datos_fraude.csv.dvc` (de apenas unos bytes).
*   DVC añade automáticamente el archivo pesado original al `.gitignore` para que Git no lo rastree por accidente.

#### 3. Versionar el puntero en Git
Ahora usa Git para guardar la referencia a esa versión específica de los datos.
```bash
# Rastrear el puntero ligero en Git
git add datos_fraude.csv.dvc .gitignore
git commit -m "Añadir versión inicial de los datos"
```

#### 4. Modificación y actualización (Data Iteration)
Supongamos que adquiere nuevas muestras y actualiza `datos_fraude.csv`. DVC detectará que el **checksum** del directorio o archivo ha cambiado.
```bash
# Actualizar el rastro de los nuevos datos
dvc add datos_fraude.csv
# Guardar el nuevo puntero en Git
git add datos_fraude.csv.dvc
git commit -m "Dataset actualizado con muestras de julio"
```

#### 5. El valor práctico: Revertir versiones
Si descubre que los nuevos datos introdujeron un sesgo o error (problema de *data lineage*), puede volver exactamente a la configuración anterior:
```bash
# Volver al commit de Git de la versión anterior
git checkout <hash_del_commit_anterior>
# Sincronizar el archivo pesado real con lo que dice el puntero de Git
dvc checkout
```
Este último comando, `dvc checkout`, restaura instantáneamente el archivo de 1 GB correspondiente a esa versión del código, garantizando la **reproducibilidad** total del experimento.

#### Resumen de ventajas:
*   **Ahorro de espacio:** Git solo almacena punteros ligeros, no los archivos gigantistas.
*   **Trazabilidad:** Puede vincular cada versión del modelo con la versión exacta del dato que lo generó (vía el commit de DVC).
*   **Colaboración:** Los datos pueden almacenarse en un servidor remoto (como S3 o Google Drive), y los colegas solo necesitan bajar los punteros de Git y ejecutar `dvc pull` para obtener los datos pesados correspondientes.


### Seguimiento y Versionamiento de Experimentos

<center>
<figure>
![](img/doc-experimentos.jpg)
<figcaption>No depender de la memoria. Documentar cada ejecución permite comparar iteraciones.</figcaption>
</figure>
</center>

En el desarrollo de modelos se realizan cientos de pruebas; documentar este proceso evita la pérdida de "promesas" de modelos que luego no se pueden replicar.
*   **Registro de artefactos:** Se deben guardar los archivos generados durante el entrenamiento, como curvas de pérdida (*loss curves*), logs de velocidad y métricas de rendimiento del sistema (uso de CPU/GPU).

*   **Herramientas especializadas:** Utilizar plataformas como **MLflow**, **Weights & Biases** o **Comet.ml** permite centralizar y comparar versiones de modelos y sus respectivos artefactos de manera automática.

### Documentación Narrativa y Técnica
Existen diferentes niveles de documentación según la audiencia:
*   **Model Cards (Tarjetas de Modelo):** Son documentos breves que acompañan al modelo detallando cómo fue entrenado, sus métricas de evaluación, el uso previsto y sus **limitaciones éticas**. Son esenciales cuando los usuarios del modelo no son los mismos que lo desarrollaron. Esto estandariza el reporte ético y técnico, definieindo las limitaciones y los casos fuera de alcance (Out-of-scope).

<center>
<figure>
![](img/doc-card.jpg)
<figcaption>No depender de la memoria. Documentar cada ejecución permite comparar iteraciones.</figcaption>
</figure>
</center>

*   **Notebooks Explicativos:** Utilizar Jupyter Notebooks o RMarkdown permite intercalar el código con explicaciones, gráficas y resultados inmediatos, funcionando como un "cuaderno de notas" universitario.

*   **README estructurado:** Todo proyecto debe contar con un archivo README que guíe a una persona técnica a través de la instalación y ejecución del pipeline.

### Mejores Prácticas
*   **Modularidad:** El código debe estar modularizado para permitir que las etapas del pipeline (limpieza, ingeniería de características, entrenamiento) se reproduzcan fielmente en diferentes entornos (Desarrollo, QA, Producción).

*   **Grafos de Flujo de Datos:** El uso de herramientas que generen un **grafo de flujo** (como los DAGs en Airflow o Metaflow) facilita enormemente la comprensión visual del proceso y ayuda a rastrear dependencias.

*   **Comentarios Explicativos:** Se deben incluir abundantes comentarios en el código, especialmente si se planea volver al proyecto meses después, explicando el "porqué" de ciertas decisiones técnicas.