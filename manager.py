"""entrance of application
"""

from flask_script import Manager, Server
from application import app

manager = Manager(app)

# flask shell command
manager.add_command("runserver",
                    Server(host=app.config['SERVER_HOST'],
                           port=app.config['SERVER_PORT'],
                           use_debugger=app.config['DEBUG']))


def main():
    manager.run()


if __name__ == '__main__':
    try:
        import sys
        sys.exit(main())
    except Exception as e:
        import traceback
        traceback.print_exc()
