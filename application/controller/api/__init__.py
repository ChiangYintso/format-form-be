from flask import Blueprint

api_blueprint = Blueprint('api_blueprint', __name__)

from . import wx_login
from .form_templates import FormTemplatesAPI

api_blueprint.add_url_rule('/form_templates',
                           view_func=FormTemplatesAPI.as_view('form_templates'),
                           methods=['POST', ])

# print(id(api_blueprint))
# print(id(wx_login.api_blueprint))
