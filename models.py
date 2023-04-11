
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
from datetime import datetime  # Import datetime for handling timestamps

from datetime import datetime
# Create an instance of SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    profile = db.Column(db.String(255))
    cart = db.relationship('Cart',backref=db.backref('user', lazy=True))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, name, email, password, profile):
        self.name = name
        self.email = email
        self.password = password
        self.profile = profile

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'password': self.password,
            'profile': self.profile,
            'cart': [cart.to_dict() for cart in self.cart],
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

class Product(db.model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    descr = db.Column(db.String(400),nullable=False)
    quantity = db.column(db.Integer,primary_key=True)
    price = db.column(db.Integer,primar_key = True)
    category = db.Column(db.String(100), nullable=False)
    image1 = db.Column(db.String(255))
    image2 = db.Column(db.String(255))
    user_id = db.column(db.String(255))
    user = db.relationship('User', backref=db.backref('products', lazy=True))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self,product_name,descr,quantity,price,category,image1,image2):
        self.product_name = product_name
        self.descr = descr
        self.quantity = quantity
        self.price = price
        self.category = category
        self.image1 = image1
        self.image2 = image2
    
    def to_dict(self):
        return {
            'id':self.id,
            'descr':self.descr,
            'quantity':self.quantity,
            'price':self.price,
            'category':self.category,
            'image1':self.image1,
            'image2':self.image2,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
class Cart(db.model):
    id = db.Column(db.Integer, primary_key=True)
    descr = db.Column(db.String(400),nullable=False)
    quantity = db.column(db.Integer,primary_key=True)
    price = db.column(db.Integer,primar_key = True)
    category = db.Column(db.String(100), nullable=False)
    image1 = db.Column(db.String(255))
    image2 = db.Column(db.String(255))
    product = db.relationship('Product',backref=db.backref('cart', lazy=True))
    user = db.relationship('User',backref=db.backref('cart', lazy=True))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self,product_name,descr,quantity,price,category,image1,image2):
        self.product_name = product_name
        self.descr = descr
        self.quantity = quantity
        self.price = price
        self.category = category
        self.image1 = image1
        self.image2 = image2

    def to_dict(self):
        return {
            'id':self.id,
            'descr':self.descr,
            'quantity':self.quantity,
            'price':self.price,
            'category':self.category,
            'image1':self.image1,
            'image2':self.image2,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
