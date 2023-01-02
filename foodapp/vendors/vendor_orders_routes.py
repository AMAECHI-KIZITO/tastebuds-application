from flask import render_template,request,flash,abort,make_response,redirect,session,jsonify
from datetime import datetime,date,timedelta
from werkzeug.security import generate_password_hash, check_password_hash
#from foodapp.user.userroutes import restaurants
from . import vendorobj
from foodapp.models import * 


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