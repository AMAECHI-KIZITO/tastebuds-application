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
    
    
@vendorobj.route('/validate-account-number/')
def validate_account_number():
    name=session.get("rest_name")
    id=session.get("restaurant_id")
    if name!= None and id!= None:
        acct = request.args.get('account')
        bank = request.args.get('bank')
        #bank_deets = db.session.query(Banks).filter(Banks.bank_id == bank).first()
        #bankcode = bank_deets.bank_code
        
        payload = {
            "account_number":str(acct), 
            "account_bank":str(bank), 
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization":"Bearer FLWSECK_TEST-97a829830c93ce6fed7d14ade42d7628-X"
        }
        response = requests.post( f"https://api.flutterwave.com/v3/accounts/accounts/resolve",{
            "account_number":str(acct), 
            "account_bank":str(bank), 
        }, headers=headers)
        rsp_json = response.json()
        
        
        print(rsp_json)
        return 'checked'
    
        if rsp_json['status'] == 'success':
            return rsp_json['data']['account_name'] 
        elif rsp_json['status'] == 'error':
            return rsp_json['message']
        else:
            return "Unable to verify this account"
        
        
        # try:
        #     response = requests.post( f"https://api.flutterwave.com/v3/accounts/accounts/resolve", headers=headers, data=json.dumps(data) )
        #     rsp_json = response.json()
        #     if rsp_json['status'] == 'success':
        #         return rsp_json['data']['account_name'] 
        #     elif rsp_json['status'] == 'error':
        #         return rsp_json['message']
        #     else:
        #         return "Unable to verify this account"
        # except:
        #     return "Unable to verify account. Ensure Internet connection is secure."          
    else:
        return redirect('/vendor/login/')