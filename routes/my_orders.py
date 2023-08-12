from flask import Blueprint, render_template, session
from models.tables import Order, OrderItem, Product, Address

my_orders_bp = Blueprint('my_orders', __name__)


@my_orders_bp.route('/my_orders', methods=['GET'])
def my_orders():
    user_id = session.get('user_id')
    orders = Order.query.filter_by(user_id=user_id).order_by(
        Order.order_date).all()

    address_map = {}

    for order in orders:
        order.items = OrderItem.query.filter_by(order_id=order.id).all()
        address = Address.query.filter_by(id=order.selected_address_id).first()
        address_map[order.selected_address_id] = address.house_no + ' ' + \
            address.landmark + ' ' + address.city + ' ' + \
            address.state + ' ' + address.zip_code

    products = Product.query.all()
    product_map = {}

    for i in products:
        product_map[i.id] = i

    return render_template('my_orders.html', orders=orders, product_map=product_map, address_map=address_map)
