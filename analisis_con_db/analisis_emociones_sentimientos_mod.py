import numpy as np
import pandas as pd

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


diccEstados = { 
'aguascalientes': 'Aguascalientes',
'mexicali':'Baja California',
'tijuana': 'Baja California',
'baja california': 'Baja California',
'la paz': 'Baja California Sur',
'baja california sur': 'Baja California Sur' ,
'campeche': 'Campeche',
'cdmx': 'Ciudad de México',
'distrito federal': 'Ciudad de México',
'benito juarez': 'Ciudad de México',
'cuajimalpa': 'Ciudad de México',
'cuajimalpa de morelos': 'Ciudad de México',
'alvaro obregon': 'Ciudad de México',
'naucalpan': 'Ciudad de México',
'naucalpan de juarez': 'Ciudad de México',
'cuautitlan izcalli': 'Ciudad de México',
'cuauhtemoc': 'Ciudad de México',
'tlalpan': 'Ciudad de México',
'coyoacan': 'Ciudad de México',
'gustavo a. madero': 'Ciudad de México',
'venustiano carranza': 'Ciudad de México',
'miguel hidalgo': 'Ciudad de México',
'xochimilco': 'Ciudad de México',
'azcapotzalco': 'Ciudad de México',
'iztacalco': 'Ciudad de México',
'centro universitario de arte': 'Ciudad de México',
'universum': 'Ciudad de México',
'district federal': 'Ciudad de México',
'teatro juan ruiz de alarcon':'Ciudad de México',
'distretto federale': 'Ciudad de México',
'milpa alta': 'Ciudad de México',
'tlahuac': 'Ciudad de México',
'chihuahua': 'Chihuahua',
'chiapas':'Chiapas',
'tuxtla gutierrez':'Chiapas',
'coahuila': 'Coahuila',
'saltillo': 'Coahuila',
'coahuila de zaragoza': 'Coahuila',
'colima': 'Colima',
'durango':'Durango',
'guanajuato':'Guanajuato',
'celaya':'Guanajuato',
'apodaca':'Guanajuato',
'san miguel de allende':'Guanajuato',
'irapuato':'Guanajuato',
'guerrero': 'Guerrero',
'chilpancingo': 'Guerrero',
'acapulco': 'Guerrero',
'acapulco de juarez': 'Guerrero',
'chilpancingo de los bravo': 'Guerrero',
'tulancingo de bravo':'Hidalgo',
'hidalgo': 'Hidalgo',
'apan': 'Hidalgo',
'pachuca': 'Hidalgo',
'jalisco': 'Jalisco',
'guadalajara': 'Jalisco',
'puerto vallarta': 'Jalisco',
'zapopan': 'Jalisco',
'tlaquepaque': 'Jalisco',
'san martin de las piramides':'Estado de México',
'estado de mexico':'Estado de México',
'villa del carbon':'Estado de México',
'soyaniquilpan de juarez':'Estado de México',
'toluca':'Estado de México',
'tlalnepantla':'Estado de México',
'tlalnepantla de baz':'Estado de México',
'nezahualcoyotl':'Estado de México',
'atizapan de zaragoza':'Estado de México',
'ixtapaluca':'Estado de México',
'iztapalapa':'Estado de México',
'ecatepec de morelos':'Estado de México',
'ixtapan de la sal':'Estado de México',
'huixquilucan':'Estado de México',
'tultitlan':'Estado de México',
'san felipe del progreso':'Estado de México',
'cuautitlan':'Estado de México',
'ixtapan del oro':'Estado de México',
'lerma':'Estado de México',
'luvianos':'Estado de México',
'valle de chalco solidaridad':'Estado de México',
'metepec':'Estado de México',
'tepotzotlan':'Estado de México',
'tecamac':'Estado de México',
'jilotepec':'Estado de México',
'coacalco de berriozabal':'Estado de México',
'tultepec':'Estado de México',
'chalco':'Estado de México',
'almoloya de juarez':'Estado de México',
'texcoco':'Estado de México',
'villa guerrero':'Estado de México',
'valle de bravo':'Estado de México',
'tejupilco':'Estado de México',
'tezoyuca':'Estado de México',
'chimalhuacan':'Estado de México',
'zumpango':'Estado de México',
'teotihuacan':'Estado de México',
'el oro':'Estado de México',
'nicolas romero':'Estado de México',
'zinacantepec':'Estado de México',
'atlacomulco':'Estado de México',
'mexicaltzingo':'Estado de México',
'chapultepec':'Estado de México',
'jocotitlan':'Estado de México',
'san mateo atenco':'Estado de México',
'tianguistenco':'Estado de México',
'temoaya':'Estado de México',
'coyotepec':'Estado de México',
'jiquipilco':'Estado de México',
'tenancingo':'Estado de México',
'xonacatlan':'Estado de México',
'ixtlahuaca':'Estado de México',
'tenango del valle':'Estado de México',
'chicoloapan':'Estado de México',
'jilotzingo':'Estado de México',
'tequixquiac':'Estado de México', 
'atenco':'Estado de México',
'amecameca':'Estado de México',
'tenango del aire':'Estado de México',
'huehuetoca':'Estado de México', 
'capulhuac':'Estado de México',
'teoloyucan':'Estado de México',
'calimaya':'Estado de México',
'nextlalpan':'Estado de México',
'acambay':'Estado de México',
'ocoyoacac':'Estado de México',
'otumba':'Estado de México',
'temascalapa':'Estado de México',
'tlalmanalco':'Estado de México',
'isidro fabela':'Estado de México',
'apaxco':'Estado de México',
'polotitlan':'Estado de México',
'ozumba':'Estado de México',
'chiautla':'Estado de México',
'chiconcuac':'Estado de México', 
'melchor ocampo':'Estado de México',
'temascalcingo':'Estado de México', 
'acolman':'Estado de México',
'otzolotepec':'Estado de México',
'michoacan': 'Michoacán',
'morelia': 'Michoacán',
'michoacan de ocampo': 'Michoacán',
'morelos':'Morelos',
'cuernavaca':'Morelos',
'nayarit': 'Nayarit',
'tepic': 'Nayarit',
'nuevo leon':'Nuevo León',
'monterrey':'Nuevo León',
'san nicolas de los garza':'Nuevo León',
'oaxaca': 'Oaxaca',
'villa diaz ordaz': 'Oaxaca',
'oaxaca de juarez': 'Oaxaca',
'puebla':'Puebla',
'san pedro cholula':'Puebla',
'san andres cholula':'Puebla' ,
'queretaro': 'Querétaro',
'queretaro arteaga': 'Querétaro',
'quintana roo':'Quintana Roo',
'chetumal':'Quintana Roo',
'san luis potosi':'San Luis Potosí',
'sinaloa':'Sinaloa',
'culiacan':'Sinaloa',
'sonora':'Sonora',
'hermosillo':'Sonora',
'tabasco': 'Tabasco',
'villahermosa': 'Tabasco',
'tamaulipas':'Tamaulipas',
'ciudad victoria':'Tamaulipas',
'tampico':'Tamaulipas',
'reynosa':'Tamaulipas',
'tlaxcala': 'Tlaxcala',
'veracruz':'Veracruz',
'xalapa':'Veracruz',
'boca del rio':'Veracruz',
'cordoba':'Veracruz',
'veracruz de ignacio de la llave':'Veracruz',
'panuco':'Veracruz',
'poza rica de hidalgo':'Veracruz',
'yucatan': 'Yucatán',
'merida': 'Yucatán',
'cancun': 'Yucatán',
'puerto cancun': 'Yucatán',
'zacatecas': 'Zacatecas'
}

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

