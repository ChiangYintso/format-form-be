# -*- coding: utf-8 -*-
from bson import ObjectId
from application.utils.json_validator import (
    JsonValidator,
    StringValidator
)


class FormDataModel:
    __validator = JsonValidator(validator={
        'open_id': StringValidator(min_length=1),
        'object_id': StringValidator(min_length=1)
    }, enable_extra_key=True)

    @classmethod
    def __validate(cls, data: dict):
        return cls.__validator.validate(data)

    @classmethod
    def write_form_data(cls, current_app, data: dict) -> bool:
        """
        Validate and Write form data to MongoDB.
        :param current_app: Current Flask instance.
        :param data: Form data received from mini program.
                        {
                            'form_data': <value>,
                            'object_id': <value>,
                            'open_id': <value>,
                            'form_types': <value>
                        }
        :return: A boolean represents whether form data is successfully saved.
        """

        if cls.__validate(data):
            res = current_app.mongo.db.form_templates.update_one(
                filter={'_id': ObjectId(data['object_id'])},
                update={
                    '$addToSet': {
                        'form_data': {
                            'answer': data['form_data'],
                            'open_id': data['open_id']
                        }
                    }
                }
            )

            if res.matched_count > 0:
                _idx = 0
                _data_idx = 0
                for ans_type in data['form_types']:
                    if ans_type == 'radio' and data['form_data'][_data_idx] != '':
                        current_app.mongo.db.form_templates.update_one(
                            filter={'_id': ObjectId(data['object_id'])},
                            update={
                                '$inc': {
                                    'statistical_results.{}.res.{}'.format(_idx, data['form_data'][_data_idx]): 1
                                }
                            }
                        )
                    elif ans_type == 'select':
                        for j in data['form_data'][_data_idx]:
                            current_app.mongo.db.form_templates.update_one(
                                filter={'_id': ObjectId(data['object_id'])},
                                update={
                                    '$inc': {
                                        'statistical_results.{}.res.{}'.format(_idx, j): 1
                                    }
                                }
                            )
                    else:
                        _idx -= 1
                    _idx += 1
                    _data_idx += 1

            return True
        else:
            return False
