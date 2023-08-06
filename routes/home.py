from flask import Blueprint, redirect, render_template, session, request
from models.tables import Product, Category, Cart


home_bp = Blueprint('home', __name__)


def get_category(categories, id):
    for i in categories:
        if id == i.id:
            return i


@home_bp.route('/<string:name>/home', methods=['GET', 'POST'])
def home(name):
    categories = Category.query.all()
    cart = Cart.query.all()

    cart_map = {}

    for i in cart:
        cart_map[i.product_id] = i.quantity

    category_map = {}

    session['query'] = request.args.get('search_query')

    if session['query']:
        products = Product.query.filter(
            Product.name.ilike(f'%{session["query"]}%')).all()
    else:
        session['query'] = ''
        products = Product.query.all()

    return render_template('home.html', products=products, username=username)
