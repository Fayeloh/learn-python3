#---------------------------------------模块
#一个.py文件就是一个模块，函数->模块->包
#ps：每一个包目录下面都会有一个__init__.py的文件，这个文件是必须存在的，否则，Python就把这个目录当成普通目录，而不是一个包


#---------------------------------------使用模块

#module的标准格式

#!/usr/bin/env python3          #Windows系统用不到
# -*- coding: utf-8 -*-         #采用UTF-8编码

' a test module '

__author__ = 'Faye Loh'         #作者名字

import sys

def test():
    args = sys.argv
    if len(args)==1:
        print('Hello, world!')
    elif len(args)==2:
        print('Hello, %s!' % args[1])
    else:
        print('Too many arguments!')

if __name__=='__main__':
    test()

#作用域
#		全局变量：__name__,__age__
#      公有变量：name,age
#		私有变量：__name,__age


#---------------------------------------安装第三方模块
#安装第三方模块，用到了包管理工具pip，pip一般在安装Python时勾选了pip和Add python.exe to Path
#安装图片库   pip install pillow(PIL中的活跃项目pillow)
#使用图片库
from PIL import Image
#MySQL的驱动：mysql-connector-python
#用于科学计算的NumPy库：numpy
#用于生成文本的模板工具Jinja2
#路径查找
import sys
print(sys.path)