def queryMongoTiempo(tweets):
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

# def analisisEmociones_X_Tweet(mensajes):
#     non_words = list(punctuation)
#     non_words.extend(['¿', '¡'])
#     non_words.extend(map(str,range(10)))
    
#     lemmatizer = WordNetLemmatizer() 
#     #print(lemmatizer)
#     lexicon = EmoLex(data_path+'lexicon_spanish.txt')
#     #print(lexicon)
#     dSet=pd.DataFrame(mensajes) 
#     dSet['tweetF']=[lemmatizer.lemmatize(w,'v') for w in dSet.tweet] 
   
#     dSet['tweetF'] = dSet.tweetF.str.strip().str.split('[\W_]+')
#     #print(dSet['tweetF'])
        
#     rows = list()
    
#     for row in dSet[['tweetF']].iterrows():
#         r = row[1]
#     for word in r.tweetF:
#         rows.append((word))
#     #print(rows)
#     tweet9 = pd.DataFrame(rows, columns=['tweet'])
#     #print(tweet9)
#     summary = lexicon.summarize_doc(tweet9)
#     #print(summary)
#     dSet['anger'] = 0.0
#     dSet['anticipation'] = 0.0
#     dSet['disgust'] = 0.0
#     dSet['fear'] = 0.0
#     dSet['joy'] = 0.0
#     dSet['negative'] = 0.0
#     dSet['positive'] = 0.0
#     dSet['sadness'] = 0.0
#     dSet['surprise'] = 0.0
#     dSet['trust'] = 0.0
    
    
#     for index, _ in dSet.iterrows():
#         try:
#             to_lower = list(map(lambda x:x.lower(),dSet.loc[index].tweetF))
#             summary = lexicon.summarize_doc(to_lower)
#             for key in summary.keys():
#                 dSet.at[index, key] = summary[key]
#                 #print(dataset8.at[index, key] )
#         except:
#             continue
#     dSet['TweetNeutro'] = np.where((dSet['positive'] == dSet['negative']),  1.0,0)
#     dSet['TweetPositivo'] = np.where((dSet['positive'] > dSet['negative']),  1.0,0)
#     dSet['TweetNegativo'] = np.where((dSet['negative'] > dSet['positive']), 1.0,0)
    
    
    
