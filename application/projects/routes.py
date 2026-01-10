from flask import render_template, request, redirect, url_for

from application import db
from application.projects.forms import AddProject, EditProject
from application.home.models import Projects
from application.projects import projects_bp


@projects_bp.route('/projects', methods = ['GET', 'POST'])
def projects():
    page = db.paginate(db.select(Projects).order_by(Projects.id), per_page=3)
    return render_template('projects.html', page = page)

@projects_bp.route('/add_project', methods = ['GET', 'POST'])
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
        return redirect(url_for('home_bp.home'))
    return render_template('add_project.html', form = form)

@projects_bp.route('/view', methods = ['GET','POST'])
def view():
    return render_template('view.html')

@projects_bp.route('/edit_project/<int:project_id>', methods = ['GET','POST'])
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

@projects_bp.route('/delete_project/<int:project_id>', methods = ['GET','POST'])
def delete_project(project_id):
    project_to_delete= db.session.execute(db.select(Projects).where(Projects.id == project_id)).scalar()
    db.session.delete(project_to_delete)
    db.session.commit()
    return render_template('projects.html',project = project_to_delete)
