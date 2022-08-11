from time import time
from hashlib import sha256
from uuid import uuid4
from flask import Flask, request
from re import match
from sqlite3 import connect
from rich.logging import RichHandler
from rich import inspect
from json import dumps, loads
from logging import basicConfig, getLogger
from flask_cors import *
from c import code

FORMAT = "%(message)s"
basicConfig(
    level="INFO", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)
log = getLogger("rich")
conn = connect("data.db3", check_same_thread=False)
c = conn.cursor()
app = Flask(__name__)
cors = CORS(app)
log.info("Feather Forum 正在启动")


def getConfigByKey(key: str) -> str:

    for i in c.execute(f"""
    SELECT value FROM config WHERE "key"='{key}'
    """):
        return i[0]


def request_parse(req_data):
    if(req_data.method == 'POST'):
        data = req_data.json
    elif(req_data.method == 'GET'):
        data = req_data.args
    return data


def build_request(code: int, msg: str, **kwargs):
    obj = {}
    obj.update({"code": code})
    obj.update({"time": format(time(), '.3f')})
    obj.update({"msg": msg})
    k = {}
    for key, value in kwargs.items():
        k.update({key: value})
    obj.update({"data": k})
    return dumps(obj, ensure_ascii=False)


def validate_authkey(authkey: str):
    obj = {}
    if(len(authkey) > 36 or len(authkey) < 36 or '-' not in authkey or '"' in authkey or "'" in authkey):
        return None
    for dname, dpw, dlast, dtime, duid, duuid, davartar, dcoin, demail, dauthkey in c.execute(f"""
    SELECT * FROM user WHERE "authkey"='{authkey}'
    """):
        log.info(time() > dtime+int(getConfigByKey('authKeyTime')))
        log.info(time())
        log.info(dtime)
        log.info(int(getConfigByKey('authKeyTime')))
        if(time() > dtime+int(getConfigByKey('authKeyTime'))):
            obj.update({"name": dname,
                        "uid": duid,
                        "email": demail,
                        "coin": dcoin,
                        "regtime": dtime,
                        "last": dlast,
                        "avartar": davartar,
                        "uuid": duuid})
            break
    else:
        obj = None
    return obj


