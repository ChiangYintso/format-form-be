import json

from flask import request, make_response, current_app
from flask.views import MethodView
from application.models.launched_forms_model import LaunchedFormsModel
from application.utils.exception.custom_exception import CustomException


class LaunchedFormsAPI(MethodView):
    url = '/launched_forms'

    def put(self):
        data: dict = json.loads(request.data)
        try:
            launched_forms_model = LaunchedFormsModel(current_app, data['open_id'])
            launched_forms_model.put_launched_forms(data['form_temp_id'], data['date_time'])
        except CustomException as e:
            return e.make_response(request_str='PATCH /launched_forms')

        return make_response({
            'err_code': 0,
            'err_msg': 'ok',
            'request': 'PATCH /launched_forms'
        })
