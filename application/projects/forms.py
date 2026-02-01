from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, SubmitField, IntegerField


class AddProject(FlaskForm):
    project_name = StringField('Project Name ')

    image = FileField("Upload Image", validators=[FileRequired()], render_kw={"class": "mb-3 mt-3"})

    url = StringField('GitHub Url ')
    description = StringField('Description ')
    save = SubmitField('Save ')

# class EditProject(FlaskForm):
#     project_name = StringField('Project Name ')
#     image_url = StringField('Image Url/Name ')
#     github = StringField('GitHub Url ')
#     description = StringField('Description ')
#     save = SubmitField('Save ')


class EditProject(FlaskForm):
    project_name = StringField('Project Name ')
    image = FileField("Upload Image", validators=[FileRequired()], render_kw={"class": "mb-3 mt-3"})
    url = StringField('GitHub Url ')
    description = StringField('Description ')
    save = SubmitField('Save ')

