from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



from application.home.models import Users

from flask_bootstrap import Bootstrap5


bootstrap = Bootstrap5()




login_manager = LoginManager()
login_manager.login_view = "auth.login"  #point to your login route

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(Users, user_id)