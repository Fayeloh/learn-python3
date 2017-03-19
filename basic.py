
#!/usr/bin/python
#-------------------------------------中文编码
# -*-coding:utf-8-*-

#---------------------------------------格式化
format = 'hi,%s,I give you $%d' %('guy',99)
print(format)

#-----------------------------------------list
#list定义，增删查改
#定义
classmates = ['tom','marry','joson']
print(classmates)
#查
print('classmates[2]:',classmates[2])
print('classmates[-2]:',classmates[-2])
#长度
print('len(classmates):',len(classmates))
#增
classmates.append('ss')
classmates.insert(1,'faye')
print(classmates)
#删,利用索引
classmates.pop(1)
print(classmates)
# 改
classmates[2]='jack'
print(classmates)

#----------------------------list二维数组
#list定义成二维数组时
p = [2,3,4]
s = ['tom',p,'ww']
print(s)

#------------------------------tuple
#list用中括号定义，tuple用小括号定义，均为python内置的有序集合
#tuple   与list的区别在于tuple一旦初始化就不能再修改，但是tuple里面的【】数组是可变的
#注意：t=（1）相当于运算1，我们规定t=（1，）才是tuple序列
t = (1)
tt = (1,)
print(t,tt)
ttt = (1,classmates,2)
#ttt[0]=2
#报错：‘tuple’ object does not support item assigment
#修改classmates集合里面的就不会，因为classmates是tuple中的list集合

ttt[1][2] = 'faye'
print(ttt)

#-----------------------------------条件判断
age = input('please your age:')
age = int(age)  #务必转型，不然报错：unorderable type:str() >= int()
if age>=18:     #一个冒号为一个缩进，一个代码块
	print('your age is', age,'adult')
elif age >=6:
	print('your age is', age,'teenager')
else:
	print('your age is', age,'kid')

#-------------------------------------循环(for...in)
sum = 0
for x in range(10):  #range(10)就是可以生成0-9的整数序列
	sum = sum + x
	print(sum)
#-------------------------------------循环(while)
sum = 0
n = 10
while n>0:
	sum = sum + n
	n = n - 2
	print(sum,n)

#--------------------------break跳出循环，continun下一个循环

#--------------------------dict->python内置字典
#相当于java语言中的map，使用key-value
#通过key来计算位置的算法就是哈希算法-----查字典
d = {'jack':11,'tom':33}
#查
print(d['jack'])
#增
#把数据放入dict中的方法，除初始化时指定外，还可以通过key放入
d['Bob'] = 99
print(d)
#删,不可改
d.pop('jack')
print(d)

#---------------------------------------set
#set与dict相似，但是set只有key，没有value，key不可以重复
#要创建一个set，需要提供一个list作为输入集合
s  = set([1,2,3])
#查
print(s)
#增
s.add(4)
print(s)
#删
s.remove(2)
print(s)
#set可以看成高中数学中的无序和无重复的集合
s1 = set([1,2,4])
s2 = set([1,2,5])
#交集
print(s1 & s2)
#并集
print(s1 | s2)