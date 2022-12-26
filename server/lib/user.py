"""
此文件属于Feather-Forum!
© 2022 chhongzh

用户数据操作相关
"""
from .database import query
from . import share
from .cache import Cache


pool = share.datacache['user']['id']
pool: Cache


def get_name_by_uid(uid: int | str) -> str | None:
    if (not pool.searchItem(str(uid))):
        q = query('SELECT name FROM user WHERE "uid"=(?)',
                  [uid], one=True).get('name', None)
        pool.setItem(str(uid), q, 3600)
        return q
    else:
        return pool.getItem(str(uid))
