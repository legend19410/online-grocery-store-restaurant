from .. import db, encrypter
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash

class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45), nullable=False)
    last_name = db.Column(db.String(45), nullable=False)
    telephone = db.Column(db.String(11), nullable=False)
    email = db.Column(db.String(45), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    town = db.Column(db.String(45), nullable=False)
    parish = db.Column(db.String(45), nullable=False)

    orders = db.relationship('Order', backref='customer', cascade="all,delete")

    #cart associated many to many
    cart_items = db.relationship("Cart", back_populates="customer_carts", cascade="all,delete")

    #ratings associated many to many
    grocery_ratings = db.relationship("Rating", back_populates="customer_ratings", cascade="all,delete")

    def __init__(self, first_name, last_name, telephone, email, password, town, parish):
        self.first_name = encrypter.encrypt(first_name)
        self.last_name = encrypter.encrypt(last_name)
        self.telephone = encrypter.encrypt(telephone)
        self.email = encrypter.encrypt(email)
        self.password = generate_password_hash(password, method='pbkdf2:sha256:310000', salt_length=256)
        self.town = encrypter.encrypt(town)
        self.parish = encrypter.encrypt(parish)
        

class Employee(db.Model):
    __tablename__ = 'employee'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45), nullable=False)
    last_name = db.Column(db.String(45), nullable=False)
    telephone = db.Column(db.String(11), nullable=False)
    email = db.Column(db.String(45), nullable=False, unique=True)
    password = db.Column(db.String(45), nullable=False)
    street = db.Column(db.String(200), nullable=False)
    town = db.Column(db.String(200), nullable=False)
    parish = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    salary = db.Column(db.Numeric(10,2), nullable=True)

    # represent the payment collected an employee (many to one relationship)
    payments_collected = db.relationship('Payment', backref='employee', cascade="all,delete")
    checkouts = db.relationship('Order', backref='employee', cascade="all,delete")

    def __init__(self, first_name, last_name, telephone, email, password, street, town, parish, role, salary):
        self.first_name = encrypter.encrypt(first_name)
        self.last_name = encrypter.encrypt(last_name)
        self.telephone = encrypter.encrypt(telephone)
        self.email = encrypter.encrypt(email)
        self.password = generate_password_hash(password, method='pbkdf2:sha256:310000', salt_length=256)
        self.town = encrypter.encrypt(town)
        self.town = encrypter.encrypt(town)
        self.parish = encrypter.encrypt(parish)
        self.role = encrypter.encrypt(role)
        self.salary = salary

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    orderdate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.Enum(encrypter.encrypt('canceled'),encrypter.encrypt('served'),\
                        encrypter.encrypt('checked out'),encrypter.encrypt('pending'), name='OrderStatus'))
    deliverydate = db.Column(db.DateTime)    
    deliverystreet = db.Column(db.String(100))
    deliverytown = db.Column(db.String(100))
    deliveryparish = db.Column(db.String(100),db.ForeignKey('delivery_parish.parish'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)

    # represents the many-to-many relationship between  orders and groceries
    groceries = db.relationship("OrderGroceries", back_populates="orders", cascade="all,delete")

    # represents a one-to-one relationship between payment and order
    payment = db.relationship('Payment', backref=db.backref('orders', uselist=False), cascade="all,delete")

    # represents a one to many-to-many relationship between employee and orders
    checkout_by = db.Column(db.Integer, db.ForeignKey('employee.id'))

    def __init__(self, customer_id):
        self.customer_id = customer_id
    


class Grocery(db.Model):
    __tablename__ = 'grocery'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(1000), nullable=False)# unique=True)
    quantity = db.Column(db.Integer, nullable=False)
    units = db.Column(db.String(100), nullable=False)
    cost_per_unit = db.Column(db.Numeric(10,2), nullable=False)
    grams_per_unit = db.Column(db.Numeric(10,2), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    photo = db.Column(db.String(100), default='grocery.jpg')
    sku = db.Column(db.String(50), nullable=True)

    #order associated many to many
    orders = db.relationship("OrderGroceries", back_populates="groceries", cascade="all,delete")

    #cart associated many to many
    customer_carts = db.relationship("Cart", back_populates="cart_items", cascade = "all,delete")

    #ratings associated many to many
    customer_ratings = db.relationship("Rating", back_populates="grocery_ratings", cascade="all,delete")

    taxes = db.relationship("Taxes_on_goods", back_populates="grocery", cascade="all,delete")

    def __init__(self, name, description, quantity, units, cost_per_unit, grams_per_unit, category, photo, sku):
        self.name = name
        self.description = description
        self.quantity = quantity
        self.units = units
        self.cost_per_unit = cost_per_unit
        self.category = category
        self.photo = photo
        self.sku = encrypter.encrypt(sku)
        


class OrderGroceries(db.Model):
    __tablename__ = 'order_groceries'
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), primary_key=True)
    grocery_id = db.Column(db.Integer, db.ForeignKey('grocery.id'), primary_key=True)
    quantity = db.Column(db.Integer)

    orders = db.relationship("Order", back_populates="groceries")
    groceries = db.relationship("Grocery", back_populates="orders")

class Cart(db.Model):
    __tablename__ = 'cart'
    cart_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('grocery.id'), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    
    cart_items = db.relationship("Grocery", back_populates="customer_carts")
    customer_carts = db.relationship("Customer", back_populates="cart_items")

class Rating(db.Model):
    __tablename__ = 'rating'
    cust_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('grocery.id'), primary_key=True)
    rating = db.Column(db.Integer, nullable=False)

    grocery_ratings = db.relationship("Grocery", back_populates="customer_ratings")
    customer_ratings = db.relationship("Customer", back_populates="grocery_ratings")

class Payment(db.Model):
    __tablename__ = 'payment'
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), primary_key=True)
    recorded_by = db.Column(db.Integer, db.ForeignKey('employee.id'))
    payment_date = db.Column(db.DateTime(),default=datetime.utcnow)
    amount_tendered = db.Column(db.Numeric(10,2), nullable=False)
    change = db.Column(db.Numeric(10,2), nullable=True)

class DeliveryParish(db.Model):
    parish = db.Column(db.String(45), primary_key=True)
    delivery_rate = db.Column(db.Numeric(10,2), nullable=False)

    
class Taxes(db.Model):
    tax = db.Column(db.String(50), nullable=False, primary_key=True)
    rate = db.Column(db.Numeric(10,2), nullable=False)

    groceries = db.relationship("Taxes_on_goods", back_populates="tax_type", cascade="all,delete")

class Taxes_on_goods(db.Model):
    tax = db.Column(db.String, db.ForeignKey('taxes.tax'), primary_key=True)
    grocery_id = db.Column(db.Integer, db.ForeignKey('grocery.id'), primary_key=True)

    grocery = db.relationship("Grocery", back_populates="taxes")
    tax_type = db.relationship("Taxes", back_populates="groceries")