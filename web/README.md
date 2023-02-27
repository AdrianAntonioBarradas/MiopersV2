# Miopers-Web

Este repositorio contienen el código de la página de web de **MiOpERS** desarrolla en su mayoría en `React`. El repositorio tiene los archivos que alimentan la página web en `src` así como el código de multiples gráficas interactivas en la versión 1.0 del proyecto MiOpERS.

## Introducción:

Este respositorio es uno de los 5 subrepositorios del proyecto **MiOpERS** que alimentan la página principal de <a href="http://www.miopers.unam.mx">MiOpERS</a>. Contienen los códigos que soportan la información de los colaboradores del proyecto así como el diseño gráfico de la página web, además del diseño de las gráficas interactivas de la misma.



## Tabla de contenido
El repositorio contiene 2 carpetas principales llamadas `public` y `src` donde la primera contiene imagenes de los logos institucionales y un *index.html* y la segunda carpeta todo el código que soporta la página distribuido de la siguiente manera:

- [**about**](#about)
- [**content**](#content)
- [**emotions**](#emotions)
- [**symptoms**](#symptoms)

## **about**
La carpeta about contiene la parte del código donde se hace mención a los desarrolladores del proyecto y sus aportes a este. 

### Contenido:
- About.js


## **content**
Esta carpeta contienen el grueso del código que soporta la página web, contiene documentos que son el inico de la página así como los elementos interactivos en `JavaScript` para que los usuarios puedan interactar con los gráficos dinámicos de la historía de los tweets.

### Contenido:
- `Cards.js`: Código de las targetas dinámicas con información de las menciones, hashtags y palabras del día-
- `EmotionalRadar.js`: - Código del conteo de sentimientos 
- `Home.js`: - Código del inicio de la página web.
- `Timeline.js`: - Visualización en forma de registro de los elementos que se encuentran en la página web.
- `WorldMap.js`: - Mapa interactivo de los tweets por estado de la republica.
- `map.css`: - Estilos de los mapas interactivos en la página.


## **emotions**
Esta carpeta corresponde a la sección de **Analísis de emociones** en la página web y los elementos que ahí se pueden observar.

Principalmente contiene información sobre la gráfica de la línea de tiempo de los sintomas vs salud mental y el mapa interactivo de la CDMX y los sintomas presentados.
### Contenido:
- `EmotionalRadar.js`: - Realiza un analisis de los tweets y los clasifica según el sentimiento que mejor se adecue.
- `SentimentAnalysis.js`: - Modulo principal de sentimientos de analísis y clasificación de tweets por sentimiento.
- `TimelineEmotions.js`: - Implementación cronológica de la clasificación de los sentimientos de SentimentAnalysisl.js
- `TimelinePolarity.js`: - Clasificación de la polaridad de los tweets por polaridad para despliegue en MiOpERS
- `WorldMap.js`: - Implementación en el mapa de la ciudad de méxico donde se cuenta el número de sintomas por alcaldía.

## **symptoms**
Esta carpeta corresponde a la sección de **Análisis de emociones** en la página web y los elementos que ahí se observan.

Principalmente se contiene información relativa con la polaridad y los tipos de emociones detectados con los tweets a lo largo del tiempo en el estudio del COVID-19.
### Contenido:
 - `MexicoCityMap.js`:- Mapa interactivo del número de casos 
 - `SymptomsMonitor.js`: - ??
 - `Timeline.js`: - Implementación gráfica de los tipos de sentimientos clasificados de manera cronologíca.

## Leer datos
En la carpeta web/src/data se guardan los JSON generados por los distintos análisis con los que se construyen las gráficas y mapas.

