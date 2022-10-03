import os,re,random,requests,json
import schedule,time,threading
from flask import render_template,request,flash,abort,make_response,redirect,session,jsonify
from datetime import datetime,date,timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from . import userobj
from foodapp.models import *

           
            
## Home Template
@userobj.route('/')
@userobj.route('/home/')
def home():
    shopping_ID = session.get('user_cart_id')
    if shopping_ID == None:
        session['user_cart_id']=int(random.random()*123421)
        shopping_ID = session.get('user_cart_id')
        usercart=db.session.query(Temporarycart).filter(Temporarycart.user_temp_id == shopping_ID, Temporarycart.temp_cart_date==date.today()).count()
        
        usercartdeets=db.session.query(Temporarycart).filter(Temporarycart.user_temp_id==shopping_ID, Temporarycart.temp_cart_date==date.today()).all()
        
        if usercartdeets!=[]:
            total=0
            for i in usercartdeets:
                total=total+i.amount
        else:
            total=0
        rests=db.session.query(Restaurant).all()
        return render_template('userindex.html', rests=rests, usercart=usercart, usercartdeets=usercartdeets, total=total)
    else:
        shopping_ID = session.get('user_cart_id')
        usercart=db.session.query(Temporarycart).filter(Temporarycart.user_temp_id==shopping_ID, Temporarycart.temp_cart_date==date.today()).count()
        usercartdeets=db.session.query(Temporarycart).filter(Temporarycart.user_temp_id==shopping_ID, Temporarycart.temp_cart_date==date.today()).all()
        rests=db.session.query(Restaurant).all()
        
        if usercartdeets!=[]:
            total=0
            for i in usercartdeets:
                total=total+i.amount
        else:
            total=0
        return render_template('userindex.html', rests=rests, usercart=usercart, usercartdeets=usercartdeets, total=total)
    
    
#Resturants Page Template
@userobj.route('/restaurants/<id>')
def restaurants(id):
    shopping_ID = session.get('user_cart_id')
    if shopping_ID!=None:
        rest_info=db.session.query(Restaurant).get(id)
        rest_maindish=db.session.query(Product).filter(Product.prod_rest==id,Product.prod_cat=='1').all()
        rest_swallow=db.session.query(Product).filter(Product.prod_rest==id,Product.prod_cat=='2').all()
        rest_soups=db.session.query(Product).filter(Product.prod_rest==id,Product.prod_cat=='3').all()
        rest_proteins=db.session.query(Product).filter(Product.prod_rest==id,Product.prod_cat=='4').all()
        rest_desserts=db.session.query(Product).filter(Product.prod_rest==id,Product.prod_cat=='5').all()
        rest_bread=db.session.query(Product).filter(Product.prod_rest==id,Product.prod_cat=='6').all()
        rest_salads=db.session.query(Product).filter(Product.prod_rest==id,Product.prod_cat=='7').all()
        rest_drinks=db.session.query(Product).filter(Product.prod_rest==id,Product.prod_cat=='8').all()
        
        usercart=db.session.query(Temporarycart).filter(Temporarycart.user_temp_id==shopping_ID, Temporarycart.temp_cart_date==date.today()).count()
        usercartdeets=db.session.query(Temporarycart).filter(Temporarycart.user_temp_id==shopping_ID, Temporarycart.temp_cart_date==date.today()).all()
        if usercartdeets!=[]:
            total=0
            for i in usercartdeets:
                total=total+i.amount
        else:
            total=0
        return render_template('restaurants.html', rest_info=rest_info, rest_maindish=rest_maindish, swallow=rest_swallow, soup=rest_soups, protein=rest_proteins, desserts=rest_desserts, bread=rest_bread, salad=rest_salads, drink=rest_drinks,usercart=usercart, usercartdeets=usercartdeets, total=total)
    else:
        return redirect('/user/')

