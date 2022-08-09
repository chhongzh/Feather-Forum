from pip import main

# packs = [
#     'flask',
#     'flask-cors',
#     'rich'
# ]


def i(packs):
    for pack in packs:
        print(f'开始安装:{pack}')
        main(['install', pack])
