import numpy as np
import pandas as pd
import tempfile
from nltk import pos_tag
from nltk.corpus import stopwords
from string import punctuation
from nltk.stem import WordNetLemmatizer
from py_lex import EmoLex
from IO_json import ordenar
from datetime import datetime, timedelta
import consultaMongo as mongo
import json
import re


def preprocess(text):
    text = text.lower()
    text = text.replace('á','a')
    text = text.replace('é','e')
    text = text.replace('í','i')
    text = text.replace('ó','o')
    text = text.replace('ú','u')
    text = text.replace('\n','')
    return text

def conseguirLugar(data):
    data = preprocess(data)
    if len(data.split(',')) == 2:
        return  data.split(',')[0].strip(),data.split(',')[1].strip()
    else:
        return '*','*'

    
def fechasQuery(fecha):
    #print(fecha)
    formato_fecha = "%Y-%m-%d"
    fechaInicial = datetime.strptime(fecha, formato_fecha)
    milliseconds1 = int(round(fechaInicial.timestamp() * 1000))
    ##print(fechaInicial)
    #print(milliseconds1) 
    fechaFinal = fechaInicial+ timedelta(days=1)
    #print(fechaFinal)
    milliseconds2 = int(round(fechaFinal.timestamp() * 1000))
    #print(milliseconds2) 
    return milliseconds1,milliseconds2    

def queryMongoTiempo(tweets,db):
    """entrega un data frame con los tweets, la entidad donde fueron publicados y una marca para distinguir si está o no relacionado al COVID"""   
    rows_list = []
    rows_listPlace = []
    rows_name = []
    rows_create=[]
    zona1 = []
    zona2=[]
    rows_Id = []
    counter=1

    map = dict()
    data = dict()
    results = dict()
    results['time'] = datetime.today().ctime()

    print("eltamaño de tweets filtrados",len(tweets))
    for tweet in tweets: 
        s=tweet['text'].replace('\n', ' ').replace('\r', '')
        r=tweet['place']['full_name']
        n=tweet['place']['name'] 
        rows_list.append(s) 
        rows_listPlace.append(r)
        rows_name.append(n) 
        counter= counter +1 
        place0,place1 = conseguirLugar(tweet['place']['full_name'])
        zona1.append(place0)
        zona2.append(place1)          
    dataset8= pd.DataFrame( {'Entidad':zona2 , 'tweet':rows_list ,  'full_name':rows_listPlace, 'lugar2':zona1  }) 
    diccEstados = json.loads(db.getAnalisisDicc('analisis_emociones_polaridad'))
    dataset8['Zona1'] = dataset8['lugar2'].map(diccEstados)
    dataset8['Zona2'] = dataset8['Entidad'].map(diccEstados)
    del dataset8['full_name']
    del dataset8['lugar2'] 
    dataset8['Entidad']=dataset8['Zona2'].mask(pd.isnull, dataset8['Zona1'])
    del dataset8['Zona1']
    del dataset8['Zona2']
    dataset8['Entidad']=dataset8['Entidad'].mask(pd.isnull, 'ZzDesconocido')
    p = mongo.crearExpresion(mongo.dataImport(['/home/adrian/Miopers/master/data/diccionarios/filtro_covid.txt']))
    dataset8['text'] =(((((dataset8['tweet'].str.lower()).str.replace('á','a')).str.replace('é','e')).str.replace('í','i')).str.replace('ó','o')).str.replace('ú','u')
    dataset8['deCOVIDEncontrando']=dataset8['tweet'].apply(lambda x: re.findall(p, x)) 
    dataset8['deCOVID'] = dataset8['deCOVIDEncontrando'].apply(lambda x: 2 if x ==[] else 1)
    del dataset8['text']
    del dataset8['deCOVIDEncontrando']
    return(dataset8)

