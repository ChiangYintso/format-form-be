from flask import Blueprint

api_blueprint = Blueprint('api_blueprint', __name__)

from . import wx_login

# print(id(api_blueprint))
# print(id(wx_login.api_blueprint))
