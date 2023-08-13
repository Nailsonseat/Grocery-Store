from flask import Blueprint, render_template, request, redirect, flash
from models.tables import db, User

register_bp = Blueprint('register', __name__)


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
                # Create a new user record and add it to the database
                new_user = User(name=name, email=email,
                                mobile_number=mobile_number, password=password)  # Include date_of_birth
                db.session.add(new_user)
                db.session.commit()

                flash('Registration complete', 'reg_success')
                return redirect('/')

            return "Passwords do not match. Please try again."

        return "Email already taken. Please use a different one."

    return render_template('register.html')
