import React from 'react';
import Container from 'react-bootstrap/Container';
import TimelineEmotions from './TimelineEmotions';
import TimelinePolarity from './TimelinePolarity';

class SentimentAnalysis extends React.Component{
    render(){
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
                    <h1> Linea del tiempo de emociones </h1>
                  </div>

                  <div className='d-flex justify-content-center text-secondary'>
                    <p>
                      La siguiente linea del tiempo presenta las emociones causadas en los usuarios de la
                      red social.
                    </p>
                  </div>
                  <div className='d-flex justify-content-center text-secondary'>
                    <TimelineEmotions/>
                  </div>

                </div>

      
                <div className='mt-5 mb-5'>
                  <div className='d-flex justify-content-center'>
                    <h1> Linea del tiempo de polaridad </h1>
                  </div>

                  <div className='d-flex justify-content-center text-secondary'>
                    <p>
                      La siguiente linea del tiempo presenta la polaridad de los mensajes
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