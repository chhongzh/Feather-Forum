from time import time
from json import dumps


def buildRequest(code: int, msg: str = "", **kwargs):
    obj = {}
    obj.update({"code": code})
    obj.update({"time": format(time(), '.3f')})
    obj.update({"msg": msg})
    k = {}
    for key, value in kwargs.items():
        k.update({key: value})
    obj.update({"data": k})
    return dumps(obj, ensure_ascii=False)
