""" entrance of application
"""
import os

# from flask_apscheduler import APScheduler
from application import Application

app = Application(__name__, root_path=os.getcwd())


def main():
    # scheduler = APScheduler()
    # scheduler.init_app(app=app)
    # scheduler.start()
    app.run(port=8000)


if __name__ == '__main__':
    try:
        import sys
        from werkzeug.middleware.proxy_fix import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)
        sys.exit(main())
    except Exception as e:
        import traceback
        traceback.print_exc()
