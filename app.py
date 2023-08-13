# app.py

from routes.login import login_bp
from routes.register import register_bp
from routes.admin_dashboard import admin_dashboard_bp
from routes.home import home_bp
from routes.logout import logout_bp
from routes.categories import categories_bp
from routes.products import products_bp
from routes.profile import profile_bp
from routes.my_orders import my_orders_bp
from routes.cart import cart_bp
from routes.coupons import coupons_bp
from routes.pending_orders import pending_orders_bp
from routes.distribute_coupons import distribute_coupons_bp
from flask import Flask, render_template
from models.tables import db, User


app = Flask(__name__)
app.secret_key = '345357evfe3234r3'

# Configure the database URI (replace 'sqlite:///your_database.db' with the path to your SQLite database file)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main'

app.config['SQLALCHEMY_BINDS'] = {
    'users': 'sqlite:///users.db',
    'products': 'sqlite:///products.db'
}


def create_initial_admin():
    admin_name = 'admin'
    admin_email = 'admin@test.com'
    admin_password = 'adminpass'
    admin_mobile_number = "1234567890"

    admin_user = User.query.filter_by(email=admin_email).first()
    if not admin_user:
        admin_user = User(name=admin_name, email=admin_email, mobile_number=admin_mobile_number,
                          password=admin_password, is_admin=True)
        db.session.add(admin_user)
        db.session.commit()


# Initialize the database
db.init_app(app)

# Create the tables (this step should be performed once to create the tables in the database)
with app.app_context():
    db.create_all(bind_key=['users', 'products'])
    create_initial_admin()

# Register the blueprints

app.register_blueprint(register_bp)
app.register_blueprint(login_bp)
app.register_blueprint(admin_dashboard_bp)
app.register_blueprint(home_bp)
app.register_blueprint(logout_bp)
app.register_blueprint(categories_bp)
app.register_blueprint(products_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(my_orders_bp)
app.register_blueprint(coupons_bp)
app.register_blueprint(distribute_coupons_bp)
app.register_blueprint(pending_orders_bp)
# ... (other routes and code)

if __name__ == '__main__':
    app.run(debug=True)
