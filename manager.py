""" entrance of application
"""

from flask_apscheduler import APScheduler
from application import app


def main():
    # scheduler = APScheduler()
    # scheduler.init_app(app=app)
    # scheduler.start()
    app.run(port=8000)


if __name__ == '__main__':
    try:
        import sys
        from werkzeug.contrib.fixers import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)
        sys.exit(main())
    except Exception as e:
        import traceback
        traceback.print_exc()
