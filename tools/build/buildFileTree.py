# FeatherForum 构建文件树

import hashlib
import json
import os
from rich.console import Console
console = Console()
console.log('开始扫描')
current_address = os.path.dirname(os.path.abspath(__file__))
obj = []


def md5er(path):
    m = hashlib.md5()  # 创建md5对象
    with open(path, 'rb') as fobj:
        while True:
            data = fobj.read(1024)
            if not data:
                break
            m.update(data)  # 更新md5对象

    return m.hexdigest()  # 返回md5对象


with console.status('扫描中...'):
    console.log(os.getcwd())
    for parent, dirnames, filenames in os.walk('./'):
        if(os.path.basename(parent) == "node_modules" or os.path.basename(parent) == ".git" or os.path.basename(parent) == "dist"):
            dirnames[:] = []
        for filename in filenames:
            if(filename == '.DS_Store' or '.git' in filename):
                continue
            fname, ext = os.path.splitext(filename)
            obj1 = {}
            obj1.update(
                {
                    'name': fname,
                    'path': os.path.join(parent, filename)[1:]
                }
            )
            obj.append(obj1)
with open('./build.dist.json', 'w') as f:
    json.dump(obj, f, ensure_ascii=False)
