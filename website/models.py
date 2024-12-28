from . import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash # this whole package comes with flask-login module

class Customer(db.Model,UserMixin): # db.model is a db and usermixin will allow for user authetication
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100))
    password_hash = db.Column(db.String(150))
    date_joined = db.Column(db.DateTime(), default=datetime.utcnow)

    cart_items = db.relationship('Cart', backref=db.backref('customer', lazy=True))
    orders = db.relationship('Order', backref=db.backref('customer', lazy=True))


    # Since our password attribute was private therefor using property decorators to set it
    @property
    def password(self):
        raise AttributeError ("Password is not a readable attribute")


    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password=password)
    def verify_password(self,password):
        return check_password_hash(self.password_hash,password=password)

    def __str__(self): # to return a readable form of our class
        return '<Customer %r>' % Customer.id



class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(20),nullable=False)
    current_price = db.Column(db.Float, nullable=False)
    previous_price = db.Column(db.String, nullable=False)
    in_stock = db.Column(db.Integer, nullable=False)
    product_picture = db.Column(db.String(1000), nullable=False)
    flash_sale=db.Column(db.Integer, default=False)
    date_added = db.Column(db.DateTime(), default=datetime.utcnow())

    def __str__(self):
        return '<Product %r>' % self.product_name

    carts = db.relationship('Cart', backref=db.backref('product', lazy=True))
    orders = db.relationship('Order', backref=db.backref('product', lazy=True))


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)

    customer_link = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    product_link = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)



    # customer product

    def __str__(self):
        return '<Cart %r>' % self.id






class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(100), nullable=False)
    payment_id = db.Column(db.String(1000), nullable=False)

    customer_link = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    product_link = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)



    def __str__(self):
        return '<Order %r>' % self.id