#Account Registration Template
@userobj.route('/account/')
def newaccount():
    shopping_ID = session.get('user_cart_id')
    usercart=db.session.query(Temporarycart).filter(Temporarycart.user_temp_id==shopping_ID, Temporarycart.temp_cart_date==date.today()).count()
    usercartdeets=db.session.query(Temporarycart).filter(Temporarycart.user_temp_id==shopping_ID, Temporarycart.temp_cart_date==date.today()).all()
    rests=db.session.query(Restaurant).all()
        
    if usercartdeets!=[]:
        total=0
        for i in usercartdeets:
            total=total+i.amount
    else:
        total=0
    return render_template('newaccount.html', rests=rests, usercart=usercart, usercartdeets=usercartdeets, total=total)

#Account Login Template
@userobj.route('/login/')
def login():
    shopping_ID = session.get('user_cart_id')
    usercart=db.session.query(Temporarycart).filter(Temporarycart.user_temp_id==shopping_ID, Temporarycart.temp_cart_date==date.today()).count()
    usercartdeets=db.session.query(Temporarycart).filter(Temporarycart.user_temp_id==shopping_ID, Temporarycart.temp_cart_date==date.today()).all()
    rests=db.session.query(Restaurant).all()
        
    if usercartdeets!=[]:
        total=0
        for i in usercartdeets:
            total=total+i.amount
    else:
        total=0
    return render_template('login.html', rests=rests, usercart=usercart, usercartdeets=usercartdeets, total=total)

#Account Registration Form Verification Process
@userobj.route("/createaccount/", methods=["POST"])
def signup():
    fname=request.form.get('firstname')
    lname=request.form.get("lastname")
    cellphone=request.form.get("phone")
    e_mail=request.form.get("email")
    passcode=request.form.get("password")
    
    
    if fname!="" and lname!="" and cellphone!="" and e_mail!="" and passcode!="":
        if len(cellphone)==11 and cellphone.isnumeric():
            valid_phone=re.findall("^(080)|^(081)|^(070)|^(090)",cellphone)
            if valid_phone:
                valid_mail1=re.search("^\D",e_mail)
                valid_mail2=re.findall("(@gmail.com)$|(@yahoo.com)$|(@hotmail.com)$",e_mail)
                if valid_mail1:
                    if valid_mail1 and valid_mail2:
                        formatted_pswd=generate_password_hash(passcode)
                        try:
                            newacct=Customer(cust_firstname=fname,cust_lastname=lname,cust_phone=cellphone,cust_pswd=formatted_pswd,cust_email=e_mail)
                            db.session.add(newacct)
                            db.session.commit()
                            return 'Registration Complete. Proceed to Login'
                        except:
                            return 'Registration Failed. This email already exists'
                    else:
                        return "Invalid email address. Only Google, Yahoo and Hotmail accounts are allowed"
                else:
                    return "Invalid email format. Email cannot start with digit"
            else:
                return "Phone Number Invalid. Please provide a Nigerian mobile number"
        else:
            return "Invalid Phone Number"
    else:
        return "Fields cannot be empty"
    
#Account Login Verification Process
@userobj.route("/verifylogin/", methods=["POST"])
def verifylogin():
    user_email=request.form.get("email")
    user_pswd=request.form.get("password")
    
    if user_email!="" and user_pswd!="":
        cust_info=db.session.query(Customer).filter(Customer.cust_email==user_email).first()
        if cust_info:
            allowed_email=cust_info.cust_email
            allowed_pswd=cust_info.cust_pswd
            if user_email==allowed_email and check_password_hash(allowed_pswd,user_pswd):
                session['customer_id']=cust_info.cust_id
                session['customer_name']=cust_info.cust_firstname
                return redirect("/user/")
            else:
                flash('Details Incorrect', category='WrongDetails')
                return redirect("/user/login/")
        else:
            flash('Credentials Incorrect', category='WrongDetails')
            return redirect("/user/login/")
    else:
        flash('Kindly fill out all fields', category='WrongDetails')
        return redirect("/user/login/")
    
    
# Account Logout Process
@userobj.route("/logout/")
def customerlogout():
    session.pop('customer_id', None)
    session.pop('customer_name',None)
    session.pop('user_cart_id',None)
    return redirect('/user/login/')

