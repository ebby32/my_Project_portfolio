from flask import render_template
from flask import abort

from application import db
from errors import error_bp


@error_bp.app_errorhandler(404)
def not_found(error):
    return render_template('404.html'),404

@error_bp.app_errorhandler(500)
def server_error(error):
    db.session.rollback()
    return render_template('500.html'),500

@error_bp.route('/test-404')
def test_404():
    abort(404)