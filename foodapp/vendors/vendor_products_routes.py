import os,re,random,requests,json
import schedule,time,threading
from flask import render_template,request,flash,abort,make_response,redirect,session,jsonify
from datetime import datetime,date,timedelta
from werkzeug.security import generate_password_hash, check_password_hash
#from foodapp.user.userroutes import restaurants
from . import vendorobj
from foodapp.models import * 

    
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