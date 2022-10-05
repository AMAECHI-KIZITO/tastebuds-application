""""This module handles the user dashboard experience"""
import os,re,random,requests,json
import schedule,time,threading
from flask import render_template,request,flash,abort,make_response,redirect,session,jsonify
from datetime import datetime,date,timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from . import userobj
from foodapp.models import *

           
# Customers Order Tracker
@userobj.route('/myaccount/')
def customer_orders():
    if session.get('customer_id')!=None and session.get('customer_name')!=None:
        
        #Fetching most patronized restaurant for a customer
        Restaurants=db.session.query(Restaurant).all()
        highest=0
        the_rest=''
        
        orders=db.session.query(Order).filter(Order.buyer==session.get('customer_id'), Order.payment_status=='Paid').all()
        for ord in orders:
            for fav in Restaurants:
                restaurant_number=db.session.query(Order_details).filter(Order_details.restaurant==fav.rest_id).count()
                if restaurant_number > highest:
                    highest=restaurant_number
                    the_rest=fav.rest_id
        
        # GETTING INFORMATION FOR THE TEMPLATE
        name_of_fav_restaurant=db.session.query(Restaurant).get(the_rest)
        
        number_of_successful_orders=db.session.query(Order).filter(Order.buyer==session.get('customer_id'), Order.payment_status=='Paid').count()
        
        customer=db.session.query(Customer).filter(Customer.cust_id==session.get('customer_id')).first()
        firstname=customer.cust_firstname
        lastname=customer.cust_lastname
        customer= f'{firstname} {lastname}'
        
        return render_template("customer/customer_dashboard2.html",fav_rest=name_of_fav_restaurant.rest_name, order_numbers=number_of_successful_orders,customer=customer)
    else:
        return redirect("/user/login/")
    


# TRACKING TODAYS ORDERS
@userobj.route('/today-orders/')
def monitor_order_progress():
    if session.get('customer_id')!=None and session.get('customer_name')!=None:
        #customer details
        customer=db.session.query(Customer).filter(Customer.cust_id==session.get('customer_id')).first()
        firstname=customer.cust_firstname
        lastname=customer.cust_lastname
        customer= f'{firstname} {lastname}'
        
        today_date=date.today()
        
        #order details
        today_orders=db.session.query(Order).filter(Order.buyer==session.get('customer_id'), Order.payment_status=='Paid', Order.order_date==today_date).count()
        
        orders=db.session.query(Order).filter(Order.buyer==session.get('customer_id'), Order.payment_status=='Paid', Order.order_date==today_date).order_by(Order.order_date.desc()).all()
        
        return render_template("customer/track_orders.html", customer=customer, today_orders=today_orders, orders=orders)
    else:
        return redirect("/user/login/")
    
# TRACKING ORDERS DETAILS
@userobj.route('/order/details/<id>')
def order_details(id):
    if session.get('customer_id')!=None and session.get('customer_name')!=None:
        #customer details
        customer=db.session.query(Customer).filter(Customer.cust_id==session.get('customer_id')).first()
        firstname=customer.cust_firstname
        lastname=customer.cust_lastname
        customer= f'{firstname} {lastname}'
        
        details=db.session.query(Order_details).filter(Order_details.order_id==id).all()
        return render_template("customer/order_details.html", customer=customer,details=details)
    else:
        return redirect("/user/login/")
    
    
# TRACKING All Transactions
@userobj.route('/all-transactions/')
def find_all_transactions():
    if session.get('customer_id')!=None and session.get('customer_name')!=None:
        #customer details
        customer=db.session.query(Customer).filter(Customer.cust_id==session.get('customer_id')).first()
        firstname=customer.cust_firstname
        lastname=customer.cust_lastname
        customer= f'{firstname} {lastname}'
        
        #order details
        today_orders=db.session.query(Order).filter(Order.buyer==session.get('customer_id')).count()
        
        orders=db.session.query(Order).filter(Order.buyer==session.get('customer_id')).order_by(Order.order_date.desc()).all()
        
        return render_template("customer/all_transactions.html", customer=customer, today_orders=today_orders, orders=orders)
    else:
        return redirect("/user/login/")
    
    
# Password Settings
@userobj.route('/customer/password-settings/')
def customer_change_password():
    if session.get('customer_id')!=None and session.get('customer_name')!=None:
        #customer details
        customer=db.session.query(Customer).filter(Customer.cust_id==session.get('customer_id')).first()
        firstname=customer.cust_firstname
        lastname=customer.cust_lastname
        customer= f'{firstname} {lastname}'
        
        return render_template("customer/password_settings.html", customer=customer)
    else:
        return redirect("/user/login/")
    
    
## Password Change Form
@userobj.route('/pswd_change/',methods=['POST'])
def pswd_change():
    if session.get('customer_id')!=None and session.get('customer_name')!=None:
        # This is to retrieve current customer info
        Userdeets=db.session.query(Customer).filter(Customer.cust_id==session.get('customer_id')).first()
        
        # This is to get the form data
        form_old_pswd=request.form.get("old_pswd")
        form_new_pswd=request.form.get("new_pswd")
        form_confirm_pswd=request.form.get("new_pswd_confirm")
        
        
        if Userdeets:
            currentpswd=Userdeets.cust_pswd
            
            if form_old_pswd!="" and form_new_pswd!="" and form_confirm_pswd!="":
                matching=check_password_hash(currentpswd,form_old_pswd)
                if matching and form_new_pswd==form_confirm_pswd:
                    hashedpwd=generate_password_hash(form_confirm_pswd)
                    Userdeets.cust_pswd=hashedpwd
                    db.session.commit()
                    return "Password Successfully Changed"
                else:
                    return "Password Change Failed. Ensure details are correct"
            else:
                return "Please complete all fields"
        else:
            return redirect('/user/login/')           
    else:
        return redirect('/user/login/')


## Password Change Form for small screens
@userobj.route('/smallscreens_pswd_change/',methods=['POST'])
def smallscreens_pswd_change():
    if session.get('customer_id')!=None and session.get('customer_name')!=None:
        # This is to retrieve current admin info
        Userdeets=db.session.query(Customer).filter(Customer.cust_id==session.get('customer_id')).first()
        
        # This is to get the form data
        form_old_pswd=request.form.get("smallscreen_old_pswd")
        form_new_pswd=request.form.get("smallscreen_new_pswd")
        form_confirm_pswd=request.form.get("smallscreen_new_pswd_confirm")
        
        
        if Userdeets:
            currentpswd=Userdeets.cust_pswd
            
            if form_old_pswd!="" and form_new_pswd!="" and form_confirm_pswd!="":
                matching=check_password_hash(currentpswd,form_old_pswd)
                if matching and form_new_pswd==form_confirm_pswd:
                    hashedpwd=generate_password_hash(form_confirm_pswd)
                    Userdeets.cust_pswd=hashedpwd
                    db.session.commit()
                    return "Password Successfully Changed"
                else:
                    return "Password Change Failed. Ensure details are correct"
            else:
                return "Please complete all fields"
        else:
            return redirect('/user/login/')
    else:
        return redirect('/user/login/')
