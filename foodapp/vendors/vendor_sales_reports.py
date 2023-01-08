import os,re,random,requests,json
from flask import render_template,request,flash,abort,make_response,redirect,session,jsonify
from datetime import datetime,date,timedelta
from werkzeug.security import generate_password_hash, check_password_hash
#from foodapp.user.userroutes import restaurants
from . import vendorobj
from foodapp.models import * 

def get_vendor_products(vendor_id):
    vendor_products = db.session.query(Product).filter(Product.prod_rest == vendor_id).all() 
    if vendor_products != []:
        products = []
        for product in vendor_products:
            products.append(product.prod_name)
            
        return products
    else:
        products = []
        return products


    
def get_sales(vendor_id):
    vendor_products = db.session.query(Product).filter(Product.prod_rest == vendor_id).all() 
    if vendor_products != []:
        sales_numbers=[]
        for product in vendor_products:
            the_qty_sold = Order_details.query.filter(Order_details.restaurant == product.prod_rest, Order_details.payment_status == 'Paid', Order_details.prod_id == product.prod_id).count()
            sales_numbers.append(the_qty_sold)
            
        return sales_numbers
    else:
        sales_numbers=[]
        return sales_numbers



def get_sales_revenue(vendor_id):
    vendor_products = db.session.query(Product).filter(Product.prod_rest == vendor_id).all() 
    if vendor_products != []:
        income=[]
        for product in vendor_products:
            
            the_income_per_product = Order_details.query.filter(Order_details.restaurant == product.prod_rest, Order_details.payment_status == 'Paid', Order_details.prod_id == product.prod_id).all()
            
            if the_income_per_product != []:
                total = 0
                for units in the_income_per_product:
                    total = total + units.amount
                income.append(total)
            else:
                income.append(0)
        return income
    else:
        income = []
        return income


    
## Vendor generate sales history
@vendorobj.route("/sales-history/")
def analyze_sales():
    name=session.get("rest_name")
    id=session.get("restaurant_id")
    if name!= None and id!= None:
        vendor_goods = get_vendor_products(id)
        product_sales = get_sales(id)
        income = get_sales_revenue(id)
        return render_template('generate-sales-history.html', vendor_goods=vendor_goods, product_sales=product_sales, income=income)
    else:
        return redirect("/vendor/login/")

