import sqlite3
from flask_restful import Resource, reqparse
from models.Users import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', 
                        type=str, 
                        required=True, 
                        help="This is a mandatory payload input field")
    parser.add_argument('password', 
                        type=str, 
                        required=True, 
                        help="This is a mandatory payload input field")

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'An user with this username already exists'}

        user = UserModel(data['username'], data['password'])
        UserModel.save_to_db(user)

        return {"message": "User created succefully"}, 201
