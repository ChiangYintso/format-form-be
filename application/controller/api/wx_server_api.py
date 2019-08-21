from flask import request, make_response, current_app

from application.models.wx_backend import get_qr_code
from application.models.person_model import PersonModel
from application.utils.exception.custom_exception import CustomException
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
    wx_res = PersonModel.auth_wx_login(js_code=js_code)
    print(wx_res)
    # TODO: save session_key
    # TODO： merge requests

    if 'openid' not in wx_res:
        return make_response({
            'err_msg': 'server error',
            'err_code': '5000'
        }, 500)

    person = PersonModel(current_app, open_id=wx_res['openid'])
    launched_forms = person.get_launched_forms()
    response = make_response({
        'err_code': 0,
        'err_msg': 'ok',
        'forms': launched_forms,
        'open_id': wx_res['openid'],
        'request': 'POST /wx_login'
    })

    return response


@api_blueprint.route('/wx_get_qr_code', methods=['POST'])
def wx_get_qr_code():
    data = request.get_json()
    print(data)
    get_qr_code(data['_id'])
    return 'abc'
