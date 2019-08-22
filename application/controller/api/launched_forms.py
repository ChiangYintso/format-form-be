import json

from flask import request, make_response, current_app
from flask.views import MethodView
from application.models.launched_forms_model import LaunchedFormsModel


class LaunchedFormsAPI(MethodView):
    url = '/launched_forms'

    def patch(self):
        data: dict = json.loads(request.data)

        launched_forms_model = LaunchedFormsModel(current_app, data['open_id'])
        launched_forms_model.patchLaunchedForms(data['form_temp_id'], data['date_time'])

        return make_response({
            'err_code': 0,
            'err_msg': 'ok',
            'request': 'PATCH /launched_forms'
        })
