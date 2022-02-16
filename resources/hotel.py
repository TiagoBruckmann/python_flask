from flask_restful import Resource, reqparse
from models.hotel_class import HotelModel

class Hoteis(Resource):
    def get(self):
        return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}

class Hotel(Resource):

    arguments = reqparse.RequestParser()
    arguments.add_argument("name", type=str, required=True, help="Informe o campo nome")
    arguments.add_argument("stars", type=float, required=True, help="Informe o campo estrelas")
    arguments.add_argument("price", type=float, required=True, help="Informe o campo preço")
    arguments.add_argument("city", type=str, required=True, help="Informe o campo cidade")

    # buscando hoteis
    def get(self, id):
        hotel_finded = HotelModel.find(id)
        if hotel_finded:
            return hotel_finded.json()
        return {"message": "Não encontramos nenhum hotel com este id: " + str(id)}, 400

    # criando hotel
    def post(self, id):
        if HotelModel.find(id):
            return {"message": "Já existe um hotel com este id: " + str(id)}, 400

        data = Hotel.arguments.parse_args()

        hotel = HotelModel(id, **data)

        try:
            hotel.save()
        except:
            return {"message": "Não foi possivel cadastrar o hotel, tente novamente mais tarde"}, 500

        return hotel.json()

    # atualizando um hotel
    def put(self, id):
        data = Hotel.arguments.parse_args()

        hotel_finded = HotelModel.find(id)

        if hotel_finded:
            hotel_finded.update(**data)

            try:
                hotel_finded.save()
            except:
                return {"message": "Não foi possivel atualizar o hotel: '{}', tente novamente mais tarde" . format(id)}, 500

            return hotel_finded.json(), 200 # updated

        hotel = HotelModel(id, **data)

        try:
            hotel.save()
        except:
            return {"message": "Não foi possivel cadastrar o hotel, tente novamente mais tarde"}, 500

        return hotel.json(), 201 # created

    # deletando um hotel
    def delete(self, id):
        
        hotel = HotelModel.find(id)
        if hotel:

            try:
                hotel.delete()
            except:
                return {"message": "Não foi possivel deletar o hotel: '{}', tente novamente mais tarde" . format(id)}, 500

            return {"message": "Hotel deletado com sucesso"}, 200
        return {"message": "Não encontramos nenhum hotel com este id: " + str(id)}, 400