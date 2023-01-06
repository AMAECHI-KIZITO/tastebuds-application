from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from flask_mail import Mail, Message
from foodapp.admin import adminobj
from foodapp.user import userobj
from foodapp.foodapp_api import apiobj
from foodapp.vendors import vendorobj

migrate=Migrate()
mail=Mail()
def create_app():
    food = Flask(__name__,instance_relative_config=True)
    food.config.from_pyfile('config.py')
    from foodapp import config
    food.config['MAIL_SERVER'] = 'smtp.gmail.com'
    food.config['MAIL_PORT'] = 465
    food.config['MAIL_USERNAME'] = 'konkakira1960@gmail.com'
    food.config['MAIL_PASSWORD'] = 'xicfwnrqibmeehov'
    food.config['MAIL_USE_SSL'] = True
    food.config['TESTING'] = False
    food.config['MAIL_SUPPRESS_SEND '] = False
    food.config.from_object(config)

    from foodapp.models import db
    
    db.init_app(food)
    migrate.init_app(food,db)
    
    food.register_blueprint(adminobj)
    food.register_blueprint(userobj)
    food.register_blueprint(apiobj)
    food.register_blueprint(vendorobj)
    
    
    mail.init_app(food)
    

    csrf=CSRFProtect(food)
    csrf.exempt(apiobj)
    return food