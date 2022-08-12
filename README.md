<a name="readme-top"></a>


<br />
<div align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="images/FeatherForum.png" alt="Logo">
  </a>
  <h3 align="center">Best-Forum-System</h3>

  <p align="center">
    一个简单的论坛系统
    <br />
    <a href="https://github.com/othneildrew/Best-README-Template"><strong>前往官网 »</strong></a>
    <br />
    <br />
    <a href="https://github.com/othneildrew/Best-README-Template">View Demo</a>
    ·
    <a href="https://github.com/othneildrew/Best-README-Template/issues">Report Bug</a>
  </p>

</div>


## 关于本项目



世界上有许多优秀的论坛系统，而**Feather-Forum**也是其中之一 可是,这些论坛大多是基于PHP等技术,这些不是我理想中的论坛系统,所以我下定决心开发了这款轻量级的论坛系统

<p align="right">(<a href="#readme-top">返回顶部</a>)</p>


## 快速开始

**在安装之前,您必须先安装[Node>=16][https://nodejs.org/zh-cn/download/current/]**和[Python3.9.6>=][https://www.python.org/downloads/]

### 手动编译

```shell
# 克隆仓库
git clone https://github.com/chhongzh/Feather-Forum.git

cd Feather-Forum

# 安装依赖
npm install

# 编译项目
npm run build
```

等待编译完成后,复制dist文件夹下所有文件到您的Ngnix或Apache的网页根目录下

### 自动编译

```shell
# 下载脚本
wget https://raw.githubusercontent.com/chhongzh/Feather-Forum/dev/tools/install/install.py ./setup.py
# or
curl -o setup.py https://raw.githubusercontent.com/chhongzh/Feather-Forum/dev/tools/install/install.py

# 执行脚本
python3 install.py
# or
python install.py
```

等待自动编译完成后打开新建的目录(目录名为安装时的时间戳),复制dist文件夹下所有文件到您的Ngnix或Apache的网页根目录下

### 大功告成

接下来你可已启动server文件夹下的server.py即可

<p align="right">(<a href="#readme-top">返回顶部</a>)</p>

## License

Distributed under the Apache 2.0 License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">返回顶部</a>)</p>

