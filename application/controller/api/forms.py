from flask import request, make_response
from flask.views import MethodView
from application import mongo
from datetime import datetime


class FormAPI(MethodView):
    def get(self, open_id):
        pass

    def post(self, open_id):
        if open_id is None:
            response = make_response({
                'err_msg': 'argument openid is not found',
                'err_code': '4002'
            }, 400)
            response.mimetype = 'application/json'
            return response
        doc = {

        }
        mongo.db.forms.insert_one(doc)
