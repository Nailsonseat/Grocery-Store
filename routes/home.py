from flask import Blueprint, redirect, render_template, session, request
from models.tables import Product, Category, Cart
from datetime import datetime

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

    # Apply filters
    filter_category = request.args.get('filter_category')
    filter_max_price = request.args.get('filter_max_price')
    filter_min_price = request.args.get('filter_min_price')
    filter_mfd_over = request.args.get('filter_mfd_over')
    filter_expire_below = request.args.get('filter_expire_below')

    if filter_category:
        products = [
            product for product in products if product.category_id == int(filter_category)]

    if filter_max_price:
        products = [product for product in products if product.rate_per_unit <= float(
            filter_max_price)]

    if filter_min_price:
        products = [product for product in products if product.rate_per_unit >= float(
            filter_min_price)]

    if filter_mfd_over:
        products = [
            product for product in products if product.manufacture_date and product.manufacture_date >= datetime.strptime(filter_mfd_over, "%Y-%m-%d").date()]

    if filter_expire_below:
        products = [
            product for product in products if product.expiry_date and product.expiry_date < datetime.strptime(filter_expire_below, "%Y-%m-%d").date()]

    for product in products:
        if get_category(categories, product.category_id) in category_map:
            category_map[get_category(
                categories, product.category_id)].append(product)
        else:
            category_map[get_category(categories, product.category_id)] = [
                product]

    return render_template('home.html', category_map=category_map, cart_map=cart_map, name=name, query=session['query'])
