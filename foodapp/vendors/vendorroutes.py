import os,re,random,requests,json
from flask import render_template,request,flash,abort,make_response,redirect,session,jsonify
from datetime import datetime,date,timedelta
from werkzeug.security import generate_password_hash, check_password_hash
#from foodapp.user.userroutes import restaurants
from . import vendorobj
from foodapp.models import * 


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
    