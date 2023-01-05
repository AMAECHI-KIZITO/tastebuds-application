import os,re
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

## vendor Reg Restaurant Form
@vendorobj.route("/register-business/", methods=['POST'])
def registerRestaurant():
    if session.get('vendor_id')!=None and session.get('vendor_name')!=None:
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
                    valid_mail=re.search("^\D",ResEmail)
                    if valid_mail:
                        originalfilename=ResImage.filename
                        name,extension=os.path.splitext(originalfilename)
                        if extension in allowed:
                            originalfile = "foodapp/user/static/rest_imgs/"+originalfilename
                            ResImage.save(originalfile)
                            securepassword=generate_password_hash('0000')
                            try:
                                reg=Restaurant(rest_name=ResName, rest_address=ResAddress, rest_phone=ResPhone, rest_email=ResEmail, rest_about=ResAbout, rest_img=originalfilename, rest_pswd=securepassword)
                                db.session.add(reg)
                                db.session.commit()
                                
                                # Send verification email
                                token = s.dumps(ResEmail, salt='email-confirm')
                                email_link = url_for('confirm_email', token=token, _external=True)
                                
                                msg = Message("Confirm Email", sender=('TasteBuds', 'ccmarketsgroup@gmail.com'), recipients=[ResEmail])
    
                                msg.body = f"Hello Taste Buddy,\n\nThank you for signing up to TasteBuds. We are pleased to have you onboard as a vendor. To confirm your email address click here {email_link}\n\nIf you do not recognize this email please ignore.\n\nKeep Debugging,\nThe Debugger Team."
                                    
                                foodapp.mail.send(msg)
                                flash("A verification mail has been sent to your email.", category="Good_rest_reg")
                                return redirect("/vendor/create-account/")
                            except:
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
    else:
        return redirect("/vendor/login/")