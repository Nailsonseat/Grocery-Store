# routes/register.py

from flask import Blueprint, render_template, request
from models import db, User

register_bp = Blueprint('register', __name__)


@register_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if the username is available
        if User.query.filter_by(username=username).first() is None:
            # Check if the password and confirm_password match
            if password == confirm_password:
                # Create a new user record and add it to the database
                new_user = User(username=username, password=password)
                db.session.add(new_user)
                db.session.commit()

                return "User registered successfully!"

            return "Passwords do not match. Please try again."

        return "Username already taken. Please choose a different one."

    return render_template('register.html')
