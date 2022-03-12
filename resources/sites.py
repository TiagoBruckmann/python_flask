from flask_restful import Resource
from models.site import SiteModel

class Sites(Resource):
    
    def get(self):
        return {
            "sites": [site.json() for site in SiteModel.query.all()]
        }

class Site(Resource):

    def get(self, url):

        site = SiteModel.find(url)
        if site:
            return site.json()
        
        return {
            "message": "Site não encontrado em nossa base de dados."
        }, 404 # not found

    def post(self, url):
        
        if SiteModel.find(url):
            return {
                "message": "O site especificado já existe."
            }, 400 # bad request

        site = SiteModel(url)
        
        try:
            site.save()
        except:
            return {
                "message": "Não foi possivel realizar sua solicitação, tente novamente mais tarde!"
            }, 500

        return site.json()

    def delete(self, url):
        
        site = SiteModel.find(url)

        if site:

            try:
                site.delete()
                return {
                    "message": "Site deletado com sucesso!"
                }, 200
            except: 
                return {
                    "message": "Não foi possivel realizar sua solicitação, tente novamente mais tarde!"
                }, 404
