# ---------------------------------------------------------------------------
from . import share
cache = share.cache
lock = share.lock
c = share.c
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
def getConfigByKey(key: str) -> str:
    if (cache.searchItem(key)):
        return cache.getItem(key)

    if (lock.acquire()):
        for i in c.execute(f"""
        SELECT value FROM config WHERE "key"='{key}'
        """):
            lock.release()
            cache.setItem(key, i[0])
            return i[0]
        lock.release()
# ---------------------------------------------------------------------------
