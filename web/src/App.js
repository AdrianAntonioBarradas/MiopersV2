import React from 'react';
import {Switch, Route} from 'react-router-dom';
import Home from './content/Home';
import SentimentAnalysis from './emotions/SentimentAnalysis';
import SymptomsMonitor from './symptoms/SymptomsMonitor'
import About from './about/About';
import Footer from './Footer';
import NavBar from './NavBar';


/** 
@fileoverview: App.js
@version: 1.0.0
@author: Miopers
@copyright: GIL UNAM 
@see: http://www.miopers.unam.mx/covid/#/

History: Versón 1.0.0 Verión inical del programa desplegable de Miopers para analisis de 
  tweets COVID19 versión actualmente desplegable.

Summary: Página principal de inicio de Miopers, el cual contiene la llamada a los otros componentes de la página web
  como lo son, Home,SentimentAnalysis, SymptomsMonitor, About. Esta sección de código sirve a manera de referencia el resto
  de elementos de la página web que conforma MioPers
*/


class App extends React.PureComponent {
  /**
     * @overview: Clase principal que extiende de React.PureComponent, la cual sirve de base para mandar a llamar al resto de páginas, que forman
     * parte de este proyecto de Miopers web.
     * @returns: Dejamos todos los elementos listos para poder llamar y tener conectitividad de la página web entre sus elementos.
     * 
     */
  render(){

    return (
      <div>
      <NavBar/>
      <Switch>
          <Route exact path={'/'} component={Home}/>
          <Route path='/emociones' component={SentimentAnalysis}/>
          <Route path='/sintomas' component={SymptomsMonitor}/>
          <Route path='/about' component={About}/>
      </Switch>
      <Footer/>
      </div>

    );
  }
}

export default App;
