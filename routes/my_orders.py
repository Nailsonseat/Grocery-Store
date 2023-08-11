from flask import Blueprint, render_template, session
from models.tables import Order, OrderItem, Product

my_orders_bp = Blueprint('my_orders', __name__)


@my_orders_bp.route('/my_orders', methods=['GET'])
def my_orders():
    user_id = session.get('user_id')
    orders = Order.query.filter_by(user_id=user_id).order_by(
        Order.order_date.desc()).all()

    for order in orders:
        order.items = OrderItem.query.filter_by(order_id=order.id).all()

    products = Product.query.all()
    product_map = {}

    for i in products:
        product_map[i.id] = i

    return render_template('my_orders.html', orders=orders, product_map=product_map)
