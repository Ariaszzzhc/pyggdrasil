# PYggdrasil API

![](https://img.shields.io/badge/language-python-blue.svg) ![](https://img.shields.io/badge/coverage-50%25-orange.svg)

## Description

本项目使用Flask/MongoDB实现了Minecraft的Yggdrasil API (authserver/sessionserver)

感谢@yushijinhun对Yggdrasil API进行的相关整理，其wiki请点击[此处](https://github.com/yushijinhun/authlib-injector/wiki)



## How to Use

项目主要用使用MongoDB进行数据持久化，但部分API使用到了Redis数据库，请确保已经安装。

```shell
git clone https://github.com/Ariaszzzhc/pyggdrasil.git
cd pyggdrasil
pipenv install
# 签名密钥对
openssl genrsa 4096 > private
openssl rsa -in private -pubin > public
```

本项目自带了uwsg支持，如要使用uwsgi，修改config.ini：

```ini
[uwsgi]

# uwsgi 启动时所使用的地址与端口
socket = 127.0.0.1:8001

# 指向网站目录
chdir = /path/to/pyggdrasil

# 指向Virtualenv目录
home = /path/to/virtualenv

# python 启动程序文件
module = pyggdrasil:create_app('prod')

# 处理器数
processes = 1

# 线程数
threads = 2

#状态检测地址
stats = 127.0.0.1:9191
```

配置完后即可使用Nginx+uwsgi的方式完成部署。其他的部署形式请参考flask官网[文档](http://flask.pocoo.org/docs/1.0/deploying/)。

