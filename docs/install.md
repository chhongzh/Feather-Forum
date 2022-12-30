安装Feather-Forum
-------------------
在安装之前, **你需要在目标设备上安装Python3和Node和Vue**

**注意**:Feather-Forum正处于**快速开发**阶段, 它拥有一切的*不稳定性*和*未知性* 欢迎你提出**issuse**和**pull request**

步骤1
-------
**下载**或**克隆**此仓库:

```shell
git clone https://github.com/chhongzh/Feather-Forum.git
cd Feather-Forum
```

**安装依赖**
```shell
pip install flask
pip install rich

npm install yarn --location=global

yarn install
```

步骤2
-------
如果您需要**自定义前端**, 请前往`/src/config/web.js`修改配置

- forumName : 您的论坛的名字
- baseURL : 后端的请求地址
- hideFeather : 是否隐藏底部的提示
- webHost : 获取首页的URL, 值为auto时将会自动获取

如果您需要**自定义后端**, 请前往`/server/lib/config.py`修改配置

- Host : flask监听的地址
- UseDebugMode : 使用debug模式
- ServerPort : flask监听的端口
- SecretKey : 秘钥, 必须修改
- DbPath : 数据库地址

步骤3
--------
接下来将告诉宁如何**启动**/**编译**本项目

对于前端运行调试, 请使用`yarn run client`

对于前端编译, 请使用`yarn run build`**(编译后会在`/dist`文件夹下生产文件)**

对于后端运行, 请使用`yarn run python`**(如果您是`Mac`用户, 请使用`yarn run server3`)**


**大功告成! 恭喜你已经完成了安装!**