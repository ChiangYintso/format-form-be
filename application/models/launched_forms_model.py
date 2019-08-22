from bson import ObjectId

from .person_model import PersonModel
from application.utils.exception.custom_exception import CustomException


class LaunchedFormsModel:

    def __init__(self, current_app, open_id):
        self.__current_app = current_app
        self.__person = PersonModel(self.__current_app, open_id)

    def patchLaunchedForms(self, form_temp_id: str, date_time: str):
        if date_time == 'now':
            res = self.__current_app.mongo.db.form_templates.update_one({
                '_id': ObjectId(form_temp_id)
            }, {
                'type': 'ended'
            })
        else:
            res = self.__current_app.mongo.db.form_templates.update_one({
                '_id': ObjectId(form_temp_id)
            }, {
                'end_time': date_time
            })

        if res.matched_count <= 0:
            raise CustomException(3000, 'invalid data', 300)