def analisisEmociones(mensajes,data_path):
    non_words = list(punctuation)
    non_words.extend(['¿', '¡'])
    non_words.extend(map(str,range(10)))
    lemmatizer = WordNetLemmatizer() 
    
    lexicon = EmoLex(data_path+'lexicon_spanish.txt')
    dSet=pd.DataFrame(mensajes) 
    #print(dSet)
    dSet['tweetF']=[lemmatizer.lemmatize(w,'v') for w in dSet.tweet] 
    #print(dSet)
    dSet['tweetF'] = dSet.tweetF.str.strip().str.split('[\W_]+')
    #print(dSet)
    rows = list()
    
    for row in dSet[['tweetF']].iterrows():
        r = row[1]
        #print(r)
    for word in r.tweetF:
        rows.append((word))
        #print(rows)
    
    tweet9 = pd.DataFrame(rows, columns=['tweet'])
    #print(tweet9)
    summary = lexicon.summarize_doc(tweet9)
    #print(summary)
    dSet['anger'] = 0.0
    dSet['anticipation'] = 0.0
    dSet['disgust'] = 0.0
    dSet['fear'] = 0.0
    dSet['joy'] = 0.0
    dSet['negative'] = 0.0
    dSet['positive'] = 0.0
    dSet['sadness'] = 0.0
    dSet['surprise'] = 0.0
    dSet['trust'] = 0.0
    for index, _ in dSet.iterrows():
        try:
            to_lower = list(map(lambda x:x.lower(),dSet.loc[index].tweetF)) 
            summary = lexicon.summarize_doc(to_lower) 
            for key in summary.keys():
                dSet.at[index, key] = summary[key] 
                #print(dataset8.at[index, key] )
        except:
            continue
    dSet['TweetNeutro'] = np.where((dSet['positive'] == dSet['negative']),  1.0,0)
    dSet['TweetPositivo'] = np.where((dSet['positive'] > dSet['negative']),  1.0,0)
    dSet['TweetNegativo'] = np.where((dSet['negative'] > dSet['positive']), 1.0,0)
    
 

    #print(dSet)
    df_array =  np.array(dSet) 
    row, col = df_array.shape 
   
    listasuma = []
    listasumaTweets = []
    
    sumaTotal1=0
    sumaTotal2=0
    sumaTotalTweets=0
    for x in range(2,12): 
        sumaColumnas=0 
        for y in range(0,row):
            sumaColumnas=sumaColumnas +df_array[y][x]
        listasuma.insert(x, round(sumaColumnas,2))
        if x==7 or x==8 :
            sumaTotal2=sumaTotal2+sumaColumnas
        else:
            sumaTotal1=sumaTotal1+sumaColumnas 
        
    for p in range(12,15): #23
        sumaTweets=0
        for y in range(0,row):
            sumaTweets=sumaTweets +df_array[y][p]
            
        listasumaTweets.insert(p, sumaTweets)
        sumaTotalTweets=sumaTotalTweets+sumaTweets 
    #return(lista,listasuma,listasumaTweets,sumaTotal1,sumaTotal2,sumaTotalTweets)

    return(dSet) 

