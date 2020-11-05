import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

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
        item = self.find_by_name(name)
        if item:
            return item
        return {'message': 'Item not found.'}, 400

    @classmethod
    def find_by_name(cls,name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query,(name,))
        row = result.fetchone()
        cursor.close()
        if row:
            return {'item':{'name':row[0], 'price':row[1]}}, 200

    def post(self, name):
        item = self.find_by_name(name)
        if item:
            return {'message':'item with name "{}" already exists.'.format(name)}
        data = Item.parser.parse_args()
        item = {'name':name, 'price':data['price']}

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        insert_query = "INSERT INTO items VALUES(?,?)"
        cursor.execute(insert_query,(item['name'],item['price']))

        connection.commit()
        connection.close()

        return item, 201
    
    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        delete_query = "DELETE FROM items WHERE name = ?"
        cursor.execute(delete_query,(name,))

        connection.commit()
        connection.close()

        return {'message':'Item deleted.'}, 200

#     def put(self, name):
#         data = Item.parser.parse_args()
#         item = next(filter(lambda x : x['name'] == name, items), None)
#         if item:
#             item.update(data)
#         else:
#             item = {'name':name, 'price':data['price']}
#             items.append(item)
#         return item, 200

# class ItemList(Resource):

#     def get(self):
#         if len(items) == 0:
#             return {'items':None}, 404
#         return {'items':items}, 200