from django.http.response import JsonResponse, HttpResponse
from django.views import View
from .models import *
from django.db.models import Q, Max, Sum
import json
import datetime

#import tools
# Create your views here.

class TemasView(View):
    
    def get(self, request):
        temas = list(Temas.objects.values())
        
        if len(temas) > 0:
            datos = {'message':"Success",'temas': temas}
        else:
            datos = {'message':"Temas no encontrados"}
        query = JsonResponse(datos)
        print(type(Temas.objects.values()))
        return query

class ResultadosView(View):
    
    def get(self, request):
        temas = list(Temas.objects.values())
        
        if len(temas) > 0:
            datos = {'message':"Success",'temas': temas}
        else:
            datos = {'message':"Temas no encontrados"}
        query = JsonResponse(datos)
#        print(type(Temas.objects.values()))

        resp = dict()

        

        for e in Resultados.objects.filter(cantidad__gt=0, id_proceso=Proceso.objects.all().order_by('-id_proceso')[0]).select_related('id_proceso', 'id_detalle'):
            print(e.cantidad,e.id_detalle.descripcion)
            resp[e.id_detalle.descripcion] = e.cantidad

        
        rel = json.dumps(resp)





        return HttpResponse(rel, content_type="application/json")

class TimelineView(View):
    
    def get(self, request):
        
        dictlist = list()
        

        timeline = AnalisisPorTemas.objects.get(
                Q(descripcion_analisis__icontains='timeline') & 
                Q(id_tema=Temas.objects.get(tema__icontains='COVID').id_tema)
            )

        query = Resultados.objects.filter(
            id_analisis=timeline.id_analisis
        ).prefetch_related(
            'id_proceso',
            'id_detalle'
        ).select_related(
            'id_proceso',
            'id_detalle'
        ).order_by(
            'id_proceso__fecha_inicio',
            'id_detalle__descripcion')
        


       

        for i in range(0,len(query),6):
            resp = dict()
            
            resp["quedateencasa"] = query[i+4].cantidad
            resp["coronavirus"] = query[i+2].cantidad
            resp["covid19"] = query[i+3].cantidad
            resp["@HLGatell"] = query[i].cantidad
            resp["@lopezobrador_"] = query[i+1].cantidad
            resp["SusanaDistancia"] = query[i+5].cantidad
            fecha= query[i].id_proceso.fecha_inicio - datetime.timedelta(days=1) # se resta un día porque corresponden a los tweets del día anterior al procesamiento 
            resp["day"] = fecha.strftime("%Y-%m-%d")

            dictlist.append(resp)

            #print(r.id_detalle.descripcion, r.cantidad, r.id_proceso.fecha_inicio.strftime("%Y-%m-%d"),end="")
#            resp[e.id_detalle.descripcion] = e.cantidad

        

        data = dict()
        data ["time"] = query[len(query)-1].id_proceso.fecha_inicio.strftime("%a %b %d %H:%M:%S %Y") #fecah de actualización

        ###### OJO falta agregar fecha de fin de proceso
        data ["data"] = dictlist
        rel = json.dumps(data)
        return HttpResponse(rel, content_type="application/json")

class AlcaldiasResultView(View):
    
    def get(self, request):
        
        
        alcaldiaSentimientos = AnalisisPorTemas.objects.get(
                Q(descripcion_analisis__icontains='sintomas') & 
                Q(id_tema=Temas.objects.get(tema__icontains='COVID').id_tema)
            )
        id_analisisA = alcaldiaSentimientos.id_analisis
        sintomas = AnalisisDetalle.objects.filter(
            id_analisis = id_analisisA
        )

        ##
        id_tema = Temas.objects.get(tema__contains="COVID").id_tema
        result = Proceso.objects.filter(id_tema=id_tema).aggregate(Max('id_proceso'))
        max_id_proceso = result['id_proceso__max']

        estado = Localidad.objects.get(
            Q(nombre__icontains='Ciudad de México')
        )
        observaciones = dict()
        for e in sintomas:
            #print(e.descripcion, max_id_proceso)
            observaciones[e.descripcion] = 0
        resp = dict()
        query =  Resultados.objects.filter(id_analisis=id_analisisA,id_proceso=max_id_proceso).prefetch_related(
            'id_proceso',
            'id_detalle'
        ).select_related(
            'id_proceso',
            'id_detalle'
        )
        for i in query:
            # print(i.id_localidad.nombre,i.id_detalle.descripcion,i.cantidad)
            aux = resp.get( i.id_localidad.nombre, observaciones.copy())
            aux[i.id_detalle.descripcion] = i.cantidad
            resp[i.id_localidad.nombre] = aux
       

        rel = json.dumps(resp)

        return HttpResponse(rel, content_type="application/json")
    
