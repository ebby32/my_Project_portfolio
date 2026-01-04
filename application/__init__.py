from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy

import config
from application.auth import auth_bp
from application.extensions import bootstrap, db
from application.home import home_bp
from application.projects import projects_bp
from application.extensions import login_manager


#Globally accessible libraries


def create_app():
    """Initialize the core application"""
    app =  Flask(__name__, instance_relative_config= False)
    app.config.from_object(config.Config)

    with app.app_context():
        db.create_all()

    """Initialize the plugins"""
    db.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)
    # Bootstrap5(app)

    with app.app_context():
        #include our routes
        from . import routes
        from .auth import routes
        from .home import routes
        from .projects import routes

        #Register BluePrints
        app.register_blueprint(auth_bp)
        app.register_blueprint(home_bp)
        app.register_blueprint(projects_bp)



    return app
