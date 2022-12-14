from datetime import datetime,date

from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class Customer(db.Model):
    cust_id=db.Column(db.Integer(), primary_key=True, autoincrement=True)
    cust_firstname=db.Column(db.String(30), nullable=False)
    cust_lastname=db.Column(db.String(30), nullable=False)
    cust_phone=db.Column(db.String(15), nullable=False)
    cust_regdate=db.Column(db.Date(), nullable=False, default=date.today())
    cust_email=db.Column(db.String(80), nullable=False, unique=True)
    cust_pswd=db.Column(db.String(200),nullable=False)
    
    
class Restaurant(db.Model):
    rest_id=db.Column(db.Integer(), primary_key=True, autoincrement=True)
    rest_name=db.Column(db.String(255), nullable=False)
    rest_address=db.Column(db.Text(), nullable=False)
    rest_phone=db.Column(db.String(11), nullable=False, unique=True)
    rest_email=db.Column(db.String(200), nullable=False, unique=True)
    rest_about=db.Column(db.Text(500), nullable=False)
    rest_img=db.Column(db.String(80), nullable=False)
    rest_pswd=db.Column(db.String(200),nullable=False)
    account_number = db.Column(db.String(10), nullable=True)
    account_bank = db.Column(db.Integer(), db.ForeignKey('banks.bank_id'))
    account_name = db.Column(db.String(255), nullable=True)
    verify_account = db.Column(db.Enum("True","False"), nullable=False, default='False')
    rest_reg_date=db.Column(db.Date(), nullable=False, default=date.today())
    
        
class Admin(db.Model):
    admin_id=db.Column(db.Integer(), primary_key=True, autoincrement=True)
    admin_firstname=db.Column(db.String(30), nullable=False)
    admin_lastname=db.Column(db.String(30), nullable=False)
    admin_email=db.Column(db.String(80), nullable=False)
    admin_pswd=db.Column(db.String(200),nullable=False)

class Category(db.Model):
    cat_id=db.Column(db.Integer(), primary_key=True, autoincrement=True)
    cat_name=db.Column(db.String(50), nullable=False)
    
       
class Product(db.Model):
    prod_id=db.Column(db.Integer(), primary_key=True, autoincrement=True)
    prod_name=db.Column(db.String(50), nullable=False)
    prod_description=db.Column(db.Text(), nullable=False)
    prod_rest=db.Column(db.Integer(), db.ForeignKey('restaurant.rest_id')) #FK
    prod_cat=db.Column(db.Integer(), db.ForeignKey('category.cat_id')) #FK
    prod_price=db.Column(db.Float(), nullable=False)
    prod_image=db.Column(db.String(50), nullable=False)

    product_category=db.relationship("Category", backref="category_products")
    product_restaurant=db.relationship("Restaurant", backref="restaurant_products")
    
class Temporarycart(db.Model):
    temp_cart_id=db.Column(db.Integer(), primary_key=True, autoincrement=True)
    user_temp_id=db.Column(db.Integer(), nullable=False)
    product=db.Column(db.Integer(), db.ForeignKey('product.prod_id')) #FK
    product_qty=db.Column(db.Integer(), nullable=False)
    prod_restaurant=db.Column(db.Integer(), db.ForeignKey('restaurant.rest_id')) #FK
    amount=db.Column(db.Float(), nullable=False)
    temp_cart_date=db.Column(db.Date(), nullable=False)
    
    productinfo=db.relationship('Product',backref='prod_tempcart_deets')
    
    
class Order(db.Model):
    order_id=db.Column(db.Integer(), primary_key=True, autoincrement=True)
    buyer=db.Column(db.Integer(), db.ForeignKey('customer.cust_id'))#FK
    shipping_address=db.Column(db.Text(),nullable=False)
    ref_no=db.Column(db.String(30), nullable=False)
    order_date=db.Column(db.Date(), nullable=False, default=datetime.utcnow())
    order_status=db.Column(db.Enum('Completed', 'Pending', 'Dispatched', 'Declined','Failed'), nullable=False)
    order_amount=db.Column(db.Float(), nullable=False)
    payment_status=db.Column(db.Enum('Pending', 'Paid', 'Failed', 'Network Failed'), nullable=False)

    Order_cust_info=db.relationship('Customer',backref='cust_orders')
    
    
    
class Order_details(db.Model):
    details_id=db.Column(db.Integer(), primary_key=True, autoincrement=True)
    order_id=db.Column(db.Integer(), db.ForeignKey('order.order_id'))#FK
    prod_id=db.Column(db.Integer(), db.ForeignKey('product.prod_id'))#FK
    prod_qty=db.Column(db.Integer(), nullable=False)
    amount=db.Column(db.Float(), nullable=False)
    restaurant=db.Column(db.Integer(), db.ForeignKey('restaurant.rest_id')) #FK
    delivery_status=db.Column(db.Enum('Pending','Declined','Dispatched','Success', 'Failed'), nullable=False)
    payment_status=db.Column(db.Enum('Pending', 'Paid', 'Failed'), nullable=False)
    
    Ord_details_prod_info=db.relationship('Product',backref='orderdetails_deets')
    Order_info=db.relationship('Order',backref='orderdetails_info')
    Order_rest_info=db.relationship('Restaurant',backref='rest_order_info')
   
class Payment(db.Model):
    pay_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    pay_orderid =db.Column(db.Integer(), db.ForeignKey('order.order_id'))#FK
    pay_amt=db.Column(db.Float(), nullable=False)
    pay_ref = db.Column(db.String(30), nullable=False, unique=True)
    pay_date = db.Column(db.DateTime(), default=datetime.now())
    pay_status = db.Column(db.Enum('Paid', 'Pending', 'Failed'), nullable=True, default='Pending')
    pay_feedback = db.Column(db.Text(), nullable=True)
    
    
class Banks(db.Model):
    bank_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    fwave_bank_id= db.Column(db.Integer(), nullable=False, unique=True)
    bank_code = db.Column(db.String(10), nullable=False, unique=True)
    bank_name = db.Column(db.String(50), nullable=False)