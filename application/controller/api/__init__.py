from flask import Blueprint

api_blueprint = Blueprint('api_blueprint', __name__)

from . import wx_server_api

from .form_data import FormDataAPI
from .blank_form import BlankFormAPI
from .involved_forms import InvolvedFormsAPI
from .launched_forms import LaunchedFormsAPI, LaunchedFormsExcelAPI, LaunchedFormsStatusAPI


form_data_view_func = FormDataAPI.as_view('form_data')
api_blueprint.add_url_rule('/form_data',
                           view_func=form_data_view_func,
                           methods=['POST', ])

blank_form_view_func = BlankFormAPI.as_view('blank_form')
api_blueprint.add_url_rule('/blank_form',
                           view_func=blank_form_view_func,
                           methods=['GET', ])

APIs = {InvolvedFormsAPI, LaunchedFormsAPI, LaunchedFormsExcelAPI, LaunchedFormsStatusAPI}
for API in APIs:
    api_blueprint.add_url_rule(API.url,
                               view_func=API.as_view(API.url[1:]))
