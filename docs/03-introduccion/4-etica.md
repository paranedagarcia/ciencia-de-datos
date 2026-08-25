---
id: etica
title: "Ética y privacidad de datos"
sidebar_label: "📚 Ética"
description: "Aplicación y uso ético de los datos"
slug: /etica
---
import YouTubeVideo from '@site/src/components/YouTubeVideo';

## Aspectos éticos

La implementación de sistemas de Inteligencia Artificial (IA) en el ámbito público y social no se reduce a un desafío puramente tecnológico; constituye, ante todo, un reto ético y normativo de alta complejidad. Dado que las decisiones y predicciones de estos sistemas impactan de manera directa sobre los derechos, el bienestar y las oportunidades de vida de los ciudadanos, es indispensable articular un marco ético riguroso que guíe todo el ciclo de vida del sistema (diseño, recolección de datos, desarrollo, validación y monitoreo).

https://ceedia.org/comision-europea-directrices-eticas-sobre-una-ineligencia-artificial-confiable/


### Videos

Éticay regulación en IA - CDO Latam
<YouTubeVideo id="a5qI551l0wo" title="Etica y regulación en la IA" />

Conferencia Magistral: "La recomendación sobre la ética de la inteligencia artificial"
- Programa Universitario de Bioética- UNAM
<YouTubeVideo id="iNoOj41oRYY" title="Etica y regulación en la IA" />



Se detallan los principales aspectos éticos implicados en la implementación de la IA, fundamentados en las directrices de organismos internacionales como la **OCDE** y la **UNESCO**, así como en marcos regulatorios y políticas públicas nacionales.

---

### El Principio de Primacía Humana y Supervisión (*Human Oversight*)
Este principio establece que la IA debe concebirse estrictamente como una herramienta al servicio de las personas, respetando la dignidad humana y la autonomía personal, garantizando que el control y la vigilancia final de las decisiones críticas permanezcan bajo el criterio humano. 

La interacción y gobernanza humano-máquina se estructura bajo tres arquetipos de supervisión:
*   **Humano en el bucle (*Human-in-the-loop* - HITL):** El sistema de IA actúa como un soporte o asistente que genera recomendaciones o borradores, pero es un operador humano quien toma, aprueba o ejecuta de manera obligatoria la decisión final. Este enfoque es imperativo en áreas de alto riesgo, como la salud, la adjudicación de beneficios sociales o decisiones judiciales.

*   **Humano sobre el bucle (*Human-on-the-loop* - HOTL):** El sistema opera de forma autónoma en tiempo real, pero el supervisor humano monitorea continuamente su comportamiento y tiene la facultad y capacidad técnica de intervenir o detener (*switch-off*) el proceso ante un funcionamiento anómalo o un error del algoritmo.

*   **Humano fuera del bucle (*Human-out-of-the-loop* - HOOTL):** El sistema toma y ejecuta decisiones de manera totalmente autónoma sin intervención humana directa. En la gestión pública, la delegación a sistemas totalmente automatizados de este tipo debe ser sumamente restringida o prohibida cuando afecte derechos fundamentales.

#### El Sesgo de Automatización (*Automation Bias*)

Uno de los mayores riesgos en la supervisión humana es el **sesgo de automatización**: la propensión cognitiva de los funcionarios a confiar ciegamente en las salidas del modelo por percibirlas como "neutrales" u "objetivas". Esto puede provocar que los operadores acepten decisiones erróneas o alucinadas del algoritmo sin someterlas a un escrutinio crítico o juicio profesional. Para mitigarlo, se requiere capacitación continua y el diseño de interfaces que obliguen al funcionario a justificar activamente cualquier discrepancia.

---

### Equidad, Diversidad y Mitigación del Sesgo Algorítmico
La equidad algorítmica (*fairness*) exige que los sistemas de IA no perpetúen, amplifiquen o creen discriminación sistémica o estereotipos nocivos hacia personas o grupos protegidos por factores como género, raza, edad, etnicidad o nivel socioeconómico.

#### El Ciclo del Sesgo y Datos de Entrenamiento
La IA aprende de datos históricos que inevitablemente reflejan prejuicios, inequidades y desigualdades del mundo real. Si estos datos se inyectan sin una curación rigurosa, el algoritmo codificará y escalará el sesgo de forma automatizada:
*   **Ejemplo Histórico de Reclutamiento:** En 2015, un sistema experimental de selección de personal de Amazon entrenado con currículums de los diez años anteriores (una década dominada por hombres debido al sesgo histórico del sector tecnológico) aprendió a discriminar sistemáticamente a las candidatas mujeres, penalizando currículums que incluyeran la palabra "femenino".

*   **Sesgos en Reconocimiento Facial:** Diversos algoritmos de visión artificial han mostrado tasas de error significativamente mayores en rostros femeninos y de pieles oscuras debido a la subrepresentación de estos grupos en los datasets de entrenamiento.

*   **Casos de Exclusión en el Estado:** El escándalo *Toeslagenaffaire* en los Países Bajos ilustró cómo un algoritmo de detección de fraude en beneficios por cuidado infantil sesgado se dirigió injustamente hacia familias de origen inmigrante y doble nacionalidad, destruyendo vidas antes de ser cancelado.

