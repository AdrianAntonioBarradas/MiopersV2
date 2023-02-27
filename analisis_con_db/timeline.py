# encoding:utf8
from pymongo import MongoClient
from datetime import datetime, timedelta, date
import time
import json
import re
import urllib
#from IO_json import ordenar

#mongo --host 132.247.22.53:27017 -u ConsultaTwitter --authenticationMechanism SCRAM-SHA-256 --authenticationDatabase twitterdb


'''
Palabras de contexto

Se busca
- Comportamiento del usuario
- Estado de animo
- Medidas del gobierno
- Síntomas del usuario


Para obtener contexto sacaré 2 palabras principales de 3 categorías:
1.- Hashtags
2.- Personas (Menciones)
3.- Sintomas
Con sus diferentes variaciones


1.-
- (covid19) covid covidmx
- (coronavirus) virus
- quedateencasa cuarentena encasa
2.-
- (Gatell)
- (AMLO) andres manuel lopez obrador
- SusanaDistancia
3.-
- (ansiedad)
- (depresión)
'''

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

def ejecutarAnalisis(tweets,db):    
    if db.toupdateAnalisis("timeline")==0:
        print("no se actualizó timeline")
        return None

    # Creamos una expresión regular para volver a extraer, aquellos tweets que tienen información relevante. 
    contexto = re.compile(r'(covid|(v|b)iru(s|z)|sars(-| )?cov|contingencia|sanitaria|sintoma|neumonia|quedateencasa|pandemia|encierro|cuarentena|encasa|cuandoestoseacabe|aislamientosocial|susana ?distancia)',re.I)

    # Creamos un diccionario para poder guardar la información de los hashtags
    timeline = dict()
    # Información de las palabras claves y hastags relevantes para el estudio.  
    tokens = ['quedateencasa','coronavirus', 'covid19' ,'@HLGatell','@lopezobrador_','SusanaDistancia']

    # Inicialización del tiempo de ejecución del script
    start_time = time.time()

    # Variable para poder contar el número de veces que aparece alguno de los topicos de interés en los tweets
    total_contexto = 0

    # Buscamos entre los tweets consultados de Mongo
    for i,tweet in enumerate(tweets):
        # Extraemos tweets, la fecha en que se emitieron y los almacenamos en variables
        text = getText(tweet)
        date = getDate(tweet).date()
        data = timeline.get(str(date),{})
        #print('Fecha: ' + str(getDate(tweet)))
        
    


        # Vamos analizando cada uno de los tweets y contabilizamos el número de estos. 
        total_contexto = total_contexto + 1
        # Buscamos cada uno de los tokens y si los hayamos en una lista guardamos un registro de ellos y aumentamos el contador
        for token in tokens:
            if token in text:
                aux = data.get(token,0)
                data[token] = aux + 1
            else:
                data[token] = data.get(token,0)
            

        timeline[str(date)] = data
        
    #print(total_contexto)
    #print("a continuación imprimimos data: \n", data)
    
    #para ingresar los datos a la base de datos
    
    id_analisis = db.getIdAnalisis("timeline")
    id_proceso = db.getCurrentProceso()

    sql = "INSERT INTO resultados (id_detalle,id_analisis,id_proceso,cantidad,id_localidad) VALUES "

    analisisTema = db.getAllAnalisisTopic("timeline")

    for  i in analisisTema:
        if i[1] in data:
            comp = "({},{},{},{},NULL),".format(i[0],id_analisis,id_proceso,data[i[1]])
            sql = sql + comp
    
    sql = sql[: -1]
    sql = sql + ";"

    #print(sql)
    
    
    db.update(sql)