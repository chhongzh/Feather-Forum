from json import dump, load
import time
from InquirerPy import inquirer
import git

print('自动版本构建工具')
with open('./package.json', 'r') as f:
    data = load(f)
print('当前版本:{}'.format(data['version']))


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
    print('--------------------------------生成commit:--------------------------------')
    commit = f"""版本:v{name}
此版本由'版本构建机器人'构建于:{time.asctime( time.localtime(time.time()) )}"""
    print(commit)
    print('---------------------------------------------------------------------------')
    print('执行提交Commit...')
    with open('./package.json', 'w') as f:
        dump(data, f, ensure_ascii=False)
    repo = git.Repo.init('.')
    repo.index.add(['package.json'])
    repo.index.commit(commit)
    repo.remote().push()
    print('Done')
