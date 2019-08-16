# -*- coding: utf-8 -*-
from bson import ObjectId
from application.utils.json_validator import (
    JsonValidator,
    StringValidator
)


class FormDataModel:
    __validator = JsonValidator(validator={
        'object_id': StringValidator(min_length=1)
    }, enable_extra_key=True)

    @classmethod
    def __validate(cls, data: dict):
        return cls.__validator.validate(data)

    @classmethod
    def post_form_data(cls, current_app, data: dict) -> bool:
        """
        Validate and Write form data to MongoDB.
        :param current_app: Current Flask instance.
        :param data: Form data received from mini program.
        :return: A boolean represents whether form data is successfully saved.
        """
        if cls.__validate(data):
            res = current_app.mongo.db.form_templates.update_one(
                filter={'_id': ObjectId(data['object_id'])},
                update={
                    '$push': {'form_data': data['form_data']}
                }
            )
            return res.matched_count > 0
        else:
            return False