#### Criterios Matemáticos de Justicia Algorítmica

Dado que el concepto filosófico de "justicia" es amplio, el equipo técnico, bajo la dirección de los responsables de políticas públicas, debe formalizar criterios matemáticos de equidad, los cuales a menudo son mutuamente excluyentes:
1.  **Paridad Demográfica:** Exige que la tasa de selección o predicción positiva sea equivalente para todos los subgrupos (ej. misma proporción de créditos aprobados para hombres y mujeres).
2.  **Equidad de Posibilidades:** Requiere que el desempeño predictivo del modelo (sus tasas de falsos positivos y falsos negativos) sea independiente de la variable protegida cuando se conoce el valor verdadero.
3.  **Justicia Contrafactual:** Establece que la predicción del modelo para un individuo debe ser exactamente la misma si se cambia el valor de su atributo protegido (por ejemplo, cambiar el género de "femenino" a "masculino"), manteniendo el resto de las variables constantes.

---

### Transparencia, Explicabilidad y Auditabilidad
Para garantizar la rendición de cuentas (*accountability*), el Estado debe evitar el uso de sistemas que operen como una **"caja negra"** (*black-box*), donde la complejidad interna del modelo (con millones de parámetros y capas no lineales) impida comprender cómo se llegó a un resultado específico.

#### Requisitos Éticos de Transparencia
*   **Derecho a la Explicación:** Regulaciones internacionales (como el Artículo 22 del RGPD de la Unión Europea) respaldan el derecho de los ciudadanos a obtener explicaciones claras sobre la lógica de las decisiones automatizadas que afecten sus derechos.

*   **Trazabilidad:** Exige la documentación exhaustiva del ciclo de vida del dato, el código, el ambiente de cómputo y las decisiones de diseño del modelo, permitiendo que un tercero independiente replique el proceso.

*   **Métodos de Explicabilidad Individual:** Ante modelos complejos como redes neuronales profundas, se deben aplicar metodologías como explicaciones contrafactuales, valores de Shapley o gradientes integrados para descomponer la contribución de cada variable a la decisión final.

*   **Registros Algorítmicos Públicos:** Herramientas proactivas de transparencia implementadas en ciudades como Ámsterdam, Helsinki y Nueva York que divulgan abiertamente el propósito, el funcionamiento, los datos utilizados y la supervisión humana de los algoritmos gubernamentales activos.

---

### Privacidad, Gobernanza de Datos y Seguridad
Los sistemas de IA modernos requieren volúmenes masivos de datos para su entrenamiento, lo que genera serias tensiones con la protección de datos personales y la privacidad de los ciudadanos.

*   **Riesgo de Memorización y Reconstrucción:** Los Modelos de Lenguaje de Gran Tamaño (LLMs) pueden memorizar involuntariamente información personalmente identificable (PII) presente en sus datasets de entrenamiento, exponiéndola en sus respuestas (*regurgitation*).

*   **Derechos de Participación Individual:** Los derechos de acceso, rectificación, portabilidad y supresión (derecho al olvido) resultan sumamente complejos de aplicar en IA, ya que eliminar la información de un ciudadano puede requerir un reentrenamiento costoso de todo el modelo.

*   **Tecnologías de Preservación de la Privacidad (PETs):** Para mitigar estos riesgos, se deben implementar salvaguardas técnicas como la privacidad diferencial (*differential privacy*), la anonimización y seudonimización rigurosa de datos, y entornos de cómputo confidencial.

---

### Sostenibilidad Ambiental e Impacto en el Empleo
*   **Sostenibilidad Ambiental:** El entrenamiento y despliegue de grandes modelos fundacionales e infraestructuras de supercómputo exigen un consumo energético y de agua extraordinariamente alto, con una huella de carbono significativa. Es un deber ético promover la eficiencia de los recursos de hardware, aplicar técnicas de compresión (como la cuantización) y utilizar fuentes de energía renovables.

*   **Impacto en el Trabajo:** La automatización no debe enfocarse éticamente en el reemplazo masivo de los trabajadores públicos, sino en el aumento de sus capacidades (*augmented intelligence*). Se debe prever y mitigar la "intensificación del trabajo" o el **"taylorismo digital"** derivado del uso de sistemas de gestión algorítmica para monitorear y regular de forma invasiva la conducta laboral de los funcionarios.



### Atribución de Responsabilidad (*Responsibility Gaps*)
La delegación progresiva de decisiones críticas a algoritmos autónomos genera el peligro de crear "brechas de responsabilidad" (*responsibility gaps*). Esto ocurre cuando se produce un daño algorítmico, pero resulta imposible asignar la culpabilidad legal o moral a un actor humano específico debido a la complejidad en la cadena de desarrollo (diseñadores de software, proveedores de datos, implementadores, usuarios intermedios).

La ética aplicada exige que, en última instancia, **la responsabilidad profesional y legal de las consecuencias del funcionamiento de un sistema de IA recaiga de forma indelegable sobre los seres humanos y las instituciones** que decidieron diseñar, comprar, desplegar u operar dicha tecnología.


