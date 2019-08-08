from flask import request, jsonify, make_response

from application.utils.wx_login import auth_wx_login
from . import api_blueprint


@api_blueprint.route('/wx_login', methods=['POST'])
def wx_login():
    data = request.get_json()
    if 'code' not in data:
        response = make_response({
            'err_msg': 'argument code is not defined',
            'err_code': '4002'
        }, 400)
        response.mimetype = 'application/json'
        return response
    js_code = data['code']
    response = auth_wx_login(js_code=js_code)
    print(response)
    # TODO: save session_key
    if 'openid' in response:
        return jsonify(open_id=response['openid'])
    else:
        response = make_response({
            'err_msg': 'server error',
            'err_code': '5000'
        }, 500)
        response.mimetype = 'application/json'
        return response
