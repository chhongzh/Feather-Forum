# ---------------------------------------------------------------------------
from flask import Blueprint, request
from lib.request import buildRequest
from lib.request import request_parse
from lib.code import code
from time import time
from lib.database import getConfigByKey
from lib import share
from lib.authkey import validate_authkey
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
lock = share.lock
c = share.c
conn = share.conn
log = share.log
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
blueprint = Blueprint('post', __name__, url_prefix='/api/post')
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
@blueprint.route("/write", methods=["POST"])
def apiWritePost():
    data = request_parse(request)
    authkey = data.get('authkey')
    title = data.get('title')
    content = str(data.get('content'))
    if (data is None or title is None or content is None):
        return buildRequest(code.REQUEST_BAD_QUERY, "缺省参数")
    ak = validate_authkey(authkey)
    if (ak):
        uid = ak["uid"]
        ttime = int(time())
        content = content.replace('"', '""').replace("'", "''")
        title = title.replace('"', '""').replace("'", "''")
        if (lock.acquire()):
            c.execute(f"""
            INSERT INTO post (title,content,uid,time)
            VALUES ('{title}', '{content}', {uid}, {ttime});
            """)
            conn.commit()
            lock.release()
            return buildRequest(code.REQUEST_OK, "帖子已经推送,等待审核")
    else:
        return buildRequest(code.REQUEST_BAD_AUTHKEY, "无法验证authkey")
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
@blueprint.route('/read', methods=["POST"])
def apiPostRead():
    data = request_parse(request)
    if (data.get('authkey') is None or data.get('pid') is None):
        return buildRequest(code.REQUEST_BAD_QUERY, "参数缺少")
    if (not str(data.get('pid')).isdigit()):
        return buildRequest(code.REQUEST_BAD_AUTHKEY, 'pid应为一个数字')
    authkey = data.get('authkey')
    pid = data.get('pid')
    log.info(
        f"[客户端:{request.remote_addr}] 请求 -> 查看帖子 | AuthKey:{authkey} Pid:{pid}")
    if (lock.acquire()):
        for dtitle, dcontent, duid, dtime, dpid in c.execute(f"""
        SELECT title,content,uid,time,pid FROM post WHERE pid={int(pid)}
        """):
            for dname in c.execute(f"SELECT name,uid FROM user WHERE uid = {int(duid)}"):
                lock.release()
                return buildRequest(code.REQUEST_OK, "查询成功", title=dtitle, content=dcontent, time=dtime, name=dname[0])
            lock.release()
            return buildRequest(code.REQUEST_BAD_QUERY, "帖子不存在")
        lock.release()
        return buildRequest(code.REQUEST_BAD_QUERY, "帖子不存在")
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
@blueprint.route('/top')
def apiPostTop():
    log.info(
        f"[客户端:{request.remote_addr}] 请求 -> 查看最新帖子")
    obj = []
    if (lock.acquire()):
        for dtitle, duid, dpid in c.execute("""
            SELECT title,uid,pid FROM post ORDER BY pid DESC LIMIT 5
        """):
            obj1 = {}
            obj1.update({
                "title": dtitle,
                "uid": duid,
                "pid": dpid
            })
            obj.append(obj1)
        lock.release()
        return buildRequest(code.REQUEST_OK, "查询成功", list=obj)
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
@blueprint.route("/list", methods=["GET"])
def apiListPost():
    data = request_parse(request)
    p = int(getConfigByKey('itemLimit'))
    page = p * \
        data.get('page', default=0, type=int)
    log.info(f"[客户端:{request.remote_addr}] 请求 -> 获取帖子列表")
    obj = []
    log.info(
        f"[客户端:{request.remote_addr}] 请求 -> 查看帖子列表 | 页:{page}")
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
# ---------------------------------------------------------------------------
