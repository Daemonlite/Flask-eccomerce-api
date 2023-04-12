
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
    carts = db.relationship('Cart', backref='user', lazy=True)
    products = db.relationship('Product', backref='user', lazy=True)
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
            'profile': self.profile,
            'carts': [cart.to_dict() for cart in self.carts],
            'products': [product.to_dict() for product in self.products],
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    descr = db.Column(db.String(400), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    image1 = db.Column(db.String(255))
    image2 = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Updated foreign key
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, product_name, descr, quantity, price, category, image1, image2, user_id):
        self.product_name = product_name
        self.descr = descr
        self.quantity = quantity
        self.price = price
        self.category = category
        self.image1 = image1
        self.image2 = image2
        self.user_id = user_id
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_name': self.product_name,
            'descr': self.descr,
            'quantity': self.quantity,
            'price': self.price,
            'category': self.category,
            'image1': self.image1,
            'image2': self.image2,
            'user_id': self.user_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
# Cart class
class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descr = db.Column(db.String(400), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    image1 = db.Column(db.String(255))
    image2 = db.Column(db.String(255))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product = db.relationship('Product', backref=db.backref('cart', lazy=True))
    user = db.relationship('User', backref=db.backref('user_carts', lazy=True))  # Update backref name to 'user_carts'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, descr, quantity, price, category, image1, image2, product_id, user_id):
        self.descr = descr
        self.quantity = quantity
        self.price = price
        self.category = category
        self.image1 = image1
        self.image2 = image2
        self.product_id = product_id
        self.user_id = user_id

    def to_dict(self):
        return {
            'id': self.id,
            'descr': self.descr,
            'quantity': self.quantity,
            'price': self.price,
            'category': self.category,
            'image1': self.image1,
            'image2': self.image2,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


