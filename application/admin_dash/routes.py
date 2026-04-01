from flask import render_template
from sqlalchemy import func

from application.extensions import db
from application.admin_dash import admin_dash_bp
from application.home.models import Projects


@admin_dash_bp.route('/admin_dashboard', methods = ['GET','POST'])
def admin_dash():
    project_count = db.session.execute(db.select(func.count()).select_from(Projects)).scalar()
    published_count = db.session.execute(db.select(func.count()).where(Projects.status == 'published')).scalar()
    draft_count = db.session.execute(db.select(func.count()).where(Projects.status == 'draft')).scalar()
    return render_template('dashboard.html', project_count = project_count, published_count = published_count, draft_count = draft_count)