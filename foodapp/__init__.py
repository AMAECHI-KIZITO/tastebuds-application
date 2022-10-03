from flask import Flask
from flask_wtf.csrf import CSRFProtect
from foodapp.admin import adminobj
from foodapp.user import userobj
from foodapp.foodapp_api import apiobj

def create_app():
    food = Flask(__name__,instance_relative_config=True) #we instantiated an object for the class Flask
    food.config.from_pyfile('config.py')
    from foodapp import config
    food.config.from_object(config) #here we are saying read the config from our class config

    from foodapp.models import db
    db.init_app(food)
    
    food.register_blueprint(adminobj)
    food.register_blueprint(userobj)
    food.register_blueprint(apiobj)


    csrf=CSRFProtect(food)
    csrf.exempt(apiobj)
    return food

