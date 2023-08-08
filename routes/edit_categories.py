from flask import Blueprint, render_template, request, redirect, url_for
from models.tables import db, Category
import os

categories_bp = Blueprint('categories', __name__)


@categories_bp.route('/edit_categories', methods=['GET', 'POST'])
def edit_categories():
    if request.method == 'POST':
        new_category_name = request.form['category_name']
        new_category_image = request.files.get('category_image')

        if new_category_image:
            image_filename = new_category_image.filename
            new_category_image.save(os.path.join(
                'static', 'category_images', image_filename))
        else:
            image_filename = 'placeholder.jpg'  # Use the placeholder image

        # Create a new Category instance and add it to the database
        new_category = Category(name=new_category_name,
                                image_filename=image_filename)
        db.session.add(new_category)
        db.session.commit()

        # Redirect back to the edit_categories page
        return redirect(url_for('categories.edit_categories'))

    categories = Category.query.all()
    return render_template('edit_categories.html', categories=categories)


@categories_bp.route('/delete_category/<int:category_id>', methods=['POST'])
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for('categories.edit_categories'))
