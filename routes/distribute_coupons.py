from flask import Blueprint, render_template, request, redirect, url_for
from models.tables import db, Coupon, User, UserCoupon

distribute_coupons_bp = Blueprint('distribute_coupons', __name__)


@distribute_coupons_bp.route('/distribute_coupons', methods=['GET', 'POST'])
def distribute():
    if request.method == 'POST':
        coupon_id = request.form.get('coupon_id')

        for user in User.query.all():
            coupon_quantity = request.form.get(
                'coupon_quantity_' + str(user.id))
            if coupon_quantity and int(coupon_quantity) > 0:
                user_coupon = UserCoupon(
                    user_id=user.id,
                    coupon_id=coupon_id,
                    quantity=coupon_quantity
                )
                db.session.add(user_coupon)

        db.session.commit()
        return redirect(url_for('distribute_coupons.distribute'))

    coupons = Coupon.query.all()
    users = User.query.all()
    users.remove(users[0])

    return render_template('distribute_coupons.html', coupons=coupons, users=users)
