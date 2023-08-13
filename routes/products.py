from flask import Blueprint, render_template, request, redirect, url_for
from models.tables import db, Product, Category
import os
from datetime import datetime
import shutil

products_bp = Blueprint('products', __name__)


def get_category(categories, id):
    for i in categories:
        if id == i.id:
            return i


@products_bp.route('/add_products', methods=['GET', 'POST'])
def add_products():
    if request.method == 'POST':
        product_name = request.form['product_name']
        category_id = request.form['product_category']
        manufacture_date = request.form['mfd']
        expiry_date = request.form['expiry_date']
        rate_per_unit = request.form['rate_per_unit']
        product_image = request.files['product_image']

        # Convert manufacture_date and expiry_date to date objects
        if manufacture_date:
            manufacture_date = datetime.strptime(
                manufacture_date, '%d-%m-%Y').date()

        if expiry_date:
            expiry_date = datetime.strptime(expiry_date, '%d-%m-%Y').date()

        if product_image:
            image_extension = product_image.filename.rsplit('.', 1)[1]
            image_filename = f"{product_name}_product.{image_extension}"
            product_image.save(os.path.join(
                'static', 'product_images', image_filename))
        else:
            category = Category.query.get(category_id)
            if category.image_filename != 'placeholder.jpg':
                image_extension = category.image_filename.rsplit('.', 1)[1]
                image_filename = f"{product_name}_product.{image_extension}"
                category_image_path = os.path.join(
                    'static', 'category_images', category.image_filename)
                product_image_path = os.path.join(
                    'static', 'product_images', image_filename)
                shutil.copy2(category_image_path,
                             '/'.join(product_image_path.split('/')[:-1]))
                os.rename('/'.join(product_image_path.split('/')
                          [:-1])+'/'+category.image_filename, product_image_path)
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

    category_map = {}

    for i in categories:
        category_map[i] = []

    for product in products:
        category_map[get_category(
            categories, product.category_id)].append(product)

    return render_template('add_products.html', category_map=category_map)