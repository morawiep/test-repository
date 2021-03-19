import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from db import db
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

application = Flask(__name__)

application.config['DEBUG'] = True

application.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.secret_key = 'jose'
api = Api(application)

jwt = JWT(application, authenticate, identity)  # /auth

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')

api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    db.init_app(application)

    if application.config['DEBUG']:
        @application.before_first_request
        def create_tables():
            db.create_all()

    application.run()