#     df_array =  np.array(dSet) 
#     row, col = df_array.shape 
#     lista=['enojo','anticipacion','disgusto','miedo','alegria','negativo','positivo', 'tristeza','sorpresa','confianza',
#            'Tweets_Neutro','Tweets_Positivo','Tweets_Negativo','TweetAlegria','TweetConfianza','TweetSorpresa','TweetAnticipacion',
#           'TweetDisgusto','TweetEnojo','TweetMiedo','TweetTristeza'] 
#     listasuma = []
#     listasumaTweets = []
    
#     sumaTotal1=0
#     sumaTotal2=0
#     sumaTotalTweets=0
#     for x in range(2,12): 
#         sumaColumnas=0 
#         for y in range(0,row):
#             sumaColumnas=sumaColumnas +df_array[y][x]
#         listasuma.insert(x, round(sumaColumnas,2))
#         if x==7 or x==8 :
#             sumaTotal2=sumaTotal2+sumaColumnas
#         else:
#             sumaTotal1=sumaTotal1+sumaColumnas 
        
#     for p in range(12,15): #23
#         sumaTweets=0
#         for y in range(0,row):
#             sumaTweets=sumaTweets +df_array[y][p]
            
#         listasumaTweets.insert(p, sumaTweets)
#         sumaTotalTweets=sumaTotalTweets+sumaTweets 
        
#     #Se toman las calumnas de las emociones para determinar númericamente el valor más alto en la ponderacion que 
#     #le asigna el analisis y posteriormente se clásifica a ese tweet con la emoción más alta.
#     Set =  pd.DataFrame(dSet.loc[:, ('anger','anticipation','disgust','fear','joy','sadness','surprise','trust')].values,
#                         columns= ('anger','anticipation','disgust','fear','joy','sadness','surprise','trust'))
#     Set['MaxColumna']  = Set.idxmax(axis=1)
#     dicc_Emociones={'anger':0,'anticipation':1,'disgust':2,'fear':3,'joy':4, 'sadness':5,'surprise':6,'trust':7}
#     Set ['MaxColumna']
#     Set['id_MaxColumna'] = Set ['MaxColumna'].map(dicc_Emociones)
#     Set['TweetEnojo'] = np.where((Set['id_MaxColumna'] == 0) & (Set['anger'] >0),1.0, 0)
#     Set['TweetAnticipacion'] = np.where((Set['id_MaxColumna'] == 1) & (Set['anticipation'] >0),1.0, 0)
#     Set['TweetDisgusto'] = np.where((Set['id_MaxColumna'] == 2) & (Set['disgust'] >0),1.0, 0)
#     Set['TweetMiedo'] = np.where((Set['id_MaxColumna'] == 3) & (Set['fear'] >0),1.0, 0)
#     Set['TweetAlegria'] = np.where((Set['id_MaxColumna'] == 4) & (Set['joy'] >0),1.0, 0)
#     Set['TweetTristeza'] = np.where((Set['id_MaxColumna'] == 5) & (Set['sadness'] >0),1.0, 0)
#     Set['TweetSorpresa'] = np.where((Set['id_MaxColumna'] == 6) & (Set['surprise'] >0),1.0, 0)
#     Set['TweetConfianza'] = np.where((Set['id_MaxColumna'] == 7) & (Set['trust'] >0),1.0, 0) 
#     #print(Set) 
    
