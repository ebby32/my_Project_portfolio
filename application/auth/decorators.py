from functools import wraps
from flask import current_app, request, redirect, url_for, flash, abort
from flask_login import current_user


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("You need to be logged in to view this page.","error")
            print("You need to be logged in to view this page.","error")
            return redirect(url_for('auth_bp.login', next = request.url))
        print(current_user.id)
        return f(*args, **kwargs)
    return decorated_function

def role_required(role):
    def decorator(f):
        @wraps(f)
        def wrapped_function(*args, **kwargs):
            #Assumes the current_user role is available in current_user.role
            if current_user.role != role:
                abort(403)
            return f(*args, **kwargs)
        return wrapped_function
    return decorator
