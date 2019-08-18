import json
from flask import request, make_response, current_app
from flask.views import MethodView

from application.models.form_templates_model import FormTemplatesModel


class FormTemplatesAPI(MethodView):
    def get(self):
        object_id = request.args.get('object_id')
        if object_id is None:
            _open_id: str = request.args.get('open_id')
            res = FormTemplatesModel.find_form_template_by_open_id(current_app, _open_id)
            print(res)
            response = make_response({
                'err_code': 0,
                'err_msg': 'ok',
                'request': 'GET /form_templates',
                'form_temps': res
            })
            response.mimetype = 'application/json'
            return response
        else:
            res = FormTemplatesModel.find_one_form_template_by_id(current_app, object_id)
            print(res)
            response = make_response({
                'err_code': 0,
                'err_msg': 'ok',
                'request': 'GET /form_templates/?object_id=OBJECT_ID',
                'form_temp': res
            })
            response.mimetype = 'application/json'
            return response

    def post(self):
        data: dict = json.loads(request.data)
        if data is None:
            response = make_response({
                'err_msg': 'no data',
                'err_code': '4002'
            }, 400)
            response.mimetype = 'application/json'
            return response

        # If data is valid and successfully inserted into database,
        # res is value of '_id', or res is False.

        res = FormTemplatesModel.insert_a_document(
            current_app, data)
        if res is False:
            response = make_response({
                'err_msg': 'invalid data',
                'err_code': '4002'
            }, 400)
            response.mimetype = 'application/json'
            return response
        else:
            res = str(res.inserted_id)
            response = make_response({
                'error_code': 0,
                'msg': 'ok',
                'request': 'POST /form_templates',
                'form_temp_id': res
            }, 201)
            response.mimetype = 'application/json'
            return response

    def delete(self):
        query: dict = request.get_json()
        res = FormTemplatesModel.del_form_template(current_app, query['_id'], query['open_id'])
        if res['n'] == 1:
            response = make_response({
                'error_code': 0,
                'msg': 'ok',
                'request': 'DELETE /form_templates',
            }, 200)
            response.mimetype = 'application/json'
            return response
