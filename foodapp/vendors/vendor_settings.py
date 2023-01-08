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

## Password Change Form
@vendorobj.route('/pswd_change/', methods=['POST'])
def pswd_change():
    name=session.get("rest_name")
    id=session.get("restaurant_id")
    if name!= None and id!= None:
        vendor_info = db.session.query(Restaurant).filter(Restaurant.rest_id == id).first()
        
        form_old_pswd=request.form.get("old_pswd")
        form_new_pswd=request.form.get("new_pswd")
        form_confirm_pswd=request.form.get("new_pswd_confirm")
        
        
        if vendor_info:
            currentpswd=vendor_info.rest_pswd
            
            if form_old_pswd!="" and form_new_pswd!="" and form_confirm_pswd!="":
                matching = check_password_hash(currentpswd, form_old_pswd)
                if matching and form_new_pswd==form_confirm_pswd:
                    hashedpwd=generate_password_hash(form_confirm_pswd)
                    vendor_info.rest_pswd = hashedpwd
                    db.session.commit()
                    return "Password Successfully Changed"
                else:
                    return "Password Change Failed. Ensure details are correct"
            else:
                return "Please complete all fields"
        else:
            return redirect('/vendor/login/')           
    else:
        return redirect('/vendor/login/')


## Password Change Form for small screens
@vendorobj.route('/smallscreens_pswd_change/', methods=['POST'])
def vendor_small_screens_pswd_change():
    name=session.get("rest_name")
    id=session.get("restaurant_id")
    if name!= None and id!= None:
        vendor_info = db.session.query(Restaurant).filter(Restaurant.rest_id == id).first()
        
        form_old_pswd=request.form.get("smallscreen_old_pswd")
        form_new_pswd=request.form.get("smallscreen_new_pswd")
        form_confirm_pswd=request.form.get("smallscreen_new_pswd_confirm")
        
        
        if vendor_info:
            currentpswd = vendor_info.rest_pswd
            
            if form_old_pswd!="" and form_new_pswd!="" and form_confirm_pswd!="":
                matching = check_password_hash(currentpswd, form_old_pswd)
                if matching and form_new_pswd==form_confirm_pswd:
                    hashedpwd = generate_password_hash(form_confirm_pswd)
                    vendor_info.rest_pswd = hashedpwd
                    db.session.commit()
                    return "Password Successfully Changed"
                else:
                    return "Password Change Failed. Ensure details are correct"
            else:
                return "Please complete all fields"
        else:
            return redirect('/vendor/login/')
    else:
        return redirect('/vendor/login/')