def analisisEmociones_Sentimientos_X_Tweet(mensajes,db):
    non_words = list(punctuation)
    non_words.extend(['¿', '¡'])
    non_words.extend(map(str,range(10)))
    lemmatizer = WordNetLemmatizer()
    
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
        temp_file.write(db.getAnalisisDicc('analisis_emociones_sentimientos'))
    lexicon = EmoLex(temp_file.name)
    

    dSet=pd.DataFrame(mensajes) 
    dSet['tweetF']=[lemmatizer.lemmatize(w,'v') for w in dSet.tweet] 
    dSet['tweetF'] = dSet.tweetF.str.strip().str.split('[\W_]+')
    rows = list()
    
    for row in dSet[['tweetF']].iterrows():
        r = row[1]
    for word in r.tweetF:
        rows.append((word))
    
    tweet9 = pd.DataFrame(rows, columns=['tweet'])
    summary = lexicon.summarize_doc(tweet9)
    dSet['anger'] = 0.0
    dSet['anticipation'] = 0.0
    dSet['disgust'] = 0.0
    dSet['fear'] = 0.0
    dSet['joy'] = 0.0
    dSet['negative'] = 0.0
    dSet['positive'] = 0.0
    dSet['sadness'] = 0.0
    dSet['surprise'] = 0.0
    dSet['trust'] = 0.0
    
    
    for index, _ in dSet.iterrows():
        try:
            to_lower = list(map(lambda x:x.lower(),dSet.loc[index].tweetF))
            summary = lexicon.summarize_doc(to_lower)
            for key in summary.keys():
                dSet.at[index, key] = summary[key]
                #print(dataset8.at[index, key] )
        except:
            continue
            
    dSet['TweetNeutro'] = np.where((dSet['positive'] == dSet['negative']),  1.0,0)
    dSet['TweetPositivo'] = np.where((dSet['positive'] > dSet['negative']),  1.0,0)
    dSet['TweetNegativo'] = np.where((dSet['negative'] > dSet['positive']), 1.0,0)
    
    
    
    df_array =  np.array(dSet) 
    row, col = df_array.shape 

    lista_Polaridad=["Tweets_Neutro",'Tweets_Positivo','Tweets_Negativo'] 
    listasuma = []
    listasumaTweetsPolaridad = []
    
    sumaTotal1=0
    sumaTotal2=0
    sumaTotalTweets=0
    for x in range(2,12): 
        sumaColumnas=0 
        for y in range(0,row):
            sumaColumnas=sumaColumnas +df_array[y][x]
        #print("La suma de la columna "+str(x-1)  + " es "+ lista[x-2]+" "+  str(sumaColumnas))
        listasuma.insert(x, round(sumaColumnas,2))
        if x==7 or x==8 :
            sumaTotal2=sumaTotal2+sumaColumnas
        else:
            sumaTotal1=sumaTotal1+sumaColumnas 
        
    for p in range(12,15): #23
        sumaTweets=0
        for y in range(0,row):
            sumaTweets=sumaTweets +df_array[y][p]
            
        #print("La suma de la columna "+str(p-1) + " es "+ str(sumaTweets))
        listasumaTweetsPolaridad.insert(p, sumaTweets)
        sumaTotalTweets=sumaTotalTweets+sumaTweets 
        
    #Se toman las calumnas de las emociones para determinar númericamente el valor más alto en la ponderacion que 
    #le asigna el analisis y posteriormente se clásifica a ese tweet con la emoción más alta.
    Set =  pd.DataFrame(dSet.loc[:, ('anger','anticipation','disgust','fear','joy','sadness','surprise','trust')].values,
                        columns= ('anger','anticipation','disgust','fear','joy','sadness','surprise','trust'))
    Set['MaxColumna']  = Set.idxmax(axis=1)
    dicc_Emociones={'anger':0,'anticipation':1,'disgust':2,'fear':3,'joy':4, 'sadness':5,'surprise':6,'trust':7}
    Set ['MaxColumna']
    Set['id_MaxColumna'] = Set ['MaxColumna'].map(dicc_Emociones)
    Set['TweetEnojo'] = np.where((Set['id_MaxColumna'] == 0) & (Set['anger'] >0),1.0, 0)
    Set['TweetAnticipacion'] = np.where((Set['id_MaxColumna'] == 1) & (Set['anticipation'] >0),1.0, 0)
    Set['TweetDisgusto'] = np.where((Set['id_MaxColumna'] == 2) & (Set['disgust'] >0),1.0, 0)
    Set['TweetMiedo'] = np.where((Set['id_MaxColumna'] == 3) & (Set['fear'] >0),1.0, 0)
    Set['TweetAlegria'] = np.where((Set['id_MaxColumna'] == 4) & (Set['joy'] >0),1.0, 0)
    Set['TweetTristeza'] = np.where((Set['id_MaxColumna'] == 5) & (Set['sadness'] >0),1.0, 0)
    Set['TweetSorpresa'] = np.where((Set['id_MaxColumna'] == 6) & (Set['surprise'] >0),1.0, 0)
    Set['TweetConfianza'] = np.where((Set['id_MaxColumna'] == 7) & (Set['trust'] >0),1.0, 0) 
    #print(Set) 
    
    Set2 =  pd.DataFrame(Set.loc[:, ('TweetEnojo','TweetAnticipacion','TweetDisgusto','TweetMiedo',
          'TweetAlegria','TweetTristeza','TweetSorpresa','TweetConfianza')].values, columns= (  'TweetEnojo','TweetAnticipacion','TweetDisgusto','TweetMiedo',
          'TweetAlegria','TweetTristeza','TweetSorpresa','TweetConfianza'))
    
    dSet_array =  np.array(Set2) 
    row, col = dSet_array.shape 
    lista_Temocion=['enojo','anticipacion','disgusto','miedo','alegria',  'tristeza','sorpresa','confianza' ] 
    
    listSumaTweetEmocion = []     
    sumaTotEmo=0      
    for x in range(0,8): 
        sumaColEmocion=0 
        for y in range(0,row):
            sumaColEmocion=sumaColEmocion +dSet_array[y][x]
        #print("La suma de la columna "+str(x) + " es "+ lista_Temocion[x]+" "+ str(sumaColEmocion))
        listSumaTweetEmocion.insert(x, round(sumaColEmocion,2))
        sumaTotEmo=sumaTotEmo+sumaColEmocion
     
    ####
    import os
    temp_file.close()
    os.remove(temp_file.name)
    ####
    return(lista_Polaridad,listasumaTweetsPolaridad,sumaTotalTweets,lista_Temocion, listSumaTweetEmocion,sumaTotEmo)

