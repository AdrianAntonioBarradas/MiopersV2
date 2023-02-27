import metrics_b as mt
import downTweets_b as dt
import data_json_b as dj
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
        # direccion = data_path+'json/'
        # mapa_alcaldias = direccion+'alcaldias.json'
        feed = "sintomas/feed.pickle"
        feed_json = "sintomas/feed.json"
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
    # data_p = mt.rept_clase(data_mp, 'mentales')
    # data_f = mt.agrupaFecha(data_mp)
    

    dataS = mt.etiqueta(data, sintomas)
    data_Sp = dataS[dataS['etiqueta'] == 1]
    twe2 = data_Sp['id'].tolist()
    # data_ps = mt.rept_clase(data_Sp, 'sintomas')
    # data_f2 = mt.agrupaFecha(data_Sp)
    

    # total = pd.merge(data_f, data_f2, on='fecha2')
    # #return  mt.unionData(data_ps, data_p)
    # total.to_csv(data_path+'data_timeline.csv')
 
    # dj.json_timeline(direccion+'timeline', total, dth) #esta función sobreescribe el JSON con la nueva info
    # dj.procesar_mapa2(direccion+'alcaldias', mt.unionData(data_ps, data_p), mapa_alcaldias, dth)
   

    try:
        # dj.list_id(twe+twe2, feed)
        dj.list_id(twe+twe2, feed)
        dj.convert_pickle(feed, feed_json)
    except:
        print("Hubo algún error con el pickle")
    #return  mt.unionData(data_ps, data_p)
    print('Analisis Sintomas terminado')
    
    #return data_mp, data_Sp

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
