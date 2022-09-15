# ---------------------------------------------------------------------------
from maps import post
from maps import user
from maps import other
from lib import cors
from sys import version
from lib import share
from lib.config import Config
from flask import Flask
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
app = Flask(__name__)
log = share.log
app.config['SECRET_KEY'] = Config.SecretKey
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
app.register_blueprint(post.blueprint)
app.register_blueprint(user.blueprint)
app.register_blueprint(other.blueprint)
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
app.after_request(cors.after_request)
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
if (Config.UseDebugMode):
    log.warning('!---------警告---------!')
    log.warning('使用Debug模式!')
    log.warning('请勿在生产环境中使用Debug模式!')
    log.warning('若要关闭Debug模式,请前往lib/config.py更改!')
    log.warning('!----------------------!')
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
log.info(
    'FeatherForum版本({}.{}.{})'.format(Config.Version[0], Config.Version[1], Config.Version[2]))
log.info(
    version
)
app.run(port=Config.ServerPort, debug=Config.UseDebugMode)
# ---------------------------------------------------------------------------
