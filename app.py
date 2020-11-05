from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from flask_jwt import JWT, jwt_required
from security import identity, authenticate
from user import UserRegister



app = Flask(__name__)
app.secret_key = 'its very secret'
api = Api(app)

jwt = JWT(app, authenticate, identity)

items = []

class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
            'price',
            type=float,
            required=True,
            help='This field cannot be left blank'
        )

    @jwt_required()
    def get(self, name):
        item = next(filter(lambda list_items : list_items['name'] == name, items), None)
        return {'item':item}, 200 if item is not None else 404

    def post(self, name):
        if next(filter(lambda list_items : list_items['name'] == name, items), None):
            return {'msg':f"item with name {name} already exists."}, 400
        data = Item.parser.parse_args()
        item = {'name':name, 'price':data['price']}
        items.append(item)
        return item, 201
    
    def delete(self, name):
        global items
        items = list(filter(lambda item: item['name'] != name, items))
        return {'message': 'item deleted'}, 200

    def put(self, name):
        data = Item.parser.parse_args()
        item = next(filter(lambda x : x['name'] == name, items), None)
        if item:
            item.update(data)
        else:
            item = {'name':name, 'price':data['price']}
            items.append(item)
        return item, 200

class ItemList(Resource):

    def get(self):
        if len(items) == 0:
            return {'items':None}, 404
        return {'items':items}, 200


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
app.run(port=5000, debug=True)