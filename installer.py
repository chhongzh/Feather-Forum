from sqlite3 import connect


def querry(title, q):
    while (True):
        print(title)
        index = 1
        print('Numeber\tSelect')
        for i in q:
            print(f'{index}\t{i}')
            index += 1
        val = input('Please Select:')
        val: str
        if (val.isdigit()):
            val = int(val)-1
            try:
                q[val]
                return val
            except:
                print('Unknow Input')

        else:
            print('Unknow Input')


def langs(path):
    import json
    with open(path) as f:
        return json.load(f)


print('Welcome to install Feather-Forum')
print('')
s = querry('Select a language before install.', ['简体中文', 'English'])
lang = {}
if (s == 0):
    print('读取语言文件...')
    lang = langs('install/lang/zhCn.json')
elif (s == 1):
    print('Read Lang File...')
    lang = langs('install/lang/enUs.json')
else:
    print('未知语言(Unknow Lang)')
    raise SystemError()

print(lang['resetDb']['ing'])
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
print(lang['resetDb']['finish'])
