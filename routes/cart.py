from flask import Blueprint, redirect, url_for, session, render_template, flash, request
from models.tables import db, Cart, Product, Address, Order, OrderItem, Coupon, UserCoupon
from datetime import datetime

cart_bp = Blueprint('cart', __name__)


def delivery_charge(total):
    if total < 500:
        return total + 40
    else:
        return total


def cart_item_to_quantity_map(user_id):
    cart_items = Cart.query.filter_by(user_id=user_id).all()

    cart_products = []
    cart_map = {}

    for cart_item in cart_items:
        product = Product.query.get(cart_item.product_id)
        if product:
            cart_products.append(product)
            cart_map[product.id] = cart_item.quantity
    return cart_map, cart_products


def get_grand_total(cart_map):
    grand_total = 0

    for i in Product.query.all():
        if i.id in cart_map and cart_map[i.id] > 0:
            grand_total += i.rate_per_unit * cart_map[i.id]
    return grand_total


@cart_bp.route('/cart', methods=['GET', 'POST'])
def view_cart():
    user_id = session.get('user_id')

    cart_map, cart_products = cart_item_to_quantity_map(user_id)

    grand_total = get_grand_total(cart_map)

    addresses = Address.query.filter_by(user_id=user_id).all()

    user_coupons = UserCoupon.query.filter_by(user_id=user_id).all()

    coupon_map = {}

    for i in user_coupons:
        coupon_map[Coupon.query.filter_by(id=i.coupon_id).first()] = i.quantity

    session.pop('grand_total', None)
    session.pop('coupon_id', None)

    if request.method == 'POST' and request.form['coupon_code']:

        selected_coupon_id = request.form.get('coupon_code')
        selected_coupon = Coupon.query.filter_by(id=selected_coupon_id).first()

        if grand_total >= selected_coupon.min_cart_value:
            grand_total -= grand_total*selected_coupon.discount/100
            session['grand_total'] = grand_total
            session['coupon_id'] = selected_coupon_id
            return render_template('cart.html', selected_coupon=selected_coupon, cart_products=cart_products, cart_map=cart_map, grand_total=delivery_charge(grand_total), addresses=addresses, coupon_map=coupon_map)
        else:
            flash(
                f'The minimum cart value should be {selected_coupon.min_cart_value}', 'cart')

    session['grand_total'] = delivery_charge(grand_total)

    return render_template('cart.html', cart_products=cart_products, cart_map=cart_map, grand_total=delivery_charge(grand_total), addresses=addresses, coupon_map=coupon_map)


@cart_bp.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    # Get the user_id from the session (you may need to adjust this based on your session setup)
    user_id = session.get('user_id')

    # Check if the product is already in the cart, if not, add it
    cart_item = Cart.query.filter_by(
        user_id=user_id, product_id=product_id).first()
    if not cart_item:
        new_cart_item = Cart(
            user_id=user_id, product_id=product_id, quantity=1)
        db.session.add(new_cart_item)
    else:
        cart_item.quantity += 1

    db.session.commit()
    return redirect(request.referrer)


@cart_bp.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    # Get the user_id from the session (you may need to adjust this based on your session setup)
    user_id = session.get('user_id')

    # Check if the product is in the cart, if yes, reduce its quantity
    cart_item = Cart.query.filter_by(
        user_id=user_id, product_id=product_id).first()
    if cart_item:
        cart_item.quantity -= 1
        if cart_item.quantity <= 0:
            db.session.delete(cart_item)
        db.session.commit()
    return redirect(request.referrer)


@cart_bp.route('/place_order', methods=['POST'])
def place_order():
    user_id = session.get('user_id')

    # Retrieve the selected address ID from the form data
    if 'delivery_address' in request.form:
        selected_address_id = int(request.form['delivery_address'])
    else:
        flash('Please select a delivery address before placing an order.', 'cart')
        return redirect(request.referrer)

    # Get the cart items for the user
    cart_items = Cart.query.filter_by(user_id=user_id).all()

    if cart_items:
        if 'coupon_id' in session:
            coupon = UserCoupon.query.filter_by(
                coupon_id=session['coupon_id'], user_id=session['user_id']).first()
            coupon.quantity -= 1
            if coupon.quantity <= 0:
                db.session.delete(coupon)
        session.pop('coupon_id', None)

        # Create a new order
        new_order = Order(
            user_id=user_id,
            order_date=datetime.utcnow(),
            selected_address_id=selected_address_id,
            total_amount=session['grand_total'],
            status="Pending"
        )
        db.session.add(new_order)
        db.session.commit()

        # Create order items for each product in the cart
        for cart_item in cart_items:
            new_order_item = OrderItem(
                order_id=new_order.id,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                price_per_unit=Product.query.get(
                    cart_item.product_id).rate_per_unit
            )
            db.session.add(new_order_item)
            db.session.delete(cart_item)

        session.pop('grand_total', None)
        db.session.commit()
        flash('Order placed successfully!', 'cart')
    else:
        flash('Your cart is empty. Please add items before placing an order.', 'cart')

    return redirect(url_for('cart.view_cart'))
