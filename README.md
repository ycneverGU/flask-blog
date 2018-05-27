# flask-blog
## 使用指南

在树莓派terminal下按顺序执行以下命令:

* git clone https://github.com/ycneverGU/flask-blog.git

* cd flask-blog 

* git checkout dev   //切换到开发分支

* virtualenv env --no-site-packages //创建空白的虚拟环境

* . env/bin/activate  //进入虚拟环境 

* pip install -r requirement.txt //在虚拟环境下安装项目所需的模块

* . test.sh  //引用外部环境变量

以后每次使用都需要进入虚拟环境和引用外部变量。

然后需要创建数据库，在flask-blog目录下执行以下命令：

* flask db init
* flask db migrate -m 'initial migration'
* flask db upgrade
* flask seed 

这几行命令初始化了数据库，创建了一个超级用户 admin,用户名是admin，密码是1234567890

这样环境就搭配好了

现在有两种启动方式 

1. python manager.py runserver  
默认使用这种方式
2. flask run


以上两种方式只是用在开发环境下，在生产环境要使用gunicorn，输入命令：

* gunicorn -w 4 manager:app -b 127.0.0.0:5000

打开网页 进入127.0.0.0:5000 就能使用了。


但还不够，要让树莓派能被本机以外的设备访问，要开通花生壳的服务。
花生壳会送一个免费域名。
校内网没有公网IP，IP地址随时会变，要让不同的IP地址对应同一个域名，就需要使用花生壳的内网穿透功能。

具体教程在：http://service.oray.com/question/2680.html

## 图
 ![Alt text](https://github.com/ycneverGU/flask-blog/tree/master/image/login.PNG)
 ![Alt text](https://github.com/ycneverGU/flask-blog/tree/master/image/写日志.PNG)
 ![Alt text](https://github.com/ycneverGU/flask-blog/tree/master/image/detial和删除.PNG)
 ![Alt text](https://github.com/ycneverGU/flask-blog/tree/master/image/数据图示1.PNG)


