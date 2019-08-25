from bson import ObjectId
from openpyxl import Workbook

from .person_model import PersonModel
from application.utils.exception.custom_exception import CustomException


class LaunchedFormsModel:

    def __init__(self, current_app, open_id):
        self.__current_app = current_app
        self.__person = PersonModel(self.__current_app, open_id)

    def put_launched_forms(self, form_temp_id: str, date_time: str):
        if date_time == 'now':
            res = self.__current_app.mongo.db.form_templates.update_one({
                '_id': ObjectId(form_temp_id)
            }, {
                '$set': {'type': 'ended'}
            })
        else:
            res = self.__current_app.mongo.db.form_templates.update_one({
                '_id': ObjectId(form_temp_id)
            }, {
                '$set': {'end_time': date_time}
            })

        if res.matched_count <= 0:
            raise CustomException(3000, 'invalid data', 300)

    def generate_excel(self, form_id):
        res = self.__current_app.mongo.db.form_templates.find_one({
            '_id': ObjectId(form_id),
            'open_id': self.__person.get_open_id()
        }, projection={
            'title': True,
            'questions': True,
            'form_data': True
        })

        if res is None:
            raise CustomException(3000, 'invalid data', 200)

        wb = Workbook()

        ws1 = wb.active
        ws1.merge_cells('A1:D1')
        ws1.cell(1, 1).value = res['title']

        ws1.append([item['desc'] for item in res['questions']])

        for people in res['form_data']:
            row = []
            order = 0
            for ans in people['answer']:
                if res['questions'][order]['type'] == 'radio':
                    row.append(res['questions'][order]['detail'][int(ans)])
                elif res['questions'][order]['type'] == 'essay':
                    row.append(ans)
                else:
                    s = ''
                    for option in ans:
                        s += res['questions'][order]['detail'][int(option)]+';'
                    row.append(s)
                order += 1
            ws1.append(row)

        dirname = './application/static/excel/{}.xlsx'.format(form_id)
        wb.save(filename=dirname)
