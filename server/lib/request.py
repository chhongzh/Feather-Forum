"""
此文件属于Feather-Forum!
© 2022 chhongzh

标准返回
"""
from time import time
from json import dumps

from flask import request as F_request


def build_request(code: int, msg: str = "", **kwargs) -> str:
    """生成一个返回

    Args:
        code: 返回的代码
        msg: 返回的消息
        **kwargs: 数据

    Returns:
        返回json化的字符串
    """
    obj = {}
    obj.update({"code": code})
    obj.update({"time": format(time(), '.3f')})
    obj.update({"msg": msg})
    k = {}
    for key, value in kwargs.items():
        k.update({key: value})
    obj.update({"data": k})
    return dumps(obj, ensure_ascii=False)


def request_parse(req_object: F_request):
    """解析flask的request

    Args:
        req_object: request对象

    Raises:
        TypeError: 当req_object不是flask.request    
    """
    if (req_object.method == 'POST'):
        data = req_object.json
    elif (req_object.method == 'GET'):
        data = req_object.args
    else:
        raise TypeError('Unknown type')
    return data
