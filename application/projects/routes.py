import os

from flask import render_template, request, redirect, url_for, flash, send_from_directory, current_app
from werkzeug.utils import secure_filename

from application import db
from application.auth.decorators import role_required
from application.projects.forms import AddProject, EditProject
from application.home.models import Projects
from application.projects import projects_bp
from application.projects.services import allowed_file


@projects_bp.route('/projects', methods=['GET', 'POST'])
def projects():
    page = db.paginate(db.select(Projects).order_by(Projects.id), per_page=3)
    return render_template('projects.html', page=page)


@projects_bp.route('/add_project', methods=['GET', 'POST'])
@role_required("admin")
def add_project():
    form = AddProject()
    if form.validate_on_submit():
        new_project = Projects(
            project_name=form.project_name.data,
            image=form.image.data.filename,
            url=form.url.data,
            description=form.description.data
        )

        # check if the post request has a file part
        if not form.image.data:
            flash('No file part')
            print('No file part')
            return redirect(request.url)
        file = form.image.data
        # If the user does not submit a file the browser submits
        # an empty file without a file name
        if file.filename == '':
            flash('No file selected')
            print('No file selected')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # upload_file(file)
            filename = secure_filename(file.filename)
            path = os.path.join('application/projects/static/uploads', filename)
            file.save(path)
            print("saved")
        db.session.add(new_project)
        db.session.commit()

        return redirect(url_for('projects_bp.projects'))
    return render_template('add_project.html', form=form)


@projects_bp.route('/view', methods=['GET', 'POST'])
def view():
    return render_template('view.html')


@projects_bp.route('/edit_project/<int:project_id>', methods=['GET', 'POST'])
def edit_project(project_id):
    project_to_edit = db.session.execute(db.select(Projects).where(Projects.id == project_id)).scalar()
    form = EditProject(obj=project_to_edit)

    if form.validate_on_submit():
        project_to_edit.project_name = form.project_name.data
        project_to_edit.image = form.image.data.filename
        project_to_edit.url = form.url.data
        project_to_edit.description = form.description.data

        file = form.image.data
        if file.filename == '':
            flash('No file selected')
            print('No file selected')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # upload_file(file)
            filename = secure_filename(file.filename)
            path = os.path.join('application/projects/static/uploads', filename)
            file.save(path)
            print("saved")
        db.session.commit()
        return redirect(url_for("projects_bp.projects"))
    return render_template('edit.html', form=form)


@projects_bp.route('/delete_project/<int:project_id>', methods=['GET', 'POST'])
def delete_project(project_id):
    project_to_delete = db.session.execute(db.select(Projects).where(Projects.id == project_id)).scalar()
    db.session.delete(project_to_delete)
    db.session.commit()
    flash("Deleted")
    return redirect(url_for("projects_bp.projects"))


@projects_bp.route('/uploads/<filename>', methods=['GET', 'POST'])
def upload(filename):
    print(filename)
    return send_from_directory('application/projects/static/uploads', filename)
