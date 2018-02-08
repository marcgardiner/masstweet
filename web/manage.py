#manage.py

import os
import unittest

from flask_script import Manager, prompt_bool
from flask_migrate import Migrate, MigrateCommand

from app import db, create_app
from app import models


app = create_app(config_name=os.getenv('environment'))
migrate = Migrate(app, db)
manager = Manager(app)


manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """test command"""
    tests = unittest.TestLoader().discover('./tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def create_db():
    """Creates the db tables."""
    db.create_all()


@manager.command
def drop_db():
    """Drops the db tables."""
    if prompt_bool("Are you sure you want to lose all your data"):
        db.drop_all()


@manager.command
def create_admin():
    """Creates the admin user."""
    # db.session.add(
    #     User(username='admin',
    #          password='admin',
    #          admin=True,
    #          account_limit=3))
    # db.session.commit()


if __name__ == '__main__':
    manager.run()
