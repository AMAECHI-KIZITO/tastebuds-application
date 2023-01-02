from flask import Blueprint

userobj=Blueprint('bpuser',__name__,template_folder='templates',static_folder="static",url_prefix='/user')

from . import userroutes, customer_orders_routes, error_pages
