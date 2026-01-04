from application.home.forms import ContactMe
from application.home import home_bp
from application.home.email_service import send_contact_email
from flask import request, render_template, redirect, url_for

@home_bp.route('/contact_me', methods = ['GET','POST'])
def contact_me():
    form = ContactMe()
    if request.method=='POST':
        send_contact_email(
            name=form.your_name.data,
            email=form.your_email.data,
            telephone=form.your_telephone.data,
            message=form.your_message.data
        )
        return redirect(url_for('home_bp.home'))
    return render_template('contact_me.html', form = form)

@home_bp.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@home_bp.route('/about_me')
def about_me():
    return render_template('about_me.html')

