
from flask import Blueprint, render_template

admin_dashboard_bp = Blueprint('admin_dashboard', __name__)


@admin_dashboard_bp.route('/admin/dashboard')
def admin_dashboard():
    # Add code to display the admin dashboard here
    return render_template('admin_dashboard.html')
