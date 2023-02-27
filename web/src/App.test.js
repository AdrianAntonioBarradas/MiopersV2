import React from 'react';
import { render } from '@testing-library/react';
import App from './App';

/** 
@fileoverview: App.test.js
@version: 1.0.0
@author: Miopers
@copyright: GIL UNAM 
@see: http://www.miopers.unam.mx/covid/#/

History: Versón 1.0.0 Verión inical del programa desplegable de Miopers para analisis de 
  tweets COVID19 versión actualmente desplegable.

Summary: Documentación del programa que funciona a modo de testeo para el correcto funcionamiento del programa. 
En este modulo testeamos que la página web funcione correctamente.
*/


test('renders learn react link', () => {
  const { getByText } = render(<App />);
  const linkElement = getByText(/learn react/i);
  expect(linkElement).toBeInTheDocument();
});
