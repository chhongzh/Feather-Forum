# ---------------------------------------------------------------------------
from flask import Blueprint, request
from lib.request import buildRequest
from lib.request import request_parse
from lib.code import Code
from lib.database import getConfigByKey
from lib import share
from math import ceil
from lib.database import query
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
lock = share.lock
c = share.c
conn = share.conn
log = share.log
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
blueprint = Blueprint('userlist', __name__)
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------


@blueprint.route("/list", methods=["GET"])
def ListUser():
    data = request_parse(request)
    p = int(getConfigByKey('itemLimit'))
    page = p * \
        data.get('page', default=0, type=int)

    obj = query(
        "SELECT name,uid,coin,time,last,avartar FROM user LIMIT (?) OFFSET (?)", [p, page])
    return buildRequest(Code.REQUEST_OK, "查询成功", list=obj)
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
@blueprint.route("/top")
def TopUser():
    obj = []
    obj = query("""
            SELECT name,uid,coin,time,last,avartar FROM user ORDER BY uid DESC LIMIT 5
        """)
    return buildRequest(Code.REQUEST_OK, "查询成功", list=obj)
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
@blueprint.route("/count", methods=["GET"])
def CountUser():
    return buildRequest(Code.REQUEST_OK, '查询成功', count=query("SELECT count(*) FROM user", one=True)['count(*)'])
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
@blueprint.route("/page")
def PageUser():
    total = 0
    total = query('SELECT count(*) FROM user', one=True)['count(*)']
    page = int(getConfigByKey('itemLimit'))
    total = ceil(total/page)

    return buildRequest(Code.REQUEST_OK, msg="查询成功", page=total-1)
# ---------------------------------------------------------------------------
