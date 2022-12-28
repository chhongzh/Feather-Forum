"""
此文件属于Feather-Forum!
© 2021 chhongzh

与用户鉴权相关的视图
"""


from hashlib import sha256
from uuid import uuid4
from flask import Blueprint, request
from lib.request import build_request
from lib.request import request_parse
from lib.returncode import ReturnCode
from lib import share
from time import time
from lib.database import query


lock = share.lock
c = share.c
conn = share.conn
log = share.log


blueprint = Blueprint('adminauth', __name__)


@blueprint.route("/login", methods=["POST"])
def Login():
    data = request_parse(request)
    if (data.get('name', None) is None or
                data.get('pw', None) is None
            ):
        return build_request(ReturnCode.REQUEST_BAD_QUERY, "用户名或密码为空")
    i = query("""SELECT * FROM admin WHERE name=(?)""",
              [data.get('name')], one=True)
    if (i is None):
        return build_request(ReturnCode.REQUEST_USER_LOG_ERROR, "登录失败,用户名或密码错误!")
    if (i['pw'] == sha256(bytes(data.get('pw'), encoding='utf8')).hexdigest()):
        authkey = str(uuid4())
        query(f"""
        UPDATE admin SET "authkey"=(?),"last"=(?) WHERE "name"=(?) and "pw"=(?)
        """, [authkey, time(), i['name'], i['pw']])
        conn.commit()
        return build_request(ReturnCode.REQUEST_OK, "登录成功", authkey=authkey)
    else:
        return build_request(ReturnCode.REQUEST_USER_LOG_ERROR, "登录失败,用户名或密码错误!")
