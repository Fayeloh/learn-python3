#---------------------------------函数式编程
#有无变量参与，分为无、有副作用的函数式编程

#---------------------------------高阶函数
##---------------------------------map/reduce
#map()函数接收两个参数，一个是函数，一个是Iterable，map将传入的函数依次作用到序列的每个元素，并把结果作为新的Iterator返回
#eg：比如我们有一个函数f(x)=x2，要把这个函数作用在一个list [1, 2, 3, 4, 5, 6, 7, 8, 9]上，就可以用map()实现如下：
def f(x):
	return x*x

r = map(f,[1,2,3,4,5,6])
print(list(r))

#reduce    典型案例：由字符拼凑成字符串，转化成int
#reduce(f, [x1, x2, x3, x4]) = f(f(f(x1, x2), x3), x4)
from functools import reduce

def str2int(s):
	def fn(x,y):
		return x*10+y
	def char2num(s):
		return {'0':0,'1':1,'2':2,'3':3,'4':4}[s]    #取s中的字符
	return reduce(fn,map(char2num,s))
print(str2int('134'))


#利用map和reduce编写一个str2float函数，把字符串'123.456'转换成浮点数123.456000
CHAR_TO_FLOAT = {
    '0': 0,
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    '.': -1
}
def str2float(s):
    nums = map(lambda ch: CHAR_TO_FLOAT[ch], s)
    point = 0
    def to_float(f, n):
        nonlocal point
        if n == -1:              #存在小数点时，执行
            point = 1
            return f
        if point == 0:
            return f * 10 + n
        else:
            point = point * 10
            return f + n / point
    return reduce(to_float, nums, 0.0)  #遍历第二参数给第三个参数
print(str2float('123.45600'))


##---------------------------------filter
#过滤掉结果为False，剩下结果为true

#用filter过滤掉非回数（如果a[1,2,3],则a[::-1]=[3,2,1],前两个冒号表示整个列表）
def is_palindrome(n):
	return str(n) == str(n)[::-1]
output = filter(is_palindrome,range(1,1000))
print(list(output))

#计算素数的一个方法是埃氏筛法，它的算法理解起来非常简单：
#首先，列出从2开始的所有自然数，构造一个序列：
#2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, ...
#取序列的第一个数2，它一定是素数，然后用2把序列的2的倍数筛掉：
#3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, ...
#取新序列的第一个数3，它一定是素数，然后用3把序列的3的倍数筛掉：
#5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, ...
#取新序列的第一个数5，然后用5把序列的5的倍数筛掉：
#7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, ...
#不断筛下去，就可以得到所有的素数

#构造一个从3开始的奇数数列
def _odd_iter():
	n = 1
	while True:
		n = n + 2
		yield n
#定义筛选函数
def _not_divisible(n):
	return lambda x:x%n>0
#定义一个生成器，不断返回一个素数
def primes():
	yield 2
	it = _odd_iter()
	while True:
		n = next(it)
		yield n
		it = filter(_not_divisible(n),it)
#打印100以内的素数
for n in primes():
	if n<100:
		print(n)
	else:
		break


##---------------------------------sorted(分类)
#
L = ['bob', 'about', 'Zoo', 'Credit']

print(sorted(L))    #因为大写字母的Ascii码小于小写的，所以结果是C,Z,a，b
print(sorted(L, key=str.lower))  
print(sorted(L, key = str.lower,reverse=True))   #逆序

from operator import itemgetter  
#operator模块提供的itemgetter函数用于获取对象的哪些维的数据


students = [('Bob', 75), ('Adam', 92), ('Bart', 66), ('Lisa', 88)]

print(sorted(students, key=itemgetter(0)))  #第一维度数
print(sorted(students, key=lambda t: t[1]))



#---------------------------------返回函数
#提到闭包的概念？？？？你送给我的间谍猫，就是为了知道我的年龄
#及时执行，保存值


#---------------------------------匿名函数


#---------------------------------装饰器（decorator）
import functools

def log(func):
    @functools.wraps(func)        #目前只需要记住即可
    def wrapper(*args, **kw):     #可变参数和命名参数的作用？？？？
        print('call %s():' % func.__name__)
        return func(*args, **kw)
    return wrapper

@log
def now():
    print('2015-3-25')

now()

#---------------------------------偏函数 
#当函数的参数个数太多，需要简化时，使用functools.partial可以创建一个新的函数，这个新函数可以固定住原函数的部分参数，从而在调用时更简单。
import functools

int2 = functools.partial(int, base=2)

print('1000000 =', int2('1000000'))