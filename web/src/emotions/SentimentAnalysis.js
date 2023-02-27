import React from 'react';
import Container from 'react-bootstrap/Container';
import TimelineEmotions from './TimelineEmotions';
import TimelinePolarity from './TimelinePolarity';

/** 
@fileoverview: SentimentAnalysis.js
@version: 1.0.0
@author: Miopers
@copyright: GIL UNAM 
@see: http://www.miopers.unam.mx/covid/#/emociones

History: Versón 1.0.0 Verión inical del programa desplegable de Miopers para analisis de 
  tweets COVID19 versión actualmente desplegable.

Summary: Script que aporta la estructura general de la página 'Análisis de emociones' la cual nos sirve de base para el almacenamiento
de todo el resto de gráficas.
*/

class SentimentAnalysis extends React.Component{
    render(){
      /**
     * @overview: Método de estructura general del documento, en este se establece la estructura de la página y sus gráficas
     * @returns: Diseño de secciones de la pagina web. 
     */

        return(
            <div>
                <Container className='mt-5 mb-5'>
                <div>
                  <h1>Análisis de emociones</h1>
                  <p>
                    Este es un sistema que monitorea las emociones provocadas por el COVID19 en Twitter
                  </p>
                </div>

                <div className='mt-5 mb-5'>

                  <div className='d-flex justify-content-center'>
                    <h1> Línea del tiempo de emociones </h1>
                  </div>

                  <div className='d-flex justify-content-center text-secondary'>
                    <p>
                      La siguiente línea del tiempo presenta las emociones causadas en los usuarios de la
                      red social.
                    </p>
                  </div>
                  <div className='d-flex justify-content-center text-secondary'>
                    <TimelineEmotions/>
                  </div>

                </div>

      
                <div className='mt-5 mb-5'>
                  <div className='d-flex justify-content-center'>
                    <h1> Línea del tiempo de polaridad </h1>
                  </div>

                  <div className='d-flex justify-content-center text-secondary'>
                    <p>
                      La siguiente línea del tiempo presenta la polaridad de los mensajes
                      escritos por los usuarios.
                    </p>
                  </div>
                  <div className='d-flex justify-content-center text-secondary'>
                    <TimelinePolarity/>
                  </div>
                </div>

                </Container>
            </div>
        );
    }
}

export default SentimentAnalysis;
