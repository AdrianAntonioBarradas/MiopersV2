#!/usr/bin/env python3
#!/usr/bin/env bash
DISPLAY=':0.0'

from DataBaseCon import DataBase
import json #import mongoDBCon
import timeline
import words
import mexico_hashtags as hashtags
import mexico_sintomas as sintomas
import analisis_emociones_sentimientos_mod as sentimientos
import consultaMongo as mongo #provisional
def insertProcesoTweets (db):
        #crear regsitro de proceso en la base de datos
    id_tema = 1 #corresponde al tema: COVID
    #tanto el id_proceso y fecha_inicio se generan automáticamente al realizar el insert
    sql = "INSERT INTO proceso (id_tema, conteo_tweet) VALUES ({}, {});".format(id_tema, len(tweets))
    #print(sql)
    db.update(sql)
    sql = "SELECT max(id_proceso) from proceso;"
    currentProcess = db.selectOne(sql)
    print("El id de proceso es : ", currentProcess)
    def getId (tweets):
        return tweets['id']
    sql = "INSERT INTO tweets (id_proceso, id_tweet) VALUES "
    for  i in tweets:
        comp = "({},'{}'),".format(currentProcess, getId(i))
        sql = sql + comp
        
    sql = sql[: -1]
    sql = sql + ";"

    #print(sql)
    db.update(sql)

db = DataBase()
if db.toupdateTema("COVID"):
    
    #descargar tweets (ya filtrados)
    print("Descargando tweets...")
    

    #tweets =  mongoDBCon.consulta_ayer(db) Para cuando funcione la Conexión con la Base de MongoDB
    with open('jsontweetverdadero.json', encoding='utf8') as f:# en su lugar usamos este para ver que funcione el sistema
        tweets = json.loads( f.read())

    insertProcesoTweets(db)
    #se inician los análisis
    print("analisis timeline")
    timeline.ejecutarAnalisis(tweets,db) 
    print("analisis words")
    words.ejecutarAnalisis(tweets,db)
    print("analisis hahstags")
    hashtags.ejecutarAnalisis(tweets,db)
    print("analisis sintomas")
    sintomas.ejecutarAnalisis(tweets,db)
    print("analisis sentimientos")
    ayer_str, hoy_str = mongo.fechas_ayer_hoy_string()
    sentimientos.ejecutarAnalisis(tweets, ayer_str,ayer_str,db)
    print("finish")
    db.fechaFinProceso(db.getCurrentProceso())
print("fin proceso de análisis")




db.close()