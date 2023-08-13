from flask import Blueprint, render_template, request
from models.tables import Order, User, Product, db, OrderItem, Address

pending_orders_bp = Blueprint('pending_orders', __name__)


@pending_orders_bp.route('/pending_orders', methods=['GET', 'POST'])
def pending_orders():
    # Fetch all pending orders from the database
    pending_orders = Order.query.all()

    address_map = {}

    # Fetch additional data needed for displaying orders
    for order in pending_orders:
        order.user = User.query.get(order.user_id)
        order_items = OrderItem.query.filter_by(order_id=order.id).all()
        order.order_items = []
        address = Address.query.filter_by(id=order.selected_address_id).first()
        address_map[order.selected_address_id] = address.house_no + ' ' + \
            address.landmark + ' ' + address.city + ' ' + \
            address.state + ' ' + address.zip_code

        for item in order_items:
            product = Product.query.get(item.product_id)
            order.order_items.append(
                (product, item.quantity, item.price_per_unit))

    if request.method == 'POST':
        for order in pending_orders:
            status = request.form.get('status_' + str(order.id))
            order.status = status
            db.session.commit()

    return render_template('pending_orders.html', orders=pending_orders, address_map=address_map)
