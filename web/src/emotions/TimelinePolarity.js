import axios from 'axios';
import React, { PureComponent } from 'react';
import {
  LineChart, Line, XAxis, YAxis,
  CartesianGrid, Tooltip, Legend, Sector,
  ResponsiveContainer,ReferenceLine, Brush, PieChart, Pie
  } from 'recharts';
// import json from '../data/EmocionesTwitter_X_Estados_X_Tiempo_Polaridad';

/** 
@fileoverview: TimelinePolarity.js
@version: 1.0.0
@author: Miopers
@copyright: GIL UNAM 
@see: http://www.miopers.unam.mx/covid/#/emociones

History: Versón 1.0.0 Verión inical del programa desplegable de Miopers para analisis de 
  tweets COVID19 versión actualmente desplegable.

Summary: Script donde se configura el despliegue de la gráfica de polaridad de sentimientos 
  en la página 'Análisis de emociones' de Miopers
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



// const data_pie = [
//   { name: 'Tweets Positivos', value: 6660 },
//   { name: 'Tweets Negativos', value: 2500 },
//   { name: 'Tweets Neutros', value: 3000 },
  
// ];

const renderActiveShape = (props) => {
  const RADIAN = Math.PI / 180;
  const { cx, cy, midAngle, innerRadius, outerRadius, startAngle, endAngle, fill, payload, percent, value } = props;
  const sin = Math.sin(-RADIAN * midAngle);
  const cos = Math.cos(-RADIAN * midAngle);

  
  const sx = cx + (outerRadius + 10) * cos;
  const sy = cy + (outerRadius + 10) * sin;
  const mx = cx + (outerRadius + 30) * cos;
  const my = cy + (outerRadius + 30) * sin;
  const ex = mx + (cos >= 0 ? 1 : -1) * 22;
  const ey = my;
  const textAnchor = cos >= 0 ? 'start' : 'end';

  return (
    <g>
      <text x={cx} y={cy} dy={8} textAnchor="middle" fill={fill}>
        {payload.name}
      </text>
      <Sector
        cx={cx}
        cy={cy}
        innerRadius={innerRadius}
        outerRadius={outerRadius}
        startAngle={startAngle}
        endAngle={endAngle}
        fill={fill}
      />
      <Sector
        cx={cx}
        cy={cy}
        startAngle={startAngle}
        endAngle={endAngle}
        innerRadius={outerRadius + 6}
        outerRadius={outerRadius + 10}
        fill={fill}
      />
      <path d={`M${sx},${sy}L${mx},${my}L${ex},${ey}`} stroke={fill} fill="none" />
      <circle cx={ex} cy={ey} r={2} fill={fill} stroke="none" />
      <text x={ex + (cos >= 0 ? 1 : -1) * 12} y={ey} textAnchor={textAnchor} fill="#333">{`PV ${value}`}</text>
      <text x={ex + (cos >= 0 ? 1 : -1) * 12} y={ey} dy={18} textAnchor={textAnchor} fill="#999">
        {`(Rate ${(percent * 100).toFixed(2)}%)`}
      </text>
    </g>
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
    axios.get('http://localhost:8000/api/sentimientosPolaridad')
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
        axios.get('http://localhost:8000/api/sintomaspie/')
        .then(res => {
          this.setState({ 
            data_pie: res.data.data_pie,
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

state = {
    activeIndex: 0,
  };

  onPieEnter = (_, index) => {
    this.setState({
      activeIndex: index,
    });
  };

  render() {
    /**
     * @overview: Método de lectura de los datos del método anterior y visualización. 
     * Se crea la estructura general de la gráfica o se manda le mensaje de que no puede ser desplegada. 
     * Se despliega el código de la gráfica dinamica de las polaridades de emociones de la sección: 'Análisis de emociones'
     * O en caso contrario se de información de que no se puede cargar.
     * @see: http://www.miopers.unam.mx/covid/#/emociones
     */
    const {data, time ,data_pie} = this.state;
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
          <Line type="natural" dataKey="Tweets_Negativo" stroke="#c338f5" strokeWidth='1' animationDuration={2000}/>
          <Line type="natural" dataKey="Tweets_Positivo" stroke="#433bdb" strokeWidth='1' animationDuration={2500}/>
          <Line type="natural" dataKey="Tweets_Neutro" stroke="#888888" strokeWidth='1' animationDuration={3000} />
    <Brush dataKey="day" height={40} stroke="#8884d8"  />
    </LineChart>
        </ResponsiveContainer>

	<ResponsiveContainer width="99%" height={400}>
        <PieChart width={400} height={400}>
          <Pie
            activeIndex={this.state.activeIndex}
            activeShape={renderActiveShape}
            data={data_pie} // se actualiza la propiedad data con los datos correctos
            cx="50%"
            cy="50%"
            innerRadius={80}
            outerRadius={100}
            fill="#8884d8"
            dataKey="value"
            onMouseEnter={this.onPieEnter}
          />
        </PieChart>
        </ResponsiveContainer>

        </div>



      );



  }
}


export default Timeline;
