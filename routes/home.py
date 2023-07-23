from flask import Blueprint, redirect, render_template
from models.tables import db, Product


home_bp = Blueprint('home', __name__)


@home_bp.route('/<string:username>/home', methods=['GET', 'POST'])
def home(username):
    # Get all products from the "products" database
    products = Product.query.all()

    return render_template('home.html', products=products, username=username)