class WordsResultsView(View):

    def get(self, request):

        words = AnalisisPorTemas.objects.get(
            Q(descripcion_analisis__icontains='words') & 
            Q(id_tema=Temas.objects.get(tema__icontains='COVID').id_tema)
        )
        id_analisisA = words.id_analisis
        words = AnalisisDetalle.objects.filter(
            id_analisis = id_analisisA
        )
        

        id_tema = Temas.objects.get(tema__contains="COVID").id_tema
        result = Resultados.objects.filter(id_analisis=id_analisisA).aggregate(Max('id_proceso'))
        max_id_proceso = result['id_proceso__max']
        resp = dict()
        data = []
        
        qwords = AnalisisDetalle.objects.filter(
            Q(id_analisis=id_analisisA) & ~Q(descripcion__startswith='@') & ~Q(descripcion__startswith='#')
            ).values_list('id_detalle', flat=True)
        
        
        qhash = AnalisisDetalle.objects.all().filter(
            Q(descripcion__startswith='#')
            ).values_list('id_detalle', flat=True)

        qmention = AnalisisDetalle.objects.all().filter(
             Q(descripcion__startswith='@') 
            ).values_list('id_detalle', flat=True)


        query =  Resultados.objects.filter(id_analisis=id_analisisA,id_proceso=max_id_proceso).prefetch_related(
            'id_proceso',
            'id_detalle'
        ).select_related(
            'id_proceso',
            'id_detalle'
        ).order_by(
            '-cantidad')[:5]

        aux = dict()
        for e,i in enumerate(query):
            aux["t"+str(e+1)] = i.cantidad
            aux["w"+str(e+1)] = i.id_detalle.descripcion
        data.append(aux) 
        
        query =  Resultados.objects.filter(id_analisis=id_analisisA,id_proceso=max_id_proceso, id_detalle__in=qmention).prefetch_related(
                'id_proceso',
                'id_detalle'
            ).select_related(
                'id_proceso',
                'id_detalle'
            ).order_by(
                '-cantidad')[:5]

        aux = dict()
        for e,i in enumerate(query):
            aux["t"+str(e+1)] = i.cantidad
            aux["w"+str(e+1)] = i.id_detalle.descripcion
        data.append(aux) 

        query =  Resultados.objects.filter(id_analisis=id_analisisA,id_proceso=max_id_proceso, id_detalle__in = qwords).prefetch_related(
            'id_proceso',
            'id_detalle'
        ).select_related(
            'id_proceso',
            'id_detalle'
        ).order_by(
            '-cantidad')[:5]

        aux = dict()
        for e,i in enumerate(query):
            aux["t"+str(e+1)] = i.cantidad
            aux["w"+str(e+1)] = i.id_detalle.descripcion
        data.append(aux) 

        fecha = Proceso.objects.get(pk=max_id_proceso)
        resp["time"] = fecha.fecha_inicio.strftime("%a %b %d %H:%M:%S %Y")
        resp["data"] = data

        rel = json.dumps(resp)
        return HttpResponse(rel, content_type="application/json")

