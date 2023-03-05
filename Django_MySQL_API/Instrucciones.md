


# Instalación de Django

## Creación del entorno virtual

1. Abre una terminal y navega hasta el directorio `Django_MySQL_API`.

2. Ejecuta el siguiente comando para crear un nuevo entorno virtual:
    ````
    python -m venv env
    ````

    `env` es el nombre del entorno virtual que estamos creando.

3. Una vez que se haya creado el entorno virtual, actívalo ejecutando el siguiente comando:

- En Windows:

  ```
  env\Scripts\activate
  ```

- En Unix o Linux:

  ```
  source myenv/bin/activate
  ```

Verás que el nombre de tu entorno virtual aparece en el prompt de la terminal, como: (env) $

## Instalación de paquetes desde requirements.txt

1. Asegúrate de que estás dentro del entorno virtual que acabas de crear y de que allí se encuntre el archivo `requirements.txt`.

3. Ejecuta el siguiente comando para instalar los paquetes especificados en el archivo:
```
pip install -r requirements.txt
```

Este comando instalará todos los paquetes especificados en el archivo `requirements.txt` en el entorno virtual.

Si todo funciona correctamente, verás una lista de los paquetes instalados y sus versiones.

## Ajustes de conexión a la base de datos MySQL en Django
Hay que ir a al archivo que està en la ruta: `Django_MySQL_API/Miopers_API/Proyecto_API`

1. En el archivo `settings.py`, busca la sección `DATABASES` y haz los siguientes ajustes:

- Establece el motor de la base de datos en `'django.db.backends.mysql'`.

  ```
  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.mysql',
          ...
      }
  }
  ```

- Establece el nombre de la base de datos que deseas utilizar.

  ```
  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.mysql',
          'NAME': 'nombre_de_tu_base_de_datos',
          ...
      }
  }
  ```

- Establece el nombre de usuario y la contraseña para acceder a tu base de datos.

  ```
  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.mysql',
          'NAME': 'nombre_de_tu_base_de_datos',
          'USER': 'tu_nombre_de_usuario',
          'PASSWORD': 'tu_contraseña',
          ...
      }
  }
  ```

- Establece la dirección IP y el puerto del servidor de la base de datos.

  ```
  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.mysql',
          'NAME': 'nombre_de_tu_base_de_datos',
          'USER': 'tu_nombre_de_usuario',
          'PASSWORD': 'tu_contraseña',
          'HOST': 'dirección_IP_del_servidor',
          'PORT': 'puerto_del_servidor',
          ...
      }
  }
  ```

2. Una vez hecho esto se puede empezar con el servicio de django, es necario moverse al directorio de `Django_MySQL_API` y ejecutar el comando:
    ```
    python manage.py runserver
    ```

### Finalmente, si to está en orden se debería ver la terminal de esta forma:
```
    System check identified no issues (0 silenced).
    March 04, 2023 - 08:15:56
    Django version 4.1.5, using settings 'Proyecto_API.settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CTRL-BREAK.
```
