import os,re,random,requests,json
from flask import render_template,request,flash,abort,make_response,redirect,session,jsonify
from datetime import datetime,date,timedelta
from werkzeug.security import generate_password_hash, check_password_hash
#from foodapp.user.userroutes import restaurants
from . import vendorobj
from foodapp.models import * 


## Vendor change password page
@vendorobj.route("/password-settings/")
def vendor_changepassword():
    name=session.get("rest_name")
    id=session.get("restaurant_id")
    if name!= None and id!= None:
        return render_template('change-password.html')
    else:
        return redirect("/vendor/login/")
    