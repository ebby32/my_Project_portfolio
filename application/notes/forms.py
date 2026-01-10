from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, SubmitField
from flask_ckeditor import CKEditorField, CKEditor
from wtforms.validators import DataRequired

ckeditor = CKEditor()

class CreateNotes(FlaskForm):
    date = StringField('Date')
    title = StringField('Title')
    body = CKEditorField('Body', validators=[DataRequired()])
    submit = SubmitField('Save')