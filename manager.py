""" entrance of application
"""

from flask_apscheduler import APScheduler
from flask_script import Manager, Server
from application import app

manager = Manager(app)

# flask shell command
manager.add_command("runserver",
                    Server(host=app.config['FLASK_RUN_HOST'],
                           port=app.config['FLASK_RUN_PORT'],
                           use_debugger=app.config['DEBUG']))


def main():
    scheduler = APScheduler()
    scheduler.init_app(app=app)
    scheduler.start()
    manager.run()


if __name__ == '__main__':
    try:
        import sys
        sys.exit(main())
    except Exception as e:
        import traceback
        traceback.print_exc()
