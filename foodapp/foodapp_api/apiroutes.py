import json,os
from flask import jsonify,request,make_response
from flask_httpauth import HTTPBasicAuth
from . import apiobj
from foodapp.models import *

auth=HTTPBasicAuth()


## To fetch all restaurants
@apiobj.route('/v1.0/eatry/',methods=['GET'])
def allRestaurants():
    
    eatries=db.session.query(Restaurant).all()
    if eatries==[]:
        data2ret={"status":False, "message":'No Restaurant Found'}
    else:
        record=[]
        for x in eatries:
            a={}
            a['name']=x.rest_name
            a['address']=x.rest_address
            a['contact']=x.rest_phone
            a['email']=x.rest_email
            a['about']=x.rest_about
            a['image']=x.rest_img
            
            record.append(a)
        data2ret={"status":True, "message":record}
        
    data=jsonify(data2ret)
    return data


## To fetch all Categories
@apiobj.route('/v1.0/category/',methods=['GET'])
def allcategory():
    category=db.session.query(Category).all()
    if category==[]:
        data2ret={"status":False, "message":'No Category Found'}
    else:
        cats=[]
        for i in category:
            cat_info={}
            cat_info['id']=i.cat_id
            cat_info['category_name']=i.cat_name
            cats.append(cat_info)
        data2ret={"status":True, "message":cats}
    All_Category=jsonify(data2ret)
    return All_Category



## To add a product
@apiobj.route('/v1.0/addproduct/',methods=['POST'])
def add_product():
    productName=request.form.get('name')
    productRestaurant=request.form.get('rest')
    productDesc=request.form.get('describe')
    prodCategory=request.form.get('category')
    prodPrice=request.form.get('price')
    prodImage=request.files.get('image')
    allowed=['.jpeg','.jpg']
        
    if productName!=None and productRestaurant!=None and prodCategory!=None and prodPrice!=None and prodImage!=None:
            
        originalfilename=prodImage.filename
        name,extension=os.path.splitext(originalfilename)
        if extension in allowed:
            originalfile = "foodapp/user/static/rest_prod_imgs/"+str(productRestaurant)+originalfilename
            prodImage.save(originalfile)
            save2db=str(productRestaurant)+originalfilename
            try:
                product_to_add=Product(prod_name=productName, prod_description=productDesc, prod_rest=productRestaurant, prod_cat=prodCategory, prod_price=prodPrice, prod_image=save2db)
                    
                db.session.add(product_to_add)
                db.session.commit()
                    
                data2ret={"status":1, "message":"Product Successfully Added"}
            except:
                data2ret={"status":0, "message":"Product Not added. Try again"}
        else:
            data2ret={"status":0, "message":"Invalid picture format. Please upload a .jpg or .jpeg file."}
    else:
        data2ret={"status":0, "message":"Ensure all the required values are supplied"}
        
    return jsonify(data2ret)



## To update a product image
@apiobj.route('/v1.0/updateproductimage/<id>',methods=['POST'])
def update_product_image(id):
    update_product = db.session.query(Product).get(id)
    if update_product:
        data=request.form
        new_image=request.files.get('new_product_image',f"{update_product.prod_image}")
            
        product_restaurant=update_product.prod_rest
            
        allowed=['.jpeg','.jpg']
        if new_image:
            originalfilename=new_image.filename
            name,extension=os.path.splitext(originalfilename)
            if extension in allowed:
                originalfile = "foodapp/user/static/rest_prod_imgs/"+str(product_restaurant)+originalfilename
                new_image.save(originalfile)
                    
                try:
                    update_product.prod_image=str(product_restaurant)+originalfilename
                    db.session.commit()
                            
                    data2ret={"status":1, "message":"Product Updated Successfully"}
                except:
                    data2ret={"status":0, "message":"Product Update Failed. Try again"}
            else:
                data2ret={"status":0, "message":"Invalid picture format. Please upload a .jpg or .jpeg file."}
        else:
            data2ret={"status":0, "message":"Product not found"}
    return jsonify(data2ret)


## To update a product price
@apiobj.route('/v1.0/update/productprice/<id>',methods=['POST'])
def update_product_price(id):
    update_product = db.session.query(Product).get(id)
    if update_product:
        data=request.form
        new_price=data.get('new_product_price',f"{update_product.prod_price}")
        
        if new_price.isnumeric():
            try:
                update_product.prod_price=new_price
                db.session.commit()
                            
                data2ret={"status":1, "message":"Product Price Updated Successfully"}
            except:
                data2ret={"status":0, "message":"Price Not Updated. Try again"}
        else:
            data2ret={"status":0, "message":"Please enter a valid amount in figures"}
    else:
            data2ret={"status":0, "message":"Product not found"}
    return jsonify(data2ret)



## To update a product category
@apiobj.route('/v1.0/update_product_category/<id>',methods=['POST'])
def product_category_update(id):
    update_product = db.session.query(Product).get(id)
    if update_product:
        data=request.form
        new_category=data.get('new_product_category',f"{update_product.prod_cat}")
        
        if new_category.isnumeric():
            try:
                update_product.prod_cat=new_category
                db.session.commit()
                            
                data2ret={"status":1, "message":"Product Category Updated Successfully"}
            except:
                data2ret={"status":0, "message":"Category Not Updated. Try again"}
        else:
            data2ret={"status":0, "message":"Please enter a valid category figure"}
    else:
            data2ret={"status":0, "message":"Product not found"}
    return jsonify(data2ret)


## To update a product name
@apiobj.route('/v1.0/update-product/name/<id>',methods=['POST'])
def product_name_update(id):
    update_product = db.session.query(Product).get(id)
    if update_product:
        data=request.form
        new_name=data.get('new_product_name',f"{update_product.prod_name}")
        new_description=data.get('new_product_description',f"{update_product.prod_description}")
        
        if new_name:
            try:
                update_product.prod_name=new_name
                db.session.commit()
                            
                data2ret={"status":1, "message":"Product Name Updated Successfully"}
            except:
                data2ret={"status":0, "message":"Name Not Updated. Try again"}
        else:
            data2ret={"status":0, "message":"Failed! Ensure you have the right parameters sent"}
    else:
            data2ret={"status":0, "message":"Product not found"}
    return jsonify(data2ret)



## To update a product description
@apiobj.route('/v1.0/update/product/description/<id>',methods=['POST'])
def product_desc_update(id):
    update_product = db.session.query(Product).get(id)
    if update_product:
        data=request.form
        new_description=data.get('new_product_description',f"{update_product.prod_description}")
        
        if new_description:
            try:
                update_product.prod_description=new_description
                db.session.commit()
                data2ret={"status":1, "message":"Product Name Updated Successfully"}
            except:
                data2ret={"status":0, "message":"Name Not Updated. Try again"}
        else:
            data2ret={"status":0, "message":"Failed! Ensure you have the right parameters sent"}
    else:
            data2ret={"status":0, "message":"Product not found"}
    return jsonify(data2ret)