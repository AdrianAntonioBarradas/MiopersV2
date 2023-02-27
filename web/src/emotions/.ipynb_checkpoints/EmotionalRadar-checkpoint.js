import React, { PureComponent } from 'react';
import {
  Radar, RadarChart, PolarGrid, Legend,
  PolarAngleAxis, PolarRadiusAxis,
} from 'recharts';

class EmotionalRadar extends PureComponent {


  constructor(props){
    super(props)
    this.state = {
      error:null,
      data:[],
      isLoaded:false
    }
  }

  componentDidMount(){
    fetch("https://raw.githubusercontent.com/RicardoJC/Mexico-Datos-COVID19/master/home/radar.json")
          .then(res => res.json())
          .then(
            (result) => {
              this.setState({
                isLoaded: true,
                data: result
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
    const{error,isLoaded,data} = this.state
    if(error){
      return <div>Error al cargar el radar de emociones</div>
    }else if(!isLoaded){
      return <div>Cargando información...</div>
    }else{
      return (
        <RadarChart  cx={175} cy={175} outerRadius={120} width={350} height={450} data={data}>
          <PolarGrid />
          <PolarAngleAxis dataKey="subject" />
          <PolarRadiusAxis angle={30} domain={[0, 150]} />
          <Radar name="Emociones en Twitter" dataKey="A" stroke="#2387f3" fill="#2387f3" fillOpacity={0.6} />
          <Legend />
        </RadarChart>
      );
    }


  }
}

export default EmotionalRadar;
