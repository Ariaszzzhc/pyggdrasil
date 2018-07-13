import os

from flask_script import Manager, Server

from pyggdrasil import create_app

app = create_app(os.getenv('PYGGDRASIL_ENV') or 'dev')
manager = Manager(app)
manager.add_command("server", Server())


@manager.shell
def make_shell_context():
    return dict(app=app)


if __name__ == '__main__':
    manager.run()
