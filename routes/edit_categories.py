
from flask import Blueprint, render_template, request, redirect, session, url_for
from models.tables import User

categories_bp = Blueprint('categories', __name__)


@categories_bp.route('/edit_categories')
def edit_categories():
    return render_template('edit_categories.html')
