#-----------------------------------Python的高级属性
#---------------------------------切片（Slice）
#取数组中指定索引范围中的操作，避免了十分繁琐的循环
L = ['jack','tom','faye','Bob']
print(L[1:3])
#也可以用倒数的方法取得数字
print(L[-4:-2])
#完全重新复制
print(L[:])

#字符串也可以用于此
print('ABCDEF'[2:4])


#---------------------------------迭代
#for循环遍历

#list的循环遍历是for x in list
#dict迭代的是key。如果要迭代value，可以用for value in d.values()，如果要同时迭代key和value，可以用for k, v in d.items()
#字符串的循环迭代是for ch in 'ABC'

#判断一个对象是否是可迭代对象，通过collections模块的Iterable类型判断
from collections import Iterable
print(isinstance('ABC',Iterable))
#要对list实现像java一样的下标循环：Python内置的enumerate函数可以把一个list变成索引-元素对，这样就可以在for循环中同时迭代索引和元素本身
for i,value in enumerate(['A','B','C']):       ##没有标注冒号，出现invalid syntax异常（无效语法）
	print(i,value)



#---------------------------------列表生成式
#迅速生成列表的工具
L = ['Hello','world',18,'apple']
#lower转为小写
print([s.lower() for s in L if isinstance(s,str)])  #整数会报错
#平方
print([x*x for x in range(1,11)])


#---------------------------------生成器（generator）
#创建L和g的区别仅在于最外层的[]和()，L是一个list，而g是一个generator。

#eg:斐波拉契数列（Fibonacci），原理：除了第一个和第二个数外，任意数都可由前两个数相加得到
def fib(max):
	n,a,b = 0,0,1
	while n < max:
		#print(b)
		yield b   #和generator仅仅相差一个语句
		a,b = b,a+b   #此赋值语句相当于t = (b,a+b),a=t[0],b=[1]------t是一个tuple，同位赋值的意思
		n = n + 1
	return 'done'

f = fib(6)
print(f)

#杨辉三角
def triangles(n):
	L = [1]
	while len(L)<=n:
		yield L
		L.append(0)
		L = [L[i-1]+L[i] for i in range(len(L))]
n = int(input("请输入杨辉三角的阶数:"))
for x in triangles(n):
	print(x)




#---------------------------------迭代器
#用iter()函数可将list、dict、str等可迭代转换成Iterator对象
#可for循环的对象是Iterable类型
#可next（）的对象才是Iterator类型，Iterator是一个无限大的数据流