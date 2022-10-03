import os,re
from flask import render_template,request,flash,abort,make_response,redirect,session
from . import adminobj
from foodapp.models import *

## Admin Login Template
@adminobj.route('/login/')
def adminlogin():
    return render_template("adminlogin.html")

## Admin Homepage
@adminobj.route('/homepage/')
def adminhome():
    if session.get('admin_id')!=None and session.get('admin_name')!=None:
        return render_template("adminhome.html")
    else:
        return redirect("/admin/login/")

## Admin Login Verify
@adminobj.route("/adminverifylogin/", methods=["POST"])
def verifylogin():
    admin_e_mail=request.form.get("email")
    admin_pskey=request.form.get("password")
    
    if admin_e_mail!="" and admin_pskey!="":
        admin_info=db.session.query(Admin).filter(Admin.admin_email==admin_e_mail, Admin.admin_pswd==admin_pskey).first()
        if admin_info:
            session['admin_id']=admin_info.admin_id
            session['admin_name']=admin_info.admin_firstname
            return redirect("/admin/homepage/")
        else:
            flash('Details Incorrect', category='WrongDetails')
            return redirect("/admin/login/")
    else:
        flash('Kindly fill out all fields', category='WrongDetails')
        return redirect("/admin/login/")
    
# Admin Logout Process
@adminobj.route("/logout/")
def adminlogout():
    session.pop('admin_id', None)
    session.pop('admin_name',None)
    return redirect('/admin/login/')

@adminobj.after_request
def clearcache(response):
    response.headers['Cache-Control']="no-cache, no store, must-revalidate"
    return response

## Admin Reg Restaurant
@adminobj.route("/register/restaurant/")
def newrestaurant():
    if session.get('admin_id')!=None and session.get('admin_name')!=None:
        return render_template('new_restaurant.html')
    else:
        return redirect("/admin/login/")
    
## Admin Reg Restaurant Form
@adminobj.route("/restaurant/registration/", methods=['POST'])
def registerRestaurant():
    if session.get('admin_id')!=None and session.get('admin_name')!=None:
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
                            try:
                                reg=Restaurant(rest_name=ResName, rest_address=ResAddress, rest_phone=ResPhone, rest_email=ResEmail, rest_about=ResAbout, rest_img=originalfilename)
                                db.session.add(reg)
                                db.session.commit()
                                flash("Registration Successful", category="Good_rest_reg")
                                return redirect("/admin/register/restaurant/")
                            except:
                                flash("Registration Failed. The email or phone number might already exist.", category="bad_rest_reg")
                            return redirect("/admin/register/restaurant/")
                        else:
                            flash("Invalid picture format. Please upload a .jpg or .jpeg file.", category="bad_rest_reg")
                            return redirect("/admin/register/restaurant/")
                    else:
                        flash("Invalid email format. Email cannot start with digit", category="bad_rest_reg")
                        return redirect("/admin/register/restaurant/")
                else:
                    flash("Phone Number Invalid. Please provide a Nigerian mobile number", category="bad_rest_reg")
                    return redirect("/admin/register/restaurant/")
            else:
                flash('Invalid Phone Number', category="bad_rest_reg")
                return redirect("/admin/register/restaurant/")
        else:
            flash('Kindly fill out all fields', category="bad_rest_reg")
            return redirect("/admin/register/restaurant/")
    else:
        return redirect("/admin/login/")
