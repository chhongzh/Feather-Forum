"""
此文件属于Feather-Forum!
© 2022 chhongzh

跨域问题
"""


def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Headers'] = '*'
    return resp
