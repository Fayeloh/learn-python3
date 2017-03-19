#-----------------------------------------------------进程和线程
#进程是任务
#线程是任务的子任务
#多进程和多线程的程序涉及到同步、数据共享的问题


#-----------------------------------------------------多进程
#普通函数调用一次，返回一次
#Unix\linux系统提供的fork()系统调用，调用一次，返回两次。因为操作系统自动把当前进程（称为父进程）复制了一份（称为子进程），然后，分别在父进程和子进程内返回。
#子进程永远返回0，而父进程返回子进程的ID。这样做的理由是，一个父进程可以fork出很多子进程，所以，父进程要记下每个子进程的ID，而子进程只需要调用getppid()就可以拿到父进程的ID。
#Python的os模块封装了常见的系统调用，其中就包括fork，可以在Python程序中轻松创建子进程：
#import os
#pid = os.fork()  		#此代码在windows中无法运行，因为其既不是Linux\unix系统，又不用有linux、unix内核

##---------------------------------------------------multiprocessing
#既然Python是跨平台的，对于windows无法调用fork问题，python提供multiprocessing模块作为跨平台版本的多进程模块
from multiprocessing import Process
import os

#子进程要执行的代码
def run_proc(name):
	print('Run child process %s (%s)...'  %(name,os.getpid()))

if __name__ == '__main__':
	print('parent process %s' %os.getpid())				#模块都有一个变量name,可以在模块中print name的值看来本模块独立执行的值为main

	p = Process(target = run_proc,args=('test',))   	#创建Process实例
	print('Child process will start')
	p.start()											#启动
	p.join()											#可以等待子进程结束后再继续往下运行，通常用于进程间的同步

	print('child process end')



##-------------------------------------------------------Pool
#用进程池的方式批量创建子进程
from multiprocessing import Pool
import os,time,random

def long_time_task(name):
	print('Run task %s(%s)....' %(name,os.getpid()))
	start = time.time()
	time.sleep(random.random()*3)
	end = time.time()
	print('Task %s runs %0.2f seconds.' %(name,end - start))

if __name__ == '__main__':
	print('Parent process %s.' %os.getpid())
	p = Pool(4)   			#改成p = Pool(5)就是同时跑五个进程的意思
	for i in range(5):
		p.apply_async(long_time_task,args=(i,))
	print('wait for all subprocess done...')
	p.close()			#pool创建，而非process创建
	p.join()			#join（）之前调用close就是为了避免创造新的进程
	print('All subprocess done')



##--------------------------------------------------------子进程
#很多时候，子进程并不是自身，而是一个外部进程。我们创建了子进程后，还需要控制子进程的输入和输出。
#subprocess模块可以让我们非常方便地启动一个子进程，然后控制其输入和输出。

import subprocess

print('$ nslookup www.python.org')
r = subprocess.call(['nslookup','www.python.org'])
print('Exit code:',r)


#如果子进程还需要输入，则可以调用communicate()方法
#???????????????fail,不停输出
#print('$ nslookup')
#p = subprocess.Popen(['nslookup'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#output, err = p.communicate(b'set q=mx\npython.org\nexit\n')
#print(output.decode('utf-8'))
#print('Exit code:', p.returncode)


##------------------------------------------------------进程间通讯
#进程间通讯用queue、pipes
from multiprocessing import Process,Queue
import os,time,random

#写数据进程执行代码
def write(q):
	print('Process to write: %s' %os.getpid())
	for value in ['A','B','C']:
		print('Put %s to queue....' %value)
		q.put(value)
		time.sleep(random.random())

#读数据进程执行文件
def read(q):
	print('Process to read %s' %os.getpid())
	while True:
		value = q.get(True)
		print('Get %s from queue:' %value)

if __name__ == '__main__':
	#父进程创造queue，并传给子进程
	q = Queue()
	pw = Process(target = write,args = (q,))
	pr = Process(target = read,args = (q,))
	#启用子进程，写入
	pw.start()
	#启用子进程pr，读取
	pr.start()      				#没有开启pr，导致nonetype object has no attribute报错
	#等待pw结束
	pw.join()

	#pr进程是死循环，无法等待其结束，只能强制终止
	pr.terminate()
##注意：由于Windows没有fork调用，因此，multiprocessing需要“模拟”出fork的效果，父进程所有Python对象都必须通过pickle序列化再传到子进程去，所有，如果multiprocessing在Windows下调用失败了，要先考虑是不是pickle失败了。




#-----------------------------------------------------多进程
#python的线程是真正的Posix Tread，而不是模拟出来的线程
#python标准库提供了两个模块：低级模块_thread和高级模块treading，后者对前者进行了封装
#大多数情况下，我们只需要使用Treading模块
import time,threading

#新线程执行代码
def loop():
	#current_thread()永远返回当前线程实例
	print('Tread %s is running...' % threading.current_thread().name)
	n = 0
	while n < 5:
		n = n + 1
		print('thread %s >>> %s' %(threading.current_thread().name,n))
		time.sleep(1)
	print('thread %s ended' % threading.current_thread().name)

print('thread %s is running...' % threading.current_thread().name)
#looptread仅只是子线程的名字
t = threading.Thread(target=loop, name='LoopThread')			#启动一个线程就是把一个函数传入并创建Tread实例，在start（）

