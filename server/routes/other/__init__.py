
from flask import Blueprint, request
from lib.request import build_request
from lib.request import request_parse
from lib.returncode import ReturnCode
from lib import share
from lib.authkey import get_user_by_authkey


lock = share.lock
c = share.c
conn = share.conn
log = share.log


blueprint = Blueprint('other', __name__, url_prefix='/api')


@blueprint.route('/authkey/v', methods=["POST"])
def apiAuthkeyValidate():
    data = request_parse(request)
    if (data.get("authkey") is None):
        return build_request(ReturnCode.REQUEST_BAD_QUERY, "缺少Authkey")

    if (get_user_by_authkey(data.get('authkey'))):
        return build_request(ReturnCode.REQUEST_OK, "有效的Authkey", authkey=True)
    return build_request(ReturnCode.REQUEST_BAD_AUTHKEY, "无效Authkey", authkey=False)
