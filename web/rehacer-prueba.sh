#!/bin/sh

echo direccionando a la carpeta
cd /home/adrian/Miopers/web/
echo haciendo el build...
npm run build
echo borrando carpeta anterior
rm -r /var/www/react/
echo copiando desde miopers/web
cp -r /home/adrian/Miopers/web/build /var/www/react
echo recargando nginx
service nginx reload
echo se hizo con éxito la operación!