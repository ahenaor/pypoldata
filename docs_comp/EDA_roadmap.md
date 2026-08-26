# Roadmap de un EDA en Ciencias Sociales

### Subtemas secuenciales organizados por nivel de madurez analítica

> *Guía integral para estructurar un Análisis Exploratorio de Datos de principio a fin.*
> *El EDA es un proceso iterativo; cada nivel asume dominio y aplicación del anterior.*

---

## 🟢 Nivel Básico — «Auditoría Estructural y Panorama Inicial»

**Objetivo del nivel:** ¿Qué tengo entre manos, cuál es su forma y en qué estado de calidad se encuentra?

---

### Paso 1 · Carga y primer contacto

Importar el dataset (CSV, Excel, API, base de datos, JSON) e inspeccionar la estructura inicial usando `.head()`, `.tail()`, `.sample()` y las dimensiones del dataset (filas × columnas). Es vital leer el diccionario de datos o metadata si existe: sin saber qué significa cada columna, cualquier análisis posterior será a ciegas.

---

### Paso 2 · Estructura y tipos de datos

Identificar el tipo de cada variable (numéricas continuas y discretas, categóricas nominales y ordinales, booleanas, temporales, texto libre) y verificar que los tipos asignados por el sistema sean correctos. Un error frecuente es que una fecha se cargue como string o un código postal como entero. Renombrar columnas si es necesario para claridad y consistencia analítica.

---

### Paso 3 · Diagnóstico de valores faltantes

Conteo y porcentaje de nulos por variable y visualización de patrones de ausencia (por ejemplo, mapa de nulos con `missingno` o heatmap) para clasificar su naturaleza: ¿son aleatorios (MCAR), condicionados a otra variable (MAR) o sistemáticos (MNAR)? El objetivo no es resolver los faltantes todavía, sino documentar hipótesis sobre *por qué* faltan.

---

### Paso 4 · Diagnóstico de duplicados y rangos plausibles

Búsqueda de filas completamente duplicadas y de duplicados por clave lógica (por ejemplo, mismo código DANE con datos contradictorios). Verificación de rangos plausibles: edades negativas, porcentajes mayores a 100, fechas futuras en datos históricos, inversiones per cápita iguales a cero en municipios con presupuesto asignado. Este paso es la primera línea de defensa contra datos corruptos.

---

### Paso 5 · Estadística descriptiva univariada

Cálculo de medidas de tendencia central (media, mediana, moda), dispersión (desviación estándar, rango, cuartiles Q1–Q3, rango intercuartílico IQR) para variables numéricas y frecuencias absolutas y relativas, moda y cardinalidad (número de categorías únicas) para variables categóricas. El `.describe()` es un punto de partida rápido, pero nunca el punto final.

---

### Paso 6 · Visualización univariada y detección de outliers

Histogramas para evaluar la forma de las distribuciones (simétrica, sesgada, bimodal), gráficos de barras para frecuencias categóricas y boxplots para dispersión y **detección visual de casos extremos (outliers)**. Este es el momento de *observar y documentar* los outliers: ¿cuántos son, en qué variables aparecen, qué tan lejos están del grueso de los datos? Aquí no se toman decisiones sobre ellos; solo se identifican y se registran como hallazgos para el siguiente nivel.

---

## 🟡 Nivel Intermedio — «Limpieza, Interacciones y Contexto»

**Objetivo del nivel:** ¿Cómo estandarizo la información y cómo se relacionan las variables entre sí para revelar verdaderos patrones?

---

### Paso 7 · Tratamiento de valores faltantes e inconsistencias

Decidir la estrategia para cada variable con nulos según su naturaleza y proporción: eliminación (si son pocos y aleatorios), imputación por media, mediana o moda, imputación por grupo, o marcado como categoría propia ("Sin dato"). Paralelamente, estandarizar inconsistencias tipográficas: "Medellín", "MEDELLÍN", "Medellin" deben converger en una sola forma. Unificar formatos de fecha y corregir tipos de datos mal asignados detectados en el Paso 2.

---

### Paso 8 · Tratamiento de outliers

Decidir, con justificación documentada, qué hacer con los outliers detectados en el Paso 6. Las opciones incluyen: mantenerlos (si son valores extremos legítimos y relevantes), excluirlos (si son errores de registro o pertenecen a otra población), o transformarlos (winsorización, capping al percentil 95/99). La decisión debe considerar el impacto que tendrán en los análisis y modelos posteriores. Un outlier en la inversión pública de un municipio puede ser un dato corrupto o puede ser la historia más importante del dataset.

