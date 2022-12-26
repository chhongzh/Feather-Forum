
from math import ceil
from flask import Blueprint, request
from lib.request import build_request
from lib.request import request_parse
from lib.code import ReturnCode
from time import time
from lib.database import get_config_by_key
from lib import share
from lib.authkey import get_user_by_authkey
from lib.database import query
from lib.user import get_name_by_uid
from re import findall, search, sub


lock = share.lock
c = share.c
conn = share.conn
log = share.log


blueprint = Blueprint('post', __name__, url_prefix='/api/post')


@blueprint.route("/write", methods=["POST"])
def WritePost():
    data = request_parse(request)
    authkey = data.get('authkey')
    title = data.get('title')
    content = str(data.get('content'))
    if (data is None or title is None or content is None):
        return build_request(ReturnCode.REQUEST_BAD_QUERY, "缺省参数")
    ak = get_user_by_authkey(authkey)
    if (ak):
        uid = ak["uid"]
        ttime = int(time())
        query("""
            INSERT INTO post (title,content,uid,time)
            VALUES ((?),(?),(?),(?))
            """, (title, content, uid, ttime))
        conn.commit()

        return build_request(ReturnCode.REQUEST_OK, "帖子发布成功")
    else:
        return build_request(ReturnCode.REQUEST_BAD_AUTHKEY, "无法验证authkey")


@blueprint.route('/read', methods=["POST"])
def PostRead():
    data = request_parse(request)
    if (data.get('authkey') is None or data.get('pid') is None):
        return build_request(ReturnCode.REQUEST_BAD_QUERY, "参数缺少")
    if (not str(data.get('pid')).isdigit()):
        return build_request(ReturnCode.REQUEST_BAD_AUTHKEY, 'pid应为一个数字')
    pid = data.get('pid')
    post = query(
        "SELECT title,content,uid,time,pid FROM post WHERE pid=(?)", pid, one=True)
    if (not post):
        return build_request(ReturnCode.REQUEST_BAD_QUERY, "帖子不存在")
    for title, link in findall(r"(?<!!)\[(.*?)\]\((.*?)\)", post['content']):
        new = "#/jump?url={}".format(link)
        post['content'] = post['content'].replace("[{}]({})".format(title, link),
                                                  "[{}]({}&redirect=/post/{})".format(title, new, pid), 1)
    name = get_name_by_uid(post['uid'])
    return build_request(ReturnCode.REQUEST_OK, "查询成功", title=post['title'], content=post['content'], time=post['time'], name=name, uid=post['uid'])


@blueprint.route('/top')
def PostTop():
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
        return build_request(ReturnCode.REQUEST_OK, "查询成功", list=obj)


@blueprint.route("/list", methods=["GET"])
def ListPost():
    data = request_parse(request)
    p = int(get_config_by_key('itemLimit'))
    page = p * \
        data.get('page', default=0, type=int)
    obj = []
    for v in query("SELECT * FROM post ORDER BY \"time\" DESC LIMIT (?) OFFSET (?)", [p, page]):
        v['name'] = get_name_by_uid(v['uid'])
        v['content'] = v['content'].replace('#', '').replace(
            ':', ''
        ).replace('|', ''
                  ).replace('-', ''
                            ).replace('\n', ''
                                      ).replace('*', ''
                                                ).replace('```', ''
                                                          ).replace(' ', ''
                                                                    ).replace('~~', ''
                                                                              )[:50]
        obj.append(v)
    return build_request(ReturnCode.REQUEST_OK, "查询成功", list=obj)


@blueprint.route("/page")
def PageUser():
    total = 0
    total = query('SELECT count(*) FROM post', one=True)['count(*)']
    page = int(get_config_by_key('itemLimit'))
    total = ceil(total/page)

    return build_request(ReturnCode.REQUEST_OK, msg="查询成功", page=total-1)
