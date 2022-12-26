"""
此文件属于Feather-Forum!
© 2022 chhongzh

数据共享相关
"""
from threading import Lock
from .cache import Cache
from .config import Config
from sqlite3 import connect
from rich.logging import RichHandler
from logging import basicConfig, getLogger
from rich.console import Console
from logging import FileHandler, Formatter, DEBUG, INFO, WARN, ERROR, CRITICAL


lock = Lock()
cache = Cache()
console = Console()
datacache = {}


conn = connect(Config.DbPath, check_same_thread=False)
c = conn.cursor()


datacache['user'] = {}
datacache['user']['id'] = Cache()


FORMAT = "%(message)s"
basicConfig(
    level="DEBUG", format=FORMAT, datefmt="[%X]", handlers=[RichHandler(console=console, rich_tracebacks=True)]
)
log = getLogger("rich")