#Add to temporary cart
@userobj.route('/temporarycart/')
def temporaryCart():
    shopping_ID = session.get('user_cart_id')
    if shopping_ID!=None:
        tempID=request.args.get('temp_id')
        productID=request.args.get('product')
        product_quantity=request.args.get('quantity')
        restaurant=request.args.get('eatry')
        amount_to_pay=request.args.get('amount')
        
        todays_date=date.today()
        
        temp=Temporarycart(user_temp_id=tempID, product=productID, product_qty=product_quantity, prod_restaurant=restaurant, amount=amount_to_pay,temp_cart_date=todays_date)
        db.session.add(temp)
        db.session.commit()
        
        return 'Added Successfully. To have an updated cart, kindly refresh the page."'
    else:
        return redirect('/user/')

## Remove Temporary cartitem
@userobj.route('/removeitem/')
def remove_temporary_item():
    trashID=request.args.get('trash')
    item_to_delete=db.session.query(Temporarycart).filter(Temporarycart.temp_cart_id==trashID).first()
    db.session.delete(item_to_delete)
    db.session.commit()
    return "Item deleted. To have an updated cart, kindly refresh the page."



## Empty Temporary cart
@userobj.route('/emptytemporarycart/')
def empty_temporary_cart():
    user_id=request.args.get('emptycartID')
    todaydate=date.today()
    items_to_delete = db.session.query(Temporarycart).filter(Temporarycart.user_temp_id==user_id, Temporarycart.temp_cart_date==todaydate).all()
    
    if items_to_delete !=[]:
        for deletecart in items_to_delete:
            db.session.delete(deletecart)
            db.session.commit()
        return "Cart Emptied Successfully. Please Refresh The Page."
    
    
# checkout
@userobj.route('/checkout/', methods=["POST"])
def checkout_temporary_cart():
    
    if session.get('customer_id')!=None and session.get('customer_name')!=None:
        if session.get('user_cart_id')!=None:
            # Generating a strong transaction reference
            characterset="asdfghjklpoiuytrewqzxcvbnmASDFGHJKLPOIUYTREWQZXCVBNM1234567890"
            characterset2="qwrtyplkjhgfdszxvbnmcXNDRQIVPIOA"
            for id in range(1):
                identity=""
                for uniq in range(5):
                    identity = identity + random.choice(characterset) + random.choice(characterset2)    
                reference=int(random.random()*1047700583)
                reference2=int(random.random()*1583)
                txnref=str(reference) + identity + str(reference2)
            
            
            # Generated Transaction Reference
            session['transaction_ref'] = txnref
            
            
            #Getting Form Details
            total_amount=request.form.get('totalamt')
            shipping=request.form.get('shipping_address')
            the_order_date=date.today()
            
            
            #Writing the cart details to the order table
            customer_order=Order(buyer=session.get('customer_id'), shipping_address=shipping, ref_no=session.get('transaction_ref'), order_date=the_order_date, order_status="Pending", order_amount=total_amount, payment_status="Pending")
            db.session.add(customer_order)
            db.session.commit()
            
            
            #Writing to the order details table
            Cust_OrderId=db.session.query(Order).filter(Order.buyer==session.get('customer_id'), Order.ref_no==session.get('transaction_ref')).first()
            
            orderplacedID=Cust_OrderId.order_id
            orderplacedDate=Cust_OrderId.order_date
            
            cart_details=db.session.query(Temporarycart).filter(Temporarycart.user_temp_id==session.get('user_cart_id'), Temporarycart.temp_cart_date==orderplacedDate).all()
            
            for cart_deets in cart_details:
                ord_details= Order_details(order_id=orderplacedID, prod_id=cart_deets.product, prod_qty=cart_deets.product_qty, amount=cart_deets.amount, restaurant=cart_deets.prod_restaurant, delivery_status="Pending",payment_status="Pending")
                db.session.add(ord_details)
                #db.session.delete(cart_deets)
            db.session.commit()
            
            
            # Sending the customer to information page
            information=db.session.query(Order_details).filter(Order_details.order_id==orderplacedID).all()
            
            return render_template('informationpage.html', ref=session.get('transaction_ref'), totalamount=total_amount, info=information)
        else:
            return redirect('/user/')
    else:
        flash("Login Required", category='Login_Required')
        return redirect("/user/login/")





## Transaction Outcome
@userobj.route('/transaction_outcome/')
def txn_outcome():
    txn_status=request.args.get('status')
    txn_ref=request.args.get('tx_ref')
    txn_id=request.args.get('transaction_id')
    data=jsonify(status=txn_status, reference=txn_ref, txn_id=txn_id)
    return data


