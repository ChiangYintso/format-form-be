from flask import request, make_response
from flask.views import MethodView
import json


class FormTemplatesAPI(MethodView):
    def get(self, open_id):
        pass

    def post(self):
        data = json.loads(request.data)
        # if request is None:
        response = make_response({
            'err_msg': 'argument openid is not found',
            'err_code': '4002'
        }, 400)
        response.mimetype = 'application/json'
        return response
        # doc = {
        #
        # }
        # mongo.db.forms.insert_one(doc)
