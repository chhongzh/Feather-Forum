# ---------------------------------------------------------------------------
from flask import Blueprint, request
from lib.request import buildRequest
from lib.request import request_parse
from lib.code import code
from time import time
from lib.database import getConfigByKey
from lib import share
from lib.authkey import validate_authkey
from math import ceil
from time import time
from hashlib import sha256
from uuid import uuid4
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
lock = share.lock
c = share.c
conn = share.conn
log = share.log
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
blueprint = Blueprint('other', __name__, url_prefix='/api')
# ---------------------------------------------------------------------------


@blueprint.route('/authkey/v', methods=["POST"])
def apiAuthkeyValidate():
    data = request_parse(request)
    if (data.get("authkey") is None):
        return buildRequest(code.REQUEST_BAD_QUERY, "缺少Authkey")

    if (validate_authkey(data.get('authkey'))):
        return buildRequest(code.REQUEST_OK, "有效的Authkey", authkey=True)
    return buildRequest(code.REQUEST_BAD_AUTHKEY, "无效Authkey", authkey=False)
