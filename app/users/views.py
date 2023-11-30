from flask import flash, redirect, render_template, url_for, make_response, request
from flask_login import login_user, current_user, logout_user, login_required

from app import db
from .models import User
from .saver import save_picture

from .forms import RegistrationForm
from .forms import LoginForms
from .forms import UpdateAccountForm

from . import users


@users.route("/register", methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('portfolio.home'))

    form = RegistrationForm()

    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        existing_email = User.query.filter_by(email=form.email.data).first()

        if existing_user:
            flash('Username already taken. Please choose a different username.', 'danger')

            if existing_email:
                flash('Email already taken. Please choose a different email.', 'danger')

        else:

            new_user = User(username=form.username.data, email=form.email.data, password=form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash(f'Account successfully created for {form.username.data}!', 'success')
            return redirect(url_for('users.login'))
    
        flash(f'Something went wrong', 'warning')
    return render_template('register.html', form=form, title='Register')


@users.route("/login", methods=['GET', 'POST'])
def login():   

    if current_user.is_authenticated:
        return redirect(url_for('portfolio.home'))
     
    form = LoginForms()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and user.verify_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash('You have been logged in!', category='success')
            return redirect(url_for('portfolio.home'))
        else:
            flash('Login unsuccessful. Please check your email and password.', category='danger')
                
    return render_template("login.html", form=form, title='Login')


@users.route('/userslist')
def userslist():
    all_users = User.query.all()
    total_users = len(all_users)
    return render_template("users.html", all_users=all_users, total_users=total_users)


@users.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('portfolio.home'))


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        if form.username.data != current_user.username or form.email.data != current_user.email or form.about_me.data != current_user.about_me:
            current_user.username = form.username.data
            current_user.email = form.email.data
            current_user.about_me = form.about_me.data
            current_user.last_seen = form.last_seen.data
            db.session.commit()

            flash('Your account has been updated!', 'success')
            return redirect(url_for('users.account'))

        if form.image_file.data:
            current_user.image_file = save_picture(form.image_file.data)
            db.session.commit()

            flash('Your account has been updated!', 'success')
            return redirect(url_for('users.account'))
        
        else:
            flash('No changes were made to your account.', 'info')

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data =  current_user.about_me
        form.last_seen.data = current_user.last_seen

    return render_template('account.html', title='Account', form=form)



