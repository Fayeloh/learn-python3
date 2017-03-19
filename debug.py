#-------------------------------------------错误、调试和测试
#-------------------------------------------错误处理
##-------------------------------------------try...except...finally
try:
    print('try...')
    r = 10 / int('2')
    print('result:', r)
except ValueError as e:
    print('ValueError:', e)
except ZeroDivisionError as e:
    print('ZeroDivisionError:', e)
else:
    print('no error!')
finally:
    print('finally...')
print('END')

##-------------------------------------------调用堆栈
#从上往下，寻找错误根源
# err.py:
def foo(s):
    return 10 / int(s)

def bar(s):
    return foo(s) * 2

def main():
    bar('0')

main()


##-------------------------------------------记录错误
# err_logging.py

import logging

def foo(s):
    return 10 / int(s)

def bar(s):
    return foo(s) * 2

def main():
    try:
        bar('0')
    except Exception as e:
        logging.exception(e) 	#记录错误信息

main()
print('END')

##-------------------------------------------抛出错误
# err_reraise.py

def foo(s):
    n = int(s)
    if n==0:
        raise ValueError('invalid value: %s' % s)		#raise：错误处理
    return 10 / n

def bar():
    try:
        foo('0')
    except ValueError as e:
        print('ValueError!')
        raise   	#raise语句如果不带参数，就会把当前错误原样抛出。好处：将错误层层往上抛


bar()

#-------------------------------------------调试
##-------------------------------------------print
#最简单的查错方式，但是将来还是要删掉

##--------------------------------------------断言（assert）
#代替print的工具
def foo(s):
    n = int(s)
    assert n != 0, 'n is zero!'      #assert的意思是当n ！= 0时，程序继续执行，否则，抛出AssertionError
    return 10 / n

def main():
    foo('0')
main()
#程序中如果到处充斥着assert，和print()相比也好不到哪去。不过，启动Python解释器时可以用-O参数来关闭assert：
#????????运行时将python debug.py 换成python -0 debug.py，即可关掉Assert，将其当做pass看待



##-------------------------------------------logging
#logging不会抛出错误，而且还可以输出到文本
import logging
logging.basicConfig (level = logging.INFO)   #错误信息级别是info以上，输出错误
#错误信息级别（从低到高）：debug、info、warning、error

s = '0'
n = int(s)
logging.info('n = %d' % n)
print(10 / n)

##-------------------------------------------pdb
#pdb单步调试
##-------------------------------------------pdb.set_trace()
#通过pdb在命令行调试的方法理论上是万能的，但实在是太麻烦了，如果有一千行代码，要运行到第999行得敲多少命令啊。
#还好，我们还有另一种调试方法pdb.set_trace()


##-------------------------------------------IDE
#如果要比较爽地设置断点、单步执行，就需要一个支持调试功能的IDE。目前比较好的Python IDE有PyCharm：
#http://www.jetbrains.com/pycharm/
#另外，Eclipse加上pydev插件也可以调试Python程序。
s = '0'
n = int(s)
pdb.set_trace() # 运行到这里会自动暂停
print(10 / n)

#-------------------------------------------单元测试

##-------------------------------------------运行单元测试

##-------------------------------------------setUp与tearDown
#在单元测试中编写两个特殊的setUp()和tearDown()方法。这两个方法会分别在每调用一个测试方法的前后分别被执行
#简单讲：就是类似于数据库连接中的DBUtil
class TestDict(unittest.TestDict):

	def setUp(self):
		print('setUp....')

	def tearDown(self):
		print('tearDown')

#-------------------------------------------文档测试（doctest）
#运行时python debug.py -v;据说加了-v清晰不少
class Dict(dict):
    '''
    Simple dict but also support access as x.y style.

    >>> d1 = Dict()
    >>> d1['x'] = 100
    >>> d1.x
    100
    >>> d1.y = 200
    >>> d1['y']
    200
    >>> d2 = Dict(a=1, b=2, c='3')
    >>> d2.c
    '3'
    >>> d2['empty']
    Traceback (most recent call last):
        ...
    KeyError: 'empty'
    >>> d2.empty
    Traceback (most recent call last):
        ...
    AttributeError: 'Dict' object has no attribute 'empty'
    '''
    def __init__(self, **kw):
        super(Dict, self).__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

if __name__=='__main__':
    import doctest
    doctest.testmod()
