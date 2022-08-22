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
blueprint = Blueprint('user', __name__, url_prefix='/api/user')
# ---------------------------------------------------------------------------


@blueprint.route("/register", methods=["POST"])
def apiRegister():
    log.info(f"[客户端:{request.remote_addr}] 请求 -> 注册用户")
    data = request_parse(request)
    if (data.get('name', None) is None or
            data.get('pw', None) is None or
            data.get('email', None) is None
            ):
        log.info("[服务器] -> 错误请求")
        return buildRequest(code.REQUEST_BAD_QUERY, "用户名或密码或email为空")
    for _ in c.execute(f"SELECT name FROM user WHERE name='{data.get('name')}'"):
        return buildRequest(code.REQUEST_USER_REG_ERROR, "用户名已存在")
    name = data.get('name').replace("'", "''").replace('"', '""')
    pw = data.get('pw').replace("'", "''").replace('"', '""')
    email = data.get('email').replace("'", "''").replace('"', '""')
    if (lock.acquire()):
        c.execute(f"""
                INSERT INTO user (name,password,email,time,last,authkey,uuid)
                VALUES ("{name}","{sha256(bytes(pw,encoding='utf8')).hexdigest()}","{email}",{
                        int(time())},0,Null,"{uuid4()}")
            """)
        conn.commit()
        lock.release()
        return buildRequest(code.REQUEST_OK, "注册成功")


@blueprint.route("/login", methods=["POST", "GET"])
def apiLogin():
    log.info(f"[客户端:{request.remote_addr}] 请求 -> 登录用户")
    data = request_parse(request)
    if (data.get('name', None) is None or
            data.get('pw', None) is None
            ):
        log.info("[服务器] -> 错误请求")
        return buildRequest(code.REQUEST_BAD_QUERY, "用户名或密码为空")
    if (lock.acquire()):
        for dname, dpw, duid, demail, dcoin, dtime, dlast, dauthkey, duuid, davrtar in c.execute(f"""SELECT * FROM user WHERE name='{data.get('name')}'"""):
            if (dpw == sha256(bytes(data.get('pw'), encoding='utf8')).hexdigest()):
                authkey = str(uuid4())
                c.execute(f"""
                UPDATE user SET "authkey"='{authkey}',"last"={int(time())} WHERE "name"='{dname}' and "password"='{dpw}'
                """)
                conn.commit()
                lock.release()
                return buildRequest(code.REQUEST_OK, "登录成功", authkey=authkey)
            else:
                lock.release()
                return buildRequest(code.REQUEST_USER_LOG_ERROR, "登录失败,用户名或密码错误!")
        return buildRequest(code.REQUEST_USER_LOG_ERROR, "登录失败,用户名或密码错误!")


@blueprint.route("/info", methods=["POST"])
def apiInfo():
    data = request_parse(request)
    authkey = data.get('authkey')
    if (authkey is None or '"' in authkey or "'" in authkey or len(authkey) > 36 or len(authkey) < 36 or '-' not in authkey):
        return buildRequest(code.REQUEST_BAD_QUERY, "无效的AuthKey")
    ak = validate_authkey(authkey)
    if (ak):
        log.info(
            f"[客户端:{request.remote_addr}] 请求 -> 查看用户资料 | AuthKey:{authkey}")

        return buildRequest(code.REQUEST_OK, "有效的AuthKey",
                            name=ak["name"],
                            uid=ak["uid"],
                            email=ak["email"],
                            coin=ak["coin"],
                            regtime=ak["regtime"],
                            last=ak["last"],
                            uuid=ak["uuid"],
                            avartar=ak["avartar"],
                            authkey=True
                            )
    else:
        return buildRequest(code.REQUEST_BAD_AUTHKEY, "不存在或过期的AuthKey", authkey=False)


@blueprint.route('/info/<uid>')
def apiUserPublicInfo(uid: str):
    if (not uid.isdigit()):
        return buildRequest(code.REQUEST_BAD_QUERY, 'uid必须为数字')
    uid = int(uid)
    if (uid == 0 or uid < 0):
        return buildRequest(code.REQUEST_BAD_QUERY, 'uid不合法')

    if (lock.acquire()):
        for dname, _, dlast, dtime, duid, duuid, davartar, dcoin, demail, _ in c.execute(f"""SELECT * FROM user WHERE uid='{uid}'"""):
            lock.release()
            return buildRequest(code.REQUEST_OK, "查询成功",
                                name=dname,
                                uid=duid,
                                email=demail,
                                coin=dcoin,
                                time=dtime,
                                last=dlast,
                                uuid=duuid,
                                avartar=davartar
                                )

        lock.release()
        return buildRequest(code.REQUEST_BAD_QUERY, 'uid未找到')


@blueprint.route("/list", methods=["GET"])
def apiListUser():
    data = request_parse(request)
    p = int(getConfigByKey('itemLimit'))
    page = p * \
        data.get('page', default=0, type=int)
    log.info(f"[客户端:{request.remote_addr}] 请求 -> 获取用户列表")
    obj = []
    log.info(
        f"[客户端:{request.remote_addr}] 请求 -> 查看用户列表 | 页:{page}")
    if (lock.acquire()):
        for dname, duid, dcoin, dtime, dlast, davartar in c.execute(f"SELECT name,uid,coin,time,last,avartar FROM user LIMIT {p} OFFSET {page}"):
            obj1 = {}
            obj1.update({
                "name": dname,
                "uid": duid,
                "coin": dcoin,
                "time": dtime,
                "last": dlast,
                "avartar": davartar
            })
            obj.append(obj1)
        lock.release()
    last = False
    if (len(obj) < p):
        last = True
    return buildRequest(code.REQUEST_OK, "查询成功", list=obj, last=last)


@blueprint.route("/top")
def apiTopUser():
    log.info(
        f"[客户端:{request.remote_addr}] 请求 -> 查看最新用户")
    obj = []
    if (lock.acquire()):
        for dname, duid, dcoin, dtime, dlast, davartar in c.execute("""
            SELECT name,uid,coin,time,last,avartar FROM user ORDER BY uid DESC LIMIT 5
        """):
            obj1 = {}
            obj1.update({
                "name": dname,
                "uid": duid,
                "coin": dcoin,
                "time": dtime,
                "last": dlast,
                "avartar": davartar
            })
            obj.append(obj1)
    lock.release()
    return buildRequest(code.REQUEST_OK, "查询成功", list=obj)


@blueprint.route("/count", methods=["GET"])
def apiCountUser():
    log.info(
        f"[客户端:{request.remote_addr}] 请求 -> 查看用户资料")
    if (lock.acquire()):
        for i in c.execute("SELECT count(*) FROM user"):
            lock.release()

            return buildRequest(code.REQUEST_OK, "查询成功", count=i[0])


@blueprint.route("/page")
def apiPageUser():
    total = 0
    if (lock.acquire()):
        for i in c.execute("""
        SELECT count(*) FROM user
        """):
            total = i[0]
        lock.release()
    page = int(getConfigByKey('itemLimit'))
    total = ceil(total/page)

    return buildRequest(code.REQUEST_OK, msg="查询成功", page=total-1)




