#app/route/admin/__init__.py

from flask import Blueprint


admin_routes = Blueprint('admin_routes', __name__, url_prefix='/admin')
