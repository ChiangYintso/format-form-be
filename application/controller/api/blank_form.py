from flask import request, make_response, current_app
from flask.views import MethodView

from application.models.form_templates_model import FormTemplatesModel
from application.utils.exception.custom_exception import CustomException


class BlankFormAPI(MethodView):

    """ Corresponding mini program `/pages/fillIn/fillIn`.
    The client request for open_id and blank form.
    """
    def get(self):

        _object_id = request.args.get('object_id')
        _js_code = request.args.get('code')

        try:
            res = FormTemplatesModel.login_and_send_blank_form(
                js_code=_js_code,
                current_app=current_app,
                form_temp_id=_object_id
            )
        except CustomException as e:
            return e.make_response('GET /blank_form')

        response = make_response({
            'err_code': 0,
            'err_msg': 'ok',
            'request': 'GET /form_templates/?object_id=OBJECT_ID',
            'form_temp': res[0],
            'open_id': res[1]
        })
        response.mimetype = 'application/json'
        return response
