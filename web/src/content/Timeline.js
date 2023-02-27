import React, { Component, PureComponent } from 'react';
import {
  LineChart, Line, XAxis, YAxis,
  CartesianGrid, Tooltip, Brush,Legend, AreaChart, Area,
  ResponsiveContainer,ReferenceLine, ReferenceArea
  } from 'recharts';
import ReferenceDot from 'recharts/lib/cartesian/ReferenceDot';

import axios from 'axios';
import {useState, useEffect} from 'react';
// import  json from '../data/timeline_result';

/** 
@fileoverview: Timeline.js
@version: 1.0.0
@author: Miopers
@copyright: GIL UNAM 
@see: http://www.miopers.unam.mx/covid/#/

History: Versón 1.0.0 Verión inical del programa desplegable de Miopers para analisis de 
  tweets COVID19 versión actualmente desplegable.

Summary: Script donde se configura el despliegue de la gráfica de palabras clave en la sección de linea del
  tiempo de palabras clave en la página COVID-19 México de Miopers
*/


// Constantes de bordes y forma del gráfico
const styles = {
  chart:{
    flex: 1,
    width: 0
  },
  updateDate:{
    marginBottom:'10px'
  }
};




// Ejemplo customatizado de referencia con dot Reference.
const CustomReferenceDotOrange = props => {
  return (
    <circle cx={props.cx} r="5" cy={props.cy} fill="#e65100">
      <animate
        attributeName="r"
        from="8"
        to="15"
        dur="1.5s"
        begin="0s"
        repeatCount="indefinite"
      />
    </circle>
  );
};


class Timeline extends PureComponent {

  constructor(props){
    super(props);
    this.state = {
      error: null,
      isLoaded: false,
      data: [],
      time:''
    };
  }

  componentDidMount() {
    axios.get('http://localhost:8000/api/timeline')
        .then(res => {
          this.setState({ 
            data: res.data.data,
            time: res.data.time,
            isLoaded: true 
          });
        })
        .catch(error => {
          this.setState({
            isLoaded: true,
            error
          });
        });
  }

  
    
    render() {
      /**
     * @overview: Método de lectura de los datos del método anterior y visualización. 
     * Se crea la estructura general de la gráfica o se manda le mensaje de que no puede ser desplegada. 
     * Se despliega el código de la gráfica dinamica de los tweets de las palabras claves seleccionadas.
     * @see: http://www.miopers.unam.mx/covid/#/
     */
      const { data, time, error, isLoaded } = this.state;
      if (error) {
        return <div>Error: {error.message}</div>;
      } else if (!isLoaded) {
        return <div>Loading...</div>;
      } else {
        return (
          <div>
            <div style={styles.updateDate} className='d-flex justify-content-center font-weight-lighter'>
              <span>Última actualización: {time}</span>
            </div>
            <ResponsiveContainer width="100%" height={400}>
              <LineChart
                data={data}
                margin={{
                top: 5, right: 25, left: 20, bottom: 7,
                }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="day" />
                <YAxis />
                <Tooltip />
                <Legend verticalAlign="top" wrapperStyle={{ lineHeight: '40px' }} />
                <ReferenceLine x="2020-05-31" label="Fin de jornada de sana distancia" stroke="red" />
                <ReferenceDot x="2020-07-26" y={600} label="Semaforo" shape={CustomReferenceDotOrange}/>
                <ReferenceDot x="2020-04-21" y={200} label="Fase 3" stroke="red"/>
                <ReferenceDot x="2021-05-13" y={200} label="Inicio Vacunación" />
                <ReferenceDot x="2020-06-16" y={200} label="Segunda ola contagios" stroke="blue"/>
                <ReferenceDot x="2020-05-07" y={350} label="Segundo confinamiento" stroke="red"/>
                <Line type="monotone" dataKey="coronavirus" stroke="#00e676" strokeWidth='1' animationDuration={4000} />
                <Line type="monotone" dataKey="quedateencasa" stroke="#1b5e20" strokeWidth='1' animationDuration={3500}/>
                <Line type="monotone" dataKey="covid19" stroke="#e65100" strokeWidth='1' animationDuration={1500}/>
                <Line type="natural" dataKey="@HLGatell" stroke="#f44336" strokeWidth='1' animationDuration={3000}/>
                <Line type="natural" dataKey="@lopezobrador_" stroke="#b71c1c" strokeWidth='1' animationDuration={2500}/>
                <Line type="natural" dataKey="SusanaDistancia" stroke="#ffab00" strokeWidth='1' animationDuration={2000}/>
                <Brush dataKey="day" height={40} stroke="#8884d8"  />
              </LineChart>
            </ResponsiveContainer>
          </div>
        );
      }
    }
}




export default Timeline;
