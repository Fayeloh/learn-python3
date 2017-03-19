#---------------------------------------------------异步IO

#异步IO模型需要一个消息循环，在消息循环过程中，主线程不断地重复“读取消息--处理消息”这一过程
#loop = get_event_loop()
#while True:
#		event = loop.get_event()
#		process_event(event)

#---------------------------------------------------协程
#子程序就是协程的特例，协程可以在运行过程中中断
#python对协程的支持是通过generator实现的
def consumer():			#consum就是一个generator
	r=''
	while True:
		n=yield r
		if not n:
			return 
		print('[CONSUMER] Consuming %s...' %n)
		r = '200 OK'

def produce(c):
	c.send(None)
	n=0
	while n<5:
		n=n+1
		print('[PRODUCER] Producing %s...' %n)
		r = c.send(n)
		print('[PRODUCER] Consumer return: %s' %r)
	c.close()

c = consumer()
produce(c)

#---------------------------------------------------asyncio
#asyncio直接内置对异步IO的支持
#asyncio的编程模型就是一个消息循环
import asyncio

@asyncio.coroutine				#此语句将一个generator标志为coroutine类型，然后在内部用yield from调用另一个coroutine

def hello():
	print('Hello World')
	#异步调用asyncio.sleep（1）
	r = yield from asyncio.sleep(1)
	print('Hello again')

#获取Eventloop
loop = asyncio.get_event_loop()
#执行coroutine
loop.run_until_complete(hello())
loop.close()

#用Task封装两个coroutine
#’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’

#用asyncio的异步网络连接获取sina,sohu和163网站页面
#‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’‘’

#---------------------------------------------------async/await
#为了更好地标示异步，让coroutine代码更简洁，asyncio引用了async和wait
#将上面一段代码改成
async def hello():
	print('Hello World!')
	r = await asyncio.sleep(1)
	print('Hello again!')

#---------------------------------------------------aiohttp
#asyncio可以实现单线程并发IO操作。如果仅用在客户端，发挥的威力不大。如果把asyncio用在服务器端，例如Web服务器，由于HTTP连接就是IO操作，因此可以用单线程+coroutine实现多用户的高并发支持。
#asyncio实现了TCP、UDP、SSL等协议，aiohttp则是基于asyncio实现的HTTP框架。
#我们先安装aiohttp：
#pip install aiohttp

import asyncio

from aiohttp import web

async def index(request):
    await asyncio.sleep(0.5)
    return web.Response(body=b'<h1>Index</h1>')    		

async def hello(request):
    await asyncio.sleep(0.5)
    text = '<h1>hello, %s!</h1>' % request.match_info['name']
    return web.Response(body=text.encode('utf-8'))

async def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/', index)
    app.router.add_route('GET', '/hello/{name}', hello)
    srv = await loop.create_server(app.make_handler(), '127.0.0.1', 8000)
    print('Server started at http://127.0.0.1:8000...')
    return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()