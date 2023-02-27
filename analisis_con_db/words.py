# encoding:utf8
from pymongo import MongoClient
from datetime import datetime, timedelta, date
import spacy
import time
import json
import re
import urllib

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
    text = re.sub(r'http\S+',' ',text)
    text = re.sub(r'#(\w+)',r'h2sht2g@\1',text)
    text = text.replace('á','a')
    text = text.replace('é','e')
    text = text.replace('í','i')
    text = text.replace('ó','o')
    text = text.replace('ú','u')
    text = text.replace(',',' ')
    text = text.replace('\n',' ')
    return text
#recibir tweets y data_path

def ejecutarAnalisis(tweets, db):
    '''
    Creamos 3 diccionarios diferentes para almacenar información relativa a los tweets que se generan y 
    los hashtags a los que hacen mencion. 
    '''
    if db.toupdateAnalisis("words")==0:
        print("no se actualizó words")
        return None
    words = dict()
    hashtags = dict()
    mentions = dict()

    # Inicializamos temporaizador para contar el tiempo de ejecución del script
    start_time = time.time()

    # Inicializamos con spacy el procesamiento de información reuniendo los hashtags que nos intereaan por medio de NLP
    nlp = spacy.load('es_core_news_sm')


    # Corremos un loop donde se consultan los tweets del momento. 
    for i,tweet in enumerate(tweets):
        # Extraemos las fechas y textos de los tweets consultados
        text = preprocess(getText(tweet).lower()).strip()
        date = getDate(tweet)

        # Analizamos por medio del avariable nlp los tweets buscando la información de la lista de hashtags que nos interesan. 
        sentence = nlp(text)
        # Una vez extraidos los tweets con hashtags objetivos procedemos a tokenizar y clasificar los hashtags
        for token in sentence:
            if token.text.startswith('h2sht2g@'):
                aux = hashtags.get(token.text.replace('h2sht2g@','#'),0)
                hashtags[token.text.replace('h2sht2g@','#')] = aux + 1
            elif token.text.startswith('@'):
                aux = mentions.get(token.text,0)
                mentions[token.text] = aux + 1
            else:
                # En caso contrario tokenizar los tweets extrayendo los 'ADJ' y 'NOUN'
                if 'ADJ' in token.pos_ or 'NOUN' in token.pos_:
                    aux = words.get(token.text,0)
                    words[token.text] = aux + 1


    # Se crean dos listas en especifico para poder guardar las fechas de los tweets
    data = list() # Sera una lista de diccionarios.
    aux = dict()
    dataDict = dict()

    # Se crea un loop para poder contar la cantidad de twets ('t') y words ('w') que se lograron contabilizar.
    for i, w in enumerate(sorted(hashtags,key=hashtags.get,reverse=True)):
        #aux['t'+str(i+1)] = str(round(hashtags[w]/1000,2)) + 'k'
        aux['t'+str(i+1)] = str(hashtags[w])
        aux['w'+str(i+1)] = w
        #print(w, hashtags[w])
        if hashtags[w] > 1:
            dataDict[w] = hashtags[w] #para ingresar datos a base de datos 
        # Si el son muy pocos ni siquiera correr el proceso. 
        #if not i < 2:
         #   break

    # Creamos gurdamos todos los tweets procesados anteriormente en la lista data 
    data.append(aux)
    aux = dict()

    # Creamos un loop donde se repite el mismo procedimiento pero esta vez para los tweets en los que fueron mencionados los usuarios de interés
    for i, w in enumerate(sorted(mentions,key=mentions.get,reverse=True)):
        aux['t'+str(i+1)] = str(mentions[w])
        aux['w'+str(i+1)] = w
        if mentions[w] > 1:
            dataDict[w] = mentions[w] #para ingresar datos a base de datos 
        #if not i < 2:
         #   break
    # Se almacenan las menciones en la misma lista de datos. 
    data.append(aux)
    aux = dict()

    # Se repite el mismo procedimiento una 3ra vez pero ahora almacenamos las palabras de cada uno de los tweets y las guardamos en una lista. 
    for i, w in enumerate(sorted(words,key=words.get,reverse=True)):
        aux['t'+str(i+1)] = str(words[w])
        aux['w'+str(i+1)] = w
        if words[w] > 1:
            dataDict[w] = words[w] #para ingresar datos a base de datos 
        #if not i < 2:
         #   break
    data.append(aux)

    # Creamos un diccionario para la información de los hashtags, mensiones y words y el momento en que fueron procesados 
    # y lo guardamos en un .json para su posterior uso. 
    
    
    arr = list(dataDict.keys())

    wordsDB = db.getAllAnalisisTopic("words")
    listaPal = []

    for i in wordsDB:
        listaPal.append(i[1])

    id_analisis = db.getIdAnalisis("words")
    #print(id_analisis)
    cent = False


    sql = "INSERT INTO analisis_detalle (id_analisis, descripcion) VALUES "
    for  i in arr:
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
        
    id_analisis = db.getIdAnalisis("words")
    id_proceso = db.getCurrentProceso()
    wordsDB = db.getAllAnalisisTopic("words")
    sql = "INSERT INTO resultados (id_detalle,id_analisis,id_proceso,cantidad,id_localidad) VALUES "



    for  i in wordsDB:
        if i[1] in arr:
            comp = "({},{},{},{},NULL),".format(i[0],id_analisis,id_proceso,dataDict[i[1]])
            sql = sql + comp
        
    sql = sql[: -1]
    sql = sql + ";"

    
    #print(sql)
        
        
    db.update(sql)