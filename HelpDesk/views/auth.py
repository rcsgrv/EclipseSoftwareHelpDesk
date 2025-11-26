import pyotp
import pyqrcode
import base64
from flask import Blueprint, render_template, request, flash, redirect, url_for, session, current_app
from flask_login import login_user, login_required, logout_user, current_user
from ..models import User
from ..extensions import db
from ..utils.registration_helper import validate_registration_form
from werkzeug.security import generate_password_hash, check_password_hash

# Route logic was informed a tutorial by Tech With Tim (Tech With Tim, 2021).
# PyOTP usage was informed by a tutorial from NeuralNine (NeuralNine, 2022).

# This Blueprint handles login and authentication.
# Form validation is used to ensure data integrity before database operations are performed, and appropriate user feedback is provided via flash messages.
# 2FA setup and verification is implemented using TOTP via the PyOTP library.
# User authentication state is managed using Flask-Login.
# Password hashing is implemented using Werkzeug security utilities. 

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in.", "info")
        return redirect(url_for('home.home'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or '@' not in email or '.' not in email.split('@')[-1]:
            flash('Please enter a valid email address.', 'error')
        elif not password:
            flash('Please enter your password.', 'error')
        else:
            user = db.session.query(User).filter_by(email=email).first()
            if user and check_password_hash(user.password, password):
                if current_app.config.get("DISABLE_2FA"):
                    login_user(user, remember=True)
                    flash("Logged in successfully (2FA bypassed for testing)", "success")
                    return redirect(url_for('home.home'))

                # Check if 2FA is enabled
                if not user.is_2fa_enabled:
                    session['pending_2fa_user_id'] = user.id
                    return redirect(url_for('auth.setup_2fa'))
                else:
                    session['pending_login_2fa_user_id'] = user.id
                    return redirect(url_for('auth.login_2fa'))
            else:
                flash('Incorrect email or password.', 'error')

    return render_template('login.html', user=current_user, email='')

@auth_bp.route('/login_2fa', methods=['GET', 'POST'])
def login_2fa():
    if current_user.is_authenticated:
        flash("You are already logged in.", "info")
        return redirect(url_for('home.home'))

    user_id = session.get('pending_login_2fa_user_id')
    if not user_id:
        flash('No pending login found.', 'error')
        return redirect(url_for('auth.login'))

    user = db.session.get(User, user_id)
    totp = pyotp.TOTP(user.totp_secret)

    if request.method == 'POST':
        token = request.form.get('token')
        if totp.verify(token):
            login_user(user, remember=True)
            session.pop('pending_login_2fa_user_id', None)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('home.home'))
        else:
            flash('Invalid authentication code. Please try again.', 'error')

    qr_uri = totp.provisioning_uri(user.email, issuer_name="Eclipse Software Help Desk")
    qr_b64 = base64.b64encode(pyqrcode.create(qr_uri).png_as_base64_str(scale=5).encode()).decode()

    return render_template('login_2fa.html', user=user, qr_b64=qr_b64)

@auth_bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    if request.method == 'POST':
        logout_user()
        return redirect(url_for('auth.login'))
    return render_template('logout_confirm.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash("You have already created an account.", "info")
        return redirect(url_for('home.home'))

    if request.method == 'POST':
        email = request.form.get('email')
        forename = request.form.get('forename')
        surname = request.form.get('surname')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')

        user = db.session.query(User).filter_by(email=email).first()
        error = validate_registration_form(forename, surname, email, password, password_confirm, user)
        if error:
            flash(error, 'error')
            return render_template('register.html', user=current_user, forename=forename, surname=surname, email=email)

        # Create user immediately
        new_user = User(
            email=email,
            forename=forename,
            surname=surname,
            is_admin=False,
            password=generate_password_hash(password, method='pbkdf2:sha256'),
            is_2fa_enabled=False
        )
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully. Please log in to continue.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html', user=current_user)

@auth_bp.route('/setup_2fa', methods=['GET', 'POST'])
def setup_2fa():
    if current_user.is_authenticated:
        flash("You have already setup 2FA.", "info")
        return redirect(url_for('home.home'))

    user_id = session.get('pending_2fa_user_id')
    if not user_id:
        flash('No pending 2FA setup found.', 'error')
        return redirect(url_for('auth.login'))

    user = db.session.get(User, user_id)
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('auth.login'))

    # Generate TOTP and QR code
    if not user.totp_secret:
        user.totp_secret = pyotp.random_base32()
        db.session.commit()

    totp = pyotp.TOTP(user.totp_secret)
    totp_uri = totp.provisioning_uri(name=user.email, issuer_name="Eclipse Software Help Desk")
    qr_code = pyqrcode.create(totp_uri).png_as_base64_str(scale=4)

    if request.method == 'POST':
        token = request.form.get('token')
        if totp.verify(token):
            user.is_2fa_enabled = True
            db.session.commit()
            login_user(user)
            session.pop('pending_2fa_user_id', None)
            flash('2FA setup complete. You are now logged in.', 'success')
            return redirect(url_for('home.home'))
        else:
            flash('Invalid authentication code.', 'error')

    return render_template('setup_2fa.html', qr_code=qr_code, user=user)