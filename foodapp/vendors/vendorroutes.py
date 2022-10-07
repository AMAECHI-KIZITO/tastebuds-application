""""This module handles the vendor experience enabling the addition, update, viewing orders, updating orders request etc"""
import os,re,random,requests,json
import schedule,time,threading
from flask import render_template,request,flash,abort,make_response,redirect,session,jsonify
from datetime import datetime,date,timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from . import vendorobj
from foodapp.models import * 


# Restaurant Admin Dashboary Entry (Login Page)
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
        if vendor_details:
            allowed_mail=vendor_details.rest_email
            allowed_password=vendor_details.rest_pswd
            if mail_address==allowed_mail and check_password_hash(allowed_password,passkey):
                session['restaurant_id']=vendor_details.rest_id
                session['rest_name']=vendor_details.rest_name
                return redirect('/vendor/vendor-dashboard/')
            else:
                flash('Details Incorrect', category='WrongDetails')
                return redirect("/vendor/login/")
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
   
   
## Vendor Dashboard Entry
@vendorobj.route("/vendor-dashboard/")
def vendor_dashboard():
    name=session.get("rest_name")
    id=session.get("restaurant_id")
    if name!= None and id!= None:
        today_order_ids=[]
        today_orders_numbers=""
        
        
        order_no=db.session.query(Order).filter(Order.order_date==date.today(), Order.payment_status=="Paid").all()
        if order_no!=[]:
            for i in order_no:
                today_order_ids.append(i.order_id)
        
            # Looping over the Ids
            for x in today_order_ids:
                info=db.session.query(Order_details).filter(Order_details.order_id==x).all()
            
            
        return render_template("vendordashboard.html")
    else:
        return redirect("/vendor/login/")