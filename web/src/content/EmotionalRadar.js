import React, { PureComponent } from 'react';
import {
  Radar, RadarChart, PolarGrid, Legend,
  PolarAngleAxis, PolarRadiusAxis,
} from 'recharts';


/** 
@fileoverview: EmotionalRadar.js
@version: 1.0.0
@author: Miopers
@copyright: GIL UNAM 
@see: http://www.miopers.unam.mx/covid/#/emociones

History: Versón 1.0.0 Verión inical del programa desplegable de Miopers para analisis de 
  tweets COVID19 versión actualmente desplegable.

Summary: Script donde se configura la carga de información para el despliegue de las visualizaciónes de las
  cargas de emociones en la aplicación web final. Se compone de la clase EmotionalRadar que permite la conección 
  a la información por médio de un repositorio.
*/

class EmotionalRadar extends PureComponent {

  // Método constructor para el almacenamiento de información de los tweets y sus datos de descarga.
  constructor(props){
    super(props)
    this.state = {
      error:null,
      data:[],
      time:'',
      isLoaded:false
    }
  }

  componentDidMount(){
    /**
     * @overview: Método que conecta con el repositorio de datos de los tweets y los lee para extraer el 
     * número total de  tweets descargados y la información que se meustra en las gráficas de sentimientos. 
     * @returns: La conexión para la carga de tweets o en su caso el mensaje de error.
     */
    fetch("https://raw.githubusercontent.com/RicardoJC/Mexico-Datos-COVID19/master/home/radar.json")
          .then(res => res.json())
          .then(
            (result) => {
              this.setState({
                isLoaded: true,
                data: result.data,
                time:result.time
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

  render() {
    /**
     * @overview: Método de lectura de los datos del método anterior y visualización. 
     * Se crean un RadarChart de los sentimientos de tweets así como la carga de la relativa información de cada una. 
     * El código muestra la configuración de la gráfica que es desplegada en la página web. 
     * @see: http://www.miopers.unam.mx/covid/#/sintomas
     */
    const{error,isLoaded,data,time} = this.state
    if(error){
      return <div>Error al cargar el radar de emociones</div>
    }else if(!isLoaded){
      return <div>Cargando información...</div>
    }else{
      return (
        <div>
        <div className='d-flex justify-content-center font-weight-lighter'>
          <span>Última actualización: {time}</span>
        </div>
        <RadarChart  cx={175} cy={175} outerRadius={120} width={350} height={450} data={data}>
          <PolarGrid />
          <PolarAngleAxis dataKey="subject" />
          <PolarRadiusAxis angle={30} domain={[0, 150]} />
          <Radar name="Emociones en Twitter" dataKey="A" stroke="#2387f3" fill="#2387f3" fillOpacity={0.6} />
          <Legend />
        </RadarChart>
        </div>

      );
    }


  }
}

export default EmotionalRadar;
