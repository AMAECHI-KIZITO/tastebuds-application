""""This module handles the vendor experience enabling the addition, update, viewing orders, updating orders request etc"""
import os,re,random,requests,json
import schedule,time,threading
from flask import render_template,request,flash,abort,make_response,redirect,session,jsonify
from datetime import datetime,date,timedelta
from werkzeug.security import generate_password_hash, check_password_hash

from foodapp.user.userroutes import restaurants
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
@vendorobj.route("/")
def vendor_dashboard():
    name=session.get("rest_name")
    id=session.get("restaurant_id")
    if name!= None and id!= None:
        today_order_ids=[]
        today_orders_numbers=0
        
        #this will store distinct order ids having the restaurants orders in them
        restaurants_specific_ids=[]
        #this will store the dictionary of each restaurant order info 
        restaurants_specific_ids_orders=[]
        
        
        order_no=db.session.query(Order).filter(Order.order_date==date.today(), Order.payment_status=="Paid").all()
        if order_no!=[]:
            for i in order_no:
                today_order_ids.append(i.order_id)
        
            # Looping over the Ids to get amount made for the day
            for x in today_order_ids:
                info=db.session.query(Order_details).filter(Order_details.order_id==x, Order_details.restaurant==id).all()
                for amt_made in info:
                    today_orders_numbers=today_orders_numbers+amt_made.amount
                    if amt_made.order_id not in restaurants_specific_ids:
                        restaurants_specific_ids.append(amt_made.order_id)
                    else:
                        continue
              
              
            #here we put together a dictionary of the order info for each restaurant and count the number
            orders_placed_today=0     
            for order_deets in restaurants_specific_ids:
                orders_placed_today=orders_placed_today + 1
                
                the_dict={}
                details=db.session.query(Order).filter(Order.order_id==order_deets).first()
                
                
                the_dict['order_id']=details.order_id
                the_dict['customer']=details.buyer
                the_dict['ref']=details.ref_no
                the_dict['address']=details.shipping_address
                the_dict['order_status']=details.order_status
                restaurants_specific_ids_orders.append(the_dict)
            
            
            #emptying the ids thereafter
            today_order_ids=[]    
            
            return render_template("vendordashboard.html", amountmade=today_orders_numbers, orderdetails=restaurants_specific_ids_orders,orders_placed_today=orders_placed_today)
        else:
            return render_template("vendordashboard.html", amountmade=0, orderdetails="No orders today",orders_placed_today=0)
    else:
        return redirect("/vendor/login/")
    
    
## Vendor Today Orders Tracker
@vendorobj.route("/today-orders/")
def vendor_orders():
    name=session.get("rest_name")
    id=session.get("restaurant_id")
    
    if name!= None and id!= None:
        today_order_ids=[]
        today_orders_numbers=0
        
        #this will store distinct order ids having the restaurants orders in them
        restaurants_specific_ids=[]
        #this will store the dictionary of each restaurant order info 
        restaurants_specific_ids_orders=[]
        
        
        order_no=db.session.query(Order).filter(Order.order_date==date.today(), Order.payment_status=="Paid").all()
        if order_no!=[]:
            for i in order_no:
                today_order_ids.append(i.order_id)
        
            # Looping over the Ids to get amount made for the day
            for x in today_order_ids:
                info=db.session.query(Order_details).filter(Order_details.order_id==x, Order_details.restaurant==id).all()
                for amt_made in info:
                    today_orders_numbers=today_orders_numbers+amt_made.amount
                    if amt_made.order_id not in restaurants_specific_ids:
                        restaurants_specific_ids.append(amt_made.order_id)
                    else:
                        continue
              
              
            #here we put together a dictionary of the order info for each restaurant and count the number
            orders_placed_today=0     
            for order_deets in restaurants_specific_ids:
                orders_placed_today=orders_placed_today + 1
                
                the_dict={}
                details=db.session.query(Order).filter(Order.order_id==order_deets).first()
                
                
                
                the_dict['customer']=f'{details.Order_cust_info.cust_firstname} {details.Order_cust_info.cust_lastname}'
                #the_dict['ref']=details.ref_no
                the_dict['address']=details.shipping_address
                #the_dict['order_status']=details.order_status
                the_dict['order_date']=details.order_date
                the_dict['order_id']=details.order_id
                restaurants_specific_ids_orders.append(the_dict)
            
            #emptying the ids thereafter
            today_order_ids=[]    
            
            #return f'{restaurants_specific_ids_orders}'
        return render_template('vendor_orders.html', restaurants_specific_ids_orders=restaurants_specific_ids_orders)
    else:
        return redirect("/vendor/login/")
 
    
# Vendor Order Details
@vendorobj.route("/orderdetails/<id>")
def vendor_order_deets(id):
    if session.get('rest_name')!=None and session.get("restaurant_id")!=None:
        order_id_deets=db.session.query(Order_details).filter(Order_details.order_id==id, Order_details.restaurant==session.get('restaurant_id')).all()
        
        order_ref=db.session.query(Order).get(id)
        ref=order_ref.ref_no
        
        OrderStatusofOne=db.session.query(Order_details).filter(Order_details.order_id==id, Order_details.restaurant==session.get('restaurant_id')).first()
        
        current_status=OrderStatusofOne.delivery_status
        
        return render_template('vendor_order_details.html', order_details=order_id_deets, id=id, ref=ref, current_status=current_status)
    else:
        return redirect("/vendor/login/")
    
    
