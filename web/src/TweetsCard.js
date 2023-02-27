import React from 'react';
import Card from 'react-bootstrap/Card';


/** 
@fileoverview: TweetsCard.js
@version: 1.0.0
@author: Miopers
@copyright: GIL UNAM 
@see: http://www.miopers.unam.mx/covid/#/

History: Versón 1.0.0 Verión inical del programa desplegable de Miopers para analisis de 
  tweets COVID19 versión actualmente desplegable.

Summary: Módulo .js para la lectura y cración de targetas en la página web con información del número de tweets
    acumulados a lo largo de los días. El código es un esquema general para poder crar targertas sobre la cantidad 
    de tweets totales y reconocer aquellos cuya tematica principal es el Covid 19
TODO: --Tengo la duda sobre que otros modulos influye esta, pues parece ser padre. 


*/


class TweetsCard extends React.Component{
    /**
     * @overview: Clase general de estructura para creación de targetas con información relativa a los tweets de covid 19
     * @returns: La clase general sobre la creación de targetas de tweets en la CDMX. m
     */

    render(){
        return(
            <div className='d-flex justify-content-center'>
            <Card border="secondary" style={{ width: '18rem' }}>
                <Card.Body>
                    <Card.Title class='text-center'>Tweets totales</Card.Title>
                    <Card.Text class='text-center'>
                        <h1>123</h1>
                    </Card.Text>
                </Card.Body>
            </Card>
            <Card border="secondary" style={{ width: '18rem' }}>
                <Card.Body>
                    <Card.Title class='text-center'>Tweets sobre Covid19</Card.Title>
                    <Card.Text class='text-center'>
                        <h1>123</h1>
                    </Card.Text>
                </Card.Body>
            </Card>
        </div>            
        );
    }
}

export default TweetsCard;