from flask import Blueprint

api_blueprint = Blueprint('api_blueprint', __name__)

from . import wx_login
from .form_templates import FormTemplatesAPI

form_templates = FormTemplatesAPI.as_view('form_templates')
api_blueprint.add_url_rule('/form_templates',
                           view_func=form_templates,
                           methods=['POST', ])
api_blueprint.add_url_rule('/form_templates/',
                           defaults={'open_id': None},
                           view_func=form_templates,
                           methods=['GET', ])
