import json
import ast
from model_crud import ModelCrud

class LambdaModel:
    def __init__(self, event):
        self.event = event
    
    def getParameters(self):
        """
            Obtiene los parametros de la Url para usarlos
            en la busqueda en la Api de Odoo.
        """
        self.httpMethod = self.event['httpMethod']
        self.queryStrings = self.event['multiValueQueryStringParameters']
        self.model_name = self.queryStrings['model'][0]
        try:
            self.fields = str(self.queryStrings['fields'])[4:-4].split("','")
        except:
            self.fields = []
        try:
            self.domains = ast.literal_eval(self.queryStrings['domains'][0])
        except:
            self.domains = []
        try:
            self.limit = int(self.queryStrings['limit'][0])
        except:
            self.limit = 0
        try:
            self.offset = int(self.queryStrings['offset'][0])
        except:
            self.offset = 0
    
    def handler(self):
        """
            Realiza las peticiones a la base de datos
            dependiendo del tipo de peticion HTTP.
        """
        self.getParameters()
        
        if(self.httpMethod == "GET"):
            result = ModelCrud(self.model_name).searchRead(self.fields, self.domains, self.offset, self.limit)

        if(self.httpMethod == "POST"):
            result = ModelCrud(self.model_name).create(json.loads(self.event['body']))
            
        if (self.httpMethod == "PUT"):
            result = ModelCrud(self.model_name).write(self.domains, json.loads(self.event['body']))
        
        if (self.httpMethod == "DELETE"):
            result = ModelCrud(self.model_name).unlink(self.domains)
        
        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }
