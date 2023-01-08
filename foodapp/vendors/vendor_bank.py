import os,re,random,requests,json
from flask import render_template,request,flash,abort,make_response,redirect,session,jsonify
from datetime import datetime,date,timedelta
from werkzeug.security import generate_password_hash, check_password_hash
#from foodapp.user.userroutes import restaurants
from . import vendorobj
from foodapp.models import * 


## Vendor change password page
@vendorobj.route("/add-bank-account/")
def vendor_bank_account():
    name=session.get("rest_name")
    id=session.get("restaurant_id")
    if name!= None and id!= None:
        bank_list = Banks.query.all()
        vendor_deets= Restaurant.query.filter(Restaurant.rest_id==id).first()
        return render_template('add-bank-account.html', banks=bank_list, vendor_info=vendor_deets)
    else:
        return redirect("/vendor/login/")