def jSONTweets_X_Estados_X_Tiempo(mensajes,fecha_lista,db):
    
    dR=pd.DataFrame(mensajes) 
    
    evaluaciones = dict()
    evaluaciones['time'] = datetime.today().ctime() 
     
    
    dPE = dR
    if len(dPE.index)==0:
        #cuando la información es nula para todos los estados
        lista=['enojo','anticipacion','disgusto','miedo','alegria','negativo','positivo', 'tristeza','sorpresa','confianza','Tweets_Positivo','Tweets_Negativo','Tweets_Neutro'] 
        porEstadoNada ={lista[0]:0,lista[1]:0,lista[2]:0, lista[3]:0,lista[4]:0,lista[5]:0 , lista[6]:0,lista[7]:0,lista[8]:0,lista[9]:0,"day":fecha_lista} 
        
 
    else:

        dFVaEmocion=dPE.drop(columns=['Entidad'])            



        #anterios=>(lista,listasuma,listasumaTweets,sumaTotal1,sumaTotal2,sumaTotalTweets) 
        (lista_Polaridad,listasumaTweetsPolaridad,sumaTotalTweets,lista_Temocion, listSumaTweetEmocion,sumaTotEmo)=analisisEmociones_Sentimientos_X_Tweet(dFVaEmocion,db)
        y ={lista_Temocion[0]:listSumaTweetEmocion[0],lista_Temocion[1]:listSumaTweetEmocion[1],lista_Temocion[2]:listSumaTweetEmocion[2] , lista_Temocion[3]:listSumaTweetEmocion[3],lista_Temocion[4]:listSumaTweetEmocion[4],lista_Temocion[5]:listSumaTweetEmocion[5] , lista_Temocion[6]:listSumaTweetEmocion[6],lista_Temocion[7]:listSumaTweetEmocion[7]} 
        
        polaridad_dict = {lista_Polaridad[0]:listasumaTweetsPolaridad[0] , lista_Polaridad[1]:listasumaTweetsPolaridad[1], lista_Polaridad[2]:listasumaTweetsPolaridad[2]}
        
        
    
        senti = y
        pol = polaridad_dict
        ###Subir resultados a Base de datos
        arr = list(senti.keys())

        #para ingresar los datos a la base de datos
            
        id_analisis = db.getIdAnalisis("analisis_emociones_sentimientos")
        id_proceso = db.getCurrentProceso()
        wordsDB = db.getAllAnalisisTopic("analisis_emociones_sentimientos")
        sql = "INSERT INTO resultados (id_detalle,id_analisis,id_proceso,cantidad,id_localidad) VALUES "

        for  i in wordsDB:
            if i[1] in arr:
                comp = "({},{},{},{},NULL),".format(i[0],id_analisis,id_proceso,senti[i[1]])
                sql = sql + comp
            
        sql = sql[: -1]
        sql = sql + ";"


        # print(sql)
        db.update(sql)

        arr = list(pol.keys())

        #para ingresar los datos a la base de datos
            
        id_analisis = db.getIdAnalisis("analisis_emociones_polaridad")
        id_proceso = db.getCurrentProceso()
        wordsDB = db.getAllAnalisisTopic("analisis_emociones_polaridad")
        sql = "INSERT INTO resultados (id_detalle,id_analisis,id_proceso,cantidad,id_localidad) VALUES "

        for  i in wordsDB:
            if i[1] in arr:
                comp = "({},{},{},{},NULL),".format(i[0],id_analisis,id_proceso,pol[i[1]])
                sql = sql + comp
            
        sql = sql[: -1]
        sql = sql + ";"

        # print(sql)
        db.update(sql)


        
