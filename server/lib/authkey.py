from lib.database import getConfigByKey
from . import share
from time import time
lock = share.lock
log = share.log
c = share.c


def validate_authkey(authkey: str):
    obj = {}
    if (len(authkey) > 36 or len(authkey) < 36 or '-' not in authkey or '"' in authkey or "'" in authkey):
        return None
    ak = int(getConfigByKey('authKeyTime'))
    log.info(ak)
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
