from flask import Blueprint

vendorobj=Blueprint('bpvendor',__name__,template_folder='templates',static_folder="static",url_prefix='/vendor')

from . import vendorroutes