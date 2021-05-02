from flask import Flask
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required

from resources.Items import Item, Itemlist
from resources.store import Store, StoreList
from security import authenticate, identity
from resources.Users import UserRegister

from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "Dimpu"
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(Itemlist, '/itemlist')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/storelist')

if __name__=='__main__':
    db.init_app(app)
    app.run(port=5000,debug=True)