#/app/__init__.py

"""create flask app and bind to database"""

import os


from flask import Flask
from flask_sqlalchemy import SQLAlchemy


from instance.config import APP_CONFIG
from app.route.user import user_routes
from app.route.admin import admin_routes


db = SQLAlchemy()


def create_app(config_name):
    """create app instance"""

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(APP_CONFIG[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    blueprints = [
        user_routes,
        admin_routes
    ]
    configure_blueprints(app, blueprints)

    return app


def configure_blueprints(app, blueprints):
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
