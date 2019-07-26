from flask import request
from . import api_blueprint


@api_blueprint.route('/wx_login', methods=['POST'])
def wx_login():
    print(request.data)
    return request.data
