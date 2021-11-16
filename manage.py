import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import create_app, db

env = os.getenv("FLASK_ENV") or "test"
print(f"Active environment: * {env} *")


app = create_app(env)

migrate = Migrate(app, db)

manager = Manager(app)


@manager.command
def run():
    app.run(debug=True)


manager.add_command('db', MigrateCommand)


if __name__ == "__main__":
    manager.run()


