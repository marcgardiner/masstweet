#app/route/user/__init__.py

from flask import Blueprint


user_routes = Blueprint('user_routes', __name__, url_prefix='/user')