---

### Paso 9 · Análisis bivariado: numérica vs. numérica

Diagramas de dispersión (scatter plots) para pares de variables clave y matrices de correlación con mapa de calor (heatmap) para visión global. Cálculo de coeficientes de correlación de Pearson (relaciones lineales) y Spearman (relaciones monótonas no lineales). Interpretación crítica: correlación no implica causalidad; identificar posibles variables confusoras o relaciones espurias.

---

### Paso 10 · Análisis bivariado: categórica y mixta

Tablas de contingencia (crosstabs) con frecuencias absolutas y relativas para asociaciones entre variables categóricas, acompañadas de heatmaps de frecuencia o gráficos de barras apiladas. Para el cruce categórica vs. numérica: boxplots agrupados, violin plots o estadísticos descriptivos segmentados (`.groupby()` + `.describe()`) para comparar distribuciones entre grupos (por ejemplo, participación electoral por departamento, inversión pública por subregión).

---

### Paso 11 · Análisis de distribuciones

Evaluar la normalidad de las variables numéricas clave mediante histograma con curva teórica superpuesta, QQ-plot y métricas de forma (asimetría y curtosis). Si es necesario para análisis posteriores, aplicar transformaciones: logarítmica, raíz cuadrada o Box-Cox. Este paso es relevante porque muchos modelos estadísticos y de ML asumen o se benefician de distribuciones simétricas.

---

### Paso 12 · Segmentación por subgrupos

Filtrar y comparar subconjuntos poblacionales relevantes (urbano vs. rural, hombres vs. mujeres, pre vs. post reforma, subregión A vs. subregión B) para confirmar que los patrones generales se sostienen dentro de cada grupo. Este paso es crítico para evitar la **paradoja de Simpson**: un patrón que existe en los datos agregados puede desaparecer o invertirse cuando se desagrega. Usar faceting o small multiples para comparación visual rápida.

---

### Paso 13 · Exploración temporal

Si el dataset tiene dimensión de tiempo: gráficos de línea para identificar tendencia general, estacionalidad y quiebres; cálculo de tasas de cambio (variación porcentual período a período); medias móviles para suavizar ruido. Identificar eventos atípicos en el tiempo y correlacionarlos con hechos conocidos (reformas, elecciones, crisis).

---

### Paso 14 · Exploración geoespacial

Si el dataset tiene dimensión territorial: mapas coropléticos para colorear regiones según una variable (abstención por municipio, NBI por departamento), mapas de puntos y de calor para datos geolocalizados. Evaluar autocorrelación espacial (¿los municipios vecinos se parecen entre sí?) y cruzar capas de información sobre el mismo mapa (datos electorales + socioeconómicos + conflicto armado).

---

## 🔴 Nivel Avanzado — «Estructura Latente y Preparación para el Modelo»

**Objetivo del nivel:** ¿Qué patrones invisibles existen, hay sesgos en la recolección y cómo adecúo los datos para el Machine Learning?

---

### Paso 15 · Ingeniería de características (Feature Engineering)

Crear variables derivadas que aporten valor sustantivo a partir de las existentes: ratios (inversión per cápita), diferencias (cambio electoral entre períodos), indicadores binarios (¿superó umbral X?), agrupaciones (rangos de edad, quintiles de ingreso). Codificar variables categóricas para el modelado algorítmico: one-hot encoding, label encoding, frequency encoding. Extraer componentes temporales si aplica (año, mes, trimestre, día de la semana).

---

### Paso 16 · Análisis multivariado y reducción de dimensionalidad

Pair plots (matrices de dispersión) o coordenadas paralelas para explorar simultáneamente múltiples relaciones e interacciones (¿el efecto de X sobre Y cambia según el nivel de Z?). Aplicar PCA (Análisis de Componentes Principales) para comprimir variables numéricas en pocas componentes que retengan la mayor varianza; visualizar en 2D con biplots. Utilizar t-SNE o UMAP para proyecciones no lineales que preserven estructura local y revelen agrupaciones que PCA no captura. Interpretar: ¿qué variables originales contribuyen más a cada componente? ¿Los grupos emergentes tienen sentido sustantivo?

---

### Paso 17 · Clustering exploratorio

Aplicar segmentación para descubrir agrupaciones naturales sin etiquetas previas. K-Means con el método del codo y el coeficiente de silueta para elegir k óptimo; DBSCAN para clusters de forma irregular y detección simultánea de outliers; clustering jerárquico con dendrogramas para visualizar la estructura a diferentes niveles de granularidad. El paso clave es el **perfilamiento**: ¿qué caracteriza a cada grupo? ¿Tienen interpretación política o social coherente? Un cluster sin sentido sustantivo es un artefacto estadístico, no un hallazgo.

