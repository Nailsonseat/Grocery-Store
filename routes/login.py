# routes/login.py

from flask import Blueprint, render_template, request, redirect, session
from models import User

login_bp = Blueprint('login', __name__)


@login_bp.route('/', methods=['GET', 'POST'])
@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user:
            # Check if the password matches the user's password in the database
            if user.password == password:
                session['username'] = username

                if user.is_admin:
                    # Redirect to admin dashboard
                    return redirect('/admin/dashboard')
                else:
                    # Redirect to regular user dashboard
                    return redirect('/home')

            else:
                return "Incorrect password. Please try again."

        return "User does not exist. Please register an account."

    return render_template('login.html')
