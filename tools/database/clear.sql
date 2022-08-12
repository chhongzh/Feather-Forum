-- Feather Forum 重置数据库

-- 删除POST
DELETE FROM post;
UPDATE sqlite_sequence SET seq = 0 WHERE name = 'post';

-- 删除用户
DELETE FROM user;
UPDATE sqlite_sequence SET seq = 0 WHERE name = 'user';