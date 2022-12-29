本文章仅适用于**有能力者**以及**有基础者**进行**2次创作**

了解文件树以及作用
------------------
```
.
├── BuildBot.py                             调试用的构建工具
├── CHANGELOG.md                            变更日志
├── LICENSE                                 条款
├── README.md                               Readme
├── babel.config.js                         Babel配置
├── images                                  Readme图片
│   ├── FeatherForum.png                    Logo
│   └── FeatherForum.svg                    Logo
├── install                                 安装程序资源
│   ├── base.html                           
│   ├── check_error.gif
│   ├── check_right.gif
│   ├── reset.html
│   ├── step1.html
│   └── step2.html
├── installer.py                            安装程序
├── jsconfig.json                           
├── package.json        
├── public                                  前端公共资源
│   ├── favicon.ico                         网站Logo
│   └── index.html                          模板
├── server                                  服务端
│   ├── __init__.py
│   ├── data.db3                            主数据库
│   ├── lib                                 Library
│   │   ├── authkey.py                      服务端authkey操作
│   │   ├── cache.py                        服务端缓存
│   │   ├── config.py                       服务端主配置
│   │   ├── cors.py                         服务端跨域
│   │   ├── database.py                     服务端数据库操作
│   │   ├── error.py                        服务端错误操作
│   │   ├── request.py                      服务端返回值
│   │   ├── returncode.py                   服务端返回代码
│   │   ├── share.py                        服务端共享变量
│   │   ├── user.py                         服务端用户操作
│   │   └── utils.py                        服务端使用工具
│   ├── requirements.txt                    依赖
│   ├── routes                              路由
│   │   ├── admin                           管理员相关
│   │   │   ├── __init__.py                 
│   │   │   └── auth.py                     管理员用户
│   │   ├── other                           其他
│   │   │   └── __init__.py                
│   │   ├── post                            帖子
│   │   │   └── __init__.py
│   │   └── user                            用户
│   │       ├── __init__.py
│   │       ├── auth.py
│   │       ├── follow.py
│   │       ├── info.py
│   │       └── list.py
│   ├── server.py                           服务端入口文件
│   └── templates                           服务端模板
│       ├── ApiNotFound.html
│       └── Base.html
├── src                                     前端
│   ├── App.vue                             前端主文件
│   ├── assets                              前端资源文件
│   │   └── js                              JS相关
│   │       ├── config.js                   旧config
│   │       └── date.js                     旧时间库
│   ├── components                          组件
│   │   └── counter.vue                     
│   ├── config                              配置
│   │   ├── apiRoute.js                     路由表
│   │   └── web.js                          前端配置
│   ├── i18n                                翻译
│   │   ├── cn.js                           简体中文语言包
│   │   ├── en.js                           English语言包
│   │   └── index.js                        入口文件
│   ├── lib                                 前端库
│   │   ├── auth.js                         用户鉴权
│   │   ├── http.js                         HTTP操作
│   │   ├── post.js                         帖子操作
│   │   ├── time.js                         时间库
│   │   └── utils.js                        实用工具
│   ├── main.js                             前端入口文件
│   ├── router                              路由
│   │   └── index.js
│   ├── store                               VueX
│   │   └── index.js
│   └── views                               视图
│       ├── 404View.vue                     页面未找到
│       ├── HomeView.vue                    主页面
│       ├── JumpView.vue                    跳转提示
│       ├── LoginView.vue                   登录页面
│       ├── MyView.vue                      关于我
│       ├── PostView.vue                    发布帖子页面
│       ├── PostsView.vue                   帖子列表
│       ├── ReadPostView.vue                浏览帖子页面
│       ├── RegisterView.vue                注册页面
│       ├── UserView.vue                    用户页面
│       ├── UsersView.vue                   用户列表
│       └── admin                           管理员相关
│           ├── App.vue                     
│           ├── HomeView.vue
│           ├── LoginView.vue
│           └── LogsView.vue
├── tools                                   工具
│   ├── Register100.py                      注册100个账户
│   └── sort.py                             翻译排序
├── vue.config.js                           Vue配置文件
└── yarn.lock                               Yarn配置文件
```