---

### Paso 18 · Exploración textual (pre-NLP)

Si el dataset incluye texto (discursos, actas, publicaciones, encuestas abiertas): tokenización, limpieza de stopwords, normalización (lowercasing, stemming o lematización). Análisis de frecuencia de términos, nubes de palabras, bigramas y trigramas frecuentes. Aplicar TF-IDF para identificar términos distintivos por documento o categoría. Evaluar distribución de longitud de documentos y vocabulario único por grupo. Este paso prepara el terreno para técnicas de NLP avanzado (modelado de tópicos, clasificación, análisis de sentimiento).

---

### Paso 19 · Validación de hipótesis y significancia estadística

Cuantificar la validez estadística de los patrones visuales descubiertos en pasos anteriores. Comparación de dos grupos con t-test (paramétrico) o Mann-Whitney U (no paramétrico); tres o más grupos con ANOVA o Kruskal-Wallis; proporciones con test Z o test exacto de Fisher; asociación entre categóricas con Chi-cuadrado. Calcular intervalos de confianza para cuantificar incertidumbre y tamaño del efecto (Cohen's d, eta-cuadrado) para verificar si la diferencia es estadísticamente significativa **y** prácticamente relevante. Un p-valor pequeño con un efecto minúsculo no es un hallazgo útil.

---

### Paso 20 · Selección de variables (Feature Selection)

Identificar los mejores predictores para el modelado. Métodos de filtro: correlación con la variable objetivo, información mutua, ANOVA F-score. Métodos wrapper: selección hacia adelante, hacia atrás o paso a paso evaluando rendimiento de un modelo. Métodos embebidos: importancia de variables desde Random Forest o coeficientes de Lasso. Detectar y tratar multicolinealidad con VIF (Factor de Inflación de la Varianza): variables altamente correlacionadas entre sí deben eliminarse o combinarse para evitar redundancia e inestabilidad en los modelos.

---

### Paso 21 · Evaluación de sesgos y representatividad de la muestra

Antes de pasar los datos a un modelo, evaluar críticamente **a quién representan y a quién excluyen**. ¿Hay subpoblaciones sub-representadas (municipios rurales del Pacífico, comunidades indígenas, población migrante)? ¿Los datos reflejan solo centros urbanos o zonas con mejor infraestructura de reporte? ¿Existen sesgos de selección, de supervivencia o de medición que el modelo podría amplificar? Para ciencias políticas esto no es un tecnicismo: un modelo entrenado con datos que sub-representan a ciertas poblaciones producirá predicciones injustas para esas mismas poblaciones, y las decisiones de política pública basadas en él reproducirán desigualdades. Documentar los sesgos detectados y las limitaciones de generalización del análisis.

---

### Paso 22 · Profiling automatizado como auditoría cruzada

Ejecutar herramientas de EDA automatizado (`ydata-profiling`, `sweetviz`, `dataprep`) para generar un reporte HTML integral que incluya tipos, distribuciones, correlaciones, alertas de calidad y patrones de nulos. Este paso no reemplaza el análisis manual de los pasos anteriores: funciona como **auditoría cruzada** para detectar hallazgos que el ojo humano pudo haber pasado por alto y como recurso de documentación rápida para compartir el estado del dataset con un equipo o supervisor.

---

### Paso 23 · Síntesis, documentación y transición al modelado

Documentar todas las decisiones tomadas a lo largo del EDA: qué se limpió, qué se transformó, qué se excluyó y la justificación de cada acción. Resumir los hallazgos clave: patrones principales, hipótesis generadas, variables candidatas para modelado y limitaciones de los datos. Definir la variable objetivo (si aplica) y el tipo de problema (clasificación, regresión, clustering). Exportar la matriz final limpia, establecer la partición train/test y documentar el pipeline de preprocesamiento de forma reproducible. El EDA no "termina" aquí: se reactiva cada vez que el modelo revela errores, residuos anómalos o preguntas nuevas.

---

> **Nota final:** No todo EDA requiere los 23 pasos completos. La profundidad depende del problema, los datos y el objetivo. Lo esencial es que cada decisión esté documentada, justificada y sea reproducible, y que el EDA se entienda como un ciclo vivo que se retroalimenta con el modelado y la interpretación.

---
*Referencia de apoyo para el curso «Analítica de Datos y Machine Learning en Ciencias Políticas» — UdeA 2026-2*