class HashtagsResultsView(View):

    def get(self, request):
        resp = dict()
        temaId = Temas.objects.get(Q(tema__contains="COVID"))
        analisisId = AnalisisPorTemas.objects.get(Q(descripcion_analisis__contains="hashtags") & Q(id_tema= temaId))

        localidades = Localidad.objects.filter(id_loc_padre= 1)
        analisis_detalle = AnalisisDetalle.objects.filter(
            id_analisis__descripcion_analisis__contains="hashtags"
        ).annotate(tot=Sum("resultados__cantidad")).order_by('-tot')

        resultado = dict()
        features = []
        feature = dict()

        for localidad in localidades:
            # print(localidad.nombre, localidad.id_localidad)
            conteo_por_edo = 0
            feature = dict()
            feature["type"] = "Feature"
            
            data = dict()
            hastags_estado = Resultados.objects.filter(id_analisis=analisisId.id_analisis, id_localidad=localidad.id_localidad)
            for i in hastags_estado:
                
                conteo_por_edo += i.cantidad
                data[i.id_detalle.descripcion] = i.cantidad
        
            data['total'] = conteo_por_edo
            properties = dict()
            properties["name"]=localidad.nombre
            properties["data"] = data    
            
            feature["properties"] = properties

            geo = dict()
            geo["type"] = "MultiPolygon"
            geo["coordinates"] = json.loads( localidad.poligono)

            feature["geometry"] = geo
            features.append(feature)
        
        ultimaFechaAct = Resultados.objects.filter(id_analisis=analisisId.id_analisis).aggregate(Max('id_proceso__fecha_inicio'))
        resultado['time'] = ultimaFechaAct['id_proceso__fecha_inicio__max'].strftime("%a %b %d %H:%M:%S %Y")
                
        resultado["features"] = features
        rel = json.dumps(resultado)
        return HttpResponse(rel, content_type="application/json")

class TimelineSintomasView(View):
    
    def get(self, request):
        
        
        
        sintomas = AnalisisPorTemas.objects.get(
                Q(descripcion_analisis__icontains='sintomas') & 
                Q(id_tema=Temas.objects.get(tema__exact='COVID').id_tema))

        mental = AnalisisDetalle.objects.get(Q(id_analisis=sintomas.id_analisis) & Q(descripcion__exact="mentales"))

        query = Resultados.objects.filter(
            id_analisis=sintomas.id_analisis
        ).prefetch_related(
            'id_proceso',
            'id_detalle'
        ).select_related(
            'id_proceso'
        ).order_by(
            'id_proceso__fecha_inicio')
        

        fechaProceso = query[0].id_proceso.fecha_inicio

        resultados = list()

        contMent = 0
        contFis = 0
        for i in query:
            if i.id_proceso.fecha_inicio > fechaProceso:
                resp = dict()
                resp["Sintomas mentales"] = contMent
                resp["Sintomas COVID"] = contFis
                fecha = fechaProceso - datetime.timedelta(days=1)
                resp["day"] = fecha.strftime("%Y-%m-%d")
                resultados.append(resp)


                contMent = 0
                contFis = 0

                fechaProceso = i.id_proceso.fecha_inicio
            # print(i.id_detalle.id_detalle, "id del detallew")
            if i.id_detalle.id_detalle== mental.id_detalle:
                contMent += i.cantidad
            else:
                contFis += i.cantidad
                # print(i.id_proceso.fecha_inicio, i.id_detalle.descripcion, i.cantidad)
        resp = dict()
        resp["Sintomas mentales"] = contMent
        resp["Sintomas COVID"] = contFis
        fecha = fechaProceso - datetime.timedelta(days=1)
        resp["day"] = fecha.strftime("%Y-%m-%d")
        resultados.append(resp)



        data = dict()
        data ["time"] = fechaProceso.strftime("%a %b %d %H:%M:%S %Y") #fecah de actualización

        ###### OJO falta agregar fecha de fin de proceso
        data ["data"] = resultados
        rel = json.dumps(data)

        return HttpResponse(rel, content_type="application/json")  
    
