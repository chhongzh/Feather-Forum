
from . import auth
from flask import Blueprint


blueprint = Blueprint('super', __name__, url_prefix='/api/admin')
blueprint.register_blueprint(auth.blueprint)
