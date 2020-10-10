import xmlrpc.client

class ModelCrud:
    
    def __init__(self,model_name):
        self._host = "host_url"
        self._db = "db_name"
        self._user = 'user'
        self._pass = "password"
        
        self._model_name = model_name
        
        
    def connect(self):
        """
            Se crea la conexion al servidor de Odoo.sh.
        """
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(self._host))
        return common
        
    def authenticate(self):
        """
            Realiza la autenticacion del usuario
        """ 
        uid = self.connect().authenticate(self._db, self._user, self._pass, {})
        return uid
        
    def getModels(self):
        """
            Obtiene la lista de modelos de Odoo.
        """ 
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(self._host))
        return models
    
    def search(self,domains, offset, limit):
        """
            Obtiene los ids del modelo.
        """ 
        self._models = self.getModels()
        self._uid = self.authenticate()
        ids = self._models.execute_kw(self._db, self._uid, self._pass, self._model_name, 'search',[domains], {'offset': offset, 'limit':limit})
        return ids

    def searchRead(self, fields, domains, offset, limit):
        """
            Obtiene los atributos de un modelo de forma directa.
        """ 
        uid = self.authenticate()
        models = self.getModels()
        record = models.execute_kw(self._db, uid, self._pass,self._model_name, 'search_read', [domains], {'fields': fields, 'offset': offset, 'limit':limit})
        return record 
        
    def read(self,ids, fields):
        """
            Obtiene los archivos de todos los ids.
        """
        uid = self.authenticate()
        record = models.execute_kw(self._db, uid, self._pass,self._model_name, 'read',[ids], {'fields': fields})
        return record  
        
    def create(self, newValue):
        """
            Crea un nuevo archivo de un modelo
        """
        uid = self.authenticate()
        models = self.getModels()
        id = models.execute_kw(self._db, uid, self._pass, self._model_name, 'create', [newValue])
        return id
    
    def write(self, domains, newValue):
        """
            Actualizar un archivo de un modelo
        """
        ids = self.search(domains,0 , 0)
        response = self._models.execute_kw(self._db, self._uid, self._pass, self._model_name, 'write', [ids, newValue])
        return response
    
    def unlink(self, domains):
        """
            Elimina archivos de un modelo segun filtro
        """
        ids = self.search(domains,0 , 0)
        response =  self._models.execute_kw(self._db, self._uid, self._pass, self._model_name, 'unlink', [ids])
        return response
