import React from 'react';
import Card from 'react-bootstrap/Card';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

const styles = {
  updateDate:{
    marginBottom:'10px'
  }
};


class Cards extends React.Component{

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
    fetch("https://raw.githubusercontent.com/RicardoJC/Mexico-Datos-COVID19/master/home/tokens.json")
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






  render(){
    const {error,isLoaded,data,time} = this.state;
    var hashtags = {t1:'',w1:'',t2:'',w2:'',t3:'',w3:'',t4:'',w4:'',t5:'',w5:''};
    var mentions = {t1:'',w1:'',t2:'',w2:'',t3:'',w3:'',t4:'',w4:'',t5:'',w5:''};
    var words = {t1:'',w1:'',t2:'',w2:'',t3:'',w3:'',t4:'',w4:'',t5:'',w5:''};
    if(!error && isLoaded){
      hashtags = data[0];
      mentions = data[1];
      words = data[2];
    }

    return(

      <div>
      <div style={styles.updateDate} className='d-flex justify-content-center font-weight-lighter'>
        <span>Última actualización: {time}</span>
      </div>
        <Row >
        <Col className='d-flex justify-content-center'>
        <Card style={{ width: '18rem', height:'19em' }}>
          <Card.Body>
          <Card.Title className="mb-2 text-muted ">Hashtags de hoy</Card.Title>
          <div className="d-table justify-content-left">
            <div className="d-table-cell font-weight-bold"><h2>{hashtags.t1}&nbsp;</h2></div>
            <div className="d-table-cell text-muted">{hashtags.w1}</div>
          </div>

          <div className="d-table justify-content-left">
            <div className="d-table-cell font-weight-bold"><h2>{hashtags.t2}&nbsp;</h2></div>
            <div className="d-table-cell text-muted">{hashtags.w2}</div>
          </div>

          <div className="d-table justify-content-left">
            <div className="d-table-cell font-weight-bold"><h2>{hashtags.t3}&nbsp;</h2></div>
            <div className="d-table-cell text-muted">{hashtags.w3}</div>
          </div>

          <div className="d-table justify-content-left">
            <div className="d-table-cell font-weight-bold"><h2>{hashtags.t4}&nbsp;</h2></div>
            <div className="d-table-cell text-muted">{hashtags.w4}</div>
          </div>

          <div className="d-table justify-content-left">
            <div className="d-table-cell font-weight-bold"><h2>{hashtags.t5}&nbsp;</h2></div>
            <div className="d-table-cell text-muted">{hashtags.w5}</div>
          </div>

          </Card.Body>
        </Card>
        </Col>

          <Col className='d-flex justify-content-center'>
          <Card style={{ width: '18rem', height:'19em' }}>
          <Card.Body>
            <Card.Title className="mb-2 text-muted ">Menciones de hoy</Card.Title>
            <div className="d-table justify-content-left">
              <div className="d-table-cell font-weight-bold"><h2>{mentions.t1}&nbsp;</h2></div>
              <div className="d-table-cell text-muted">{mentions.w1}</div>
            </div>

            <div className="d-table justify-content-left">
              <div className="d-table-cell font-weight-bold"><h2>{mentions.t2}&nbsp;</h2></div>
              <div className="d-table-cell text-muted">{mentions.w2}</div>
            </div>

            <div className="d-table justify-content-left">
              <div className="d-table-cell font-weight-bold"><h2>{mentions.t3}&nbsp;</h2></div>
              <div className="d-table-cell text-muted">{mentions.w3}</div>
            </div>

            <div className="d-table justify-content-left">
              <div className="d-table-cell font-weight-bold"><h2>{mentions.t4}&nbsp;</h2></div>
              <div className="d-table-cell text-muted">{mentions.w4}</div>
            </div>

            <div className="d-table justify-content-left">
              <div className="d-table-cell font-weight-bold"><h2>{mentions.t5}&nbsp;</h2></div>
              <div className="d-table-cell text-muted">{mentions.w5}</div>
            </div>

          </Card.Body>
          </Card>
          </Col>

          <Col className='d-flex justify-content-center'>
          <Card style={{ width: '18rem', height:'19em' }}>
          <Card.Body>
            <Card.Title className="mb-2 text-muted ">Palabras de hoy</Card.Title>
            <div className="d-table justify-content-left">
              <div className="d-table-cell font-weight-bold"><h2>{words.t1}&nbsp;</h2></div>
              <div className="d-table-cell text-muted">{words.w1}</div>
            </div>

            <div className="d-table justify-content-left">
              <div className="d-table-cell font-weight-bold"><h2>{words.t2}&nbsp;</h2></div>
              <div className="d-table-cell text-muted">{words.w2}</div>
            </div>

            <div className="d-table justify-content-left">
              <div className="d-table-cell font-weight-bold"><h2>{words.t3}&nbsp;</h2></div>
              <div className="d-table-cell text-muted">{words.w3}</div>
            </div>

            <div className="d-table justify-content-left">
              <div className="d-table-cell font-weight-bold"><h2>{words.t4}&nbsp;</h2></div>
              <div className="d-table-cell text-muted">{words.w4}</div>
            </div>

            <div className="d-table justify-content-left">
              <div className="d-table-cell font-weight-bold"><h2>{words.t5}&nbsp;</h2></div>
              <div className="d-table-cell text-muted">{words.w5}</div>
            </div>


          </Card.Body>
          </Card>
          </Col>
        </Row>
      </div>


    );
  }
}


export default Cards;