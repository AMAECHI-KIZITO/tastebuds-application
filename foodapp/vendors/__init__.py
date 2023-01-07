from flask import Blueprint

vendorobj=Blueprint('bpvendor',__name__,template_folder='templates',static_folder="static",url_prefix='/vendor')

from . import vendorroutes, vendor_login_access, vendor_products_routes, vendor_orders_routes, vendor_accounts, vendor_settings