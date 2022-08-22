def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp
