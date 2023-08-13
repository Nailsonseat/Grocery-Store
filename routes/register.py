from flask import Blueprint, render_template, request, redirect, flash, url_for
from models.tables import db, User, Coupon, UserCoupon
import re

register_bp = Blueprint('register', __name__)


# Function to validate email format
def is_valid_email(email):
    email_pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")
    return email_pattern.match(email)


@register_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        mobile_number = request.form['mobile_number']

        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if the email is available
        if User.query.filter_by(email=email).first() is None:
            # Check if the password and confirm_password match
            if password == confirm_password:

                # Perform additional integrity checks for name and password
                if not name.strip():
                    flash("Name cannot be empty.", "reg_error")
                    return redirect(url_for('register.register'))

                if not name.replace(" ", "").isalpha():
                    flash("Name should only contain letters and spaces.", "reg_error")
                    return redirect(url_for('register.register'))

                if not is_valid_email(email):
                    flash("Invalid email format.", "reg_error")
                    return redirect(url_for('register.register'))

                if len(password) < 8:
                    flash("Password must be at least 8 characters long.", "reg_error")
                    return redirect(url_for('register.register'))

                # Create a new user record and add it to the database
                new_user = User(name=name, email=email,
                                mobile_number=mobile_number, password=password)  # Include date_of_birth
                db.session.add(new_user)
                db.session.commit()

                welcome_coupon = Coupon.query.filter_by(
                    name="WELCOME50").first()
                if welcome_coupon:
                    user_coupon = UserCoupon(
                        user_id=new_user.id, coupon_id=welcome_coupon.id, quantity=1)
                    db.session.add(user_coupon)
                    db.session.commit()

                flash('Registration complete', 'reg_success')
                return redirect('/')

            flash("Passwords do not match. Please try again.", "reg_error")
            return redirect(url_for('register.register'))

        flash("Email already taken. Please use a different one.", "reg_error")
        return redirect(url_for('register.register'))

    return render_template('register.html')
