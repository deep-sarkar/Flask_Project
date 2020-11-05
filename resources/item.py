import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

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
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found.'}, 400

    
    def post(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return {'message':'item with name {} already exists.'.format(name)}

        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'])
        try:
            item.insert()
        except:
            return {'message':'AN error occoured in inserting item.'}, 500 # internal server error

        return item, 201
    
    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        delete_query = "DELETE FROM items WHERE name = ?"
        cursor.execute(delete_query,(name,))

        connection.commit()
        connection.close()

        return {'message':'Item deleted.'}, 200

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name, data['price'])
        if item is None:
            try:
               updated_item.insert()
            except:
                return {'message':'AN error occoured in inserting item.'}, 500 # internal server error
        else:
            try:
                updated_item.update()
            except:
                return {'message':'AN error occoured in updating item.'}, 500 # internal server error
        return updated_item.json(), 200

    

class ItemList(Resource):

    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        get_query = "SELECT * FROM items"
        result = cursor.execute(get_query)

        items = [{'name':item[0], 'price':item[1]} for item in result]

        connection.commit()
        connection.close()

        return {'items':items}, 200