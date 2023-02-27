# encoding:utf8
from pymongo import MongoClient
from datetime import datetime, timedelta, date
import time
import json
import re
import urllib
"""
@Miopers-HOME - mexico_hashtags.py
Módulo de Python que permite poder realizar el analísis de los hashtag por medio del analísis de expresinoes regulares y otros 
métodos y la creación de un archivo .json donde se almacenan la información de los hashtags almacenados. Esto con el objetivo de 
almacenr la información y poder utilizarla después en el analisis y gráficas de miopers. 
Date: March-2021
Tipo de Documentación: Google Docstrings
"""

def getText(tweet):
    """
    Summary: Función que permite extraer la información de los tweets descargados desde Monto para ser procesados.
        Los textos de los tweets pueden ser descargados de forma total, truncada o el texto completo, dependiendo de
        la calidad del tweet descargado. 
    Args:
        tweet: Variable para identificar el texto de cada uno de los tweets descargados

    Returns:
        list: Se devuelve una lista con la información del texto de todos los tweets, estos pueden ser
        de forma total o de forma parcial, dependiendo de la condición del tweet

    """
    return tweet['text'] if not tweet['truncated'] else tweet['extended_tweet']['full_text']

def getDate(tweet):
    """
    Summary: Función para poder extraer de los tweets la fecha de cuando fueron emitidos cada uno de estos.
    
    Args:
        tweet: Variable para identificar el texto de cada uno de los tweets descargados

    Returns:
        Se devuelve la fecha de publicación de cada uno de los tweets en formato datetime. 

    """
    timestamp = tweet['timestamp_ms'][:-3]
    return datetime.fromtimestamp(int(timestamp)) + timedelta(hours=5)

def getPlace(data):
    """
    Summary: Función que nos regresa el valor por de el lugar donde fue publicado el tweets (estado) para esto
        se hace un split de la inofrmación que hay en el tweet pra poder extraer esta información en especifio de 
        todo el texto.

    Args:
        data: Parametro para identificar la ubicación del tweet filtrado de la función getDate() 
              donde lo que hacemos es una extracción de información en especifico.

    Returns:
        Se gresa la información del lugar donde fue publicado el tweets en caso contrario regresa un string para indicar
        que se desconoce esa información. 

    """
    data = preprocess(data)
    if len(data.split(',')) == 2:
        return  data.split(',')[0].strip(),data.split(',')[1].strip()
    else:
        return '*','*'

def preprocess(text):
    """
    Summary: Procesamos la información y la limpiamos utilizando NLP donde removemos acentos, y extraemos
        las palabras principales que nos interesan en el re.compile

    Args: 
        text: El texto del tweet que estamos analizando 

    Returns:
        Devuelve el texto pricesado sin acentos y con las palabras de interes extraidas de igual forma
        en formato de texto

    """
    text = text.lower()
    text = text.replace('á','a')
    text = text.replace('é','e')
    text = text.replace('í','i')
    text = text.replace('ó','o')
    text = text.replace('ú','u')
    text = text.replace('\n','')
    return text

def ejecutarAnalisis(tweets, db ):
    
    if db.toupdateAnalisis("hashtags")==0:
        print("no se actualizó words")
        return None
    #contexto = re.compile(r'(covid|(v|b)iru(s|z)|sars(-| )?cov|contingencia|sanitaria|sintoma|neumonia|quedateencasa|pandemia|encierro|cuarentena|encasa|cuandoestoseacabe|aislamientosocial|susana ?distancia)',re.I)

    # Creamos diccinario para ir almacenaando la información de cada estado
    # with open(data_path+"map_hashtags_hist.geojson","r") as json_file:
    #     map = json.load(json_file)
    map = dict()
    # Cronometro para medir el tiempo de ejecución
    start_time = time.time()

    # Creamos diccionario para almacenar información relativa a las fechas de los tweets
    results = dict()
    estados = json.loads(db.getAnalisisDicc("hashtags")) #caraga estados desde la base de datos
    hashtags = []
    # Vamos recorriendo la lista de cada uno de los tweets consultados y los procesamos de acuerdo a las anteriore funciones
    for i,tweet in enumerate(tweets):
        text = preprocess(getText(tweet))
        date = getDate(tweet).date()
        #print('Fecha: ' + str(getDate(tweet)))


        place0,place1 = getPlace(tweet['place']['full_name']) #recibe '*' en caso de que no venga el lugar
        # Buscamos y desplegamos la información de los tweets por cada uno de los estados de estados.py
        for state in estados:
            # Se conoce el estado
            if place0 != '*':
                if place0 in estados[state] or place1 in estados[state]:
                    aux = map.get(state,{}) # mapeamos la información de cada uno de los estados
                    for word in text.split(' '):
                        if word.startswith('#'): #Buscamos la información de las palabras que inician en hashtag
                            if word not in hashtags:
                                hashtags.append(word)
                            counter = aux.get(word,0)
                            aux[word] = counter + 1

                    #counter = aux.get('total',0)
                    #aux['total'] = counter + 1
                    #aqui se guarda la cuenta de todos los hashtags del estado
                    map[state] = aux
                    break
                # Si es el ultimo estado y el campo 1 es mexico se pasa a Estado de Mexico
                elif state == 'Zacatecas' and place1 == 'mexico':
                    aux = map.get('Estado de México',{})
                    for word in text.split(' '):
                        if word.startswith('#'):
                            if word not in hashtags:
                                hashtags.append(word)
                            counter = aux.get(word,0)
                            aux[word] = counter + 1
                    # Se recorren todos los estados hasta llegar al Edo Mex.
                    #counter = aux.get('total',0)
                    #aux['total'] = counter + 1
                    map['Estado de México'] = aux

                    break
    
    
    ####
    #arr = list(dataDict.keys())
    #print("longitud hashtagas", len(hashtags))
    wordsDB = db.getAllAnalisisTopic("hashtags")
    listaPal = []

    for i in wordsDB:
        listaPal.append(i[1])

    id_analisis = db.getIdAnalisis("hashtags")
    #print(id_analisis)
    cent = False


    sql = "INSERT INTO analisis_detalle (id_analisis, descripcion) VALUES "
    for  i in hashtags:
        if i not in listaPal:
            cent =True
            comp = "({},'{}'),".format(id_analisis, i)
            sql = sql + comp
        
    sql = sql[: -1]
    sql = sql + ";"

    #print(sql)
    if cent:
         db.update(sql)

    #para ingresar los datos a la base de datos
        
    id_analisis = db.getIdAnalisis("hashtags")
    id_proceso = db.getCurrentProceso()
    wordsDB = db.getAllAnalisisTopic("hashtags")
    
    hashtag_id = dict()
    for i in wordsDB:
        hashtag_id[i[1]]=i[0]
    
    sql = "INSERT INTO resultados (id_detalle,id_analisis,id_proceso,cantidad,id_localidad) VALUES "
    edos = list(map)
    for estado in edos:
        id_localidad = db.getIDLoc(estado)
        for hashtag in map[estado].keys():
            #print(estado,hashtag,map[estado][hashtag])
            comp = "({},{},{},{},{}),".format(hashtag_id[hashtag],id_analisis,id_proceso,map[estado][hashtag],id_localidad)
            sql = sql + comp
        
    sql = sql[: -1]
    sql = sql + ";"

    
    #print(sql)
        
        
    db.update(sql)