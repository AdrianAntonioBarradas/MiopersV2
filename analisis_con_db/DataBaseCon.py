import pymysql
class DataBase:
    def __init__(self):
        self.connection = pymysql.connect(
            host="localhost",
            user="root",
            password="123Miopers*",
            db="miopersv2"
        )
        
        
        self.cursor = self.connection.cursor()
        print("Conexión Exitosa")
    
    def selectOne (self, sql):
        """ trae solo un elemento del de la consulta """
        try:
            self.cursor.execute(sql)
            edo = self.cursor.fetchone()
            return edo[0]
            
        except Exception as e:
            raise
        
    def selectAll (self, sql):
        """Obtiene una serie de varios elementos dependiendo el query"""
        try:
            self.cursor.execute(sql)
            edo = self.cursor.fetchall()
            return edo
            
        except Exception as e:
            raise
        
    def update (self, sql):
        """Permite hacer cambios en la base de datos: update, create, delete"""
        try:
            self.cursor.execute(sql)
            self.connection.commit()
            print("operación exitosa")
            
        except Exception as e:
            raise
    
    def nTema (self, tema, actualizar, diccionario):
        """Crea un nuevo tema con los parámetros especificados"""
        sql = "INSERT INTO temas (tema, actualizar, diccionario_tema) values ('{}', {}, '{}');".format(tema, actualizar, diccionario)
        self.update(sql)
    
    def nAnalisisTema (self, idTema, descripcion, path, dicc, actualizar):
        """crea un nuevo analisis por tema con los parámetros especificados"""
        if dicc:
            sql = "INSERT INTO analisis_por_temas (id_tema, descripcion_analisis, path_analisis, diccionario_analisis, actualizar) values ({},'{}', '{}', '{}',{});".format(idTema, descripcion, path, dicc, actualizar)
        else:
            sql = "INSERT INTO analisis_por_temas (id_tema, descripcion_analisis, path_analisis, diccionario_analisis, actualizar) values ({},'{}', '{}',NULL,{});".format(idTema, descripcion, path, actualizar)   
        self.update(sql)
        
    def getCurrentProceso (self):
        """optiene el id del proceso que está en ejecución"""
        sql = "SELECT max(id_proceso) from proceso;"
        return self.selectOne(sql)
    
    def getIdAnalisis (self, analisis):
        """retorna el id del análisis"""
        sql = "SELECT id_analisis FROM analisis_por_temas WHERE descripcion_analisis LIKE '{}';".format(analisis)
        return self.selectOne(sql)
    
    def getAnalisisDicc (self, analisis):
        """retorna el diccionario del análisis por su id"""
        sql = "SELECT diccionario_analisis FROM analisis_por_temas WHERE descripcion_analisis LIKE '{}';".format(analisis)
        return self.selectOne(sql)
    
    def getAllAnalisisTopic (self, analisis):
        """consigue todos los datos relacionado con el id del análisis"""
        #obtiene todas las descripciones con sus ids a partir del nombre del analisis
        sql = "SELECT ad.id_detalle, ad.descripcion FROM analisis_detalle ad, analisis_por_temas apt where ad.id_analisis = apt.id_analisis and apt.descripcion_analisis like '{}';".format(analisis)
        return self.selectAll(sql)
    
    def getIDLoc (self,lugar):
        """consigue id del lugar por su nombre"""
        sql = "SELECT id_localidad FROM localidad WHERE nombre LIKE '{}';".format(lugar)
        return self.selectOne(sql)
    
    def getAllLocChild(self,id_locPadre) -> dict():
        """Retorna todos los lugares asociados a esa aŕea"""
        sql = "SELECT nombre, id_localidad FROM  localidad WHERE id_loc_padre = {};".format(id_locPadre)
        mun = dict()
        for t in self.selectAll(sql):
            mun[t[0]] = t[1]
        return mun
    
    def toupdateTema (self, tema):
        """Retorna el valor acorde a si se va a ejecutar el tema"""
        sql = "select actualizar from temas where tema like '{}';".format(tema)
        return self.selectOne(sql)
    
    def toupdateAnalisis(self, analisis):
        """Retorna el valor acorde a si se va a ejecutar el análisis"""
        sql = "select actualizar from analisis_por_temas where descripcion_analisis like '{}';".format(analisis)
        return self.selectOne(sql)
    
    def fechaFinProceso(self,id):
        """agregar fecha al finalizar un proceso, se debe agregar id del proceso"""
        sql = "update proceso set fecha_fin = now() where id_proceso = {};".format(id)
        self.update(sql)
            
    def close (self):
        """cierra la conexión para terminar el registro"""
        self.connection.close()