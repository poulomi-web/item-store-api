import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.Items import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', 
                        type=float, 
                        required=True, 
                        help="This is a mandatory payload input field")
   
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404
        
    def post(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        new_item = ItemModel(name, data['price'])

        if item:
            return {'message': f'The item {name} already exists in the database'}, 400
        else:
            try:
                ItemModel.upsert(new_item)
            except Exception as e:
                print(e)
                return {'message': 'An error occured while inserting'}, 500

        return new_item.json(), 201

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)
        new_item = ItemModel(name, data['price'])

        if item is None:
            item = new_item
        else:
            item.price = data['price']

        ItemModel.upsert(item)
        return new_item.json()

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item is None:
            return {'message': 'Item does not exist'}
        else:
            ItemModel.delete(item)

        return {'message': 'Item deleted'}      

class Itemlist(Resource):
    def get(self):
        items = ItemModel.query.all()
 
        return {"items": [ItemModel.json(item_obj) for item_obj in items]}
