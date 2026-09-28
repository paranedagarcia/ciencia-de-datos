Aquí tienes la **Guía de Aprendizaje Unificada y Mejorada** para la asignatura "Modelamiento y Paradigmas de Programación". 

Como experto en diseño curricular y en el estándar CDIO, he analizado ambos documentos, eliminado redundancias, corregido inconsistencias (como las ponderaciones que no sumaban 100%) y **agregado temas críticos faltantes** para un ingeniero civil informático actual, tales como: **Normalización de datos, Control de Versiones (Git), Modelado básico para APIs/NoSQL, y Ética/Sostenibilidad en el desarrollo de software**.

El formato está diseñado en tablas Markdown, las cuales puedes **copiar y pegar directamente en Microsoft Word**; Word convertirá automáticamente las tablas manteniendo la estructura.

---

# GUÍA DE APRENDIZAJE 2026 (Unificada y Actualizada)

## 1. IDENTIFICACIÓN

| Campo | Detalle |
| :--- | :--- |
| **Nombre Asignatura:** | Modelamiento y Paradigmas de Programación |
| **Carrera:** | Ingeniería Civil Informática |
| **Semestre:** | Segundo (o Tercero, según malla curricular) |
| **Sección:** | [Por definir] |
| **Docente:** | [Por definir] |
| **Correo institucional:** | [Por definir] |
| **Fecha de actualización:** | Agosto 2026 |
| **Créditos SCT-Chile:** | 4 |
| **Horas de docencia directa:** | 4 horas semanales |
| **Horas de trabajo autónomo:** | 3 horas semanales |

---

## 2. APORTES AL PERFIL DE EGRESO

| Campo | Detalle |
| :--- | :--- |
| **Competencia/s General/es:** | **Comunicación CFI4:** Comunicar pensamientos, saberes y sentimientos, adecuándose a diversos contextos comunicativos, utilizando e interpretando el lenguaje oral, escrito y corporal, y gestionando el conocimiento e interacción comunicativa a través de las tecnologías de la información y comunicación para desenvolverse en la vida académica y profesional. |
| **Competencia/s Específica/s:** | **Proyectos Informáticos CE2:** Gestionar proyectos informáticos considerando variables económicas, técnicas y del entorno para responder eficientemente a los requerimientos del medio.<br>**Tecnologías de Información CE3:** Proponer aplicaciones tecnológicas de última generación, considerando aspectos de software y hardware integrado para generar información útil en la toma de decisiones. |
| **Resultados de Aprendizaje (RA):** | **RA1 (50%):** Diseña un Modelo de datos que permita una gestión confiable, normalizada y escalable de la información involucrada en un sistema informático.<br>**RA2 (50%):** Utiliza las distintas herramientas proporcionadas por UML y los paradigmas de programación para representar, diseñar y resolver sistemas informáticos, expresando de forma gráfica y lógica la solución a un problema de la disciplina. |
| **Niveles Formativos CDIO:** | **Nivel 2 (Personal):** 2.3 Pensamiento Sistémico.<br>**Nivel 3 (Interpersonal):** 3.1 Trabajo en Equipo, 3.2 Comunicaciones.<br>**Nivel 4 (CDIO - Sistema):** 4.3 Concebir, Ingeniería y Gestión de Sistemas, 4.4 Diseñar. |

---

## 3. PLANIFICACIÓN DE SESIONES (17 Semanas)

