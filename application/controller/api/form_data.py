# -*- coding: utf-8 -*-
import json
from flask import request, make_response, current_app
from flask.views import MethodView
from application.models.person_model import PersonModel


class FormDataAPI(MethodView):
    def post(self):
        data: dict = json.loads(request.data)
        print(data)
        person = PersonModel(current_app, data['open_id'])
        if person.post_form_data(data):
            response = make_response({
                'err_code': 0,
                'err_msg': 'ok',
                'request': 'GET /form_data'
            })
        else:
            response = make_response({
                'err_code': 5101,
                'err_msg': 'form deleted',
                'request': 'GET /form_data'
            })
        response.mimetype = 'application/json'
        return response
