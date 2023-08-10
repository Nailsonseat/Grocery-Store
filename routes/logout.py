from flask import Blueprint, redirect, session, url_for


logout_bp = Blueprint('logout', __name__)


@logout_bp.route('/logout')
def logout():
    session.pop('email', None)  # Remove the username from the session
    session.pop('name', None)
    session.pop('user_id', None)
    # Redirect to the home page or login page
    return redirect(url_for('login.login'))
