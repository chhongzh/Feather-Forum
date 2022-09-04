from json import dump, load
import os
import tarfile
import time
from InquirerPy import inquirer
import git
import copy
import zipfile

print('自动版本构建工具')
with open('./package.json', 'r') as f:
    data = load(f)
print('当前版本:{}'.format(data['version']))
old = copy.deepcopy(data['version'])


def makezip(name, path, type: zipfile.ZIP_STORED | zipfile.ZIP_DEFLATED = zipfile.ZIP_STORED, dis=["node_modules", ".git", "build"]):
    with zipfile.ZipFile(name+'.zip', 'w') as z:
        for root, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if d not in dis]
            for file in files:
                if (file == 'BuildBot.py'):
                    continue
                fullpath = os.path.join(root, file)
                z.write(fullpath, compress_type=type)


def mkdir(path):
    try:
        os.mkdir(path)
    except:
        pass


def version(string: str):
    if (not string.count('.') == 2):
        return False
    for i in string.split('.'):
        for j in i:
            if (j not in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0')):
                return False

    def toint(tpl): return int(tpl)
    def v(va: str): return map(toint, va.split('.'))
    def check(version): return list(v(version))
    if (check(string) <= check(data['version'])):
        return False
    return True


name = inquirer.text(message="版本号(格式:n.n.n):", validate=version,
                     ).execute()
data['version'] = name
a = inquirer.confirm(message=f'确定发布版本({name})', default=True).execute()
if (a):
    with open('./package.json', 'w') as f:
        dump(data, f, ensure_ascii=False)
    print('--------------------------------生成commit:--------------------------------')
    commit = f"""版本:v{name}
此版本由'版本构建机器人'构建于:{time.asctime( time.localtime(time.time()) )}"""
    print('---------------------------------------------------------------------------')

    print('打包文件')
    mkdir('build')
    os.chdir('build')

    try:
        os.rename('latest.zip', "{}.zip".format(old))
    except:
        pass
    makezip('latest', '../')
    os.chdir('../')

    print(commit)
    print('执行提交Commit...')
    repo = git.Repo.init('.')
    try:
        repo.index.add(
            ['package.json', f'build/{old}.zip', 'build/latest.zip'])
    except:
        repo.index.add(['package.json', 'build/latest.zip'])
    repo.index.commit(commit)
    repo.remote().push()
    print('推送至远程服务器成功!')
    print('Done!')