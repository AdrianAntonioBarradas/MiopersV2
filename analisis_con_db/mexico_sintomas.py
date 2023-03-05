import metrics_b as mt
import downTweets_b as dt
from datetime import datetime
import re
from typing import List
import json

def dataImport(diccWords) -> List[str]:
    """lee una lista de palabras, cada renglón es un elemento de la lista resultante"""
    tokens = []
    for word in diccWords.split('\n'):
        word = re.sub('https\W*t.co/\w*', '', word)
        tokens.append(word.encode('utf-8', 'ignore').decode('utf-8'))
    return tokens

def ejecutarAnalisis(tweets,db):
    if db.toupdateAnalisis("sintomas")==0:
        print("no se actualizó words")
        return None
    try: #importa los diccionarios
        sql = "SELECT diccionario_tema FROM temas  WHERE tema LIKE 'COVID';"
        ndic = db.selectOne(sql) #para modificar cuando se convierta a class
        filtro = dataImport(ndic)
        dicc = json.loads(db.getAnalisisDicc('sintomas'))
        sintomas = dicc['sintomas']
        mentales = dicc['mentales']

    except :
        print("Error, Archivos no encontrados")
    today = datetime.now()
    dth = today.strftime('%a %b %d %H:%M:%S %Y')
    
    ####
    #return filtro, sintomas, mentales
    ####


    #try:
    #print(filtro, '\n',tweets[:10])
    dataFull = dt.downloadData(tweets,filtro)
    data = mt.ReturnDelegacion(dataFull[0])
    
    datam = mt.etiqueta(data, mentales)
    data_mp = datam[datam['etiqueta'] == 1]
    twe = data_mp['id'].tolist()
   
    

    dataS = mt.etiqueta(data, sintomas)
    data_Sp = dataS[dataS['etiqueta'] == 1]
    twe2 = data_Sp['id'].tolist()
 
    print('Analisis Sintomas terminado')
    
  

    ##para agregar todos los resultados de sintomas mentales y físicos


    id_locPadre = db.getIDLoc("Ciudad de México")
    alcaldias = db.getAllLocChild(id_locPadre)

    resDel = dict()
    for t in data_Sp['delegacion']:
        aux = resDel.get(t,0)
        aux = aux + 1
        resDel[t] = aux

    id_analisis = db.getIdAnalisis("sintomas")
    id_proceso = db.getCurrentProceso()

    sql = "INSERT INTO resultados (id_detalle,id_analisis,id_proceso,cantidad,id_localidad) VALUES "

    analisisTema = db.getAllAnalisisTopic("sintomas")

    for  t in resDel:
        sql2 = "SELECT id_localidad FROM  localidad WHERE id_loc_padre = {} AND nombre LIKE '{}';".format(id_locPadre,t)
        comp = "({},{},{},{},{}),".format(analisisTema[0][0],id_analisis,id_proceso,resDel[t],alcaldias[t])
        sql = sql + comp

    resDel = dict()
    for t in data_mp['delegacion']:
        aux = resDel.get(t,0)
        aux = aux + 1
        resDel[t] = aux
    for  t in resDel:
        sql2 = "SELECT id_localidad FROM  localidad WHERE id_loc_padre = {} AND nombre LIKE '{}';".format(id_locPadre,t)
        comp = "({},{},{},{},{}),".format(analisisTema[1][0],id_analisis,id_proceso,resDel[t],alcaldias[t])
        sql = sql + comp

    sql = sql[: -1]
    sql = sql + ";"

    #print(sql)
    db.update(sql)
