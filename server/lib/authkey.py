"""
此文件属于Feather-Forum!
© 2022 chhongzh

authkey相关操作
"""

from .database import get_config_by_key
from . import share
from .utils import is_in
from time import time
from .database import query


def get_user_by_authkey(authkey: str) -> None | dict:
    """获取一个Authkey的相关信息

    Args:
        authkey: 需要查询的Authkey

    Returns:
        如果Authkey不存在或者过期,返回None
        否则返回对应的数据
        Example:
            {
             "name": "Test",
             "uid": 1,
             "email": "test@test.com",
             "coin": 0,
             "regtime": 114514,
             "last": 19810,
             "avartar": "Nothing.",
             "uuid": "1234-1324-1234-1234-1324"
             }
    """
    obj = {}
    if (len(authkey) > 36 or
            len(authkey) < 36 or
            '-' not in authkey or
            is_in(authkey)
        ):
        return None
    ak = int(get_config_by_key('authKeyTime'))
    q = query("""SELECT * FROM user WHERE "authkey"=(?)""",
              [authkey], one=True)
    if (q is None):
        return None
    if (time() < q['last']+ak):
        obj.update(
            {"name": q['name'],
             "uid": q['uid'],
             "email": q['email'],
             "coin": q['coin'],
             "regtime": q['time'],
             "last": q['last'],
             "avartar": q['avartar'],
             "uuid": q['uuid']}
        )
    else:
        obj = None
    return obj


def get_superuser_by_authkey(authkey: str) -> None | dict:
    """获取超级用户的信息

    Args:
        authkey: 查询的Authkey

    Returns:
        如果Authkey不存在或者过期,返回None
        否则返回对应的数据
    """
    if (len(authkey) > 36 or
            len(authkey) < 36 or
            '-' not in authkey or
            is_in(authkey)
        ):
        return None
    ak = int(get_config_by_key('authKeyTime'))
    q = query("""SELECT * FROM admin WHERE "authkey"=(?)""",
              [authkey], one=True)
    if ((q is None) or (not time() < q['last']+ak)):
        return None
    return q
