from flask import render_template,request,flash, abort, make_response, redirect, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from . import vendorobj
from foodapp.models import * 


# Restaurant Login Page
@vendorobj.route("/login/")
def vendorlogin():
    return render_template("vendorloginpage.html")


# Vendor Route Login Verify
@vendorobj.route('/verifylogin/', methods=['POST'])
def vendor_login_verify():
    mail_address=request.form.get("email")
    passkey=request.form.get("pswd")
    
    if mail_address!="" and passkey!="":
        vendor_details=db.session.query(Restaurant).filter(Restaurant.rest_email==mail_address).first()
        if vendor_details and check_password_hash(vendor_details.rest_pswd, passkey):
            
            session['restaurant_id']=vendor_details.rest_id
            session['rest_name']=vendor_details.rest_name
            
            return redirect('/vendor/vendor-dashboard/')
        
        else:
            flash('Incorrect Credentials', category='WrongDetails')
            return redirect("/vendor/login/")
    else:
        flash('Kindly fill out all fields', category='WrongDetails')
        return redirect("/vendor/login/")

##Vendor Logout
@vendorobj.route("/logout/")
def vendorLogout():
    session.pop("restaurant_id",None)
    session.pop('rest_name',None)
    return redirect('/vendor/login/')

## After Request
@vendorobj.after_request
def clearcache(response):
    response.headers['Cache-Control']="no-cache, no store, must-revalidate"
    return response
