# FeatherForum 安装程序

try:
    import os
    import hashlib
    from time import time, sleep
    from rich.console import Console
    from requests import get
    from pip import main as pip
    from rich.progress import track
    from rich.console import Group
    from rich.text import Text
    from rich.live import Live
    from rich.panel import Panel
    from subprocess import run
except:
    print('安装依赖(Rich)')
    import pip
    pip.main(['install', 'rich'])
    print('依赖安装完成,请重新启动')
    raise SystemExit
console = Console()
u = str(time())


def asker(question, default: bool = True):
    try:
        k = console.input('[b]{} ({})'.format(
            question, 'Y/n' if default else 'N/y'))
    except (KeyboardInterrupt, EOFError):
        return not default
    if(k.lower() == 'y'):
        return True
    elif(k.lower() == 'n'):
        return False
    elif(k.replace(' ', '').strip() == ''):
        return default
    else:
        return default


def jsonler(url, env='https://raw.githubusercontent.com/chhongzh/Feather-Forum/dev'):
    try:
        idx = get(
            env+url).json()
        return idx

    except:
        console.log(f'[b blue]错误 在请求{url}时发生错误!')
        raise SystemError()


def safer(path, content):
    import os
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)


def downder(url, env='https://raw.githubusercontent.com/chhongzh/Feather-Forum/dev'):
    try:
        idx = get(
            env+url).text
        return idx

    except:
        console.log(f'[b blue]错误 在请求{url}时发生错误!')
        raise SystemError()


console.print('欢迎使用FeatherForum安装程序')
if(not asker('安装程序将完成一些任务,是否继续?')):
    raise SystemExit


console.log('[b blue]执行 安装依赖')
with console.status('[b blue]执行 安装依赖'):
    packs = ['rich', 'flask', 'flask-cors', 'requests']
    for pack in packs:
        console.log(f'[b blue]安装{pack}')
        pip(['install', pack])
        console.log(f'[b blue]安装{pack}完成!')

    console.log('[b blue]完成 所有依赖安装完成!')

env = 'https://raw.githubusercontent.com/chhongzh/Feather-Forum/dev'
if(not asker('使用Github下载源?(否则使用Gitee下载源)')):
    env = 'https://gitee.com/huajixc/Feather-Forum/raw/dev'

console.log('[b blue]下载 索引')
try:
    idx = jsonler(
        '/build.dist.json', env=env)
except:
    console.log('[b red]网络错误,无法请求')
    raise SystemError
console.log('[b blue]下载 成功下载索引')

try:
    os.mkdir(u)
    os.chdir(u)

    for i in track(idx, description='', total=len(idx), console=console):
        console.log(f'[b blue]下载 {i["name"]} 来自 {i["path"]}')
        b = downder(i['path'], env=env)
        safer('./'+i['path'], b)

        # sleep(0.25)
        # console.log(f'[b blue]下载 完成 {i["name"]}')


except:
    console.print('[red b]下载源出现问题')
    os.chdir('../')
    os.rmdir(u)

console.print('[b blue]我们需要收集一些信息来安装:')
while(True):
    webname = console.input('[b blue]网站名称:(如果在未来需要更改可能需要重新编译)')
    webserver = console.input(
        '[b blue]输入您的后台地址(如果您只是在本地安装,请输入:localhost,[red]您不需要输入http(s)!)')
    # webport = console.input('[b blue]输入')

    if(asker('[b blue]启用https?(如果您的网站支持https,请开启此功能)')):
        webserver = "https://"+webserver
    else:
        webserver = "http://"+webserver

    console.print('[b blue]信息确认:')
    console.print(f'[b blue]网站名称:{webname}')
    console.print(f'[b blue]后台地址:{webserver}')
    if(asker('[b blue]确认以上的信息,并确认没有问题,是否继续?')):
        break

    # 读写配置文件
with open('./src/assets/js/config.js', 'w') as f:
    obj = {
        'forumName': webname,
        'baseURL': webserver,
    }
    import json
    f.write("export default "+json.dumps(obj)+";")
    console.log('[b bold]成功写入文件')

with console.status('[b blue]执行 编译'):
    console.log('[b blue]启动 安装模块')
    console.log('[b blue]执行 npm install')
    c = os.system('npm install')
    console.log('[b blue]启动 安装模块 完成! 返回:{c}')

    console.log('[b blue]启动 编译模块')
    console.log('[b blue]执行 npm run build')
    c = os.system('npm run build')
    console.log('[b blue]启动 编译模块 完成! 返回:{c}')

with console.status("[b blue]执行 初始化"):
    import sqlite3
    conn = sqlite3.connect('server/data.db3', check_same_thread=False)
    c = conn.cursor()
    c.execute('''
    
    -- 删除POST
DELETE FROM post;
UPDATE sqlite_sequence SET seq = 0 WHERE name = 'post';

-- 删除用户
DELETE FROM user;
UPDATE sqlite_sequence SET seq = 0 WHERE name = 'user';

    ''')
    conn.commit()
    conn.close()

console.print('[b yellow]安装已完成!', justify='center')
console.print('')
console.print('接下来需要您[b]手动[/b]完成!')
console.print('')
console.print(f'打开 {os.path.join(u,"dist")} 将里面所有文件移动到您的网站根目录')
console.print(f'打开 {os.path.join(u,"server")} 将里面所有文件移动到任意的文件夹')
console.print(f'当需要启动服务器时,请先cd进您刚刚移动的文件夹')
console.print('然后再执行python3 server.py')
