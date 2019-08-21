from flask import Blueprint

api_blueprint = Blueprint('api_blueprint', __name__)

from . import wx_server_api
from .form_templates import FormTemplatesAPI
from .form_data import FormDataAPI
from .blank_form import BlankFormAPI

form_templates_view_func = FormTemplatesAPI.as_view('form_templates')
api_blueprint.add_url_rule('/form_templates',
                           view_func=form_templates_view_func,
                           methods=['POST', 'DELETE'])
api_blueprint.add_url_rule('/form_templates',
                           view_func=form_templates_view_func,
                           methods=['GET', ])

form_data_view_func = FormDataAPI.as_view('form_data')
api_blueprint.add_url_rule('/form_data',
                           view_func=form_data_view_func,
                           methods=['POST', 'GET'])

blank_form_view_func = BlankFormAPI.as_view('blank_form')
api_blueprint.add_url_rule('/blank_form',
                           view_func=blank_form_view_func,
                           methods=['GET', ])