#     Set2 =  pd.DataFrame(Set.loc[:, ('TweetEnojo','TweetAnticipacion','TweetDisgusto','TweetMiedo',
#           'TweetAlegria','TweetTristeza','TweetSorpresa','TweetConfianza')].values, columns= (  'TweetEnojo','TweetAnticipacion','TweetDisgusto','TweetMiedo',
#           'TweetAlegria','TweetTristeza','TweetSorpresa','TweetConfianza'))
    
#     dSet_array =  np.array(Set2) 
#     row, col = dSet_array.shape 
#     lista_Temocion=['enojo','anticipacion','disgusto','miedo','alegria',  'tristeza','sorpresa','confianza' ] 
    
#     listSumaTweetEmocion = []     
#     sumaTot=0      
#     for x in range(0,8): 
#         sumaColEmocion=0 
#         for y in range(0,row):
#             sumaColEmocion=sumaColEmocion +dSet_array[y][x]
#         listSumaTweetEmocion.insert(x, round(sumaColEmocion,2))
        
#         sumaTot=sumaTot+sumaColEmocion
    
#     #=======________________________________________________________________________________
#     Set7 =  pd.DataFrame(dSet.loc[:, ('trust','anticipation','joy','anger','disgust','fear','sadness','surprise')].values,
#                          columns= ('trust','anticipation','joy','anger','disgust','fear','sadness','surprise'))
#     Set7['MaxColumna']  = Set7.idxmax(axis=1)
#     dicc_Emociones={'trust':0,'anticipation':1,'joy':2,'anger':3,'disgust':4, 'fear':5,'sadness':6,'surprise':7}
#     Set7 ['MaxColumna']
#     Set7['id_MaxColumna'] = Set7 ['MaxColumna'].map(dicc_Emociones)
#     Set7['TweetConfianza'] = np.where((Set7['id_MaxColumna'] == 0) & (Set7['trust'] >0),1.0, 0) 
#     Set7['TweetAnticipacion'] = np.where((Set7['id_MaxColumna'] == 1) & (Set7['anticipation'] >0),1.0, 0)
#     Set7['TweetAlegria'] = np.where((Set7['id_MaxColumna'] == 2) & (Set7['joy'] >0),1.0, 0)
#     Set7['TweetEnojo'] = np.where((Set7['id_MaxColumna'] == 3) & (Set7['anger'] >0),1.0, 0)    
#     Set7['TweetDisgusto'] = np.where((Set7['id_MaxColumna'] == 4) & (Set7['disgust'] >0),1.0, 0)
#     Set7['TweetMiedo'] = np.where((Set7['id_MaxColumna'] == 5) & (Set7['fear'] >0),1.0, 0)
#     Set7['TweetTristeza'] = np.where((Set7['id_MaxColumna'] == 6) & (Set7['sadness'] >0),1.0, 0)
#     Set7['TweetSorpresa'] = np.where((Set7['id_MaxColumna'] == 7) & (Set7['surprise'] >0),1.0, 0)
#     #print(Set) 
    
#     Set3 =  pd.DataFrame(Set7.loc[:, ('TweetConfianza','TweetAnticipacion', 'TweetAlegria','TweetEnojo','TweetDisgusto','TweetMiedo',
#          'TweetTristeza','TweetSorpresa')].values, columns= ( 'TweetConfianza','TweetAnticipacion', 'TweetAlegria','TweetEnojo','TweetDisgusto','TweetMiedo',
#          'TweetTristeza','TweetSorpresa'))

#     dSet_array2 =  np.array(Set3) 
#     row, col = dSet_array.shape 
#     lista_Temocion2=['confianza','anticipacion', 'alegria','enojo','disgusto','miedo',
#          'tristeza','sorpresa'] 

