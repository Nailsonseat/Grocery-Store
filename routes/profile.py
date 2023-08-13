from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.tables import db, User, Address
import re
profile_bp = Blueprint('profile', __name__)

# Function to validate email format


def is_valid_email(email):
    email_pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")
    return email_pattern.match(email)


@profile_bp.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    user_id = session['user_id']
    user = User.query.get_or_404(user_id)
    addresses = Address.query.filter_by(user_id=user_id).all()

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        mobile_number = request.form.get('mobile_number')
        password = request.form.get('password')

        # Additional integrity checks
        if not name.strip():
            flash("Name cannot be empty.", "profile_error")
            return redirect(url_for('profile.edit_profile'))

        if not name.replace(" ", "").isalpha():
            flash("Name should not contain numbers or special characters.",
                  "profile_error")
            return redirect(url_for('profile.edit_profile'))

        if not is_valid_email(email):
            flash("Invalid email format.", "profile_error")
            return redirect(url_for('profile.edit_profile'))

        if len(password) < 8:
            flash("Password must be at least 8 characters long.", "profile_error")
            return redirect(url_for('profile.edit_profile'))

        user.name = name
        user.email = email
        user.mobile_number = mobile_number
        user.password = password

        db.session.commit()
        flash('Profile updated successfully!', 'profile_success')
        return redirect(url_for('profile.edit_profile'))

    return render_template('edit_profile.html', user=user, addresses=addresses)


@profile_bp.route('/add_address', methods=['POST'])
def add_address():
    user_id = session['user_id']
    new_house_no = request.form.get('new_house_no')
    new_landmark = request.form.get('new_landmark')
    new_city = request.form.get('new_city')
    new_state = request.form.get('new_state')
    new_zip_code = request.form.get('new_zip_code')

    new_address = Address(user_id=user_id, house_no=new_house_no, landmark=new_landmark,
                          city=new_city, state=new_state, zip_code=new_zip_code)
    db.session.add(new_address)
    db.session.commit()

    return redirect(url_for('profile.edit_profile'))


@profile_bp.route('/delete_address/<int:address_id>', methods=['POST'])
def delete_address(address_id):
    address = Address.query.get_or_404(address_id)
    db.session.delete(address)
    db.session.commit()
    return redirect(url_for('profile.edit_profile'))
