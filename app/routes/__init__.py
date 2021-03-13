from app import app
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask import session

"""import blueprints (routes) for different sections of the system"""
from .CustomerRoute import manage_customer_account
from .EmployeeRoute import manage_employee_account
from .GroceryRoute import manage_groceries
from .CartRoute import manage_cart


"""register blueprints"""
app.register_blueprint(manage_customer_account, url_prefix="/manage_customer_account")
app.register_blueprint(manage_employee_account, url_prefix="/manage_employee_account")
app.register_blueprint(manage_groceries, url_prefix="/manage_groceries")
app.register_blueprint(manage_cart, url_prefix="/manage_cart")


"""serves the index page for customers"""
@app.route('/')
@app.route('/index')
def index():
    # if customer is logged in return home page with customer data. Otherwise, return just the home page
    if 'cust_id' in session:
        user_data = session['cust_id']
        return render_template("customerViews/home.html", user=user_data)
    else:
        return render_template("customerViews/index.html")

