from flask import render_template, request, redirect, url_for, Blueprint
from models.tables import db, Coupon


coupons_bp = Blueprint('coupons', __name__)


@coupons_bp.route('/coupons', methods=['GET', 'POST'])
def coupons():
    if request.method == 'POST':
        name = request.form.get('name').upper()
        min_cart_value = int(request.form.get('min_cart_value'))
        discount = int(request.form.get('discount'))

        new_coupon = Coupon(
            name=name, min_cart_value=min_cart_value, discount=discount)
        db.session.add(new_coupon)
        db.session.commit()

    coupons = Coupon.query.all()

    return render_template('coupons.html', coupons=coupons)


@coupons_bp.route('/coupons/delete/<int:coupon_id>', methods=['POST'])
def delete_coupon(coupon_id):
    coupon = Coupon.query.get(coupon_id)
    if coupon:
        db.session.delete(coupon)
        db.session.commit()
    return redirect(url_for('coupons.coupons'))
