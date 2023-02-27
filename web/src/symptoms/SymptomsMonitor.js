import React from 'react';
import Container from 'react-bootstrap/Container';
import MexicoCityMap from './MexicoCityMap';
import Timeline from './Timeline';

/** 
@fileoverview: SymptomsMonitor.js
@version: 1.0.0
@author: Miopers
@copyright: GIL UNAM 
@see: http://www.miopers.unam.mx/covid/#/sintomas

History: Versón 1.0.0 Verión inical del programa desplegable de Miopers para analisis de 
  tweets COVID19 versión actualmente desplegable.

Summary: Script que sirve como estructura base de 'Monitor de síntomas' en la página de Miopers, 
  donde después depositamos las gráficas y todos los elementos que forman parte de esta sección
*/

class SymptomsMonitor extends React.Component{

    render(){
      /**
     * @overview: Método de construcción de los elementos de la página web, en esta sección creamos la página y la
     * dividimos en diferentes secciones para que se visualizen diferentes resultados en diferentes gráficas.
     * @see: http://www.miopers.unam.mx/covid/#/sintomas
     */
        return(
            <div>
            <Container className='mt-5 mb-5'>

            <div>
              <h1>Análisis de síntomas para COVID-19</h1>
              <p>
                Este es un sistema automático de vigilancia de síntomas de COVID19 para México
                Los síntomas presentados tienen 2 categorías principales: los físicos causados por
                COVID19 como fiebre, tos o gripe y los transtornos ocasionados por el asilamiento
                social como ansiedad, depresión, insomnio, entre otros.

              </p>
            </div>

            <div className='mt-5 mb-5'>

              <div className='d-flex justify-content-center'>
                <h1> Línea del tiempo de síntomas COVID vs salud mental</h1>
              </div>

              <div className='d-flex justify-content-center text-secondary'>
                <p>
                  El siguiente gráfico representa la cantidad de síntomas relacionados al COVID-19
                  y los estados de salud mental que se pueden presentar en la población debido al aislamiento social y demás factores.
                  Por cada día se presentan dos valores, cada uno de ellos indica la cantidad de apariciones de síntomas de cada tipo (COVID-19 y estados de salud mental o psicológicos),
                  esto con el fin de conocer cómo afecta el paso del tiempo a la frecuencia de estos dos valores.
                </p>
              </div>
              <div className='d-flex justify-content-center text-secondary'>
                <Timeline/>
              </div>

            </div>

            <div className='mt-5 mb-5'>
              <div className='d-flex justify-content-center'>
                <h1> Mapa de síntomas de la CDMX </h1>
              </div>
              <div className='d-flex justify-content-center text-secondary'>
                <p>
                  El siguiente mapa representa la cantidad de tweets por Alcaldía de la Ciudad de México que contienen síntomas relacionados al COVID-19 y los estados de salud mental relacionados al distanciamiento social.
                  Estos valores no son acumulativos, por lo que cada día cambian.
                </p>
              </div>
                <MexicoCityMap/>
            </div>
{/*
  <div className='d-flex justify-content-center'>
      <TweetEmbed id='692527862369357824'/>
  </div>*/
}

                </Container>
            </div>
        );
    }
}

export default SymptomsMonitor;