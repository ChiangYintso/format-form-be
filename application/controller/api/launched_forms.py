import json

from flask import request, make_response, current_app, send_from_directory
from flask.views import MethodView

from application.models.form_templates_model import FormTemplatesModel
from application.models.launched_forms_model import LaunchedFormsModel
from application.models.person_model import PersonModel
from application.utils.exception.custom_exception import CustomException


class LaunchedFormsAPI(MethodView):
    url = '/launched_forms'

    def get(self):
        """
        GET /launched_forms
        :return:
        """
        _open_id: str = request.args.get('open_id')
        if _open_id is None:
            return make_response({
                'err_code': 3000,
                'err_msg': 'no argument "open_id"',
                'request': 'GET /launched_forms'
            })
        person = PersonModel(current_app, _open_id)
        res: list = person.get_launched_forms()

        return make_response({
            'err_code': 0,
            'err_msg': 'ok',
            'request': 'GET /launched_forms',
            'forms': res
        })

    def post(self):
        """
        Create a form template.
        :return:
        """
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
                'request': 'POST /launched_forms',
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


class LaunchedFormsExcelAPI(MethodView):
    url = '/launched_forms/excel'

    def get(self):
        try:
            open_id = request.args.get('open_id')
            form_id = request.args.get('form_id')

            launched_forms_model = LaunchedFormsModel(current_app, open_id)

            launched_forms_model.generate_excel(form_id)
        except CustomException as e:
            return e.make_response('GET /launched_forms/excel')

        res = make_response(
            send_from_directory(
                directory=current_app.root_path+'/application/static/excel/',
                filename='{}.xlsx'.format(form_id)
            )
        )
        res.mimetype = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        return res