#     listSumaTweetEmocion2 = []     
#     sumaTot2=0      
#     for x in range(0,8): 
#         sumaColEmocion2=0 
#         for y in range(0,row):
#             sumaColEmocion2=sumaColEmocion2 +dSet_array2[y][x]
#         listSumaTweetEmocion2.insert(x, round(sumaColEmocion,2))

#         sumaTot2=sumaTot2+sumaColEmocion2           
            
#     #return(lista,listasuma,listasumaTweets,sumaTotal1,sumaTotal2,sumaTotalTweets)

#     return(dSet)

def analisisEmociones_Sentimientos_X_Tweet(mensajes,data_path):
    non_words = list(punctuation)
    non_words.extend(['¿', '¡'])
    non_words.extend(map(str,range(10)))
    lemmatizer = WordNetLemmatizer()
    
    #########Para pasarlo después a la base de datos 
    lexiconList = ""
    with open("/home/adrian/Miopers/sentimientos/data/lexicon_spanish.txt", "r") as f:
        for i in f:
            lexiconList += i
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
        temp_file.write(lexiconList)
    lexicon = EmoLex(temp_file.name)
    #lexicon = EmoLex(data_path+'lexicon_spanish.txt')
    print("el lexicon es: ", type(lexicon))

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

def jSONTweets_X_Estados_X_Tiempo(mensajes,fecha_lista, archivo, data_path,db):
    #formato_fecha = "%d-%m-%Y"
    #diaActual = datetime.datetime.strptime(fecha_lista, formato_fecha)
    #print(mensajes)
    dR=pd.DataFrame(mensajes) 
    #Group by contar
    #n_by_state = dR.groupby("Entidad")["tweet"].count()
    #print(n_by_state.head(33) )

    #ordenar
    #ordEst = dR.sort_values('Entidad')
    #print(ordEst) 
    #print(entidades)
    
    listaAnalizada_Estado=[]
    listaAnalizada_EstEmocion=[]
    evaluaciones = dict()
    evaluaciones['time'] = datetime.today().ctime() 
     
    resultado = [] 
    c=0
    
    nombreArchivo=['/home/adrian/Miopers/web/src/data/EmocionesTwitter_X_Estados_X_Tiempo_Polaridad.json','/home/adrian/Miopers/web/src/data/EmocionesTwitter_X_Estados_X_Tiempo_Covid.json']
    
    #abrir y leer el JSON con los datos de las emociones    
    with  open(nombreArchivo[1], mode='r', encoding='utf-8') as archivoMTP:
        zzjson = json.load(archivoMTP) 
        
    #abrir y leer el JSON con los datos de polaridad    
    with  open(nombreArchivo[0], mode='r', encoding='utf-8') as archivoMTP:
        polaridad_json = json.load(archivoMTP) 
        
    dPE = dR
    if len(dPE.index)==0:
        #cuando la información es nula para todos los estados
        lista=['enojo','anticipacion','disgusto','miedo','alegria','negativo','positivo', 'tristeza','sorpresa','confianza','Tweets_Positivo','Tweets_Negativo','Tweets_Neutro'] 
        porEstadoNada ={lista[0]:0,lista[1]:0,lista[2]:0, lista[3]:0,lista[4]:0,lista[5]:0 , lista[6]:0,lista[7]:0,lista[8]:0,lista[9]:0,"day":fecha_lista} 
        zzjson['data'].append(porEstadoNada)

        with  open(archivo, mode='w', encoding='utf-8') as archivoMTP: 
            archivoMTP.write(json.dumps(zzjson,indent=1))  
    else:

        dFVaEmocion=dPE.drop(columns=['Entidad'])            



        #anterios=>(lista,listasuma,listasumaTweets,sumaTotal1,sumaTotal2,sumaTotalTweets) 
        (lista_Polaridad,listasumaTweetsPolaridad,sumaTotalTweets,lista_Temocion, listSumaTweetEmocion,sumaTotEmo)=analisisEmociones_Sentimientos_X_Tweet(dFVaEmocion,data_path)
        #return(a,b,c,d,e,f) 
        #informacionTiempoEstado[x][2]="{enojo:"+str(listasuma[0])+",""anticipacion:"+str(listasuma[1])+",""disgusto:"+str(listasuma[2])+",""miedo:"+str(listasuma[3])+",""alegria:"+str(listasuma[4])+",""tristeza:"+str(listasuma[7])+",""sorpresa:"+str(listasuma[8])+",""confianza:"+str(listasuma[9])+",""negativo:"+str(listasuma[5])+",""positivo:"+str(listasuma[6])+",""Tweets_Positivo:"+str(listasumaTweets[0])+",""Tweets_Negativo:"+str(listasumaTweets[1])+",""Tweets_Neutro:"+str(listasumaTweets[2])+"}"
        #cadenaEstado="{enojo:"+str(round(listSumaTweetEmocion[0],4))+",""anticipacion:"+str(round(listSumaTweetEmocion[1],4))+",""disgusto:"+str(round(listSumaTweetEmocion[2],4))+",""miedo:"+str(round(listSumaTweetEmocion[3],4))+",""alegria:"+str(round(listSumaTweetEmocion[4],4))+",""tristeza:"+str(round(listSumaTweetEmocion[5],4))+",""sorpresa:"+str(round(listSumaTweetEmocion[6],4))+",""confianza:"+str(round(listSumaTweetEmocion[7],4))+","neutro:"+str(round(listasumaTweetsPolaridad[0],4))+","positivo:"+str(round(listasumaTweetsPolaridad[1],4))+","negativo:"+str(round(listasumaTweetsPolaridad[2],4)) )) +"}"
        fecha_hoy = datetime.today().ctime()
        #listaAnalizada_Estado.insert(x, entidades[x])
        #listaAnalizada_EstEmocion.insert(x, cadenaEstado)
        #y ={lista_Temocion[0]:listSumaTweetEmocion[0],lista_Temocion[1]:listSumaTweetEmocion[1],lista_Temocion[2]:listSumaTweetEmocion[2] , lista_Temocion[3]:listSumaTweetEmocion[3],lista_Temocion[4]:listSumaTweetEmocion[4],lista_Temocion[5]:listSumaTweetEmocion[5] , lista_Temocion[6]:listSumaTweetEmocion[6],lista_Temocion[7]:listSumaTweetEmocion[7],"day":fecha_lista} 
        y ={lista_Temocion[0]:listSumaTweetEmocion[0],lista_Temocion[1]:listSumaTweetEmocion[1],lista_Temocion[2]:listSumaTweetEmocion[2] , lista_Temocion[3]:listSumaTweetEmocion[3],lista_Temocion[4]:listSumaTweetEmocion[4],lista_Temocion[5]:listSumaTweetEmocion[5] , lista_Temocion[6]:listSumaTweetEmocion[6],lista_Temocion[7]:listSumaTweetEmocion[7]} 
        print("esta es la y")
        print(y)
        zzjson['data'].append(y)
        zzjson['time']=fecha_hoy
        #actualizar JSON de emociones
        # with  open(nombreArchivo[1], mode='w', encoding='utf-8') as archivoMTP: 
        #     archivoMTP.write(json.dumps(ordenar(zzjson),indent=1))
        #subir JSON al repo Miopers
        #IO_json.upload_json("sentimientos/data/EmocionesTwitter_X_Estados_X_Tiempo_Covid.json",json.dumps(zzjson,indent=1))

        #info para polaridad
        #polaridad_dict = {lista_Polaridad[0]:listasumaTweetsPolaridad[0] , lista_Polaridad[1]:listasumaTweetsPolaridad[1], lista_Polaridad[2]:listasumaTweetsPolaridad[2],"day":fecha_lista}
        polaridad_dict = {lista_Polaridad[0]:listasumaTweetsPolaridad[0] , lista_Polaridad[1]:listasumaTweetsPolaridad[1], lista_Polaridad[2]:listasumaTweetsPolaridad[2]}
        print("saca la polidaridad",polaridad_dict)
        
    
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
        
        ##fin de subida de datos a Base de Datos
        #return y, polaridad_dict
        # polaridad_json['data'].append(polaridad_dict)
        # polaridad_json['time'] = fecha_hoy
        # with  open(nombreArchivo[0], mode='w', encoding='utf-8') as archivoMTP: 
        #     archivoMTP.write(json.dumps(ordenar(polaridad_json),indent=1))
        #subir JSON al repo Miopers
        #IO_json.upload_json("sentimientos/data/EmocionesTwitter_X_Estados_X_Tiempo_Polaridad.json",json.dumps(polaridad_json,indent=1))

        
