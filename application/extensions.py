import os
from fileinput import filename

from flask import current_app
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

db = SQLAlchemy()



from application.home.models import Users

from flask_bootstrap import Bootstrap5


bootstrap = Bootstrap5()




login_manager = LoginManager()
login_manager.login_view = "auth.login"  #point to your login route

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(Users, user_id)

# def upload_file(file):
#     filename = secure_filename(file.filename)
#     path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
#     file.save(path)
#     return filename