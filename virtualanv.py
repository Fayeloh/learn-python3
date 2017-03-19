#virtualanv为应用提供隔离的python环境，解决了不同应用间多版本冲突问题
#建立一套“隔离”的python环境
#首先：pip3 install virtuallanv
#然后，假设我们要开发一个新的项目，需要一套独立的python运行环境
#1、创建目录
Mac:~ michael$ mkdir myproject
Mac:~ michael$ cd myproject/
Mac:myproject michael$


#2、创建一个独立的Python运行环境，命名为venv
Mac:myproject michael$ virtualenv --no-site-packages venv 			#参数--no-site-packages，这样，已经安装到系统Python环境中的所有第三方包都不会复制过来，这样，我们就得到了一个不带任何第三方包的“干净”的Python运行环境。
Using base prefix '/usr/local/.../Python.framework/Versions/3.4'
New python executable in venv/bin/python3.4
Also creating executable in venv/bin/python
Installing setuptools, pip, wheel...done.

#新建的Python环境被放在当前目录下的venv目录。有了venv这个python环境，可以用source进入该环境

#。。。。。。。。。。。。。。。。。。。。
#Don't ask me,it was copied by myself