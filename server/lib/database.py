# ---------------------------------------------------------------------------
from queue import Queue
from sqlite3 import Cursor, connect
from . import share
cache = share.cache
lock = share.lock
c = share.c

# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
def getConfigByKey(key: str) -> str:
    if (cache.searchItem(key)):
        return cache.getItem(key)

    for q in query("""
    SELECT value FROM config WHERE "key"=?
    """, (key,)):
        cache.setItem(key, q['value'])
        return q['value']

# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
def _query(query: str, args: tuple, one=False):
    cur = c.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
def query(query: str, args: tuple, one=False):
    if (lock.acquire()):
        q = _query(query, args, one)
        lock.release()
    return q
# ---------------------------------------------------------------------------
