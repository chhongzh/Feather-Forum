from os import system
from sqlite3 import connect
from pip import main as pip
from time import sleep
from threading import Thread, active_count


class installThread(Thread):
    def __init__(self, func, **kwargs):
        Thread.__init__(self)
        self.func = func
        self.kwargs = kwargs

    def run(self):
        self.func(**self.kwargs)


print('欢迎使用全自动安装脚本')
try:
    input('按下任意键安装...(^C退出)')
except:
    print('取消操作!')
    exit(0)
tsk = [0, 0, 0, 0]


def db():
    global tsk
    print('读取数据库...')
    conn = connect('server/data.db3', check_same_thread=False)
    c = conn.cursor()
    c.executescript("""

    PRAGMA foreign_keys = false;

    -- ----------------------------
    -- Table structure for post
    -- ----------------------------
    DROP TABLE IF EXISTS "post";
    CREATE TABLE "post" (
    "title" TEXT,
    "content" TEXT,
    "uid" INTEGER,
    "time" DATE,
    "pid" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT
    );

    -- ----------------------------
    -- Table structure for superuser
    -- ----------------------------
    DROP TABLE IF EXISTS "superuser";
    CREATE TABLE "superuser" (
    "name" TEXT,
    "pw" TEXT,
    "authkey" TEXT,
    "last" INTEGER,
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT
    );

    -- ----------------------------
    -- Table structure for user
    -- ----------------------------
    DROP TABLE IF EXISTS "user";
    CREATE TABLE "user" (
    "name" TEXT,
    "password" TEXT,
    "last" integer DEFAULT 0,
    "time" integer,
    "uid" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "uuid" text,
    "avartar" TEXT DEFAULT 什么都没留下,
    "coin" integer DEFAULT 0,
    "email" TEXT,
    "authkey" TEXT
    );

    -- ----------------------------
    -- Table structure for config
    -- ----------------------------
    DROP TABLE IF EXISTS "config";
    CREATE TABLE "config" (
    "value" TEXT,
    "key" TEXT
    );

    -- ----------------------------
    -- Records of config
    -- ----------------------------
    BEGIN;
    INSERT INTO "config" ("value", "key") VALUES ('1800', 'authKeyTime');
    INSERT INTO "config" ("value", "key") VALUES ('5', 'itemLimit');
    COMMIT;

    PRAGMA foreign_keys = true;


    """)
    conn.commit()
    conn.close()
    print('写入数据库成功!')
    tsk[0] = 1


def lib():
    global tsk
    print('安装依赖...')
    pip(['install', 'rich', 'flask'])
    print('安装完成!')
    tsk[1] = 1


def npminstall():
    global tsk
    print('安装npm依赖!')
    system('npm install')
    print('安装npm依赖完成!')
    tsk[2] = 0


def npmbuild():
    global tsk
    print('编译Npm...')
    system('npm run build')
    print('编译完成!')
    tsk[3] = 0


db()
lib()
npminstall()
npmbuild()
