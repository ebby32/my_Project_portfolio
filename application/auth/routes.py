from flask import request, render_template, flash, redirect, url_for
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from application.auth import auth_bp
from application.extensions import db
from application.home.models import Users


@auth_bp.route("/register", methods = ["GET","POST"])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        hash_password = generate_password_hash(password, method= 'pbkdf2:sha1', salt_length=8)

        in_db = db.session.execute(db.select(Users).where(Users.username == username)).scalar()
        if not in_db:
            new_user = Users(
                username = username,
                password = hash_password,
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect("home_bp.home")
    return render_template('register.html')

@auth_bp.route("/login", methods = ["GET","POST"])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        check_username = db.session.execute(db.select(Users).where(Users.username == username)).scalar()
        check_password = check_password_hash(check_username.password, password)

        if check_username and check_password or check_username and password == check_username.password:
            login_user(check_username)
            flash('Logged in')
        return redirect(url_for('home_bp.home'))

    return render_template('login.html')


@auth_bp.route('/logged_out')
def logout():
    logout_user()
    flash('logged out')
    return render_template('home.html')


