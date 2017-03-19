#----------------------------------------------------------正则表达式
#----------------------------------------------------------基础
#\d:数字，\w：字母
#*：任意个，+：至少一个人，？：0个或1个，{n}：n个，{n,m}:n-m个

#----------------------------------------------------------进阶
#要做更精确地匹配，可以用[]表示范围，比如
#[a-zA-Z\_][0-9a-zA-Z\_]*可以匹配由字母或下划线开头，后接任意个由一个数字、字母或者下划线组成的字符串，也就是Python合法的变量；
#[a-zA-Z\_][0-9a-zA-Z\_]{0, 19}更精确地限制了变量的长度是1-20个字符（前面1个字符+后面最多19个字符）。
# A|B可以匹配A或B，所以(P|p)ython可以匹配'Python'或者'python'。

# ^表示行的开头，^\d表示必须以数字开头。

# $表示行的结束，\d$表示必须以数字结束


#----------------------------------------------------------re模块
#Python提供re模块，包含所有正则表达式的功能

#r前缀
s = r'ABC\-001'			#等同于s = 'ABC\\-001'

#match方法判断是匹配成功
import re
str ='ABC\\-001'
if re.match(r'ABC\-001',str):
	print('ok')
else:
	print('No!!!!')			#Can yu tell me why no


test = '用户输入的字符串'
if re.match(r'正则表达式', test):
    print('ok')
else:
    print('failed')			#Can you tell me why fail
#----------------------------------------------------------切分字符串
print('a   c  s'.split(' '))
#识别连续空格 \s
print(re.split(r'[\s\,\;]+', 'a,b;; c  d'))

#----------------------------------------------------------分组
#除了简单判断是否匹配外，正则表达式还有提取子串的强大功能
#用（）表示要提取的Group
m = re.match(r'^(\d{3})-(\d{3,8})$','010-12345')
print(m)
print(m.group(0))			#原始字符串
print(m.group(1))
print(m.group(2))


#----------------------------------------------------------贪婪匹配
print(re.match(r'^(\d+)(0*)$', '102300').groups())
#将\d+写成\d+？，就不会将后面的0都匹配出来，形成非贪婪匹配
print(re.match(r'^(\d+?)(0*)$', '102300').groups())


#----------------------------------------------------------编译
#出于效率考虑，采用预编译形式
#即将该正则表达式赋给一个对象，编译后形成Regular Expression对象


###习题
#someone@gmail.com
#bill.gates@microsoft.com
email = re.compile(r'^[0-9a-zA-Z-._]+@\w+.[a-zA-Z]+$')
if re.match(email,'someone@gmail.com'):
	print('ok')

email = re.compile(r'^[0-9a-zA-Z-._]+@\w+.[a-zA-Z]+$')
if re.match(email,'ill.gates@microsoft.com'):
	print('ok')
#<Tom Paris> tom@voyager.org
email = re.compile(r'^<([a-zA-Z]+\s?[a-zA-Z]*)>\s([0-9a-zA-Z-._]+@\w+.[a-zA-Z]+)$')
name = re.match(email,'<Tom Paris> tom@voyager.org')
if name:
	print('ok')
	print(name.group(2))
	print()