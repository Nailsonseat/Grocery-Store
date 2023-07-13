from flask import Blueprint, redirect, session, url_for


logout_bp = Blueprint('logout', __name__)


@logout_bp.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('name', None)
    session.pop('user_id', None)
    return redirect(url_for('login.login'))
