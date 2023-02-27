import React from 'react';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import {Link} from 'react-router-dom';


/** 
@fileoverview: NavBar.js
@version: 1.0.0
@author: Miopers
@copyright: GIL UNAM 
@see: http://www.miopers.unam.mx/covid/#/

History: Versón 1.0.0 Verión inical del programa desplegable de Miopers para analisis de 
  tweets COVID19 versión actualmente desplegable.

Summary: El módulo NavBar.js se ejecuta como un módulo de navegación donde se escribe el código necesario para 
  poder transladarse entre los diferentes módulos de la página web i.e Monitor de Síntomas & Analísis de emocines
  - Con el código escrito en esta sección se puede navegar entre las páginas web dando click
*/



class NavBar extends React.Component{
  /**
     * @overview: Clase principal para el cambio y navegación entre los elementos de la página web. 
     *  Se da la orden por médio de click, para la navegación entre difetentes elementos de la pag. web.
     * @returns: Clase que posee los elementos de movilidad en la página web. 
     */
  render(){

    return(

      <Navbar collapseOnSelect expand="lg" bg="dark" variant="dark">
        
        <Navbar.Brand as={Link} to={'/'}>COVID-19 México</Navbar.Brand>
        <Navbar.Toggle aria-controls="responsive-navbar-nav" />
          <Navbar.Collapse id="responsive-navbar-nav">
          <Nav className="mr-auto">
            <Nav.Link as={Link} to='/sintomas'>Monitor de síntomas</Nav.Link>
            <Nav.Link as={Link} to='/emociones'>Análisis de emociones</Nav.Link>
          </Nav>
          <Nav>
            <Nav.Link as={Link} to="/about"> Acerca de </Nav.Link>
          </Nav>
          </Navbar.Collapse>
      </Navbar>

    );
  }


}


export default NavBar;