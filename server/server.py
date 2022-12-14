
from routes import post
from routes import user
from routes import other
from routes import admin
from lib import cors
from sys import version
from lib import share
from lib.config import Config
from flask import Flask
from lib.error import api_not_found
from lib.utils import check_version
from os import chdir
from os.path import split
from sys import argv
assert check_version()  # Not Python 3.9.5 or lower


app = Flask(__name__)
log = share.log
app.config['SECRET_KEY'] = Config.SecretKey


app.register_blueprint(post.blueprint)
app.register_blueprint(user.blueprint)
app.register_blueprint(other.blueprint)
app.register_blueprint(admin.blueprint)


app.after_request(cors.after_request)
app.register_error_handler(404, api_not_found)


if (Config.UseDebugMode):
    log.warning('!---------警告---------!')
    log.warning('使用Debug模式!')
    log.warning('请勿在生产环境中使用Debug模式!')
    log.warning('若要关闭Debug模式,请前往lib/config.py更改!')
    log.warning('!----------------------!')


if (Config.Host):
    app.run(port=Config.ServerPort, debug=Config.UseDebugMode, host=Config.Host)
else:
    app.run(port=Config.ServerPort, debug=Config.UseDebugMode)
