from flask import Flask, jsonify
from flask_restful import Api
from resources.hotel import Hoteis, Hotel
from resources.user import User, UserRegister, UserLogin, UserLogout
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = "userLoginTest"
app.config["JWT_BLACKLIST_ENABLED"] = True

api = Api(app)
jwt = JWTManager(app)

@app.before_first_request
def create_database():
    database.create_all()

@jwt.token_in_blocklist_loader
def verify_blacklist(self, token):
    return token["jti"] in BLACKLIST

@jwt.revoked_token_loader
def invalid_token(jwt_header, jwt_payload):
    return jsonify({"message": "Seu token de acesso foi revogado e acabou sendo desconectado"}), 401

api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<int:id>')
api.add_resource(User, '/users/<int:id>')
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')

if __name__ == '__main__':
    from sql_alchemy import database
    database.init_app(app)
    app.run(debug=True)