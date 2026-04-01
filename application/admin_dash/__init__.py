from flask import Blueprint


admin_dash_bp = Blueprint("admin_dash_bp", __name__,
                          template_folder='templates',
                          static_folder='static',
                          static_url_path='/admin_dash_bp-static'
                          )

from . import routes