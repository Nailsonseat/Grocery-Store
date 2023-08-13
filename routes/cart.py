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