## Bad Internet
@userobj.route('/poor/connection/')
def no_internet():
    return render_template("badinternet.html")
    

# checkout
@userobj.route('/pay_with_flutterwave/')
def pay_with_flutterwave():
    if session.get('customer_id')!=None and session.get('customer_name')!=None:
        reference=session.get('transaction_ref')
        
        orderinfo=db.session.query(Order).filter(Order.buyer==session.get('customer_id'), Order.ref_no==reference).first()
        orderplacedID=orderinfo.order_id
        orderplacedAmount=orderinfo.order_amount
        orderplacedDate=orderinfo.order_date
        #Writing into the payment table
        try:
            pay_process=Payment(pay_orderid=orderplacedID, pay_amt=orderplacedAmount, pay_ref=session.get('transaction_ref'), pay_date=datetime.now(), pay_status='Pending',pay_feedback='Pending')
            db.session.add(pay_process)
            db.session.commit()
        except:
            the_duplicate=db.session.query(Payment).filter(Payment.pay_ref==session.get('transaction_ref')).first()
            db.session.delete(the_duplicate)
            
            pay_process=Payment(pay_orderid=orderplacedID, pay_amt=orderplacedAmount, pay_ref=session.get('transaction_ref'), pay_date=datetime.now(), pay_status='Pending',pay_feedback='Pending')
            db.session.add(pay_process)
            
            db.session.commit()
            
            
        
        
        # Retrieving Customer info
        cust_deets=db.session.query(Customer).filter(Customer.cust_id==session.get('customer_id')).first()
        customer_name=f'{cust_deets.cust_firstname} {cust_deets.cust_lastname}'
        
        
        # Calling Flutterwaves Collect Payment endpoint
        data = {
            "customer": {
                "email":f"{cust_deets.cust_email}",
                "name":f"{customer_name}"
            },
            "amount":orderplacedAmount, 
            "currency":"NGN", 
            "tx_ref":reference,
            "redirect_url":"http://127.0.0.1:7500/user/transaction_outcome/"
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization":"Bearer FLWSECK_TEST-97a829830c93ce6fed7d14ade42d7628-X"
        }
        
        try:
            response = requests.post( "https://api.flutterwave.com/v3/payments", headers=headers, data=json.dumps(data) )
            rsp_json = response.json()
            
            #return rsp_json will return this format 
            # {
            #     "data": {
            #         "link": "https://ravemodal-dev.herokuapp.com/v3/hosted/pay/9277f9302ef5ec701dd1"
            #     }, 
            #     "message": "Hosted Link", 
            #     "status": "success"
            # }
            
            if rsp_json['status']=='success':
                url=rsp_json['data']['link']
                
                # delete items in cart
                cart_details=db.session.query(Temporarycart).filter(Temporarycart.user_temp_id==session.get('user_cart_id'), Temporarycart.temp_cart_date==orderplacedDate).all()
                for cart_deets in cart_details:
                    db.session.delete(cart_deets)
                db.session.commit()
                #direct to paymentlink
                return redirect(url)
        except:
            to_delete_payment=db.session.query(Payment).filter(Payment.pay_ref==session.get('transaction_ref')).first()
            id=to_delete_payment.pay_orderid
            # delete payment record
            db.session.delete(to_delete_payment)
            
            # delete order details record
            order_details_delete=db.session.query(Order_details).filter(Order_details.order_id==id).all()
            for i in order_details_delete:
                db.session.delete(i)
              
                
            # change order record
            order_delete=db.session.query(Order).filter(Order.order_id==id).first()
            order_delete.payment_status="Network Failed"
            order_delete.order_status="Failed"
            
            
            # delete items in cart
            cart_details=db.session.query(Temporarycart).filter(Temporarycart.user_temp_id==session.get('user_cart_id'), Temporarycart.temp_cart_date==orderplacedDate).all()
            for cart_deets in cart_details:
                db.session.delete(cart_deets)
            
            db.session.commit()
            
            
            session.pop("user_cart_id", None)
            return redirect("/user/poor/connection/")
    else:
        return redirect("/user/login/")






