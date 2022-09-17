# ---------------------------------------------------------------------------
from flask import Blueprint, request
from lib.request import buildRequest
from lib.request import request_parse
from lib.code import Code
from lib import share
from lib.authkey import validate_authkey
from time import time
from lib.database import query
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
lock = share.lock
c = share.c
conn = share.conn
log = share.log
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
blueprint = Blueprint('userfollow', __name__)
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------


@blueprint.route("/follow", methods=["POST"])
def FollowUser():
    data = request_parse(request)
    authkey = data.get('authkey', None)
    tofollow = data.get('to', None)
    if (type(tofollow).__name__ == 'str' and tofollow.isdigit()):
        tofollow = int(tofollow)
    if (authkey is None or tofollow is None or tofollow <= 0):
        return buildRequest(Code.REQUEST_BAD_QUERY, "参数错误")
    ak = validate_authkey(authkey)
    if (ak is None):
        return buildRequest(Code.REQUEST_BAD_AUTHKEY, '无法验证authkey')
    val = query('SELECT count(*) FROM user WHERE "uid"=(?)',
                [tofollow], one=True)
    if (val['count(*)'] != 1):
        return buildRequest(Code.REQUEST_BAD_QUERY, 'tofollow不存在')
    for _ in query('SELECT * FROM follow WHERE "from"=(?) and "to"=(?)', (ak['uid'], tofollow)):
        return buildRequest(Code.REQUEST_ERROR, "你已经关注了!")
    if ((ak['uid'] == tofollow)):
        return buildRequest(Code.REQUEST_ERROR, "不能自己关注自己")
    query("INSERT INTO follow ('from','to','time') VALUES ((?),(?),(?))",
          [ak['uid'], tofollow, int(time())])
    conn.commit()
    return buildRequest(Code.REQUEST_OK, "关注成功!")
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------


@blueprint.route("/unfollow", methods=["POST"])
def UnFollowUser():
    data = request_parse(request)
    authkey = data.get('authkey', None)
    unfollow = data.get('to', None)
    if (type(unfollow).__name__ == 'str' and unfollow.isdigit()):
        unfollow = int(unfollow)
    if (authkey is None or unfollow is None or unfollow <= 0):
        return buildRequest(Code.REQUEST_BAD_QUERY, "参数错误")
    ak = validate_authkey(authkey)
    if (ak is None):
        return buildRequest(Code.REQUEST_BAD_AUTHKEY, '无法验证authkey')
    if (query('SELECT count(*) FROM follow WHERE "from"=(?) and "to"=(?)', [ak['uid'], unfollow], one=True)['count(*)'] == 0):
        return buildRequest(Code.REQUEST_BAD_QUERY, "你还没关注这个人!")
    query('DELETE FROM follow WHERE "from"=(?) and "to"=(?)',
          [ak['uid'], unfollow])
    conn.commit()
    return buildRequest(Code.REQUEST_OK, "取消关注成功!")
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------


@blueprint.route("/isfollow", methods=["POST"])
def IsFollowUser():
    data = request_parse(request)
    authkey = data.get('authkey', None)
    unfollow = data.get('to', None)
    if (type(unfollow).__name__ == 'str' and unfollow.isdigit()):
        unfollow = int(unfollow)
    if (authkey is None or unfollow is None or unfollow <= 0):
        return buildRequest(Code.REQUEST_BAD_QUERY, "参数错误")
    ak = validate_authkey(authkey)
    if (ak is None):
        return buildRequest(Code.REQUEST_BAD_AUTHKEY, '无法验证authkey')
    return buildRequest(Code.REQUEST_OK, "查询成功", follow=query('SELECT count(*) FROM follow WHERE "from"=(?) and "to"=(?)', [ak['uid'], unfollow], one=True)['count(*)'] == 1)
# ---------------------------------------------------------------------------
