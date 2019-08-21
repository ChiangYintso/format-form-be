from flask import request, make_response, current_app
from flask.views import MethodView

from application.models.person_model import PersonModel


class InvolvedFormsAPI(MethodView):
    url = '/involved_forms'

    def get(self):
        open_id = request.args.get('open_id')

        if open_id is None:
            return make_response({
                'err_code': 3000,
                'err_msg': 'no argument "open_id"',
                'request': 'GET /involved_forms'
            }, 300)

        person = PersonModel(current_app, open_id)
        involved_forms = person.get_involved_forms()

        return make_response({
            'err_code': 0,
            'err_msg': 'ok',
            'request': 'GET /form_data',
            'forms': involved_forms
        })
