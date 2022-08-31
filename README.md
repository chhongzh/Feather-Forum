**提示:目前正在开发中,如果您有什么好建议或问题提出,请创建issues**

--------

<br />
<br />

<a name="readme-top"></a>


<br />
<div align="center">
  <a href="https://github.com/chhongzh/Feather-Forum">
    <img src="images/FeatherForum.png" alt="Logo">
  </a>
  <h3 align="center">A-Forum-System</h3>

  <p align="center">
    一个简单的论坛系统
    <br />
    <a href="https://github.com/chhongzh/Feather-Forum"><strong>前往官网 »</strong></a>
    <br />
    <br />
    <a href="https://github.com/chhongzh/Feather-Forum">View Demo</a>
    ·
    <a href="https://github.com/chhongzh/Feather-Forum/issues">Report Bug</a>
  </p>

</div>


## 快速开始

在安装之前,您必须先安装[Node>=16](https://nodejs.org/zh-cn/download/current/)和[Python3.9.6>=](https://www.python.org/downloads/)

### 编译前端

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
**TIPS**:如果您想要预览而不是编译,请使用`npm run serve`


### 启动后端

接下来你需要启动server文件夹下的server.py 即可

<p align="right">(<a href="#readme-top">返回顶部</a>)</p>

## 协议

根据MIT许可证发布,有关更多信息,请参见`LICENSE`。

<p align="right">(<a href="#readme-top">返回顶部</a>)</p>

