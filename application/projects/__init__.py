from flask import Blueprint

projects_bp = Blueprint("projects_bp",__name__, template_folder="templates", static_folder="static", static_url_path="/projects-static")

from . import routes