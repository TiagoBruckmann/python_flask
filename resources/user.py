from flask_restful import Resource, reqparse
from models.users import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from werkzeug.security import safe_str_cmp
from blacklist import BLACKLIST

attributes = reqparse.RequestParser()
attributes.add_argument('email', type=str, required=True, help="O campo email precisa ser preenchido")
attributes.add_argument('password', type=str, required=True, help="O campo senha precisa ser preenchido")

class User(Resource):

    # buscando usuarios
    @jwt_required()
    def get(self, id):
        user_finded = UserModel.find(id)
        if user_finded:
            return user_finded.json()
        return {"message": "Não encontramos nenhum usuário com este id: " + str(id)}, 400

    # deletando um usuario
    @jwt_required()
    def delete(self, id):
        
        user = UserModel.find(id)
        if user:

            try:
                user.delete()
            except:
                return {"message": "Não foi possivel deletar o usuário: '{}', tente novamente mais tarde" . format(id)}, 500

            return {"message": "Usuário deletado com sucesso"}, 200
        return {"message": "Não encontramos nenhum usuário com esse id: " + str(id)}, 400

class UserRegister(Resource):

    def post(self):

        data = attributes.parse_args()

        if UserModel.find_by_email(data["email"]):
            return {"message": "Já existe uma conta com este endereço de e-mail"}, 400
        
        user = UserModel(**data)
        user.save()
        return {"message": "Usuário criado com sucesso!"}, 201

class UserLogin(Resource):

    @classmethod
    def post(cls):
        data = attributes.parse_args()

        user = UserModel.find_by_email(data["email"])

        if user and safe_str_cmp(user.password, data["password"]):
            token = create_access_token(identity=user.id)
            return {"token": token}, 200
        
        return {"message": "usuário ou senha estão incorretos!"}, 401

class UserLogout(Resource):
    
    @jwt_required()
    def post(self):
        jwt_id = get_jwt()["jti"]
        BLACKLIST.add(jwt_id)
        return {"message": "Usuário desconectado com sucesso!"}, 200