class SentimientosView(View):

    def get(self, request):
        
        dictlist = list()
        

        sentimientos = AnalisisPorTemas.objects.get(
                Q(descripcion_analisis__icontains='analisis_emociones_sentimientos') & 
                Q(id_tema=Temas.objects.get(tema__icontains='COVID').id_tema)
            )

        query = Resultados.objects.filter(
            id_analisis=sentimientos.id_analisis
        ).prefetch_related(
            'id_proceso',
            'id_detalle'
        ).select_related(
            'id_proceso',
            'id_detalle'
        ).order_by(
            'id_proceso__fecha_inicio',
            'id_detalle__descripcion')
        


    

        for i in range(0,len(query),8):
            resp = dict()
            resp["enojo"] = query[i+4].cantidad
            resp["anticipacion"] = query[i+1].cantidad
            resp["disgusto"] = query[i+3].cantidad
            resp["miedo"] = query[i+5].cantidad
            resp["alegria"] = query[i].cantidad
            resp["tristeza"] = query[i+7].cantidad
            resp["sorpresa"] = query[i+6].cantidad
            resp["confianza"] = query[i+2].cantidad
            fecha= query[i].id_proceso.fecha_inicio - datetime.timedelta(days=1) # se resta un día porque corresponden a los tweets del día anterior al procesamiento 
            resp["day"] = fecha.strftime("%Y-%m-%d")

            dictlist.append(resp)

            #print(r.id_detalle.descripcion, r.cantidad, r.id_proceso.fecha_inicio.strftime("%Y-%m-%d"),end="")
#            resp[e.id_detalle.descripcion] = e.cantidad


        data = dict()
        data ["time"] = query[len(query)-1].id_proceso.fecha_inicio.strftime("%a %b %d %H:%M:%S %Y") #fecah de actualización

        ###### OJO falta agregar fecha de fin de proceso
        data ["data"] = dictlist
        rel = json.dumps(data)
        return HttpResponse(rel, content_type="application/json")
    
class SentimientosPolaridadView(View):

    def get(self, request):
        
        dictlist = list()
        

        sentimientos = AnalisisPorTemas.objects.get(
                Q(descripcion_analisis__icontains='analisis_emociones_polaridad') & 
                Q(id_tema=Temas.objects.get(tema__icontains='COVID').id_tema)
            )

        query = Resultados.objects.filter(
            id_analisis=sentimientos.id_analisis
        ).prefetch_related(
            'id_proceso',
            'id_detalle'
        ).select_related(
            'id_proceso',
            'id_detalle'
        ).order_by(
            'id_proceso__fecha_inicio',
            'id_detalle__descripcion')
        

       # print(query[len(query)-1].id_proceso.fecha_inicio.strftime("%a %b %d %H:%M:%S %Y"))

    

        for i in range(0,len(query),3):
            resp = dict()
            # for r in range (3):
            #     print(query[r].id_detalle.descripcion,query[r].cantidad)
            resp["Tweets_Neutro"] = query[i].cantidad
            resp["Tweets_Positivo"] = query[i+2].cantidad
            resp["Tweets_Negativo"] = query[i+1].cantidad
            fecha= query[i].id_proceso.fecha_inicio - datetime.timedelta(days=1) # se resta un día porque corresponden a los tweets del día anterior al procesamiento 
            resp["day"] = fecha.strftime("%Y-%m-%d")

            dictlist.append(resp)

            #print(r.id_detalle.descripcion, r.cantidad, r.id_proceso.fecha_inicio.strftime("%Y-%m-%d"),end="")
#            resp[e.id_detalle.descripcion] = e.cantidad

       

        data = dict()
        data ["time"] = query[len(query)-1].id_proceso.fecha_inicio.strftime("%a %b %d %H:%M:%S %Y") #fecah de actualización

        ###### OJO falta agregar fecha de fin de proceso
        data ["data"] = dictlist
        rel = json.dumps(data)
        return HttpResponse(rel, content_type="application/json")
    
