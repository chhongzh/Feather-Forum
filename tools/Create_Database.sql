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
INSERT INTO "config" ("value", "key") VALUES ('5', 'searchItemList');
COMMIT;

PRAGMA foreign_keys = true;
