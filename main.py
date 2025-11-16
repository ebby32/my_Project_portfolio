from ensurepip import bootstrap
from functools import wraps

from flask import Flask, render_template, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, DeclarativeBase
from sqlalchemy import Integer, String
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import StringField, SubmitField
from wtforms.fields.numeric import IntegerField
from wtforms.validators import DataRequired, Length
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import smtplib
from smtplib import SMTP
from dotenv import load_dotenv
import os

load_dotenv()

EMAIL_USERNAME = os.environ["EMAIL_USERNAME"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]


app = Flask(__name__)
Bootstrap5(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URL','sqlite:///site.db')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URL')



# if os.environ.get('FLASK_ENV') == "development":
#     app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"
# else:
#     app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URL')

class Base(DeclarativeBase):
    pass


app.secret_key = "Just_a_secret_key"


db = SQLAlchemy()
db.init_app(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(Users, user_id)

class Users(db.Model, UserMixin):
    __tablename__ = "users"
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    username:Mapped[str] = mapped_column(String(100), nullable = False)
    password:Mapped[str] = mapped_column(String(100), nullable= False)

#Admin only decorator, only let the user with the id ==1 access page
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.id != 1:
            return abort(403)
        #Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function

class Projects(db.Model):
    id:Mapped[int] = mapped_column(Integer, primary_key= True)
    project_name:Mapped[str] = mapped_column(String(120), nullable= False)
    image:Mapped[str] = mapped_column(String(120), nullable= False)
    url:Mapped[str] = mapped_column(String(120), nullable= False)
    description:Mapped[str] = mapped_column(String(120), nullable= False)

class AddProject(FlaskForm):
    project_name = StringField('Project Name ')
    image_url = StringField('Image Url/Name ')
    github = StringField('GitHub Url ')
    description = StringField('Description ')
    submit = SubmitField('Save ')

class EditProject(FlaskForm):
    project_name = StringField('Project Name ')
    image_url = StringField('Image Url/Name ')
    github = StringField('GitHub Url ')
    description = StringField('Description ')
    save = SubmitField('Save ')

class ContactMe(FlaskForm):
    your_name = StringField('Your Name')
    your_email = StringField('Your Email')
    your_telephone = IntegerField('Telephone Number')
    your_message = StringField('Message')
    send = SubmitField('Send')

@app.route('/login', methods = ['GET','POST'])
def login():
    username = request.form.get('username')
    print(username)
    check_username = db.session.execute(db.select(Users).where(Users.username == username)).scalar()
    print(check_username)
    check_password = db.session.execute(db.select(Users).where(Users.password == request.form.get('password'))).scalar()
    if request.method == 'POST':
        flash('Logged in')
        login_user(check_username)
        return redirect(url_for('home'))

    return render_template('login.html')

@app.route('/logged_out')
def logout():
    logout_user()
    return render_template('home.html')

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/about_me')
def about_me():
    return render_template('about_me.html')

@app.route('/contact_me', methods = ['GET','POST'])
def contact_me():
    form = ContactMe()
    if request.method=='POST':
        smtp = smtplib.SMTP("smtp.gmail.com", port =587)

        smtp.starttls()
        smtp.login(user=EMAIL_USERNAME, password=EMAIL_PASSWORD)
        smtp.sendmail(
            from_addr=EMAIL_USERNAME,
            to_addrs=EMAIL_USERNAME,
            msg=f"subject: Project Portfolio, contact me \n\nName: {request.form.get('your_name')}\n"
                f"Email:{request.form.get('your_email')}\nTelephone Number:{request.form.get('your_telephone')}\nMessage: {request.form.get('message')}"
        )
        smtp.close()
        return redirect(url_for('home'))
    return render_template('contact_me.html', form = form)

@app.route('/projects', methods = ['GET', 'POST'])
def projects():
    data = db.session.execute(db.select(Projects).order_by(Projects.id)).scalars().all()
    return render_template('projects.html', project_data = data)

@app.route('/add_project', methods = ['GET', 'POST'])
def add_project():
    form = AddProject()
    if form.validate_on_submit():
        new_project = Projects(
            project_name =request.form.get('project_name'),
            image =request.form.get('image_url'),
            url =request.form.get('github'),
            description =request.form.get('description')
        )
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add_project.html', form = form)


# with app.app_context():
#     db.create_all()

@app.route('/view', methods = ['GET','POST'])
def view():
    render_template('view.html')

@app.route('/edit_project/<int:project_id>', methods = ['GET','POST'])
def edit_project(project_id):
    project_to_edit= db.session.execute(db.select(Projects).where(Projects.id == project_id)).scalar()
    form = EditProject(
        project_name = project_to_edit.project_name,
        image_url = project_to_edit.image,
        github = project_to_edit.url,
        description = project_to_edit.description
    )
    if request.method == 'POST':
        project_to_edit.project_name = request.form.get('project_name')
        project_to_edit.image = request.form.get('image_url')
        project_to_edit.url = request.form.get('github')
        project_to_edit.description = request.form.get('description')
        db.session.commit()
    return render_template('edit.html',form = form, project = project_to_edit)



if __name__ == '__main__':
    app.run(debug=True)