# -*- coding: utf-8 -*-
import json
from flask import request, make_response, current_app
from flask.views import MethodView
from application.models.form_data_model import FormDataModel


class FormDataAPI(MethodView):
    def post(self):
        data: dict = json.loads(request.data)
        print(data)
        if FormDataModel.post_form_data(current_app, data):
            response = make_response({
                'err_code': 0,
                'err_msg': 'ok',
                'request': 'GET /form_data'
            })
        else:
            response = make_response({
                'err_code': 5000,
                'err_msg': 'server error',
                'request': 'GET /form_data'
            })
        response.mimetype = 'application/json'
        return response
