import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.store import StoreModel

class Store(Resource):

    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404
        
    def post(self, name):

        store = StoreModel.find_by_name(name)
        new_store = StoreModel(name)

        if store:
            return {'message': f'The store {name} already exists in the database'}, 400
        else:
            try:
                StoreModel.upsert(new_store)
            except Exception as e:
                print(e)
                return {'message': 'An error occured while inserting'}, 500

        return new_store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store is None:
            return {'message': 'Store does not exist'}
        else:
            StoreModel.delete(store)

        return {'message': 'store deleted'}     


class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}