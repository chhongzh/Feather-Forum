# ---------------------------------------------------------------------------
from lib.database import query
from lib import share
from lib.cache import Cache
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
pool = share.datacache['user']['id']
pool: Cache
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------


def getNameByUid(uid: int | str) -> str | None:
    if (not pool.searchItem(str(uid))):
        q = query('SELECT name FROM user WHERE "uid"=(?)',
                  [uid], one=True).get('name', None)
        pool.setItem(str(uid), q, 3600)
        return q
    else:
        return pool.getItem(str(uid))
# ---------------------------------------------------------------------------
