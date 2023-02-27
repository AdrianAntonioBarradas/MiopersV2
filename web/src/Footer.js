import React from 'react';

/** 
@fileoverview: Footer.js
@version: 1.0.0
@author: Miopers
@copyright: GIL UNAM 
@see: http://www.miopers.unam.mx/covid/#/

History: Versón 1.0.0 Verión inical del programa desplegable de Miopers para analisis de 
  tweets COVID19 versión actualmente desplegable.

Summary: Archivo de los programas footer donde nos enfocamos en configurar los 'footer' de la página web (Encabezados
  y pies de páginas), donde establecemos los estilos y tamaños. 
*/


const footerStyles ={
  height:'80px',
  paddingTop:'20px'

}



class Footer extends React.Component{

  /**
    * @overview: Clase principal de los footers que extiende de React.Component, utilizmos los elementos de esta biblioteca
    * para poder trabajar con la creación de footers dinámicos
    * @returns: Establecemos los parámetros por default para todos los footers que utiliza la página web. 
  */

  render(){
    // Encabezado de pie de página donde vienen los datos de información de GIL
    return(
      <div style={footerStyles} className='bg-dark text-light text-center'>
      <p>UNAM, México 2020 </p>
      </div>

    );
  }


}

// Exportamos los elementos para que puedan ser leidos por el resto de páginas del proyecto
export default Footer;