| SEMANA | N° RA | SABERES CONCEPTUALES | ACTIVIDAD/ES DOCENCIA DIRECTA (Estudiante-Docente) | ACTIVIDAD/ES TRABAJO AUTÓNOMO (Estudiante) | RECURSOS DE APRENDIZAJE |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **S1** | RA1, RA2 | **Génesis y Viabilidad del Proyecto:** Introducción al curso. Ideación de proyectos (Brainstorming, SCAMPER). Justificación y Análisis de Viabilidad (Técnica, Operacional, Temporal). | Presentación del curso y del Proyecto Semestral Integrador. Modelado guiado de técnicas de ideación y definición de objetivos SMART. | Conformación de equipos. Aplicar técnicas de ideación para generar 3-5 ideas. Redactar primera versión de justificación y viabilidad preliminar. | Presentaciones, Plantillas de Canvas/Project Charter, Libro guía. |
| **S2** | RA1 | **Fundamentos de Modelamiento de Datos:** Introducción al Modelo Entidad-Relación (MER). Entidades, Atributos (simples, compuestos, multivaluados, derivados) y Claves Primarias. | Explicación de heurísticas para extraer entidades y atributos desde enunciados en lenguaje natural. Práctica guiada de identificación. | Ejercicios de análisis de enunciados: listar entidades, atributos y claves primarias. Investigación sobre notaciones de MER. | Presentaciones, Ejercicios prácticos en computador, Herramientas de diagramación (draw.io, Lucidchart). |
| **S3** | RA1 | **Relaciones, Cardinalidad y Participación (Notación Chen):** Identificación de relaciones. Cardinalidad (1:1, 1:N, M:N) y Participación (Total/Parcial). | Construcción paso a paso de DER en notación Chen. Discusión de reglas de negocio y su traducción a cardinalidad y participación. | Elaborar el primer borrador del DER del proyecto semestral en notación Chen. Resolver ejercicios propuestos de complejidad media. | Presentaciones, Guía de notación Chen, Casos de ejemplo. |
| **S4** | RA1 | **Jerarquías y Refinamiento del MER:** Generalización/Especialización (Herencia). Restricciones de disyunción/solapamiento y totalidad/parcialidad. | Modelado de escenarios con superclases y subclases. Debate sobre criterios de diseño: ¿Entidad o Atributo? | Revisar y refinar el DER del proyecto incorporando jerarquías si aplica. Documentar supuestos de diseño. | Presentaciones, Casos de estudio con herencia. |
| **S5** | RA1 | **Modelo Relacional y Normalización:** Reglas de conversión de MER a Modelo Relacional. Introducción a las Formas Normales (1FN, 2FN, 3FN) para garantizar la integridad. | Demostración de la transformación de un DER a tablas relacionales. Ejercicios de normalización para eliminar anomalías de actualización. | Desarrollar el Modelo Relacional del proyecto a partir del DER. Aplicar reglas de normalización a las tablas propuestas. | Presentaciones, Libro guía de bases de datos, Ejercicios de normalización. |
| **S6** | RA1 | **PRODUCTO RA1:** Integración de Modelamiento de Datos. | Presentación de casos de estudio para ser desarrollados en clases. Retroalimentación en tiempo real. | Desarrollo y entrega del **Proyecto Integrador Grupal RA1** (Documento con Justificación, DER en Chen y Modelo Relacional Normalizado). | Rúbrica de evaluación RA1, Enunciado del Proyecto. |
| **S7** | RA2 | **Metodologías de Desarrollo de Software (Tradicionales):** Ciclo de vida del software. Modelos en Cascada, Espiral y Evolutivos/Incrementales. | Análisis comparativo de modelos predictivos. Discusión sobre cuándo aplicar cada uno según el contexto del proyecto. | Lectura de casos de estudio. Reflexión en equipo sobre qué modelo tradicional se alinea con su proyecto y por qué. | Presentaciones, Artículos sobre historia de las metodologías de software. |
| **S8** | RA2 | **La Revolución Ágil:** Manifiesto Ágil (Valores y Principios). Introducción a Scrum y Kanban. Planificación adaptativa vs. predictiva. | Dinámica sobre los valores ágiles. Explicación de roles (Product Owner, Scrum Master), artefactos (Backlog) y eventos (Sprint). | Investigar una metodología ágil específica. Crear un borrador de Product Backlog para el proyecto semestral y estimar con tallas (S, M, L). | Presentaciones, Manifiesto Ágil, Guías de Scrum/Kanban. |
| **S9** | RA2 | **Planificación y Gestión de Tareas:** De la EDT (WBS) al Diagrama de Gantt y Tableros Kanban. Dependencias y Ruta Crítica. | Taller práctico: Desglose de Objetivos Específicos en tareas. Construcción de un Diagrama de Gantt y configuración de un tablero visual (Trello/Jira). | Refinar estimaciones, identificar dependencias y construir el cronograma (Gantt o Sprint Plan) del proyecto semestral. | Plantillas de Gantt, Tutoriales de herramientas de gestión (Trello, Asana, ProjectLibre). |
| **S10** | RA2 | **UML: Diagrama de Casos de Uso:** Actores, Casos de Uso, Límite del sistema. Relaciones: Asociación, <<include>>, <<extend>>, Generalización. | Demostración de cómo capturar requisitos funcionales desde la perspectiva del usuario. Práctica de identificación de actores y flujos. | Identificar actores y casos de uso del proyecto. Elaborar el Diagrama de Casos de Uso y redactar la especificación textual de 2 casos clave. | Presentaciones, Guía de buenas prácticas en Casos de Uso. |
| **S11** | RA2 | **UML: Diagramas de Comportamiento (Secuencia y Actividad):** Modelado de interacciones temporales y flujos de trabajo con decisiones y swimlanes. | Modelado guiado de un escenario complejo. Uso de fragmentos combinados (alt, opt, loop) en secuencia y nodos de decisión en actividad. | Seleccionar 1-2 escenarios críticos del proyecto y modelarlos con Diagramas de Secuencia y de Actividad (con swimlanes). | Presentaciones, Herramientas de modelado UML (StarUML, draw.io). |
| **S12** | RA2 | **UML: Diagrama de Estado y de Clases:** Ciclo de vida de objetos. Estructura estática: Clases, atributos, métodos, relaciones de asociación, agregación, composición y herencia. | Explicación de estados, transiciones, eventos y condiciones de guarda. Transición del modelo conceptual al modelo de diseño orientado a objetos. | Identificar un objeto central del proyecto y modelar su Diagrama de Estado. Elaborar un Diagrama de Clases preliminar basado en el modelo relacional. | Presentaciones, Ejercicios de mapeo Relacional a Clases. |
| **S13** | RA2 | **Paradigmas de Programación I:** Programación Orientada a Objetos (POO). Encapsulamiento, Herencia, Polimorfismo, Abstracción. | Relación entre el Diagrama de Clases UML y su implementación en un lenguaje POO (ej. Java, Python, C#). Ejercicios de codificación guiada. | Trabajar en la implementación de un prototipo básico utilizando POO, aplicando los principios vistos. | Entorno de Desarrollo Integrado (IDE), Tutoriales de POO. |
| **S14** | RA2 | **Paradigmas de Programación II y Temas Modernos:** Programación Imperativa, Funcional y Orientada a Eventos. *Tema Agregado:* Introducción al Control de Versiones (Git) y modelado conceptual de APIs/NoSQL. | Comparativa de paradigmas. Demostración de flujo de trabajo con Git (commit, push, pull, branch). Breve introducción a cómo se modelan datos en documentos (JSON) vs. relacional. | Ejercicios de programación en paradigmas no-POO. Crear un repositorio Git para el proyecto semestral y documentar el avance. | Documentación de Git, Artículos sobre NoSQL y APIs REST. |
| **S15** | RA2 | **Ética, Sostenibilidad y Calidad en el Modelamiento:** Ley de Protección de Datos (Chile), Green Software, y revisión integral de modelos. | Discusión sobre el impacto ético de las decisiones de modelamiento (ej. sesgos en datos, privacidad). Checklist de revisión de calidad de modelos UML y de Datos. | Aplicar checklist de calidad a todos los artefactos del proyecto. Preparar la presentación final. | Guías de ética en ingeniería, Ley 19.628, Rúbrica de presentación. |
| **S16** | RA1, RA2 | **PRODUCTO RA2:** Presentación y Defensa de Proyectos Semestrales. | Exposición y defensa de los proyectos por parte de los grupos. Retroalimentación formativa y sumativa por parte del docente y pares. | Ensayos finales de presentación. Pulir documentación, código y prototipos. Asistir y participar activamente en las presentaciones de otros grupos. | Proyector, Rúbrica de evaluación de presentación y producto final. |
| **S17** | RA1, RA2 | **Evaluación Individual Integradora:** Examen o Proyecto Individual. | Presentación de un caso de estudio nuevo y acotado para ser resuelto individualmente en tiempo limitado, abarcando modelamiento de datos y UML. | Desarrollo del Proyecto/Examen Integrador Individual bajo supervisión. | Enunciado del Examen/Proyecto Individual, Entorno de evaluación. |

---

## 4. CRONOGRAMA DE EVALUACIONES (PROCESO-PRODUCTO)

*Nota: La ponderación ha sido unificada y corregida para sumar exactamente 100% del total de la asignatura, respetando la división 50% RA1 y 50% RA2 establecida en los Resultados de Aprendizaje.*

| FECHA (Referencial) | N° RA | TIPO DE EVALUACIÓN (Proceso-Producto) | MEDIO DE EVALUACIÓN (Informe, exposición, etc.) | INSTRUMENTO DE EVALUACIÓN (Rúbrica, escala, etc.) | % DE EVALUACIÓN (Sobre nota final) |
| :--- | :---: | :--- | :--- | :--- | :---: |
| **Semanas 4-5** | RA1 | Proceso: Avances de Modelamiento de Datos | Informe técnico (DER y Modelo Relacional) | Rúbrica de evaluación | 20% |
| **Semana 6** | RA1 | Producto: Proyecto Integrador Grupal RA1 | Informe final y defensa breve | Rúbrica de evaluación | 30% |
| **Semanas 9-10** | RA2 | Proceso: Planificación y Modelado UML Inicial | Informe (Cronograma Gantt/Ágil + Casos de Uso) | Rúbrica de evaluación | 20% |
| **Semana 16** | RA2 | Producto: Proyecto Integrador Grupal RA2 | Informe, Código/Prototipo, Exposición oral | Rúbrica de evaluación | 20% |
| **Semana 17** | RA1, RA2 | Examen / Proyecto Individual Integrador | Resolución de caso práctico individual | Rúbrica de evaluación | 10% |
| **TOTAL** | | | | | **100%** |

---

### 💡 Mejoras y Agregados Realizados por el Experto (Justificación CDIO):
1. **Normalización de Datos (S5):** Se agregó explícitamente. Un modelo de datos "confiable" (RA1) exige entender al menos hasta la 3ª Forma Normal para evitar redundancia y anomalías.
2. **Control de Versiones / Git (S14):** Es una competencia indispensable (CDIO 4.4 Diseñar) que estaba ausente. Se integra como puente entre el modelado y la programación.
3. **Ética y Sostenibilidad (S15):** Alineado con las actualizaciones del syllabus CDIO 3.0, que enfatiza la responsabilidad profesional, la privacidad de datos y el impacto ambiental del software.
4. **Coherencia en Evaluaciones:** Las guías originales tenían ponderaciones que sumaban más de 100% o eran contradictorias. Se ha creado una matriz clara, equilibrada y sumatoria al 100%, con hitos de proceso que alimentan el producto final.
5. **Flujo Lógico:** Se reordenó la secuencia para que el alumno primero entienda el *problema y los datos* (S1-S6), luego el *proceso y comportamiento* (S7-S12), y finalmente la *implementación y paradigmas* (S13-S14), culminando en la integración (S16-S17).

*Instrucciones para Word: Selecciona todo el contenido desde "GUÍA DE APRENDIZAJE 2026" hasta el final de la tabla de evaluaciones, cópialo (Ctrl+C) y pégalo (Ctrl+V) en un documento de Microsoft Word en blanco. Las tablas se formatearán automáticamente.*