from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from flask_mail import Mail, Message
from foodapp.admin import adminobj
from foodapp.user import userobj
from foodapp.foodapp_api import apiobj
from foodapp.vendors import vendorobj

migrate=Migrate()
def create_app():
    food = Flask(__name__,instance_relative_config=True) #we instantiated an object for the class Flask
    food.config.from_pyfile('config.py')
    from foodapp import config
    food.config.from_object(config) #here we are saying read the config from our class config

    from foodapp.models import db
    db.init_app(food)
    migrate.init_app(food,db)
    
    # mail=Mail.init_app(food)
    # food.config['MAIL_SERVER'] = 'smtp.gmail.com'
    # food.config['MAIL_PORT'] = 465
    # food.config['MAIL_USERNAME'] = 'ccmarketsgroup@gmail.com'
    # food.config['MAIL_PASSWORD'] = 'rewrscyzufbognjt'
    # food.config['MAIL_USE_SSL'] = True
    
    food.register_blueprint(adminobj)
    food.register_blueprint(userobj)
    food.register_blueprint(apiobj)
    food.register_blueprint(vendorobj)
    

    csrf=CSRFProtect(food)
    csrf.exempt(apiobj)
    return food