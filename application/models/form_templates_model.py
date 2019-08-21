# -*- coding: utf-8 -*-

from bson import ObjectId

from application.utils.exception.custom_exception import CustomException
from application.utils.json_validator import (
    JsonValidator,
    StringValidator,
    ArrayValidator
)
from .person_model import PersonModel


class FormTemplatesModel:
    validator = JsonValidator({
            'open_id': StringValidator(min_length=1),
            'title': StringValidator(min_length=1),
            'type': StringValidator(min_length=1),
            'start_time': StringValidator(required=False,
                                          min_length=12,
                                          max_length=12,
                                          re='[0-9]{12}'),
            'end_time': StringValidator(required=False,
                                        min_length=12,
                                        max_length=12,
                                        re='[0-9]{12}'),
            'questions': ArrayValidator(
                arr_temp=JsonValidator(
                    validator={
                        'type': StringValidator(min_length=1)
                    },
                    enable_extra_key=True
                ),
                required=True
            )
        },
        enable_extra_key=True)

    @classmethod
    def generate_a_form_temp(cls, current_app, doc: dict):
        """
        :param current_app: global instance of Flask app.
        :param doc: document to be insert.
        :return: if 'doc' is valid and successfully inserted to database,
                 return an instance of InsertOneResult(see document of pymongo).
                 If failed, return False.
        """
        if cls.validate(doc):
            doc['form_data'] = []
            doc['statistical_results'] = cls.__generate_statistical_results(doc['questions'])
            res = current_app.mongo.db.form_templates.insert_one(doc)
            _inserted_id = str(res.inserted_id)
            person = PersonModel(current_app, doc['open_id'])
            if person.write_form_temp(_inserted_id):
                return _inserted_id
        return False

    @classmethod
    def __generate_statistical_results(cls, questions: list):
        res = []
        for i in range(len(questions)):
            if questions[i]['type'] == 'select' or questions[i]['type'] == 'radio':
                res.append({
                    'qid': i,
                    'desc': questions[i]['desc'],
                    'res': [0, ] * len(questions[i]['detail'])
                })
        return res

    @classmethod
    def validate(cls, data):
        return cls.validator.validate(data)

    @classmethod
    def del_form_template(cls, current_app, object_id, open_id):
        _query = {'_id': ObjectId(object_id), 'open_id': open_id}
        res = current_app.mongo.db.form_templates.delete_one(_query)
        return res.raw_result

    @classmethod
    def find_one_form_template_by_id(cls, current_app, _id):
        """
        Fill in the form
        :param current_app:
        :param _id:
        :return:
        """
        res = current_app.mongo.db.form_templates.find_one({
            '_id': ObjectId(_id)
        }, projection={
            'form_data': False,
            'open_id': False
        })

        if res is None:
            raise CustomException(5000, 'form not found')
        res['_id'] = str(res['_id'])

        return res

    @classmethod
    def login_and_send_blank_form(cls, js_code, current_app, form_temp_id):

        _user_info = PersonModel.auth_wx_login(js_code=js_code)
        if 'openid' not in _user_info:
            raise CustomException(5000, 'login error')

        person = PersonModel(current_app=current_app,
                             open_id=_user_info['openid'])

        res = cls.find_one_form_template_by_id(current_app, form_temp_id)
        print(res)
        if not res['repeat_filling']:
            person.check_repeat_filling(form_temp_id)

        return res, _user_info['openid']
