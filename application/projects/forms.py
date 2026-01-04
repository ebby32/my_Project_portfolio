from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField


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

