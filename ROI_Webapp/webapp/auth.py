from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from  werkzeug.security import generate_password_hash, check_password_hash
from .validation import validate_email, validate_password
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        email = email.lower().strip()
        
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.roi'))
            else:
                flash('Invalid password, please try again.', category='error')
        else:
            flash('Email does not exist, please try again.', category='error')
    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        email = email.lower().strip()
        password1 = password1.strip()
        password2 = password2.strip()

        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('User with that email already exists!', category='error')
        elif not validate_email(email):
            flash('Invalid email, Please enter a valid email address.', category='error')
        elif not validate_password(password1):
            flash('Invalid password, Please enter a valid password. To see requirements hover over Password.', category='error')
        elif password2 != password1:
            flash('Invalid password, Please make sure your passwords match.', category='error')
        else:
            new_user = User(email=email, password=generate_password_hash(password1, method='scrypt'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.roi'))
    return render_template('sign_up.html', user=current_user)