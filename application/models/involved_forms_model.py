from application.models.person_model import PersonModel


class InvolvedFormsModel:
    def __init__(self, current_app, open_id):
        self.__current_app = current_app
        self.__person = PersonModel(self.__current_app, open_id)

    def get_involved_forms(self):
        form_temp_ids = self.__person.get_involved_forms_ids()

        involved_forms = list(self.__current_app.mongo.db.form_templates.find(
            filter={
                '_id': {'$in': form_temp_ids}
            }
        ))
        for form in involved_forms:

            # filter user's answers by his open_id
            form['form_data'] = list(
                filter(lambda x: x['open_id'] == self.__person.get_open_id(),
                       form['form_data'])
            )
            form['created_at'] = form['_id'].generation_time
            form['_id'] = str(form['_id'])

        return involved_forms
