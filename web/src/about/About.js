import React from 'react';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

/** 
@fileoverview: About
@version: 1.0.0
@author: Miopers
@copyright: GIL UNAM 
@see: http://www.miopers.unam.mx

History: Versón 1.0.0 Verión inical del programa desplegable de Miopers para analisis de 
  tweets COVID19 versión actualmente desplegable.

Summary: Descripción escrita en react, donde aparece la información de los colaboradores del proyecto.
  Y su estatus en este.
*/

class About extends React.Component{
    render(){
        return(
            <div>


                <Container>
                // Descripción de los colaboradores del proyecto.
                <div className='mt-5 mb-5'>
                  <div className='d-flex justify-content-center'>
                      <h1>Quiénes somos</h1>
                  </div>
                  <div>
                      <p>Somos un grupo de investigadores, profesores y estudiantes pertenecientes a la Universidad Nacional Autónoma de México (UNAM), particularmente al Instituto de Ingeniería (IIUNAM) y al Instituto de Investigaciones en Matemáticas Aplicadas y en Sistemas (IIMAS) con interés en el procesamiento del lenguaje natural. Este proyecto consta de un sistema automático de vigilancia de COVID19 mediante Twitter, en el cual se busca analizar mensajes de esta red social para evaluar el comportamiento de las personas, estados de ánimo, la popularidad de las medidas dadas por el gobierno, y, además, monitorear usuarios con posibles síntomas de coronavirus en tiempo real a través de Internet.</p>
                  </div>
                  <div className='d-flex justify-content-center'>
                      <h2>Colaboradores principales (orden alfabético)</h2>
                  </div>
                </div>

                <div className='mt-5 mb-5'>
                <Row >
                  <Col>
		    <h4 >Gabriel Castillo (IINGEN)</h4>
                    <ul>
                        <li>Técnico Académico Titular "B" del Instituto de Ingeniería</li>
                        <li>gch@pumas.iingen.unam.mx</li>
                  </ul>
                  </Col>

                  <Col>
                    <h4 >Gemma Bel Enguix (IINGEN)</h4>
                    <ul>
                        <li>Investigadora Titular “A”   del Instituto de Ingeniería</li>
                        <li>Miembro del Sistema Nacional de   Investigadores</li>
                        <li>Contacto: gbele@iingen.unam.mx</li>
                    </ul>
                  </Col>
                </Row>
                </div>

                <div className='mt-5 mb-5'>
                <Row >
                  <Col>
                   <h4>Gerardo Sierra   (INGEN)</h4>
                  <ul>
                      <li>Investigador Titular “B” del   Instituto de Ingeniería</li>
                      <li>Miembro del Sistema Nacional de Investigadores   Nivel II</li>
                      <li>Contacto: gsierram@iingen.unam.mx</li>
                  </ul> 
                  </Col>

                  <Col>
                  <h4>Helena Gómez Adorno (IIMAS)</h4>
                  <ul>
                      <li>Investigadora Asociada “C”   del Instituto de Investigaciones en Matemáticas Aplicadas y en Sistemas</li>
                      <li>Miembro del Sistema Nacional de   Investigadores Nivel I</li>
                      <li>Contacto: helena.gomez@iimas.unam.mx</li>
                  </ul>
                  </Col>
                </Row>
                </div>
		
		<div className='d-flex justify-content-center'>
  		  <h3>Otros colaboradores</h3><br></br>
                </div>
		<div className='d-flex justify-content-center'>
  	        <ul>
		  <li>Jessica Sarahi Méndez Rincón</li>
		  <li>Jesús Germán Ortiz Barajas</li>
		  <li>José Armando López Velasco</li>
		  <li>Pablo Camacho González</li>
		  <li>Ricardo Jiménez Cruz</li>
		</ul>
		</div>
                </Container>
            </div>
        );
    }
}

export default About;
