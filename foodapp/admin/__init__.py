from flask import Blueprint
#from  foodapp import mail
adminobj=Blueprint('bpadmin',__name__,template_folder='templates',static_folder="static",url_prefix='/admin')

from . import adminroutes
