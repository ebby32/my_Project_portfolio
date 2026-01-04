from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField


class ContactMe(FlaskForm):
    your_name = StringField('Your Name')
    your_email = StringField('Your Email')
    your_telephone = IntegerField('Telephone Number')
    your_message = StringField('Message')
    send = SubmitField('Send')