def ejecutarAnalisis(tweets, calendario1,calendario2, db): 
    '''Recibe los tweets, el período de fechas que comprenden esos tweets, y la dirección donde están guardados los diccionarios
    Se asume que la fecha final también debe ser analizada. En el caso de solo analizar un día, calendario2 debe ser la misma que calendario1'''
    def obtenerTweetsPorFecha(tweet, fecha):
        """Returns True if tweet was written on the date provided in the argument and False otherwise."""
        fecha_tweet = datetime.fromtimestamp(int(tweet['timestamp_ms'])/1000)
        return fecha_tweet.day == fecha.day

    if db.toupdateAnalisis("analisis_emociones_sentimientos")==0:
        print("no se actualizó analisis_emociones_sentimientos ni analisis_emociones_polaridad")
        return None

    #lista=['enojo','anticipacion','disgusto','miedo','alegria','negativo','positivo', 'tristeza','sorpresa','confianza','Tweets_Positivo','Tweets_Negativo','Tweets_Neutro'] 
 
    formato_fecha = "%Y-%m-%d"
    #convertir fecha inicial en un objeto datetime
    inicio = datetime.strptime(calendario1, formato_fecha)
    #convertir fecha final en un objeto datetime
    fin= datetime.strptime(calendario2, formato_fecha)
 
    lista_fechas = [(inicio + timedelta(days=d)).strftime("%Y-%m-%d") 
                        for d in range((fin - inicio).days + 1)]

    for x in range(0,len(lista_fechas)):
        #obtener el inicio y final del día x en milisegundos
        
        mensajes=queryMongoTiempo(tweets,db)
        
        #Filtrar los Tweets de COVID
        mensajesCOVID = mensajes[mensajes.deCOVID == 1]
        if len(mensajesCOVID.index)>0: #si hay  tweets de covid
            mensajeFiltrado1=mensajesCOVID.drop(columns=['deCOVID'])
            print('Analisis emociones y polaridad terminado!.' ) 
            
            jSONTweets_X_Estados_X_Tiempo(mensajeFiltrado1,lista_fechas[x], db)

        
    print('Analisis emociones y polaridad terminado!.' )                
                
                
