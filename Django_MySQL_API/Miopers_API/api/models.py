# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AnalisisDetalle(models.Model):
    id_detalle = models.AutoField(primary_key=True)
    id_analisis = models.ForeignKey('AnalisisPorTemas', models.DO_NOTHING, db_column='id_analisis')
    descripcion = models.TextField()

    class Meta:
        managed = False
        db_table = 'analisis_detalle'
        unique_together = (('id_detalle', 'id_analisis'),)


class AnalisisPorTemas(models.Model):
    id_analisis = models.AutoField(primary_key=True)
    id_tema = models.ForeignKey('Temas', models.DO_NOTHING, db_column='id_tema')
    descripcion_analisis = models.TextField()
    path_analisis = models.TextField(blank=True, null=True)
    diccionario_analisis = models.TextField(blank=True, null=True)
    actualizar = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'analisis_por_temas'


class Localidad(models.Model):
    id_localidad = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    poligono = models.TextField(blank=True, null=True)
    id_loc_padre = models.ForeignKey('self', models.DO_NOTHING, db_column='id_loc_padre', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'localidad'


class Proceso(models.Model):
    id_proceso = models.AutoField(primary_key=True)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField(blank=True, null=True)
    id_tema = models.ForeignKey('Temas', models.DO_NOTHING, db_column='id_tema')
    conteo_tweet = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'proceso'


class Resultados(models.Model):
    id_resultados = models.AutoField(primary_key=True)
    id_detalle = models.ForeignKey(AnalisisDetalle, on_delete=models.CASCADE, related_name='resultados', db_column='id_detalle')
    id_analisis = models.ForeignKey(AnalisisDetalle, on_delete=models.CASCADE, related_name='resultados_analisis', db_column='id_analisis')
    id_proceso = models.ForeignKey(Proceso, models.DO_NOTHING, db_column='id_proceso')
    cantidad = models.IntegerField(blank=True, null=True)
    id_localidad = models.ForeignKey(Localidad, models.DO_NOTHING, db_column='id_localidad', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'resultados'
    
   


class Temas(models.Model):
    id_tema = models.AutoField(primary_key=True)
    tema = models.CharField(max_length=100)
    actualizar = models.IntegerField(blank=True, null=True)
    diccionario_tema = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'temas'


class Tweet(models.Model):
    id_proceso = models.OneToOneField(Proceso, models.DO_NOTHING, db_column='id_proceso', primary_key=True)
    id_tweet = models.CharField(max_length=25)

    class Meta:
        managed = False
        db_table = 'tweet'
        unique_together = (('id_proceso', 'id_tweet'))