def validate_email(email: str):
    if(match(r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$', email)):
        return True
    return False


def after_request(resp):
    # resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Headers'] = "Content-Type"
    # resp.headers['Access-Control-Request-Method'] = ["POST", "GET"]
    return resp


app.after_request(after_request)


@app.route("/api/user/register", methods=["POST"])
def apiRegister():
    log.info(f"[客户端:{request.remote_addr}] 请求 -> 注册用户")
    data = request_parse(request)
    if(data.get('name', None) is None or
            data.get('pw', None) is None or
            data.get('email', None) is None
       ):
        log.info("[服务器] -> 错误请求")
        return build_request(code.REQUEST_BAD_QUERY, "用户名或密码或email为空")
    for d in c.execute("SELECT name FROM user"):
        if(data.get('name') == d[0]):
            log.info("[服务器] -> 错误请求")
            return build_request(code.REQUEST_USER_REG_ERROR, "用户名已存在")
    if(not validate_email(data.get('email'))):
        return build_request(code.REQUEST_USER_REG_ERROR, "邮箱错误")
    name = data.get('name').replace("'", "''").replace('"', '""')
    pw = data.get('pw').replace("'", "''").replace('"', '""')
    email = data.get('email').replace("'", "''").replace('"', '""')
    c.execute(f"""
            INSERT INTO user (name,password,email,time,last,authkey,uuid)
            VALUES ("{name}","{sha256(bytes(pw,encoding='utf8')).hexdigest()}","{email}",{
                    int(time())},0,Null,"{uuid4()}")
        """)
    conn.commit()
    return build_request(code.REQUEST_OK, "注册成功")


@app.route("/api/user/login", methods=["POST", "GET"])
def apiLogin():
    log.info(f"[客户端:{request.remote_addr}] 请求 -> 登录用户")
    data = request_parse(request)
    if(data.get('name', None) is None or
            data.get('pw', None) is None
       ):
        log.info("[服务器] -> 错误请求")
        return build_request(code.REQUEST_BAD_QUERY, "用户名或密码为空")
    for dname, dpw, duid, demail, dcoin, dtime, dlast, dauthkey, duuid, davrtar in c.execute("""SELECT * FROM user"""):
        if(dname == data.get('name') and dpw == sha256(bytes(data.get('pw'), encoding='utf8')).hexdigest()):
            authkey = str(uuid4())
            c.execute(f"""
            UPDATE user SET "authkey"='{authkey}',"last"={int(time())} WHERE "name"='{dname}' and "password"='{dpw}'
            """)
            conn.commit()
            return build_request(code.REQUEST_OK, "登录成功", authkey=authkey)
    else:
        return build_request(code.REQUEST_USER_LOG_ERROR, "登录失败,用户名或密码错误!")


@app.route("/api/user/info", methods=["POST"])
def apiInfo():
    data = request_parse(request)
    authkey = data.get('authkey')
    if(authkey is None or '"' in authkey or "'" in authkey or len(authkey) > 36 or len(authkey) < 36 or '-' not in authkey):
        return build_request(code.REQUEST_BAD_QUERY, "无效的AuthKey")
    ak = validate_authkey(authkey)
    if(ak):
        log.info(
            f"[客户端:{request.remote_addr}] 请求 -> 查看用户资料 | AuthKey:{authkey}")

        return build_request(code.REQUEST_OK, "有效的AuthKey",
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
        return build_request(code.REQUEST_BAD_AUTHKEY, "不存在或过期的AuthKey", authkey=False)


@app.route("/api/user/list", methods=["GET"])
def apiListUser():
    data = request_parse(request)
    log.info(getConfigByKey('searchItemList'))
    page = int(getConfigByKey('searchItemList')) * \
        data.get('page', default=0, type=int)
    log.info(f"[客户端:{request.remote_addr}] 请求 -> 获取用户列表")
    obj = []
    log.info(
        f"[客户端:{request.remote_addr}] 请求 -> 查看用户列表 | 页:{page}")
    for dname, duid, dcoin, dtime, dlast, davartar in c.execute(f"SELECT name,uid,coin,time,last,avartar FROM user LIMIT {int(getConfigByKey('searchItemList'))} OFFSET {page}"):
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
    for i in c.execute("SELECT count(*) FROM user"):
        return build_request(code.REQUEST_OK, "查询成功", list=obj)


@app.route("/api/user/count", methods=["GET"])
def apiCountUser():
    log.info(
        f"[客户端:{request.remote_addr}] 请求 -> 查看用户资料 | AuthKey:")
    for i in c.execute("SELECT count(*) FROM user"):
        return build_request(code.REQUEST_OK, "查询成功", count=i[0])


@app.route('/api/authkey/v', methods=["POST"])
def apiAuthkeyValidate():
    data = request_parse(request)
    if(data.get("authkey") is None):
        return build_request(code.REQUEST_BAD_QUERY, "缺少Authkey")
    if(validate_authkey(data.get('authkey'))):
        return build_request(code.REQUEST_OK, "有效的Authkey", authkey=True)
    return build_request(code.REQUEST_BAD_AUTHKEY, "无效Authkey", authkey=False)


@app.route("/api/post/write", methods=["POST"])
def apiWritePost():
    data = request_parse(request)
    authkey = data.get('authkey')
    title = data.get('title')
    content = str(data.get('content'))
    if(data is None or title is None or content is None):
        return build_request(code.REQUEST_BAD_QUERY, "缺省参数")
    ak = validate_authkey(authkey)
    if(ak):
        uid = ak["uid"]
        ttime = int(time())
        content = content.replace('"', '""').replace("'", "''")
        title = title.replace('"', '""').replace("'", "''")
        c.execute(f"""
        INSERT INTO post (title,content,uid,time)
        VALUES ('{title}', '{content}', {uid}, {ttime});
        """)
        conn.commit()
        return build_request(code.REQUEST_OK, "帖子已经推送,等待审核")
    else:
        return build_request(code.REQUEST_BAD_AUTHKEY, "无法验证authkey")


@app.route('/api/post/read', methods=["POST"])
def apiPostRead():
    data = request_parse(request)
    if(data.get('authkey') is None or data.get('pid') is None):
        return build_request(code.REQUEST_BAD_QUERY)
    if(not str(data.get('pid')).isdigit()):
        return build_request(code.REQUEST_BAD_AUTHKEY, 'pid应为一个数字')
    authkey = data.get('authkey')
    pid = data.get('pid')
    log.info(
        f"[客户端:{request.remote_addr}] 请求 -> 查看帖子 | AuthKey:{authkey} Pid:{pid}")
    for dtitle, dcontent, duid, dtime, dpid in c.execute(f"""
    SELECT title,content,uid,time,pid FROM post WHERE pid={int(pid)}
    """):
        for dname in c.execute(f"SELECT name,uid FROM user WHERE uid = {int(duid)}"):
            log.info(2)

            return build_request(code.REQUEST_OK, "查询成功", title=dtitle, content=dcontent, time=dtime, name=dname[0])
        return build_request(code.REQUEST_BAD_QUERY, "帖子不存在")
    return build_request(code.REQUEST_BAD_QUERY, "帖子不存在")


log.info("Feather Forum 完成注册")
log.info("Feather Forum 已启动")
app.run("0.0.0.0", port=14524, debug=True)
c.close()
