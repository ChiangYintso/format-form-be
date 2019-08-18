""" entrance of application
"""

from flask_apscheduler import APScheduler
#from flask_script import Manager, Server
from application import app

# manager = Manager(app)

# flask shell command
#manager.add_command("runserver",
#                   Server(host=app.config['FLASK_RUN_HOST'],
#                        port=app.config['FLASK_RUN_PORT'],
#                        use_debugger=app.config['DEBUG']))

def main():
    scheduler = APScheduler()
    scheduler.init_app(app=app)
    scheduler.start()
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
