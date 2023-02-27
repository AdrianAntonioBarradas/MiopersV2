import React, { PureComponent } from 'react';
import {
  LineChart, Line, XAxis, YAxis,
  CartesianGrid, Tooltip, Legend, Sector,
  ResponsiveContainer,ReferenceLine, Brush
  } from 'recharts';
import axios from 'axios';
  // import json from '../data/timeline.json';


/** git 
@fileoverview: Timeline.js
@version: 1.0.0
@author: Miopers
@copyright: GIL UNAM 
@see: http://www.miopers.unam.mx/covid/#/

History: Versón 1.0.0 Verión inical del programa desplegable de Miopers para analisis de 
  tweets COVID19 versión actualmente desplegable.

Summary: Script donde se configura el despliegue de la gráfica de sintomás en la sección de linea del
  tiempo de síntomas COVID vs salud mental de Miopers
*/

const styles = {
  chart:{
    flex: 1,
    width: 0
  },
  updateDate:{
    marginBottom:'10px'
  }
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
    axios.get('http://127.0.0.1:8000/api/sintomas/')
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
     * Se despliega el código de la gráfica dinamica de los tweets de los sintomas COVID vs salud mental
     * @see: http://www.miopers.unam.mx/covid/#/sintomas
     */
    const {data,time, error, isLoaded } = this.state;
    if (error) {
      return <div>Error: {error.message}</div>;
    } else if (!isLoaded) {
      return <div>Loading...</div>;
    } else {
      return (

        <div style={styles.chart} >
          <div style={styles.updateDate} className='d-flex justify-content-center font-weight-lighter'>
            <span>Última actualización: {time}</span>
          </div>
        <ResponsiveContainer width="99%" height={400}>
        <LineChart
          data={data}
          margin={{
            top: 5, right: 25, left: 20, bottom: 7,
          }}
          >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="day" />
          <YAxis />
          <Tooltip />
          <Legend verticalAlign="top" wrapperStyle={{ lineHeight: '40px' }} />
          <ReferenceLine x="2020-04-21" label="Fase 3" stroke="red" />
          <ReferenceLine x="2020-05-31" label="Fin de jornada de sana distancia" stroke="red" />
          <ReferenceLine x="2020-06-29" label="Semáforo naranja" stroke="red" />
          <Line type="natural" dataKey="Sintomas mentales" stroke="#9336b5" strokeWidth='1' animationDuration={2000} />
          <Line type="natural" dataKey="Sintomas COVID" stroke="#eb0e63" strokeWidth='1' animationDuration={1500}/>
          <Brush dataKey="day" height={40} stroke="#8884d8"  />
          </LineChart>
        </ResponsiveContainer>
        </div>
      );
    }
  }
}


export default Timeline;
