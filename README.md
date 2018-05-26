##使用指南
在树莓派terminal下按顺序执行以下命令:

* git clone https://github.com/ycneverGU/flask-blog.git

* cd flask-blog 

* git checkout dev   切换到开发分支（这个分支集成了下位机程序）

* virtualenv env --no-site-packages

* . env/bin/activate  进入虚拟环境

* pip install -r requirement.txt 安装环境

* . test.sh  引用外部环境变量

以后每次使用都需要进入虚拟环境和引用外部变量。

这样环境就搭配好了

现在有两种启动方式 

1. python manager.py runserver  
默认使用这种方式
2. flask run
这种方式不能启动下位机程序，暂时不知道为什么


打开网页 进入127.0.0.0:5000 就能使用了。
