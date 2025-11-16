import pyotp
import pyqrcode
import io
import base64
from flask import send_file, Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_user, login_required, logout_user, current_user
from ..models import User
from HelpDesk.utils.registration_helper import validate_registration_form
from werkzeug.security import generate_password_hash, check_password_hash
from ..extensions import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email:
            flash('Please enter your email address.', category='error')
        elif '@' not in email or '.' not in email.split('@')[-1]:
            flash('Please enter a valid email address.', category='error')
        elif not password:
            flash('Please enter your password.', category='error')
        else:
            user = User.query.filter_by(email=email).first()

            if user and check_password_hash(user.password, password):
                session['pending_login_2fa_user_id'] = user.id
                if user.is_2fa_enabled == True:
                    return redirect(url_for('auth.login_2fa'))
                else:
                    return redirect(url_for('auth.setup_2fa'))
            else:
                flash('Incorrect username or password. Please try again.', category='error')

    return render_template("login.html", user=current_user, email='')

@auth_bp.route('/login_2fa', methods=['GET', 'POST'])
def login_2fa():
    user_id = session.get('pending_login_2fa_user_id')
    if not user_id:
        flash('Please login first.', category='error')
        return redirect(url_for('auth.login'))

    user = User.query.get(user_id)
    totp = pyotp.TOTP(user.totp_secret)

    if request.method == 'POST':
        token = request.form.get('token')
        if totp.verify(token):
            login_user(user, remember=True)
            session.pop('pending_login_2fa_user_id', None)
            flash('You have logged in successfully.', category='success')
            return redirect(url_for('home.home'))
        else:
            flash('Incorrect authentication code. Please try again.', category='error')

    qr_uri = totp.provisioning_uri(user.email, issuer_name="Eclipse Software Help Desk")
    qr_b64 = base64.b64encode(pyqrcode.create(qr_uri).png_as_base64_str(scale=5).encode()).decode()

    return render_template('login_2fa.html', user=user, qr_b64=qr_b64)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        forename = request.form.get('forename')
        surname = request.form.get('surname')
        is_admin = request.form.get('is_admin')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')

        user = User.query.filter_by(email=email).first()
        error = validate_registration_form(forename, surname, email, password, password_confirm, user)
        if error:
            flash(error, category='error')
            return render_template(
                "register.html",
                user=current_user,
                forename=forename,
                surname=surname,
                email=email,
                is_admin=is_admin
            )

        totp_secret = pyotp.random_base32()

        session['pending_2fa_user'] = {
            'email': email,
            'forename': forename,
            'surname': surname,
            'is_admin': is_admin,
            'password': password,
            'totp_secret': totp_secret
        }

        return redirect(url_for('auth.setup_2fa'))

    return render_template("register.html", user=current_user)

@auth_bp.route('/setup_2fa', methods=['GET', 'POST'])
def setup_2fa():
    # user_id handles users that already have an account but do not have 2fa setup
    user_id = session.get('pending_login_2fa_user_id') 
    # pending_user handles new users registering for an account
    pending_user = session.get('pending_2fa_user') 

    # Determine which user is setting up 2FA
    # if user_id exists, it is an existing user logging in
    # if user.totp_secret does not exist, then we generate one and commit it to the db
    if user_id:
        user = User.query.get(user_id)
        if not user:
            flash('User not found. Please log in again.', 'error')
            return redirect(url_for('auth.login'))

        if not user.totp_secret:
            user.totp_secret = pyotp.random_base32()
            db.session.commit()

        totp = pyotp.TOTP(user.totp_secret)
        email = user.email

    # if pending_user exists, it is a new user registering
    # the totp_secret is already generated during registration, therefore we just use that
    elif pending_user:
        totp = pyotp.TOTP(pending_user['totp_secret'])
        email = pending_user['email']
    else:
        flash('No pending registration or login found.', 'error')
        return redirect(url_for('auth.login'))

    # Generate QR code for TOTP setup
    totp_uri = totp.provisioning_uri(name=email, issuer_name="Eclipse Software Help Desk")
    qr_code = pyqrcode.create(totp_uri).png_as_base64_str(scale=4)

    # If request is POST, verify the token (6 digit code) entered by the user
    # If user_id exists, enable 2FA for existing user and log them in
    # If pending_user exists, create the new user account with 2FA enabled
    # If token is invalid, we show an error message
    if request.method == 'POST':
        token = request.form.get('token')
        if totp.verify(token):
            if user_id:
                user.is_2fa_enabled = True
                db.session.commit()
                login_user(user)
                session.pop('pending_login_2fa_user_id', None)
                flash('2FA setup complete. You have logged in successfully.', 'success')
                return redirect(url_for('home.home'))

            elif pending_user:
                new_user = User(
                    email=pending_user['email'],
                    forename=pending_user['forename'],
                    surname=pending_user['surname'],
                    is_admin=False,
                    password=generate_password_hash(pending_user['password'], method='pbkdf2:sha256'),
                    totp_secret=pending_user['totp_secret'],
                    is_2fa_enabled=True
                )
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
                session.pop('pending_2fa_user', None)
                flash('Account created successfully.', 'success')
                return redirect(url_for('home.home'))
        else:
            flash('Invalid authentication code. Please try again.', 'error')

    return render_template('setup_2fa.html', qr_code=qr_code, user=(user if user_id else pending_user))