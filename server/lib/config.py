"""
此文件属于Feather-Forum!
© 2022 chhongzh

Feather-Forum主配置文件
"""


class Config(object):
    Host = None  # flask监听的地址
    UseDebugMode = True  # 使用debug模式
    ServerPort = 14524  # flask监听的端口
    SecretKey = 'Feather-Forum Demo on Debug Mode !'  # 秘钥, 必须修改
    DbPath = 'data.db3'  # 数据库地址