t.start()
t.join()
print('thread %s ended.' % threading.current_thread().name)


##-----------------------------------------------------lock
#多线程与多进程最大的区别是：多进程私有同一个变量，多线程共享一个变量
#这时，多线程的问题就浮现了，需要‘单例模式’
#假设balance是你的银行存款
balance = 0
lock = threading.Lock()

def run_thread(n):
	for i in range(100000):
		#先获取锁
		lock.acquire()			#多个线程同时执行lock.acquire()，但只有一个线程能够执行
		try:
			#随便改
			change_it(n)
		finally:
			#改完一定要释放锁
			lock.release()



##-----------------------------------------------------多核CPU
#GIL锁


#-----------------------------------------------------ThreadLocal
#全局变量的修改必须加锁，如上
#局部变量的修改如下
#TreadLock的出现是为了解决局部变量全局传递的问题
import threading

# 创建全局ThreadLocal对象:
local_school = threading.local()

def process_student():
    # 获取当前线程关联的student:
    std = local_school.student
    print('Hello, %s (in %s)' % (std, threading.current_thread().name))

def process_thread(name):
    # 绑定ThreadLocal的student:
    local_school.student = name
    process_student()

t1 = threading.Thread(target= process_thread, args=('Alice',), name='Thread-A')  //args是参数的名字

t2 = threading.Thread(target= process_thread, args=('Bob',), name='Thread-B')
t1.start()
t2.start()
t1.join()
t2.join()

#-----------------------------------------------------进程vs线程
#首先，实现多任务，通常我们会涉及Master-Worker模式
#多进程一个进程崩溃，其他无关，但开销巨大
#多线程一蹦全崩（因为共享）
#在Windows下，多线程的效率比多进程要高，所以微软的IIS服务器默认采用多线程模式。由于多线程存在稳定性的问题，IIS的稳定性就不如Apache。为了缓解这个问题，IIS和Apache现在又有多进程+多线程的混合模式，真是把问题越搞越复杂。

##-----------------------------------------------------线程切换
#单任务模式/批处理模型：五科作业按顺序在五小时内完成
#or 五科一分钟一分钟循环
#author，what are you say?????


##-----------------------------------------------------计算密集型 vs IO密集型
#将任务分为计算密集型和IO密集型
#计算密集型消耗CPU资源（适合C语言）
#IO密集型（适合代码少的，如python）


##-----------------------------------------------------异步IO
#事件驱动模型
#Nginx就是支持异步IO的Web服务器
#对应到Python语言，单进程的异步编程模型称为协程，有了协程的支持，就可以基于事件驱动编写高效的多任务程序。




#-----------------------------------------------------分布式进程
#Tread or Process,Process Frist.reason:lalalala....
#multiprocess->manager
import random,time,queue
from multiprocessing.managers import BaseManager

#发送任务队列
task_queue = queue.Queue()
#接收结果的队列
result_queue = queue.Queue()

#从BaseManager继承的QueueManager
class QueueManager(BaseManager):
	pass

#把两个Queue都注册到网络上，callable参数关联了Queue对象
QueueManager.register('get_task_queue', callable=lambda: task_queue)
QueueManager.register('get_result_queue', callable=lambda: result_queue)
#锁定端口5000，设置验证码‘abc’
manager = QueueManager(address = ('',5000),authkey = b'abc')
#启动queue
manager.start()
#获得通过网络访问的Queue对象
task = manager.get_task_queue()
result = manager.get_result_queue()
#放几个进程进去
for i in range(10):
	n = random.randint(0,10000)
	print('Put task %d....' %n)
#从result队列中读取结果
print('Try get result ...')
for i in range(10):
	r = result.get(timeout=10)
	print('result:%s' %r)
#关闭
manager.shutdown()
print('master exit.')


#然后，在另一台机器上启动任务进程（本机上启动也可以）

import time, sys, queue
from multiprocessing.managers import BaseManager

# 创建类似的QueueManager:
class QueueManager(BaseManager):
    pass

# 由于这个QueueManager只从网络上获取Queue，所以注册时只提供名字:
QueueManager.register('get_task_queue')
QueueManager.register('get_result_queue')

# 连接到服务器，也就是运行task_master.py的机器:
server_addr = '127.0.0.1'
print('Connect to server %s...' % server_addr)
# 端口和验证码注意保持与task_master.py设置的完全一致:
m = QueueManager(address=(server_addr, 5000), authkey=b'abc')			#authkey的作用：保证两台机器(authkey相同的)正常通信，不被其他机器恶意干扰
# 从网络连接:
m.connect()
# 获取Queue的对象:
task = m.get_task_queue()
result = m.get_result_queue()
# 从task队列取任务,并把结果写入result队列:
for i in range(10):
    try:
        n = task.get(timeout=1)
        print('run task %d * %d...' % (n, n))
        r = '%d * %d = %d' % (n, n, n*n)			#把计算n*n的代码换成发送邮件，就实现了邮件队列的异步发送。
        time.sleep(1)
        result.put(r)
    except Queue.Empty:
        print('task queue is empty.')
# 处理结束:
print('worker exit.')