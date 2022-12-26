"""
此文件属于Feather-Forum!
© 2022 chhongzh

数据库相关操作
"""
from . import share
cache = share.cache
lock = share.lock
c = share.c


def get_config_by_key(key: str) -> str | None:
    """通过key获取配置

    Args:
        key: 查询的key

    Returns:
        如果key不存在返回None
        否则返回对应的数据
    """
    if (cache.searchItem(key)):
        return cache.getItem(key)

    for q in query("""
    SELECT value FROM config WHERE "key"=?
    """, (key,)):
        cache.setItem(key, q['value'])
        return q['value']
    return None


def _query(query: str, args: tuple | list = (), one=False) -> list[dict[str, str | int]] | dict[str, str | int]:
    cur = c.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv


def query(query: str, args: tuple | list = (), one=False) -> list[dict[str, str | int]] | dict[str, str | int]:
    """执行query

    Args:
        query: 执行的命令
        args: 参数
        one: 是否只要一个

    Returns:
        如果one为true时, 返回dict
        否则返回list
    """
    if (lock.acquire()):
        q = _query(query, args, one)
        lock.release()
    return q
