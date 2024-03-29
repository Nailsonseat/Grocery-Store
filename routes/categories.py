from flask import Blueprint, render_template, request, redirect, url_for
from models.tables import db, Category, Product
import os

categories_bp = Blueprint('categories', __name__)


@categories_bp.route('/categories', methods=['GET', 'POST'])
def categories():
    if request.method == 'POST':
        new_category_name = request.form['category_name']
        new_category_image = request.files['category_image']

        if new_category_image:
            image_extension = new_category_image.filename.split('.')[-1]
            image_filename = f"{new_category_name}_category.{image_extension}"
            new_category_image.save(os.path.join(
                'static', 'category_images', image_filename))

        else:
            image_filename = 'placeholder.jpg'

        # Create a new Category instance and add it to the database
        new_category = Category(name=new_category_name,
                                image_filename=image_filename)
        db.session.add(new_category)
        db.session.commit()

        # Redirect back to the edit_categories page
        return redirect(url_for('categories.categories'))

    categories = Category.query.all()
    return render_template('categories.html', categories=categories)


@categories_bp.route('/delete_category/<int:category_id>', methods=['POST'])
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    products = Product.query.filter_by(category_id=category_id).all()

    # Delete products and their images under the category
    for product in products:
        if product.image_filename and product.image_filename != 'placeholder.jpg':
            image_path = os.path.join(
                'static', 'product_images', product.image_filename)
            os.remove(image_path)
        # Delete the category image
    if category.image_filename and category.image_filename != 'placeholder.jpg':
        image_path = os.path.join(
            'static', 'category_images', category.image_filename)
        os.remove(image_path)

    # Delete the category itself
    db.session.delete(category)
    db.session.commit()

    return redirect(url_for('categories.categories'))
