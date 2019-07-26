import os

from flask import Flask
from application.controller.api import api_blueprint


class Application(Flask):
    def __init__(self, import_name, root_path=None):
        super(Application, self).__init__(import_name, root_path=root_path)
        self.config.from_pyfile('.flaskenv')
        self.config.from_pyfile('{}_settings.py'.format(self.config['FLASK_ENV']))


app = Application(__name__, root_path=os.getcwd())

app.register_blueprint(api_blueprint)
