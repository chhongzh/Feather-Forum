# ---------------------------------------------------------------------------
from flask import Blueprint, request
from lib.request import buildRequest
from lib.request import request_parse
from lib.code import Code
from time import time
from lib import share
from hashlib import sha256
from uuid import uuid4
from lib.database import query
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
lock = share.lock
c = share.c
conn = share.conn
log = share.log
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
blueprint = Blueprint('userauth', __name__)
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------


@blueprint.route("/register", methods=["POST"])
def Register():
    data = request_parse(request)
    if (data.get('name', None) is None or
            data.get('pw', None) is None or
            data.get('email', None) is None
            ):
        return buildRequest(Code.REQUEST_BAD_QUERY, "用户名或密码或email为空")
    for _ in query("SELECT name FROM user WHERE name=(?)", [data.get('name')]):
        return buildRequest(Code.REQUEST_USER_REG_ERROR, "用户名已存在")
    name = data.get('name')
    pw = data.get('pw')
    email = data.get('email')
    query("""
                INSERT INTO user (name,password,email,time,last,authkey,uuid)
                VALUES ((?),(?),(?),(?),0,Null,(?))
            """,
          [name,
           str(sha256(bytes(pw, encoding='utf8')).hexdigest()),
           str(email),
           int(time()),
           str(uuid4())
           ])
    conn.commit()
    return buildRequest(Code.REQUEST_OK, "注册成功")

# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------


@blueprint.route("/login", methods=["POST"])
def Login():
    data = request_parse(request)
    if (data.get('name', None) is None or
            data.get('pw', None) is None
            ):
        return buildRequest(Code.REQUEST_BAD_QUERY, "用户名或密码为空")
    i = query("""SELECT * FROM user WHERE name=(?)""",
              [data.get('name')], one=True)
    if (i is None):
        return buildRequest(Code.REQUEST_USER_LOG_ERROR, "登录失败,用户名或密码错误!")
    if (i['password'] == sha256(bytes(data.get('pw'), encoding='utf8')).hexdigest()):
        authkey = str(uuid4())
        query(f"""
        UPDATE user SET "authkey"=(?),"last"=(?) WHERE "name"=(?) and "password"=(?)
        """, [authkey, time(), i['name'], i['password']])
        conn.commit()
        return buildRequest(Code.REQUEST_OK, "登录成功", authkey=authkey)
    else:
        return buildRequest(Code.REQUEST_USER_LOG_ERROR, "登录失败,用户名或密码错误!")

# ---------------------------------------------------------------------------
