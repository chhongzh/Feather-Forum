# ---------------------------------------------------------------------------
from lib.database import getConfigByKey
from lib import share
from lib.utils import isSpecil
from time import time
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
            not isSpecil(authkey)
        ):
        return None
    ak = int(getConfigByKey('authKeyTime'))
    if (lock.acquire()):

        for dname, _, dlast, dtime, duid, duuid, davartar, dcoin, demail, _ in c.execute(f"""
        SELECT * FROM user WHERE "authkey"='{authkey}'
        """):
            if (time() < dlast+ak):
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
        lock.release()

        return obj
# ---------------------------------------------------------------------------
