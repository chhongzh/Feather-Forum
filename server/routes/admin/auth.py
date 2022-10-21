# ---------------------------------------------------------------------------
from hashlib import sha256
from uuid import uuid4
from flask import Blueprint, request
from lib.request import buildRequest
from lib.request import request_parse
from lib.code import Code
from lib import share
from lib.authkey import validate_super
from time import sleep, time
from lib.database import query
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
lock = share.lock
c = share.c
conn = share.conn
log = share.log
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
blueprint = Blueprint('adminauth', __name__)
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------


@blueprint.route("/login", methods=["POST"])
def Login():
    data = request_parse(request)
    if (data.get('name', None) is None or
            data.get('pw', None) is None
        ):
        return buildRequest(Code.REQUEST_BAD_QUERY, "用户名或密码为空")
    i = query("""SELECT * FROM admin WHERE name=(?)""",
              [data.get('name')], one=True)
    if (i is None):
        return buildRequest(Code.REQUEST_USER_LOG_ERROR, "登录失败,用户名或密码错误!")
    if (i['pw'] == sha256(bytes(data.get('pw'), encoding='utf8')).hexdigest()):
        authkey = str(uuid4())
        query(f"""
        UPDATE admin SET "authkey"=(?),"last"=(?) WHERE "name"=(?) and "pw"=(?)
        """, [authkey, time(), i['name'], i['pw']])
        conn.commit()
        return buildRequest(Code.REQUEST_OK, "登录成功", authkey=authkey)
    else:
        return buildRequest(Code.REQUEST_USER_LOG_ERROR, "登录失败,用户名或密码错误!")

# ---------------------------------------------------------------------------
