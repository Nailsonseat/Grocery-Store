from flask import Blueprint, render_template, request, redirect, url_for
from models.tables import db, Product, Category
import os

products_bp = Blueprint('products', __name__)


@products_bp.route('/edit_products', methods=['GET', 'POST'])
def edit_products():
    if request.method == 'POST':
        product_name = request.form['product_name']
        category_id = request.form['product_category']
        manufacture_date = request.form['mfd']
        expiry_date = request.form['expiry_date']
        rate_per_unit = request.form['rate_per_unit']

        product_image = request.files['product_image']

        if product_image:
            image_filename = product_image.filename
            product_image.save(os.path.join(
                'static', 'product_images', image_filename))
        else:
            image_filename = 'placeholder.jpg'  # Use the placeholder image

        if manufacture_date == '':
            manufacture_date = None

        if expiry_date == '':
            expiry_date = None

        # Create a new Product instance and add it to the database
        new_product = Product(name=product_name, category_id=category_id,
                              manufacture_date=manufacture_date, expiry_date=expiry_date, rate_per_unit=rate_per_unit, image_filename=image_filename)
        db.session.add(new_product)
        db.session.commit()

    categories = Category.query.all()
    products = Product.query.all()
    return render_template('edit_products.html', categories=categories, products=products)


@products_bp.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('products.edit_products'))
