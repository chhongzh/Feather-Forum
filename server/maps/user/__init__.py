# ---------------------------------------------------------------------------
from . import list
from . import auth
from . import follow
from . import info
from flask import Blueprint
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
blueprint = Blueprint('user', __name__, url_prefix='/api/user')
blueprint.register_blueprint(list.blueprint)
blueprint.register_blueprint(auth.blueprint)
blueprint.register_blueprint(follow.blueprint)
blueprint.register_blueprint(info.blueprint)
# ---------------------------------------------------------------------------
