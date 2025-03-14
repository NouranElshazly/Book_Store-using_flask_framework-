from  flask import Blueprint, redirect , url_for

from flask import render_template
from werkzeug.security import generate_password_hash
from app.auth.forms import Regesristration , LoginForm
from app.models import User
from app import db
auth_blueprint = Blueprint('auth', __name__ , url_prefix='/auth')
from flask import flash
from flask_login import login_required, login_user, logout_user

@auth_blueprint.route('/register', methods=['GET', 'POST'], endpoint='register')
def register():
    form = Regesristration()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data , password= form.password.data   )
        user.save_to_db()
        return redirect(url_for('main.home'))
    else:
        return render_template('auth/register.html', form=form)
    
@auth_blueprint.route('/login',  endpoint='login' , methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
            return render_template('auth/login.html' , form=form)
    return render_template('auth/login.html' , form=form)
@auth_blueprint.route('/logout', endpoint='logout')
@login_required
def logout():
    logout_user()  # Ensure user session is cleared
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))