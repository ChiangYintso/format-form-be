import json
import os

from flask import request, make_response, current_app, send_from_directory
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
