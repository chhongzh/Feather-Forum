import os
import time
from rich.console import Console
console = Console()
u = str(time.time())
with console.pager():
    console.print('[b yellow]安装已完成!', justify='center')
    console.print('')
    console.print('接下来需要您[b]手动[/b]完成!')
    console.print('')
    console.print(f'打开{os.path.join(u,"dist")}')
