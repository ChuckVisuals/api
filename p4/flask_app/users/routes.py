from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user, login_required, login_user, logout_user
import base64
from io import BytesIO
from .. import bcrypt
from werkzeug.utils import secure_filename
from ..forms import RegistrationForm, LoginForm, UpdateUsernameForm, UpdateProfilePicForm
from ..models import User

users = Blueprint("users", __name__)

""" ************ User Management views ************ """


# TODO: implement
@users.route("/register", methods=["GET", "POST"])
def register():
    
    if current_user.is_authenticated:
        return redirect('/')
    
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        # Create a new user and store in the database
        hashed_password = bcrypt.generate_password_hash(reg_form.password.data).decode('utf-8')
        new_user = User(username=reg_form.username.data, email=reg_form.email.data ,password=hashed_password,profile_pic=None)
        new_user.save()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('users.login'))
        
    return render_template('register.html',form=reg_form)


# TODO: implement
@users.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    
    if login_form.validate_on_submit():
        # Authenticate the user
        user = User.objects(username=login_form.username.data).first()

        if user and bcrypt.check_password_hash(user.password, login_form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('users.account'))
        else:
            flash('Login unsuccessful. Please check your username and password.')  

    return render_template('login.html', form=login_form)

# TODO: implement
@users.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('movies.index')) 


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    update_username_form = UpdateUsernameForm()
    update_profile_pic_form = UpdateProfilePicForm()
    if request.method == "POST":
        if update_username_form.submit_username.data and update_username_form.validate():
            
            new_username = update_username_form.username.data
            current_user.username = new_username
            current_user.save()
            flash('Username updated successfully!', 'success')

        if update_profile_pic_form.submit_picture.data and update_profile_pic_form.validate():
  
            img = update_profile_pic_form.picture.data  
            filename = secure_filename(img.filename)
            content_type = f'images/{filename[-3:]}'

            if current_user.profile_pic.get() is None:
                current_user.profile_pic.put(img.stream, content_type=content_type)
            else:
                current_user.profile_pic.replace(img.stream, content_type=content_type)
            current_user.save()
            flash('Profile picture updated successfully!', 'success')

    return render_template('account.html', update_username_form=update_username_form, update_profile_picture_form=update_profile_pic_form)