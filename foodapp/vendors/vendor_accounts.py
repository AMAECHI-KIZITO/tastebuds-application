import os,re, random
from flask import render_template,request,flash, redirect, session, jsonify, url_for
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
from werkzeug.security import generate_password_hash, check_password_hash
from . import vendorobj
import foodapp
from foodapp.models import * 

s=URLSafeTimedSerializer('sscewykdfsFbsxnfhqhv')

# Vendor Creation of Account
@vendorobj.route("/create-account/")
def vendor_create_account():
    return render_template("vendor-create-account.html")

# Vendor Check Phone Number Availability
@vendorobj.route("/check-phone-availability/")
def check_phone_number_availability():
    phone = request.args.get('phoneNumber')
    if phone is not None:
        result = Restaurant.query.filter(Restaurant.rest_phone == phone).first()
        if result is not None:
            return "Number Already Registered"
        return "Number Available"



# Vendor Check Email Availability
@vendorobj.route("/check-email-availability/")
def check_email_availability():
    email = request.args.get('email')
    if email is not None:
        result = Restaurant.query.filter(Restaurant.rest_email == email).first()
        if result is not None:
            return "Email Already Registered"
        return "Email Available"



# Mail testing
def send_vendor_mail(ResEmail, create_auto_password, email_link):
    msg = Message("Confirm Email", sender=('TasteBuds', 'konkakira1960@gmail.com'), recipients=[ResEmail])
    
    msg.body = f"Hello Taste Buddy,\n\nWelcome to the family! Thank you for signing up to TasteBuds. We are pleased to have you onboard as a vendor.\n\nYour login details is as follows:\n\nEmail: {ResEmail}\nPassword: {create_auto_password}.\nYou are encouraged to change this password upon successful login.\n\nTo confirm your email address click here {email_link}\n\nIf you do not recognize this email please ignore.\n\nKeep Selling,\nAmaechi from TasteBuds."
    foodapp.mail.send(msg)
    
    return 'mailsent'



## vendor Reg Restaurant Form
@vendorobj.route("/register-business/", methods=['POST'])
def registerRestaurant():
    allowed=['.jpeg','.jpg']
    ResName=request.form.get('restaurantName')
    ResPhone=request.form.get('restaurantPhone')
    ResAddress=request.form.get('restaurantAddress')
    ResImage=request.files.get('restaurantPic')
    ResEmail=request.form.get('restaurantEmail')
    ResAbout=request.form.get('restaurantAbout')
        
    if ResName!="" and ResPhone!="" and ResAddress!="" and ResImage!="" and ResEmail!="" and ResAbout!="":
        if len(ResPhone)==11 and ResPhone.isnumeric():
            valid_phone=re.findall("^(080)|^(081)|^(070)|^(090)",ResPhone)
            if valid_phone:
                regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
                valid_mail=re.search(regex, ResEmail)
                if valid_mail:
                    originalfilename=ResImage.filename
                    name,extension=os.path.splitext(originalfilename)
                    if extension in allowed:
                        originalfile = "foodapp/user/static/rest_imgs/"+originalfilename
                        ResImage.save(originalfile)
                        create_auto_password = str(int(random.random() * 5142825))
                        securepassword=generate_password_hash(create_auto_password)
                        
                        try:
                            reg=Restaurant(rest_name=ResName, rest_address=ResAddress, rest_phone=ResPhone, rest_email=ResEmail, rest_about=ResAbout, rest_img=originalfilename, rest_pswd=securepassword)
                            db.session.add(reg)
                            db.session.commit()
                                
                            # Send verification email
                            token = s.dumps(ResEmail, salt='email-confirm')
                            email_link = url_for('bpvendor.confirm_email', token=token, _external=True)
                            send_vendor_mail(ResEmail, create_auto_password, email_link)  
                            
                            flash("A verification mail has been sent to your email.", category="Good_rest_reg")
                            return redirect("/vendor/create-account/")
                        except:
                            db.session.rollback()
                            flash("Registration Failed. The email or phone number might already exist.", category="bad_rest_reg")
                            return redirect("/vendor/create-account/")
                    else:
                        flash("Invalid picture format. Please upload a .jpg or .jpeg file.", category="bad_rest_reg")
                        return redirect("/vendor/create-account/")
                else:
                    flash("Invalid email format. Email cannot start with digit", category="bad_rest_reg")
                    return redirect("/vendor/create-account/")
            else:
                flash("Phone Number Invalid. Please provide a Nigerian mobile number", category="bad_rest_reg")
                return redirect("/vendor/create-account/")
        else:
            flash('Invalid Phone Number', category="bad_rest_reg")
            return redirect("/vendor/create-account/")
    else:
        flash('Kindly fill out all fields', category="bad_rest_reg")
        return redirect("/vendor/create-account/")
    
    
# confirm email
@vendorobj.route('/confirm-email/<token>')
def confirm_email(token):
    try:
        email=s.loads(token, salt='email-confirm', max_age=300)
        checking_email=db.session.query(Restaurant).filter(Restaurant.rest_email==email).first()
        if checking_email:
            checking_email.verify_account='True'
            db.session.commit()
            return redirect('/vendor/login/')
    except SignatureExpired:
        return 'token expired'
    except BadTimeSignature:
        return 'invalid token'