class AlcaldiasSintomasResultsView(View):

    def get(self, request):
        temaId = Temas.objects.get(Q(tema__contains="COVID"))
        analisisId = AnalisisPorTemas.objects.get(Q(descripcion_analisis__contains="sintomas") & Q(id_tema= temaId))
        
        locPadre =  Localidad.objects.get(Q(nombre__contains="Ciudad de México"))
        alcaldias = Localidad.objects.filter(id_loc_padre= locPadre)
        
        resultado = Resultados.objects.filter(id_analisis = analisisId.id_analisis)
        idProceso = resultado.aggregate(max_id_proceso=Max('id_proceso'))['max_id_proceso']
        
        observaciones = AnalisisDetalle.objects.filter(id_analisis=analisisId)
        sintomasDetalle = dict()
        for i in observaciones:
            sintomasDetalle[i.descripcion] = i.id_detalle

        
        resultado = dict()
        features = []
        feature = dict()

        for localidad in alcaldias:

            feature = dict()
            feature["type"] = "Feature"
            
            data = dict()
            sintomas = Resultados.objects.filter(id_analisis=analisisId.id_analisis, id_detalle=sintomasDetalle["sintomas"], id_proceso=idProceso ,id_localidad=localidad.id_localidad)
            mentales = Resultados.objects.filter(id_analisis=analisisId.id_analisis, id_detalle=sintomasDetalle["mentales"], id_proceso=idProceso ,id_localidad=localidad.id_localidad)
            if len(sintomas):
                data["sintomas"]=(sintomas.values()[0])["cantidad"]
            else:
                data["sintomas"]=0
            if len(mentales):
                data["mentales"]=(mentales.values()[0])["cantidad"]
            else:
                data["mentales"]=0

            properties = dict()
            properties["name"]=localidad.nombre
            properties["data"] = data    
            
            # feature["properties"] = properties

            geo = dict()
            geo["type"] = "Polygon"
            pol = localidad.poligono
            geo["coordinates"] = json.loads( pol)

            feature["geometry"] = geo
            feature["properties"] = properties
            features.append(feature)
        
        ultimaFechaAct = Resultados.objects.filter(id_analisis=analisisId.id_analisis).aggregate(Max('id_proceso__fecha_inicio'))
        resultado['type'] = "FeatureCollection"
        resultado['time'] = ultimaFechaAct['id_proceso__fecha_inicio__max'].strftime("%a %b %d %H:%M:%S %Y")
                
        resultado["features"] = features
        rel = json.dumps(resultado)
        return HttpResponse(rel, content_type="application/json")
    
    
class SintomasPieChartView(View):
    
    def get(self, request):
        
        sentimientos = AnalisisPorTemas.objects.get(
                Q(descripcion_analisis__icontains='analisis_emociones_polaridad') & 
                Q(id_tema=Temas.objects.get(tema__icontains='COVID').id_tema)
            )

        resp = dict()

  
        totalEmociones = dict()
        
        for e in Resultados.objects.filter(id_analisis=sentimientos.id_analisis):
            #print(e.cantidad,e.id_detalle.descripcion)
            aux = resp.get(e.id_detalle.descripcion, 0)
            if aux == 0:
                totalEmociones[e.id_detalle.descripcion] = e.cantidad
            else:
                aux += e.cantidad
                totalEmociones[e.id_detalle.descripcion] += aux
        

        resultado = []
        for i in totalEmociones:
            aux = dict()
            aux["name"] = i
            aux["value"] = totalEmociones[i]

            resultado.append(aux)
                
        
        #   { name: 'Tweets Positivos', value: 6660 },
        #   { name: 'Tweets Negativos', value: 2500 },
        #   { name: 'Tweets Neutros', value: 3000 },
        
        fin = dict()
        fin["data_pie"] = resultado

        rel = json.dumps(fin)



        return HttpResponse(rel, content_type="application/json")