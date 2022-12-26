"""
此文件属于Feather-Forum!
© 2022 chhongzh

错误相关操作
"""
from flask import render_template


def api_not_found(e):
    return render_template('ApiNotFound.html'), 404
