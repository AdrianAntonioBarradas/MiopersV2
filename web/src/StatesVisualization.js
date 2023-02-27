import React from 'react';
import DropdownButton from 'react-bootstrap/DropdownButton';
import Dropdown from 'react-bootstrap/Dropdown';
import NavBar from './NavBar';
import Footer from './Footer'
import Container from 'react-bootstrap/Container';
import TweetsCard from './TweetsCard';


/** 
@fileoverview: StatesVisualization.js
@version: 1.0.0
@author: Miopers
@copyright: GIL UNAM 
@see: http://www.miopers.unam.mx/covid/#/

History: Versón 1.0.0 Verión inical del programa desplegable de Miopers para analisis de 
  tweets COVID19 versión actualmente desplegable.

Summary: Módulo que contiene toda la informacíon relativa a las visualizaciones de los gráficos dentro del programa 
    de Miopers, contiene una funcion que nos permite obtener el nombre de los estados así como una clase con los parámetros
    de configuración para el programa. 

*/


function getStatesNames(worlddata){
    // @overview: Función que funciona a manera de auto-incremente para poder leer la cantida de estaods que emiten 
    // tweets y así poder extraer sus nombres del modulo worlddata. 
    var states_names = [];
    for(var i=0; i<worlddata.length; i++){
        states_names.push(worlddata[i].properties.name);
    }
    return states_names
};

class StatesVisualization extends React.Component{

    /**
     * @overview: La clase nos ayuda a la visualización de las targetas con la información de tweets emitidos por cada uno de los estados
     * @returns: Regresa la configuración general para poder trabajar con los datos almecenados en mexico.geojson y poder desplegar la inforamción 
     *  que aquí se almacena para poder desplegar las targetas e inforamción del mapa interactivo de la republica y los tweets de cada uno. 
     */

    constructor(props){
        super(props);
        this.state = {
            selectedOption: '',
            states:[],
            isLoaded:false,
            error:null
        };
    }

    componentDidMount(){
        // Conección con el archivo mexico.geojson para poder leer la inforamción de este
      fetch("https://raw.githubusercontent.com/RicardoJC/Mexico-Datos-COVID19/master/home/mexico.geojson")
            .then(res => res.json())
            .then(
              (result) => {
                var names = getStatesNames(result.features);
                this.setState({
                  isLoaded: true,
                  states: names,
                  selectedOption: names[0]
                });
              },
              // Note: it's important to handle errors here
              // instead of a catch() block so that we don't swallow
              // exceptions from actual bugs in components.
              (error) => {
                this.setState({
                  isLoaded: true,
                  error
                });
              }
            );
    }

    handleSelect(eventKey, event){
        /*
            @overwrite: Método para poder acceder a la información con el hecho de pasar el mouse sobre cada uno de los estados.
        */
        this.setState({selectedOption: this.state.states[eventKey]});
        console.log(this.state.selectedOption)
    };

    render(){
        return(
            <div>
                <NavBar/>
                <Container  className='mt-5 mb-5'>
                    <div className ='mt-5 mb-5'>
                        <div className='d-flex justify-content-center'>
                            <DropdownButton title="Selecciona un estado" onSelect={this.handleSelect.bind(this)}>
                                {this.state.states.map((opt,i) => (
                                    <Dropdown.Item key={i} eventKey={i}>
                                        {opt}
                                    </Dropdown.Item>
                                ))}
                            </DropdownButton>
                        </div>
                        <br/>
                        <div className='d-flex justify-content-center'>
                                <h1>{this.state.selectedOption}</h1>
                        </div>
                        <br/>
                        <div className='d-flex justify-content-center'>
                                <h3>Tweets en la entidad</h3>
                        </div>
                        <TweetsCard/>
                    </div>
                </Container>
                <Footer/>
            </div>
        );
    }
}


// Exportación de los resultados de este modulos para ser leidos por la ágina web general.
export default StatesVisualization;