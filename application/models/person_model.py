# -*- coding: utf-8 -*-

from bson import ObjectId
import requests
from .form_data_model import FormDataModel
from application.utils.exception.custom_exception import CustomException
from wx_secret import APP_SECRET, APP_ID, AUTH_URL


class PersonModel:
    def __init__(self, current_app, open_id):
        self.__current_app = current_app
        self.__open_id = open_id
        self.__form_temps = []
        self.__form_data = []

    def write_form_temp(self, form_temp_id):
        res = self.__current_app.mongo.db.people.update_one({
            '_id': self.__open_id
        }, {
            '$push': {'form_temps': ObjectId(form_temp_id)}
        }, upsert=True)
        return res.matched_count >= 0

    def write_form_data(self, form_temp_id):
        res = self.__current_app.mongo.db.people.update_one({
            '_id': self.__open_id
        }, {
            '$addToSet': {'form_data': ObjectId(form_temp_id)}
        }, upsert=True)

        return res.matched_count >= 0

    def get_launched_forms(self) -> list:
        _res = self.__current_app.mongo.db.people.find_one(filter={
            '_id': self.__open_id
        }, projection={'_id': False, 'form_temps': True})
        if _res is None:
            return []

        _form_temps = _res['form_temps']

        res = list(self.__current_app.mongo.db.form_templates.find(filter={
            '_id': {'$in': _form_temps}
        }))

        for i in res:
            i['created_at'] = i['_id'].generation_time
            i['_id'] = str(i['_id'])

        return res

    def post_form_data(self, data: dict) -> bool:
        """ POST /form_data
        :param data: Form data
        :return: Whether successfully write data to db
        """
        if FormDataModel.write_form_data(self.__current_app, data):
            if self.write_form_data(data['object_id']):
                return True

        return False

    def get_involved_forms(self) -> list:
        _res = self.__current_app.mongo.db.people.find_one(
            filter={
                '_id': self.__open_id
            },
            projection={
                '_id': False,
                'form_data': True
            })

        _form_temp_id_arr = _res.get('form_data')
        if _form_temp_id_arr is None:
            return []

        res = list(self.__current_app.mongo.db.form_templates.find(
            filter={
                '_id': {'$in': _form_temp_id_arr}
            }
        ))
        for form_data in res:
            form_data['form_data'] = list(
                filter(lambda x: x['open_id'] == self.__open_id,
                       form_data['form_data'])
            )
            form_data['created_at'] = form_data['_id'].generation_time
            form_data['_id'] = str(form_data['_id'])

        return res

    def delete_form_temp(self, form_temp_id):
        _res = self.__current_app.mongo.db.people.update_one({
            '_id': self.__open_id,
        }, update={
          '$pull': {'form_temps': ObjectId(form_temp_id)}
        })

        if _res.matched_count <= 0:
            raise CustomException(5000, 'server error', status_code=500)

    @classmethod
    def auth_wx_login(cls, js_code,
                      auth_url=AUTH_URL,
                      app_id=APP_ID,
                      secret=APP_SECRET,
                      grant_type='authorization_code'
                      ) -> dict:

        if type(js_code) is not str:
            raise TypeError('TypeError in function auth_wx_login: js_code must be string')
        _url = auth_url.format(app_id, secret, js_code, grant_type)
        response = requests.get(_url)

        return response.json()

    def check_repeat_filling(self, form_temp_id) -> bool:

        res = self.__current_app.mongo.db.people.find_one(
            filter={
                '_id': self.__open_id,
                'form_data': ObjectId(form_temp_id)
            }
        )

        if res is not None:
            raise CustomException(3000, 'repeat filling')
