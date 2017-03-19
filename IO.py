#-----------------------------------------IO编程
#以内存为中心，磁盘读取文件到内存是input操作，把数据写到磁盘文件中是output操作
#以网页为中心，浏览器向新浪服务器发数据是Output，新浪服务器向浏览器发数据时input
#类比于水管的流（Stream）；输入流，输出流
#CPU 同步IO：坐着等汉堡
#	 异步IO：边逛街边等。。。。性能远远高于同步IO，但是编程模型复杂
#异步IO的两种编程模型：回调模式：服务员跑过来通知你
#					 轮询模式：你不停的翻手机看看汉堡好了没


#-----------------------------------------文件读写
#打开文件open()
#帮忙关掉IO流 with()
##-----------------------------------------读文件
f = open('D:/program/mygit/learn-python3/basic.py','r')
f.read()

##------------------------------------------file-like Object
#open()函数返回的这种有个read()方法的对象，在Python中统称为file-like Object。除了file外，还可以是内存的字节流，网络流，自定义流等等。
#StringIO就是在内存中创建的file-like Object，常用作临时缓冲

#默认读取的都是文本文件
#要读取二进制文件，比如图片、视频等等，用‘rb’模式打开即可
#？？？？？？？以下路径有问题
#f = open('D:/program/mygit/learn-python3/pic.png','rb')
#f.read()

#读取字符编码
#f = open('D:/program/mygit/learn-python3/gbk.txt',encoding = 'gbk')
#遇到有些编码不规范的文件，你可能会遇到UnicodeDecodeError，因为在文本文件中可能夹杂了一些非法编码的字符。遇到这种情况，open()函数还接收一个errors参数，表示如果遇到编码错误后如何处理。最简单的方式是直接忽略：
#f = open('D:/program/mygit/learn-python3/gbk.txt',encoding = 'gbk'，error='ignore')

try:
    f = open('/path/to/file', 'r')
    print(f.read())
finally:
    if f:
        f.close()

##等价于
with open('/path/to/file', 'r') as f:
    print(f.read())
#with方法会自动调用close（）

##-----------------------------------------写文件
#与读文件一样用open（），传入'w'、'wb'表示写文本文件和二进制文件
try:
    f = open('/path/to/file', 'w')
    print(f.read())
finally:
    if f:
        f.close()

##等价于
#你可以反复调用write()来写入文件，但是务必要调用f.close()来关闭文件。当我们写文件时，操作系统往往不会立刻把数据写入磁盘，而是放到内存缓存起来，空闲的时候再慢慢写入。只有调用close()方法时，操作系统才保证把没有写入的数据全部写入磁盘。忘记调用close()的后果是数据可能只写了一部分到磁盘，剩下的丢失了。所以，还是用with语句来得保险：

with open('/path/to/file', 'w') as f:
    print(f.read())
#with方法会自动调用close（）


#-----------------------------------------StringIO和BytesIO
#数据读写不一定是文件，也可以在内存中读写
#两个基本点：str、二进制文件
###str
#写入
from io import StringIO
f = StringIO()
print(f.write('hi'))
print(f.getvalue())   				#打印str的值

#读取
f = StringIO('hi\nhello\n')
while True:
	s = f.readline()
	if s == '':
		break
	print(s.strip())


###二进制文件
from io import BytesIO
f = BytesIO()
f.write(b'hello')
f.write(b' ')
f.write(b'world!')
print(f.getvalue())

# read from BytesIO:
data = '岁月在变迁，彼此在成长'.encode('utf-8')
f = BytesIO(data)
print(f.read())

#-----------------------------------------操作文件和目录
import os
print(os.name)  		#查询操作系统类型
#如果是posix，说明系统是Linux、Unix或Mac OS X，如果是nt，就是Windows系统。
#os.uname获取系统信息，不过windows系统没有

#在操作系统中定义的环境变量，全部保存在os.environ这个变量中，可以直接查看
#print(os.environ)

#要获取某个环境变量的值，可以调用os.environ.get('key')
#print(os.environ.get('PATH'))
# 查看当前目录的绝对路径:
print(os.path.abspath('.'))
os.path.abspath('.')
# 在某个目录下创建一个新目录，首先把新目录的完整路径表示出来:
os.path.join('C:/Users/fayeloh/Desktop', 'testdir')

# 然后创建一个目录:
#os.mkdir('C:/Users/fayeloh/Desktop/testdir')


# 删掉一个目录:
#os.rmdir('C:/Users/fayeloh/Desktop/testdir')

#两个路径合成一个路径时，通过os.path.join(),不是直接拆
#拆分路径，用os.path.split(),而不是直接拆
#拆分成文件路径和文件名
print(os.path.split('C:/Users/fayeloh/Desktop/file.txt'))
#获取拓展名
print(os.path.splitext('C:/Users/fayeloh/Desktop/file.txt'))
# 对文件重命名:
#os.rename('test.txt', 'test.py')
# 删掉文件:
#os.remove('test.py')
print( [x for x in os.listdir('.') if os.path.isdir(x)])

#要列出所有的.py文件，也只需一行代码
print([x for x in os.listdir('.') if os.path.isfile(x) and os.path.splitext(x)[1]=='.py'])


#-----------------------------------------序列化
#将变量从内存中变成可存储或传输的过程称之为序列化，Python中的pickling
#将变量从序列化的对象重新读到内存里称之为反序列化，unpickling
import pickle
d = dict(name = 'Bob',age = 20,score = 88)
#序列化
data = pickle.dumps(d)
print(data)
#反序列化
reborn = pickle.loads(data)
print(reborn)

##--------------------------------------------------------json
#要将序列化更通用、更web化，转化成JSON模式
#JSON表示的就是JavaScript语言的对象，自行百度Json与python的对应数据类型（https://docs.python.org/3/library/json.html#json.dumps）
import json
d = dict(name = 'Tom',age = 10,score =100)
data = json.dumps(d)
print(data)

reborn = json.loads(data)
print(reborn)

##-----------------------------------------------json进阶
#上面的json不能序列化class
#类不是可序列化对象，所以直接dumps会出现TypeError异常
#让类序列化的方法：类转化成dict，再顺利序列化成Json

#通常class的实例都有一个__dict__,用来存储实例变量的。也有少数如定义了__slots__的class没有__dict__
class Student(object):

    def __init__(self, name, age, score):
        self.name = name
        self.age = age
        self.score = score

    def __str__(self):
    	#转化成dict
        return 'Student object (%s, %s, %s)' % (self.name, self.age, self.score)

s = Student('Bob', 20, 88)
#利用dict直接序列化
std_data = json.dumps(s, default=lambda obj: obj.__dict__)
print('Dump Student:', std_data)
rebuild = json.loads(std_data, object_hook=lambda d: Student(d['name'], d['age'], d['score']))
print(rebuild)




