import os

from flask import Flask


class Application(Flask):
    def __init__(self, import_name, root_path=None):
        super(Application, self).__init__(import_name, root_path=root_path)
        self.config.from_pyfile('application/config/base_settings.py')
        self.config.from_pyfile('.flaskenv')
        self.config.from_pyfile('application/config/{}_settings.py'.format(self.config['FLASK_ENV']))


app = Application(__name__, root_path=os.getcwd())
