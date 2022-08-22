# ---------------------------------------------------------------------------
from threading import Lock
from lib.cache import Cache
from sqlite3 import connect
from rich.logging import RichHandler
from logging import basicConfig, getLogger
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
lock = Lock()
cache = Cache()
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
conn = connect("data.db3", check_same_thread=False)
c = conn.cursor()
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
FORMAT = "%(message)s"
basicConfig(
    level="INFO", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)
log = getLogger("rich")
# ---------------------------------------------------------------------------
