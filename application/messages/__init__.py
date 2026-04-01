from flask import Blueprint

messages_bp = Blueprint('messages_bp', __name__,

                    static_folder= 'static',
                        template_folder= 'template',
                        static_url_path= '/messages/static')

from . import routes