def ejecutarAnalisis(tweets, calendario1,calendario2, data_path,db): 
    '''Recibe los tweets, el período de fechas que comprenden esos tweets, y la dirección donde están guardados los diccionarios
    Se asume que la fecha final también debe ser analizada. En el caso de solo analizar un día, calendario2 debe ser la misma que calendario1'''
    def obtenerTweetsPorFecha(tweet, fecha):
        """Returns True if tweet was written on the date provided in the argument and False otherwise."""
        fecha_tweet = datetime.fromtimestamp(int(tweet['timestamp_ms'])/1000)
        return fecha_tweet.day == fecha.day

    if db.toupdateAnalisis("analisis_emociones_sentimientos")==0:
        print("no se actualizó analisis_emociones_sentimientos ni analisis_emociones_polaridad")
        return None
    
    nombreArchivo=[]
    nombreArchivo=[data_path+'EmocionesTwitter_X_Estados_X_Tiempo_Polaridad.json',data_path+'EmocionesTwitter_X_Estados_X_Tiempo_Covid.json']
    
    
    lista=['enojo','anticipacion','disgusto','miedo','alegria','negativo','positivo', 'tristeza','sorpresa','confianza','Tweets_Positivo','Tweets_Negativo','Tweets_Neutro'] 
 
    formato_fecha = "%Y-%m-%d"
    #convertir fecha inicial en un objeto datetime
    inicio = datetime.strptime(calendario1, formato_fecha)
    #convertir fecha final en un objeto datetime
    fin= datetime.strptime(calendario2, formato_fecha)
 
    lista_fechas = [(inicio + timedelta(days=d)).strftime("%Y-%m-%d") 
                        for d in range((fin - inicio).days + 1)]

    for x in range(0,len(lista_fechas)):
        #obtener el inicio y final del día x en milisegundos
        (T1, T2) = fechasQuery(lista_fechas[x])
        T1_datetime = datetime.fromtimestamp(T1/1000)
        #obtener dataframe con los tweets del día x, la entidad donde fueron publicados y una marca para distinguir si está o no relacionado al COVID
        #mensajes=queryMongoTiempo(list(filter(lambda tweet: obtenerTweetsPorFecha(tweet,T1_datetime), tweets)),data_path)
        print("aquí el diablito")
        mensajes=queryMongoTiempo(tweets)
        
        #Filtrar los Tweets de COVID
        mensajesCOVID = mensajes[mensajes.deCOVID == 1]
        if len(mensajesCOVID.index)==0: #si no hay ningún tweet de covid para esta fecha:

            with  open(nombreArchivo[1], mode='r', encoding='utf-8') as archivoMTP:
                zzjson = json.load(archivoMTP) 
            #para cada estado, y para cada emoción, indicar que no hubo ninguna observación durante la fecha x
            porTipoNada ={lista[0]:0,lista[1]:0,lista[2]:0, lista[3]:0,lista[4]:0,lista[5]:0 , lista[6]:0,lista[7]:0,lista[8]:0,lista[9]:0,"day":lista_fechas[x]} 
            zzjson['data'].append(porTipoNada)

            with  open(nombreArchivo[1], mode='w', encoding='utf-8') as archivoMTP: 
                archivoMTP.write(json.dumps(zzjson,indent=1))  

        else: #si hubo al menos un tweet relacionado al COVID para la fecha x:
            mensajeFiltrado1=mensajesCOVID.drop(columns=['deCOVID'])
            print('Analisis emociones y polaridad terminado!.' ) 
            #return jSONTweets_X_Estados_X_Tiempo(mensajeFiltrado1,lista_fechas[x],nombreArchivo[1], data_path, db)
            jSONTweets_X_Estados_X_Tiempo(mensajeFiltrado1,lista_fechas[x],nombreArchivo[1], data_path, db)
        
        mensajesCOVID = mensajes[mensajes.deCOVID == 1]
         
        
    print('Analisis emociones y polaridad terminado!.' )                
                
                