# Vendor Change Delivery Status
@vendorobj.route("/change-delivery-status/", methods=['POST'])
def vendor_delivery_status():
    if session.get('rest_name')!=None and session.get("restaurant_id")!=None:
        decision=request.form.get('choice')
        id=request.form.get('orderID')
        ref=request.form.get('orderRef')
        eatry=request.form.get('restID')
        
        OrderStatusofOne=db.session.query(Order_details).filter(Order_details.order_id==id, Order_details.restaurant==eatry).first()
        
        
        if OrderStatusofOne.delivery_status=='Pending':
            orderstatus=db.session.query(Order_details).filter(Order_details.order_id==id,Order_details.restaurant==eatry).all()
            for i in orderstatus:
                i.delivery_status=decision
            db.session.commit()
            return f'Status Updated'
        else:
            return f'Unable to complete request. An action has been carried out on this order.'
    else:
        return redirect("/vendor/login/")
    
# Vendor View All Products
@vendorobj.route("/all/products/")
def vendor_all_products():
    if session.get('rest_name')!=None and session.get("restaurant_id")!=None:
        restaurant_products=db.session.query(Product).filter(Product.prod_rest==session.get("restaurant_id")).all()
        products_category=db.session.query(Category).all()
        return render_template("restaurant_products.html", products=restaurant_products, category=products_category)
    else:
        return redirect("/vendor/login/")
    

# Vendor Edit Product
@vendorobj.route("/edit-product/<id>")
def vendor_edit_products(id):
    if session.get('rest_name')!=None and session.get("restaurant_id")!=None:
        products=db.session.query(Product).get(id)
        products_category=db.session.query(Category).all()
        return render_template("editproduct.html", products=products, category=products_category)
    else:
        return redirect("/vendor/login/")
    
    
# Vendor Update Product Big Screens
@vendorobj.route("/update/product/",methods=['POST'])
def vendor_update_products():
    if session.get('rest_name')!=None and session.get("restaurant_id")!=None:
        product_identity=request.form.get('product_id')
        product_name=request.form.get('product_name')
        product_price=request.form.get('product_price')
        product_category=request.form.get('product_category')
        product_img=request.files.get('product_img')
        product_desc=request.form.get('product_desc')
        allowed=['.jpeg','.jpg']
        
        if product_identity!="" and product_name!="" and product_price!='' and product_category!="#" and product_img!="" and product_desc!="":
            
            originalfilename=product_img.filename
            
            name,extension=os.path.splitext(originalfilename)
            
            if extension in allowed:
                originalfile = "foodapp/user/static/rest_prod_imgs/"+str(session.get("restaurant_id"))+originalfilename
                product_img.save(originalfile)
                save2db=str(session.get("restaurant_id"))+originalfilename
                
                product_to_add=db.session.query(Product).get(product_identity)
                    
                product_to_add.prod_name=product_name
                product_to_add.prod_price=product_price
                product_to_add.prod_cat=product_category
                product_to_add.prod_image=save2db
                product_to_add.prod_description=product_desc
                db.session.commit()
                return "Update Successful"
            else:
                return "Invalid picture format. Please upload a .jpg or .jpeg file."
        else:
            return "Fill Out All Fields"
    else:
        return redirect("/vendor/login/")
    
    
# Vendor Update Product Small Screens 
@vendorobj.route("/update-product/",methods=['POST'])
def vendor_update_products_small_screens():
    if session.get('rest_name')!=None and session.get("restaurant_id")!=None:
        product_identity=request.form.get('smallScreenProduct_id')
        product_name=request.form.get('smallScreenProductName')
        product_price=request.form.get('smallScreenProductPrice')
        product_category=request.form.get('smallScreenProductCategory')
        product_img=request.files.get('smallScreenProductImg')
        product_desc=request.form.get('smallScreenProductDesc')
        allowed=['.jpeg','.jpg']
        
        if product_identity!="" and product_name!="" and product_price!='' and product_category!="#" and product_img!="" and product_desc!="":
            
            originalfilename=product_img.filename
            
            name,extension=os.path.splitext(originalfilename)
            
            if extension in allowed:
                originalfile = "foodapp/user/static/rest_prod_imgs/"+str(session.get("restaurant_id"))+originalfilename
                product_img.save(originalfile)
                save2db=str(session.get("restaurant_id"))+originalfilename
                
                product_to_add=db.session.query(Product).get(product_identity)
                    
                product_to_add.prod_name=product_name
                product_to_add.prod_price=product_price
                product_to_add.prod_cat=product_category
                product_to_add.prod_image=save2db
                product_to_add.prod_description=product_desc
                db.session.commit()
                return "Update Successful"
            else:
                return "Invalid picture format. Please upload a .jpg or .jpeg file."
        else:
            return "Fill Out All Fields"
    else:
        return redirect("/vendor/login/")