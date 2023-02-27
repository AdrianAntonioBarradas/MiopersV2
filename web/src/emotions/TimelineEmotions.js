import React, { PureComponent } from 'react';
import {
  LineChart, Line, XAxis, YAxis,
  CartesianGrid, Tooltip, Brush,Legend, AreaChart, Area,
  ResponsiveContainer,ReferenceLine, ReferenceArea
  } from 'recharts';
// import json from '../data/EmocionesTwitter_X_Estados_X_Tiempo_Covid';
import axios from 'axios';

/** 
@fileoverview: TimelineEmotions.js
@version: 1.0.0
@author: Miopers
@copyright: GIL UNAM 
@see: http://www.miopers.unam.mx/covid/#/emociones

History: Versón 1.0.0 Verión inical del programa desplegable de Miopers para analisis de 
  tweets COVID19 versión actualmente desplegable.

Summary: Script donde se configura el despliegue de la gráfica de palabras clave en la sección de linea del
  tiempo de palabras clave en la página COVID-19 México de Miopers
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
  // Método constructor para inicializar las variables de información
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
    axios.get('http://localhost:8000/api/sentimientos')
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
     * Se despliega el código de la gráfica dinamica de las emociones de la sección: 'Análisis de emociones'
     * O en caso contrario se de información de que no se puede cargar.
     * @see: http://www.miopers.unam.mx/covid/#/emociones
     */
    const {data, time , isLoaded, error} = this.state;
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
            top: 5, right: 20, left: 20, bottom: 5,
          }}
          >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="day" />
          <YAxis />
          <Tooltip />
          <Legend verticalAlign="top" wrapperStyle={{ lineHeight: '40px' }} />
          <ReferenceLine x="2020-04-21" label="Fase 3" stroke="red" />
          <ReferenceLine x="2020-05-31" label="Fin de jornada de sana distancia" stroke="red" />
          <Line type="natural" dataKey="enojo" stroke="#fc1303" strokeWidth='1' animationDuration={1000} />
          <Line type="natural" dataKey="anticipación" stroke="#ff9626" strokeWidth='1' animationDuration={1500}/>
          <Line type="natural" dataKey="disgusto" stroke="#c338f5" strokeWidth='1' animationDuration={2000}/>
          <Line type="natural" dataKey="miedo" stroke="#229426" strokeWidth='1' animationDuration={2500}/>
          <Line type="natural" dataKey="alegría" stroke="#f6fa1e" strokeWidth='1' animationDuration={3000} />
          <Line type="natural" dataKey="tristeza" stroke="#433bdb" strokeWidth='1' animationDuration={3500}/>
          <Line type="natural" dataKey="sorpresa" stroke="#27e0f5" strokeWidth='1' animationDuration={4000}/>
          <Line type="natural" dataKey="confianza" stroke="#9ff5ab" strokeWidth='1' animationDuration={4500}/>
      <Brush dataKey="day" height={40} stroke="#8884d8"  />
      </LineChart>
        </ResponsiveContainer>
        </div>

      );
    }
  }
}


export default Timeline;
