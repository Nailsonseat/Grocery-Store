from flask import Blueprint, redirect, session, url_for


logout_bp = Blueprint('logout', __name__)


@logout_bp.route('/logout')
def logout():
    session.pop('username', None)  # Remove the username from the session
    # Redirect to the home page or login page
    return redirect(url_for('login.login'))
