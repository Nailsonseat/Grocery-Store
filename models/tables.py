# models.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __bind_key__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    mobile_number = db.Column(db.String(15))
    dob = db.Column(db.Date)
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)


class Coupon(db.Model):
    __bind_key__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    min_purchase = db.Column(db.Integer, nullable=False)


class CartItem(db.Model):
    __bind_key__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)


class WishlistItem(db.Model):
    __bind_key__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)


class Category(db.Model):
    __bind_key__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    image_filename = db.Column(db.String(200))


class Product(db.Model):
    __bind_key__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey(
        'category.id'), nullable=False)
    manufacture_date = db.Column(db.Date)
    expiry_date = db.Column(db.Date)
    rate_per_unit = db.Column(db.Float, nullable=False)
    image_filename = db.Column(db.String(255))


class Address(db.Model):
    __bind_key__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    house_no = db.Column(db.String(100))
    landmark = db.Column(db.String(100))
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    zip_code = db.Column(db.String(20), nullable=False)
