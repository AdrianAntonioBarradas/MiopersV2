from django.db.models import Q, Max
from .models import *


def getLastProcessTopic (topic):
    id_tema = Temas.objects.get(tema__contains=topic).id_tema
    result = Proceso.objects.filter(id_tema=id_tema).aggregate(Max('id_proceso'))
    max_id_proceso = result['id_proceso__max']
    return max_id_proceso