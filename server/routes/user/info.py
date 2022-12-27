
from flask import Blueprint, request
from lib.request import build_request
from lib.request import request_parse
from lib.returncode import ReturnCode
from lib import share
from lib.authkey import get_user_by_authkey
from lib.database import query


lock = share.lock
c = share.c
conn = share.conn
log = share.log


blueprint = Blueprint('userinfo', __name__)


@blueprint.route("/info", methods=["POST"])
def Info():
    data = request_parse(request)
    authkey = data.get('authkey')
    ak = get_user_by_authkey(authkey)
    if (ak):
        return build_request(ReturnCode.REQUEST_OK, "有效的AuthKey",
                             name=ak["name"],
                             uid=ak["uid"],
                             email=ak["email"],
                             coin=ak["coin"],
                             time=ak["regtime"],
                             last=ak["last"],
                             uuid=ak["uuid"],
                             avartar=ak["avartar"],
                             authkey=True
                             )
    else:
        return build_request(ReturnCode.REQUEST_BAD_AUTHKEY, "不存在或过期的AuthKey", authkey=False)


@blueprint.route('/info/<uid>')
def PublicInfo(uid: str):
    if (not uid.isdigit()):
        return build_request(ReturnCode.REQUEST_BAD_QUERY, 'uid必须为数字')
    uid = int(uid)
    if (uid == 0 or uid < 0):
        return build_request(ReturnCode.REQUEST_BAD_QUERY, 'uid不合法')
    for i in query("SELECT * FROM user WHERE uid=(?)", [uid]):
        return build_request(ReturnCode.REQUEST_OK, "查询成功",
                             name=i["name"],
                             uid=i["uid"],
                             email=i["email"],
                             coin=i["coin"],
                             time=i["time"],
                             last=i["last"],
                             uuid=i["uuid"],
                             avartar=i["avartar"],
                             )
    return build_request(ReturnCode.REQUEST_BAD_QUERY, '未知的id')
