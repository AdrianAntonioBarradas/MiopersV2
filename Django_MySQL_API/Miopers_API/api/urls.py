from django.urls import path
from .views import *


urlpatterns=[
    path('temas/', TemasView.as_view(), name='temas_list'),
    path('resultados/', ResultadosView.as_view(), name='temas_res'),
    path('timeline/', TimelineView.as_view(), name='temas_res'),
    path('alcaldias_result/', AlcaldiasResultView.as_view(), name='alacaldias_sintomas'),
    path('words/', WordsResultsView.as_view(), name='words'), 
    path('hashtags/', HashtagsResultsView.as_view(), name='hashtags'),
    path('sintomas/', TimelineSintomasView.as_view(), name='hashtags'),
    path('sintomaspie/', SintomasPieChartView.as_view(), name='hashtags'),
    path('alacaldiassintomas/',AlcaldiasSintomasResultsView.as_view(), name='sintomaspie'),
    path('sentimientos/', SentimientosView.as_view(), name='sentimientos'),
    path('sentimientosPolaridad/',SentimientosPolaridadView.as_view(), name='senitmientosPolaridad')
    
]