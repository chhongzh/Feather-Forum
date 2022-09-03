# ---------------------------------------------------------------------------
from lib.database import getConfigByKey
from lib import share
from lib.utils import isSpecil
from time import time
from lib.database import query
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
lock = share.lock
log = share.log
c = share.c
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
def validate_authkey(authkey: str) -> None | dict:
    """参数:
        authkey:用于验证的authkey
    返回:
        如果authkey有效:
            返回信息
        如果无效:
            返回None"""
    obj = {}
    if (len(authkey) > 36 or
                len(authkey) < 36 or
                '-' not in authkey or
                isSpecil(authkey)
            ):
        return None
    ak = int(getConfigByKey('authKeyTime'))
    # if (lock.acquire()):

    #     for dname, _, dlast, dtime, duid, duuid, davartar, dcoin, demail, _ in c.execute():
    #         if (time() < dlast+ak):
    #             obj.update()
    #             break
    #     else:
    #         obj = None
    #     lock.release()

    #     return obj
    q = query("""SELECT * FROM user WHERE "authkey"=(?)""",
              [authkey], one=True)
    print(time(), q['last'], ak)
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

# ---------------------------------------------------------------------------
