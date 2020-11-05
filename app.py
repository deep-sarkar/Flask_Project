from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import identity, authenticate
from user import UserRegister
from item import Item


app = Flask(__name__)
app.secret_key = 'its very secret'
api = Api(app)

jwt = JWT(app, authenticate, identity)


api.add_resource(Item, '/item/<string:name>')
# api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')



app.run(port=5000, debug=True)