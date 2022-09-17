# ---------------------------------------------------------------------------
from time import time
from json import dumps
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
def buildRequest(code: int, msg: str = "", **kwargs) -> str:
    obj = {}
    obj.update({"code": code})
    obj.update({"time": format(time(), '.3f')})
    obj.update({"msg": msg})
    k = {}
    for key, value in kwargs.items():
        k.update({key: value})
    # if (len(kwargs) != 0):
    obj.update({"data": k})
    return dumps(obj, ensure_ascii=False)
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
def request_parse(req_data):
    if (req_data.method == 'POST'):
        data = req_data.json
    elif (req_data.method == 'GET'):
        data = req_data.args
    return data
# ---------------------------------------------------------------------------
