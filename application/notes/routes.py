from datetime import datetime

from flask import render_template, request, url_for, flash
from werkzeug.utils import redirect

from application.extensions import db
from application.notes import notes_bp
from application.notes.forms import CreateNotes
from application.notes.models import Notes
from application.auth.decorators import login_required


@notes_bp.route('/create_notes', methods = ['GET','POST'])
@login_required
def create_notes():
    form = CreateNotes()
    form.date.data = datetime.today().strftime('%B, %d, %Y')
    if form.validate_on_submit():
        new_notes = Notes(
            date = form.date.data,
            title = request.form.get('title'),
            body = request.form.get('body')
        )
        db.session.add(new_notes)
        db.session.commit()
        return redirect(url_for("home_bp.home"))

    return render_template('create_notes.html', form = form)

@notes_bp.route("/edit_note/<int:note_id>", methods = ["POST","GET"])
@login_required
def edit_note(note_id):
    note = Notes.query.get_or_404(note_id)
    form = CreateNotes(obj=note)

    if form.validate_on_submit():
        note.title = form.title.data
        note.body = form.body.data
        db.session.commit()

        flash("Note updated")
        return redirect(url_for('notes_bp.notes_content', note_id =note.id))
    return render_template('create_notes.html', form = form)

@notes_bp.route('/notes_list', methods = ['GET','POST'])
@login_required
def notes_list():
    notes = db.session.execute(db.select(Notes).order_by(Notes.id)).scalars().all()
    return render_template('view_notes_list.html', notes_data = notes)

@notes_bp.route('/note_content/<int:note_id>', methods = ['GET','POST'])
@login_required
def notes_content(note_id):
    note_to_view = db.session.execute(db.select(Notes).where(Notes.id == note_id)).scalar()
    return render_template('view_note_content.html', notes = note_to_view)