""" entrance of application
"""
import logging
from logging.handlers import RotatingFileHandler, SMTPHandler
import os
import traceback
from flask_mail import Mail
# from flask_apscheduler import APScheduler
from application import Application

app = Application(__name__, root_path=os.getcwd())
app.logger.setLevel(logging.INFO)
mail = Mail(app)


@app.route('/error')
def err():
    raise NotImplementedError


def register_file_logger():
    file_handler = RotatingFileHandler(
        'logs/err_log.log',
        maxBytes=10*1024*1024,
        backupCount=1
    )
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)


def register_mail_logger():
    mail_handler = SMTPHandler(
        mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
        fromaddr=app.config['MAIL_USERNAME'],
        toaddrs=app.config['MAIL_DEFAULT_SENDER'],
        subject='Format-form-be Error',
        credentials=(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
    )
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(formatter)
    app.logger.addHandler(mail_handler)


def main():
    # scheduler = APScheduler()
    # scheduler.init_app(app=app)
    # scheduler.start()
    # register_mail_logger()
    register_file_logger()
    app.run(host=app.config['FLASK_RUN_HOST'], port=8000)


if __name__ == '__main__':
    try:
        import sys
        from werkzeug.middleware.proxy_fix import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)
        sys.exit(main())
    except Exception as e:
        traceback.print_exc()
