import json
from flask import request, make_response, current_app
from flask.views import MethodView

from application.models.form_templates_model import FormTemplatesModel
from application.models.person_model import PersonModel


class FormTemplatesAPI(MethodView):
    def get(self):

        # GET /form_templates
        _open_id: str = request.args.get('open_id')
        person = PersonModel(current_app, _open_id)
        res: list = person.get_launched_forms()

        return make_response({
            'err_code': 0,
            'err_msg': 'ok',
            'request': 'GET /form_templates',
            'forms': res
        })

    def post(self):
        data: dict = json.loads(request.data)
        if data is None:
            return make_response({
                'err_msg': 'no data',
                'err_code': '4002'
            }, 400)

        # If data is valid and successfully inserted into database,
        # res is value of '_id', or res is False.
        res = FormTemplatesModel.generate_a_form_temp(
            current_app, data)
        if res is False:
            return make_response({
                'err_msg': 'invalid data',
                'err_code': '4002'
            }, 400)
        else:
            return make_response({
                'error_code': 0,
                'msg': 'ok',
                'request': 'POST /form_templates',
                'form_temp_id': res
            }, 201)

    def delete(self):
        query: dict = request.get_json()
        res = FormTemplatesModel.del_form_template(current_app, query['_id'], query['open_id'])
        if res['n'] == 1:
            person = PersonModel(current_app, query['open_id'])
            person.delete_form_temp(query['_id'])
            return make_response({
                'error_code': 0,
                'msg': 'ok',
                'request': 'DELETE /form_templates',
            }, 200)
