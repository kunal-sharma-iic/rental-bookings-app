from flask import render_template, request, redirect, session, send_file, Response 
from flask import Flask
from flask_login import login_required, current_user, logout_user, login_user
from app.forms import SignupForm, LoginForm
from app.models import Users,Vehicles , Encoder , Customers , Rentals
from flask import *
from sqlalchemy import select , create_engine
from app import app
from app import db
import json
import collections
import psycopg2
import pandas as pd
from sqlalchemy.sql import select
from app.controller import inventory_update , check_inventory , DateTimeEncoder



engine = create_engine('mysql://rentals:bookings@localhost/rentals')
@app.before_first_request  # read
def create_all():
    db.create_all()

"""route for home page"""

@app.route('/home' , methods = ['GET','POST'])
@login_required
def home():

    return render_template('home.html')

"""route for adding customers"""

@app.route('/add_custom' , methods = ['GET' , 'POST'])
@login_required
def add_detail():

    if request.method == 'POST':      
        name = request.form.get("name")
        phone = request.form.get("phone")
        email = request.form.get("email")
        entry = Customers(cust_name = name , user_id = current_user.id, cust_ph_no = phone , cust_email = email)
        db.session.add(entry)
        db.session.commit()
        msg = "Customer Added Successfully! Goto Home for View!"
        status = 1

        return render_template('add_cust.html' , msg = msg , status = status)

    return render_template('add_cust.html')

"""route for viewing customers"""

@app.route('/view_custom',methods = ['GET','POST'])
@login_required
def view_detail():

    json_data = []
    conn = engine.connect()
    s = select(Customers.cust_name , Customers.cust_ph_no , Customers.cust_email)
    result = conn.execute(s)
    for row in result:
            name = row.cust_name
            email = row.cust_email
            id = select(Customers.user_id).where(Customers.cust_email == email)
            for j in conn.execute(id):
                id = j.user_id
                emp_name = select(Users).where(Users.id == id)
                for k in conn.execute(emp_name):
                    emp_name = k.username
            phn = row.cust_ph_no
            data = {"Name":name , "Phone Number":phn , "Email":email , "Added_by_Employee":emp_name}
            json_data.append(data)
    json_data = json.dumps(json_data, indent = 4) 
    df = pd.read_json(json_data)

    return render_template('view_custm.html',table=(df.to_html(classes="table center table-striped table-hover col-md-6")))

"""route for adding bookings"""

@app.route('/add_rent_book' , methods=['GET','POST'])
@login_required
def add_rent_book():

    c_name = []
    v_type = []
    conn = engine.connect()
    cust_name = select(Customers.cust_name)

    for name in conn.execute(cust_name):
        c_name.append(name.cust_name)
    veh_type = select(Vehicles. vehicle_type)

    for type in conn.execute(veh_type):
        v_type.append(type.vehicle_type)

    if request.method == 'POST':
        cust_name_p = request.form.get("option1")
        rent_date = request.form.get("rental_date")
        retn_date = request.form.get("return_date")
        veh_type_p = request.form.get("option2")
        entry = Rentals(cust_name = cust_name_p ,user_id = current_user.id, rental_date = rent_date , return_date = retn_date , veh_type = veh_type_p)

        check = check_inventory(veh_type_p)

        if check == None:
            db.session.add(entry)
            db.session.commit()
            status = 1
            inventory_update(veh_type_p)
            msg = "Rentals Details Added Succesfully and Inventory Updated !! Goto Home for View!"
            return render_template('add_rent.html' , msg = msg , status = status)

        else:
            inventory_update(veh_type_p)
            status =1
            return render_template('add_rent.html' , msg = check , status =1)

    return render_template('add_rent.html' , v_type = v_type , c_name = c_name)

"""route for viewing existing bookings"""

@app.route('/view_rent',methods = ['GET','POST'])
@login_required
def view_rent_detail():

    json_data = []
    conn = engine.connect()
    s = select(Rentals.cust_name , Rentals.rental_date , Rentals.return_date ,Rentals.veh_type)
    result = conn.execute(s)

    for row in result:
            name = row.cust_name
            date_rent= row.rental_date
            date_return= row.return_date
            type_v = row.veh_type  
            data = {"Name":name , "Rental Date":date_rent , "Return Date": date_return , "Vehicle Type":type_v}
            json_data.append(data)

    json_data = json.dumps(json_data, indent = 4 , cls=DateTimeEncoder) 
    df = pd.read_json(json_data)


    return render_template('view_rent.html',table=(df.to_html(classes="table center table-striped table-hover col-md-6")))

"""route for viewing Inventory Data"""

@app.route('/inventory' , methods = ['GET' , 'POST'])
@login_required
def get_inventory():

    json_data = []
    conn = engine.connect()
    query = select(Vehicles.vehicle_type , Vehicles.count_vechicle , Vehicles.vehicle_id)

    for i in conn.execute(query):       
        type_i = i.vehicle_type
        count = i.count_vechicle
        id = i.vehicle_id
        data = {"Type":type_i , "Total No. Available":count , "ID":id}
        json_data.append(data)

    json_data = json.dumps(json_data , indent=4)
    df = pd.read_json(json_data)


    return render_template('view_inventory.html' , table=(df.to_html(classes="table center table-striped table-hover col-md-6")))

"""route for login page"""

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()

    if current_user.is_authenticated:
        return redirect('/home')

    if form.validate_on_submit():

        user = Users.query.filter_by(email=form.email.data).first()

        if user:
            if user.password == form.password.data:
                login_user(user)
                return redirect('/home')

        return flash('Incorrect username / password !', 'danger')

    return render_template('login1.html', form=form)

"""route for signup page"""

@app.route('/signup', methods=['GET', 'POST'])
def signup():

    form = SignupForm()

    if current_user.is_authenticated:
        return redirect('/home')
    if form.validate_on_submit():
        # returns the first user it gets from db and returns none if no user is found
        if Users.query.filter_by(email=form.email.data).first() != None:
            flash("Email is already present, please login")
        else:
            user = Users(email=form.email.data,
                         username=form.username.data,
                         password=form.password.data)
            db.session.add(user)
            db.session.commit()
            return redirect('/login')

    return render_template('signup1.html', form=form)

"""route for logout page"""

@app.route('/logout')
@login_required
def logout():

    session.pop('_id')
    flash("Successfully logged out!")
    logout_user()
    return redirect('/login')

