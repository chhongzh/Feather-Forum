from json import dumps
import random
import socket
from sqlite3 import connect
from pip import main
try:
    from flask import Flask, render_template, request
    from flask_socketio import SocketIO
except ImportError:
    print('安装Flask')
    main(['install', 'flask', 'flask-socketio'])
    print('完成')
    print('请重启脚本!')
    exit(0)
import os
import platform
import sys


print('启动Web服务器')
app = Flask(__name__, template_folder='install', static_folder='install')
io = SocketIO(app)


def extract_ip():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        st.connect(('10.255.255.255', 1))
        IP = st.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        st.close()
    return IP


def randstr(num):
    H = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'

    salt = ''
    for _ in range(num):
        salt += random.choice(H)

    return salt


def request_parse(req_data):
    if (req_data.method == 'POST'):
        data = req_data.json
    elif (req_data.method == 'GET'):
        data = req_data.args
    return data


key = randstr(16)

print('请访问:http://{}:5000'.format(extract_ip()))


@app.route('/')
def index():
    error = False
    obj = []
    obj1 = {}

    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in ["node_modules", ".git"]]

        for name in files:
            obj1['name'] = os.path.join(root, name)
            obj1['need'] = True
            obj1['current'] = os.access(
                obj1['name'], os.R_OK) and os.access(obj1['name'], os.W_OK)
            if (not obj1['current']):
                error = True
            obj.append(obj1.copy())
            obj1.clear()

    vererror = not (sys.version_info.major, sys.version_info.minor,
                    sys.version_info.micro) >= (3, 9, 6)
    return render_template('step1.html',
                           UseSystem=platform.system(),
                           UsePython="{}.{}.{}".format(
                               sys.version_info.major, sys.version_info.minor, sys.version_info.micro),
                           items=obj,
                           HasError=error,
                           Key=key,
                           PyVer=(sys.version_info.major,
                                  sys.version_info.minor, sys.version_info.micro),
                           PyErr=vererror)


@app.route('/step2', methods=['GET'])
def step2():
    return render_template('step2.html')


@io.on('connect')
def wsconnect():
    print('Ws Client Was Connect')


@io.on('disconnect')
def wsdisconnect():
    print('Ws Client Was Disconnect')


@io.on('install run')
def installrun(data):
    data = data['data']
    obj = {}
    obj['forumName'] = data['name']
    obj['baseURL'] = data['api']
    obj['webhost'] = 'auto'
    obj['hideFeather'] = False
    obj = dumps(obj, ensure_ascii=False)
    with open('src/assets/js/config.js', 'w') as f:
        f.write("export default "+obj+";")
    io.emit('server log', '将配置写入文件:'+'src/assets/js/config.js')
    io.emit('server log', '准备安装依赖')
    for i in ['flask', 'flask-socketio', 'rich', 'flask-cors']:
        io.emit('server log', f'执行:安装 {i}')
        main(['install', i])
        io.emit('server log', f'执行:完成 {i} 的安装')
    io.emit('server log', '执行:初始化数据库')
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
    io.emit('server log', '执行:数据库清理完成')
    io.emit('install done', '完成安装!')


@io.on('server stop')
def stop():
    import os
    import signal
    os.kill(os.getpid(), signal.SIGKILL)


# app.run()
io.run(app, host="0.0.0.0", debug=True)
