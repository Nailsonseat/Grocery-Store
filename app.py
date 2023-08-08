# app.py

from flask_sqlalchemy import SQLAlchemy
from routes.login import login_bp
from routes.register import register_bp
from routes.admin_dashboard import admin_dashboard_bp
from routes.home import home_bp
from routes.logout import logout_bp
from routes.edit_categories import categories_bp
from routes.edit_products import products_bp
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
    admin_username = 'admin'
    admin_password = 'adminpass'

    admin_user = User.query.filter_by(username=admin_username).first()
    if not admin_user:
        admin_user = User(username=admin_username,
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
# ... (other routes and code)

if __name__ == '__main__':
    app.run(debug=True)
