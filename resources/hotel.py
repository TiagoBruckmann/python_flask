from flask_restful import Resource, reqparse
from models.hotel_class import HotelModel
from flask_jwt_extended import jwt_required
import sqlite3

def normalize_path_params( city = None, stars_min = 0, stars_max = 5, price_min = 0, price_max = 10000, limit = 50, offset = 0, **data):
    if city:
        return {
            "stars_min": stars_min,
            "stars_max": stars_max,
            "price_min": price_min,
            "price_max": price_max,
            "city": city,
            "limit": limit,
            "offset": offset
        }
    return {
        "stars_min": stars_min,
        "stars_max": stars_max,
        "price_min": price_min,
        "price_max": price_max,
        "limit": limit,
        "offset": offset
    }

path_params = reqparse.RequestParser()
path_params.add_argument("stars_min", type=float)
path_params.add_argument("stars_max", type=float)
path_params.add_argument("price_min", type=float)
path_params.add_argument("price_max", type=float)
path_params.add_argument("city", type=str)
path_params.add_argument("limit", type=float)
path_params.add_argument("offset", type=float)

class Hoteis(Resource):
    def get(self):

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        data = path_params.parse_args()
        valid_data = {key:data[key] for key in data if data[key] is not None}
        params = normalize_path_params(**valid_data)

        if not params.get("city"):
            query = """
                SELECT * FROM hoteis h
                WHERE (h.stars >= ? AND h.stars <= ?)
                AND (price >= ? AND price <= ?)
                LIMIT ? OFFSET ?
            """

            tupla = tuple([params[key] for key in params])
            result = cursor.execute(query, tupla)
        else:
            query = """
                SELECT * FROM hoteis h
                WHERE (h.stars >= ? AND h.stars <= ?)
                AND (price >= ? AND price <= ?)
                AND city = ? LIMIT ? OFFSET ?
            """

            tupla = tuple([params[key] for key in params])
            result = cursor.execute(query, tupla)

        hoteis = []
        for line in result:
            hoteis.append({
                "id": line[0],
                "name": line[1],
                "stars": line[2],
                "price": line[3],
                "city": line[4]
            })        

        return {'hoteis': hoteis}

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
    @jwt_required()
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
    @jwt_required()
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
    @jwt_required()
    def delete(self, id):
        
        hotel = HotelModel.find(id)
        if hotel:

            try:
                hotel.delete()
            except:
                return {"message": "Não foi possivel deletar o hotel: '{}', tente novamente mais tarde" . format(id)}, 500

            return {"message": "Hotel deletado com sucesso"}, 200
        return {"message": "Não encontramos nenhum hotel com este id: " + str(id)}, 400